import asyncio
import qth
import re
import datetime

import aiohttp
import aiodns
import pycares
import traceback

from collections import defaultdict, namedtuple

from .version import __version__


async def http_get_text(loop, url):
    """Perform an HTTP request returning the reponse as text."""
    async with aiohttp.ClientSession(loop=loop) as http_session:
        async with http_session.get(url) as response:
            return await response.text()


class ARPLookup(object):
    """
    Look up the IP corresponding to a MAC address in an OpenWRT router's ARP
    table.
    """
    
    def __init__(self, loop, arp_table_url, arp_max_age=30*60):
        """
        Params
        ------
        loop : asyncio.BaseEventLoop
        arp_table_url : str
            The URL to request which will return the ARP table of the router in
            /proc/net/arp.
        arp_max_age : float
            ARP entries are cached for at most this length of time in seconds.
        """
        self.loop = loop
        self.arp_table_url = arp_table_url
        self.arp_max_age = arp_max_age
        
        self.lock = asyncio.Lock(loop=self.loop)
        
        # MAC -> IP
        self.arp_table = {}
        
        # Last ARP table update (used to trigger reload if data is stale
        self.last_update = None
    
    async def _get_arp_table(self):
        """
        Internal. Download and parse the ARP table.
        """
        table_ascii = await http_get_text(self.loop, self.arp_table_url)
        
        arp_table = {}
        
        rows = table_ascii.strip().split("\n")
        for row in rows[1:]:
            match = re.match(r"^([^\s]+)\s+[^\s]+\s+[^\s]+\s+([^\s]+)\s+.*", row)
            if match:
                ip, mac = match.group(1, 2)
                arp_table[mac.lower()] = ip.lower()
        
        return arp_table
    
    async def lookup(self, mac):
        """Lookup the IP of a MAC address. Returns None if not known."""
        async with self.lock:
            # Fetch a new ARP table if out of date or the MAC is not available.
            table_age = 0 if self.last_update is None else (datetime.datetime.now() - self.last_update).total_seconds()
            if (self.last_update is None or
                    table_age > self.arp_max_age or
                    # Don't reload the ARP if its only just been fetched
                    (mac not in self.arp_table and table_age > 1.0)):
                self.arp_table = await self._get_arp_table()
                self.last_update = datetime.datetime.now()
            
            return self.arp_table.get(mac.lower())


class ReverseDNSLookup(object):
    """
    Perform reverse DNS lookups (with a local cache).
    """
    
    def __init__(self, loop):
        self.loop = loop
        
        self.resolver = aiodns.DNSResolver(loop=self.loop)
        
        # A list of Events corresponding to ongoing queries. When an event
        # fires, an entry for that IP will have been updated in the cache. Only
        # access this dictionary while holding the corresponding lock.
        self.ongoing_lookups = {}
        self.ongoing_lookups_lock = asyncio.Lock(loop=self.loop)
        
        # Results of past lookups. {ip: (hostname, expires_datetime) OR Event,
        # ...} The Event will be fired when the result becomes available.
        self.cache = {}
    
    async def _do_lookup(self, ip):
        """
        Internal. Perform a reverse DNS lookup for an IP returning the IP (or
        None) and the TTL of the DNS entry.
        """
        try:
            result = await self.resolver.query(pycares.reverse_address(ip), "PTR")
            return (result.name,
                    datetime.datetime.now() + datetime.timedelta(seconds=result.ttl))
        except aiodns.error.DNSError:
            return (None, datetime.datetime.now())
    
    async def lookup(self, ip):
        """
        Lookup the hostname associated with an IP address.
        """
        now = datetime.datetime.now()
        
        # If the response is not cached or is out of date, query it now
        if ip not in self.cache or self.cache[ip][1] < now:
            # Is there already a lookup going on?
            async with self.ongoing_lookups_lock:
                lookup_complete = self.ongoing_lookups.get(ip)
                
                # If there is no lookup going on, start one now (creating the
                # corresponding event while holding the lock to ensure we're
                # the only one to perform the query.)
                perform_lookup = not lookup_complete
                if perform_lookup:
                    lookup_complete = asyncio.Event(loop=self.loop)
                    self.ongoing_lookups[ip] = lookup_complete
            
            if perform_lookup:
                self.cache[ip] = await self._do_lookup(ip)
                async with self.ongoing_lookups_lock:
                    del self.ongoing_lookups[ip]
                    lookup_complete.set()
            else:
                await lookup_complete.wait()
        
        return self.cache[ip][0]


