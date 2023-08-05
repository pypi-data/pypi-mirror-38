Qth OpenWRT Status Monitoring Client
====================================

Expose basic information about what is connected to an OpenWRT router via Qth.


Exposed Paths
-------------

* `network/`
  * `wifi/hosts` -- A list of device hostnames for currently connected WiFi
    stations (falls back on IP, then MAC if not known).
  * `internet/`
    * `down` and `up` -- Average downlink and uplink usage (MBit/s).
    * `down/` and `up/`
      * `24-hour-total` -- Total download/upload in last 24 hours (GBytes).
      * `data-used` -- Event fired regularaly with the number of megabytes
        downloaded/uploaded since the last time the event fired.
    * `connections` -- Array of tuples `[from_host, to_host, protocol, port]`.

OpenWRT CGI Pages
-----------------

This application requires (read-only) access to various information in OpenWRT,
to enable remote access to this various simple CGI scripts are provided in
`openwrt-gci-bin`. These should be placed in `/www/cgi-bin/` on the router.
