# cs-exabgp-bouncer
Crowdsec bouncer to be used with exabgp to blackhole IP addresses

# Description

This repository is an example of how to integrate [CrowdSec](https://doc.crowdsec.net/) with [Exabgp](https://github.com/Exa-Networks/exabgp) to blackhole IP to a BGP Peer within your network.

This has been tested to dynamicly blackhole prefix when the [log4j](https://crowdsec.net/blog/detect-block-log4j-exploitation-attempts/) vulnerability came out and prevent potential exploits.

# Usage

Warning: if you use both ipv4 and both ipv6, you need to register 2 bouncers.
Crowdsec use the API key to track decisions report while pulling the API

```
$ cscli bouncer add cs-exabgp-bouncer-ipv4
Api key for 'cs-bgp-bouncer-v4':

   b183089790450bc888dcb07e9cb13e51

Please keep this key since you will not be able to retrieve it!
```


You can copy this script in your `/etc/exabgp/scripts/` directory and use the following configuration as an example:

```
process dynamic_routes_v4 {
    run python3 /etc/exabgp/script/cs-exabgp-bouncer.py -4 --api-key b183089790450bc888dcb07e9cb13e51 --next-hop 192.0.2.1;
    encoder text;
}

# ipv4 example
neighbor 192.168.0.253 {
    family {
     ipv4 unicast;
    }
    announce {
     ipv4
    }
    router-id 192.168.0.30;
    local-address 192.168.0.30;
    local-as 65001;
    peer-as 65000;

    api {
        processes [dynamic_routes_v4];
    }
}
```

# Example

```
usage: cs-exabgp-bouncer.py [-h] [-6 | -4] --lapi-url LAPI_URL --api-key API_KEY --next-hop NEXT_HOP [-c COMMUNITY [COMMUNITY ...]] [-i INTERVAL]
cs-exabgp-bouncer.py: error: the following arguments are required: --lapi-url, --api-key, --next-hop
```

This script provide the ability to set BGP communities to your announce if your setup needs it.