class WifiClientStatus(object):
    """
    Look up list of currently connected WiFi clients to an OpenWRT-based access
    point.
    """
    
    def __init__(self, loop, iwinfo_url, arp_lookup, dns_lookup):
        """
        Params
        ------
        loop : asyncio.BaseEventLoop
        iwinfo_url : str
            The URL to request which will return the output of `iwinfo
            <devicename> assoclist` for the access point interface.
        arp_lookup : ARPLookup
        dns_lookup : ReverseDNSLookup
        """
        self.loop = loop
        self.iwinfo_url = iwinfo_url
        self.arp_lookup = arp_lookup
        self.dns_lookup = dns_lookup
    
    async def _mac_to_hostname(self, mac):
        """
        Given a MAC, attempt to return the hostname or IP if possible,
        otherwise returning the MAC.
        """
        ip = await self.arp_lookup.lookup(mac)
        if ip is None:
            return mac
        
        host = await self.dns_lookup.lookup(ip)
        if host is None:
            return ip
        
        return host
    
    async def get_wifi_clients(self):
        """
        Get the currently connected set of WiFi clients. An array of
        name, IP or MAC strings (in that order of preference).
        """
        iwinfo_ascii = await http_get_text(self.loop, self.iwinfo_url)
        
        mac_addrs = []
        for row in iwinfo_ascii.split("\n"):
            match = re.match(r"^(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})\s.*", row)
            if match:
                mac_addrs.append(match.group(1))
        
        return await asyncio.gather(
            *(self._mac_to_hostname(mac) for mac in mac_addrs),
            loop=self.loop)


class InterfaceStatus(object):
    """
    Get the current interface data rate statistics from an OpenWRT router.
    """
    
    InterfaceStatusTuple = namedtuple("InterfaceStatusTuple", [
        "rx_bytes",
        "tx_bytes",
        "rx_rate",
        "tx_rate",
    ])
    
    def __init__(self, loop, proc_net_dev_url, interface):
        """
        Params
        ------
        loop : asyncio.BaseEventLoop
        proc_net_dev_url : str
            The URL to request which will return the contents of /proc/net/dev.
        interface : str
            The name of the interface to report statistics for.
        """
        self.loop = loop
        self.proc_net_dev_url = proc_net_dev_url
        self.interface = interface
        
        self.rx_bytes = None
        self.tx_bytes = None
        self.last_update = None
    
    async def _get_rx_tx_bytes(self):
        response = await http_get_text(self.loop, self.proc_net_dev_url)
        
        for row in response.split("\n"):
            interface, _, values = row.partition(":")
            interface = interface.strip()
            values = values.strip()
            
            if interface == self.interface:
                cols = re.split(r"\s+", values)
                rx_bytes = int(cols[0])
                tx_bytes = int(cols[8])
                return (rx_bytes, tx_bytes)
        
        # Interface not known...
        return (0, 0)
    
    async def get_rx_tx_usage(self):
        """
        Return the interface usage status since the last call to this
        function.
        
        Returns
        -------
        InterfaceStatusTuple
            rx_bytes and tx_bytes give the number of bytes received or
            transmitted respectively.  rx_rate and tx_rate give the average
            rate in megabits per second in either direction.
            
            On the first call, the reported values will be all zero.
        """
        rx_bytes, tx_bytes = await self._get_rx_tx_bytes()
        now = datetime.datetime.now()
        
        if self.last_update is None:
            self.rx_bytes = rx_bytes
            self.tx_bytes = tx_bytes
            self.last_update = now
        
        delta_rx_bytes = rx_bytes - self.rx_bytes
        delta_tx_bytes = tx_bytes - self.tx_bytes
        
        delta_rx_mbits = delta_rx_bytes * 8.0 / 1024 / 1024
        delta_tx_mbits = delta_tx_bytes * 8.0 / 1024 / 1024
        
        delta_t = (now - self.last_update).total_seconds()
        
        self.rx_bytes = rx_bytes
        self.tx_bytes = tx_bytes
        self.last_update = now
        
        if delta_t == 0:
            return InterfaceStatus.InterfaceStatusTuple(0, 0, 0, 0)
        else:
            return InterfaceStatus.InterfaceStatusTuple(
                delta_rx_bytes,
                delta_tx_bytes,
                delta_rx_mbits / delta_t,
                delta_tx_mbits / delta_t,
            )

