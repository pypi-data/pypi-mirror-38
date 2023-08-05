from setuptools import setup, find_packages

with open("qth_openwrt_status/version.py", "r") as f:
    exec(f.read())

setup(
    name="qth_openwrt_status",
    version=__version__,
    packages=find_packages(),

    # Metadata for PyPi
    url="https://github.com/mossblaser/qth_openwrt_status",
    author="Jonathan Heathcote",
    description="A Qth interface monitoring a subset of OpenWRT router status..",
    license="GPLv2",
    classifiers=[
        "Development Status :: 3 - Alpha",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",

        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
    keywords="home-automation",

    # Requirements
    install_requires=["qth>=0.6.0", "aiohttp", "aiodns", "pycares"],

    # Scripts
    entry_points={
        "console_scripts": [
            "qth_openwrt_status = qth_openwrt_status:main",
        ],
    }
)