class NATConnectionStatus(object):
    """
    Enumerate NATed connections currently being made by an OpenWRT router.
    """
    
    def __init__(self, loop, nf_conntrack_url, dns_lookup):
        """
        Params
        ------
        loop : asyncio.BaseEventLoop
        nf_conntrack_url : str
            The URL to request which will return the contents of
            /proc/net/nf_conntrack.
        dns_lookup : ReverseDNSLookup
        """
        self.loop = loop
        self.nf_conntrack_url = nf_conntrack_url
        self.dns_lookup = dns_lookup
    
    async def _connection_ip_to_hostname(self, connection):
        """Attempt to convert src and dst into hostnames."""
        src = connection.get("src")
        if src is not None:
            connection["src"] = await self.dns_lookup.lookup(src) or src
        
        dst = connection.get("dst")
        if dst is not None:
            connection["dst"] = await self.dns_lookup.lookup(dst) or dst
        
        return connection
    
    async def enumerate_connections(self):
        """
        List the current connections to the outside world.
        
        A list of objects containing the following entries:
        * type: IP version.
        * protocol: TCP, UDP, ICMP etc.
        * src, dst: The source and detstination (hostname, if available) of the
          connection.
        * src_ip, dst_ip: The source and detstination IP of the connection.
        * sport, dport: The source and destination port numbers if UDP or TCP,
          absent otherwise.
        """
        nf_conntrack = await http_get_text(self.loop, self.nf_conntrack_url)
        
        connections = []
        
        for row in nf_conntrack.split("\n"):
            match = re.match(r"^(?P<ip_type>[^\s]+)\s+"
                             r"[^\s]+\s+"  # Unused
                             r"(?P<protocol>[^\s]+)\s+"
                             r"[^\s]+\s+"  # Unused
                             r"[^\s]+\s+"  # Unused (TTL)
                             r"(?P<flags>.*)", row)
            if match:
                connection = {
                    "type": match.group("ip_type"),
                    "protocol": match.group("protocol"),
                }
                
                flags = defaultdict(list)
                for flag in re.split(r"\s+", match.group("flags")):
                    flag_match = re.match(r"(?P<key>[^\s]+)=(?P<value>[^\s]+)", flag)
                    if flag_match:
                        key, value = flag_match.group("key", "value")
                        flags[key].append(value)
                
                if flags["src"]:
                    connection["src"] = connection["src_ip"] = flags["src"][0]
                    connection["dst"] = connection["dst_ip"] = flags["src"][1]
                if flags["dport"]:
                    connection["dport"] = int(flags["dport"][0])
                if flags["sport"]:
                    connection["sport"] = int(flags["sport"][0])
                
                connections.append(connection)
        
        return await asyncio.gather(
            *(self._connection_ip_to_hostname(connection) for connection in connections),
            loop=self.loop)



class QthOpenWRTStatus(object):
    
    def __init__(self, loop,
                 qth_prefix="network/",
                 qth_host=None, qth_port=None, qth_keepalive=10,
                 openwrt_host="http://router/",
                 openwrt_wan_interface="pppoa-wan",
                 update_rate=5.0):
        self.loop = loop

        self.qth_wifi_hosts_path = "{}wifi/hosts".format(qth_prefix)
        self.qth_up_rate_path = "{}internet/up".format(qth_prefix)
        self.qth_up_data_used_path = "{}internet/up/data-used".format(qth_prefix)
        self.qth_down_rate_path = "{}internet/down".format(qth_prefix)
        self.qth_down_data_used_path = "{}internet/down/data-used".format(qth_prefix)
        self.qth_connections_path = "{}internet/connections".format(qth_prefix)
        
        self.openwrt_host = openwrt_host
        self.openwrt_wan_interface = openwrt_wan_interface
        
        self.update_rate = update_rate
        
        self.qth_client = qth.Client("qth_openwrt_status",
                                     "Monitors connections to a OpenWRT router.",
                                     host=qth_host, port=qth_port,
                                     keepalive=qth_keepalive,
                                     loop=self.loop)
        
        self.arp_lookup = ARPLookup(self.loop, "{}proc_net_arp".format(self.openwrt_host))
        self.dns_lookup = ReverseDNSLookup(self.loop)
        
        self.wifi_client_status = WifiClientStatus(
            self.loop,
            "{}iwinfo".format(self.openwrt_host),
            self.arp_lookup,
            self.dns_lookup)
        
        self.interface_status = InterfaceStatus(
            self.loop,
            "{}proc_net_dev".format(self.openwrt_host),
            openwrt_wan_interface)
        
        self.nat_connection_status = NATConnectionStatus(
            self.loop,
            "{}proc_net_nf_conntrack".format(self.openwrt_host),
            self.dns_lookup)
        
        self.loop.run_until_complete(self.run())
    
    async def update_wifi_hosts(self):
        
        await self.qth_client.register(
            self.qth_wifi_hosts_path,
            qth.PROPERTY_ONE_TO_MANY,
            "List of devices connected to WiFi given as hostname, IP or MAC "
            "(prefering the former and falling back on the latter).",
            delete_on_unregister=True)
        
        last_clients = None
        
        while True:
            try:
                this_clients = sorted(set(await self.wifi_client_status.get_wifi_clients()))
                
                if this_clients != last_clients:
                    await self.qth_client.set_property(self.qth_wifi_hosts_path, this_clients)
                last_clients = this_clients
            except:
                traceback.print_exc()
            
            await asyncio.sleep(self.update_rate, loop=self.loop)
    
    async def update_nat_connection_status(self):
        
        await self.qth_client.register(
            self.qth_connections_path,
            qth.PROPERTY_ONE_TO_MANY,
            "Currently open NAT-forwarded connections to hosts on the Internet. "
            "An array of [source, dest, protocol, port] tuples.",
            delete_on_unregister=True)
        
        last_status = None
        
        while True:
            try:
                # Return a simplified view
                this_status = sorted(set([
                    (c["src"], c["dst"], c["protocol"], c.get("dport"))
                    for c in await self.nat_connection_status.enumerate_connections()
                ]))
                
                if this_status != last_status:
                    await self.qth_client.set_property(self.qth_connections_path, this_status)
                last_status = this_status
            except:
                traceback.print_exc()
            
            await asyncio.sleep(self.update_rate, loop=self.loop)
    
    async def update_interface_status(self):
        
        await self.qth_client.register(
            self.qth_down_rate_path,
            qth.PROPERTY_ONE_TO_MANY,
            "The current Internet downlink throughput (MBit/s)",
            delete_on_unregister=True)
        
        await self.qth_client.register(
            self.qth_down_data_used_path,
            qth.EVENT_ONE_TO_MANY,
            "Event fired at a regular interval with the number of bytes "
            "downloaded since the last time the event fired.")
        
        await self.qth_client.register(
            self.qth_up_rate_path,
            qth.PROPERTY_ONE_TO_MANY,
            "The current Internet uplink throughput (MBit/s)",
            delete_on_unregister=True)
        
        await self.qth_client.register(
            self.qth_up_data_used_path,
            qth.EVENT_ONE_TO_MANY,
            "Event fired at a regular interval with the number of bytes "
            "uploaded since the last time the event fired.")
        
        while True:
            try:
                status = await self.interface_status.get_rx_tx_usage()
                
                await asyncio.gather(
                    self.qth_client.set_property(self.qth_down_rate_path, status.rx_rate),
                    self.qth_client.set_property(self.qth_up_rate_path, status.tx_rate),
                    self.qth_client.set_property(self.qth_down_data_used_path, status.rx_bytes),
                    self.qth_client.set_property(self.qth_up_data_used_path, status.rx_bytes),
                    loop=self.loop
                )
            except:
                traceback.print_exc()
            
            await asyncio.sleep(self.update_rate, loop=self.loop)
    
    async def run(self):
        await asyncio.gather(
            self.update_wifi_hosts(),
            self.update_nat_connection_status(),
            self.update_interface_status(),
            loop=self.loop
        )


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Control an LG TV via Qth")
    
    parser.add_argument("--qth-base", "-q", default="network/",
                        help="Prefix for all Qth values.")
    
    parser.add_argument("--qth-host", "-H", default=None,
                        help="Qth (MQTT) server hostname.")
    parser.add_argument("--qth-port", "-P", default=None, type=int,
                        help="Qth (MQTT) server port number.")
    parser.add_argument("--qth-keepalive", "-K", default=10, type=int,
                        help="MQTT keepalive interval (seconds).")
    
    parser.add_argument("--openwrt-host", "-e", default="http://router/cgi-bin/", type=str,
                        help="OpenWRT server base URL (default %(default)s).")
    parser.add_argument("--openwrt-wan-interface", "-w", default="pppoa-wan", type=str,
                        help="The WAN interface name (default %(default)s).")
    
    parser.add_argument("--update-rate", "-r", default=5, type=float,
                        help="Number of seconds between updates.")
    
    parser.add_argument("--version", "-V", action="version",
                        version="$(prog)s {}".format(__version__))
    
    args = parser.parse_args()
    
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    
    QthOpenWRTStatus(loop=loop,
                     qth_prefix=args.qth_base,
                     qth_host=args.qth_host, qth_port=args.qth_port,
                     qth_keepalive=args.qth_keepalive,
                     openwrt_host=args.openwrt_host,
                     openwrt_wan_interface=args.openwrt_wan_interface,
                     update_rate=args.update_rate)


if __name__ == "__main__":
    main()
