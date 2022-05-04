#!/bin/env python3

from sys import stdout
from time import sleep
import argparse
from pycrowdsec.client import StreamClient


def clean_decisions(decisions, mode=4):
    for k in list(decisions.keys()):
        if mode == 4 and ":" in k or mode == 6 and "." in k:
            del decisions[k]
    return decisions


def run(args, crowdsec_client):
    community = ""
    if args.community:
        community = "community [{}]".format(" ".join(args.community))

    old_state = {}
    while True:
        new_state = clean_decisions(
            crowdsec_client.get_current_decisions(), mode=4 if args.ipv4 else 6
        )

        to_del = old_state.keys() - new_state.keys()
        if len(to_del):
            for ip in to_del:
                stdout.write(
                    f"withdraw route {ip} next-hop {args.next_hop} {community}\n"
                )
                stdout.flush()

        to_add = new_state.keys() - old_state.keys()
        if len(to_add):
            for ip in to_add:
                stdout.write(
                    f"announce route {ip} next-hop {args.next_hop} {community}\n"
                )
                stdout.flush()

        old_state = new_state
        sleep(args.interval)


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-4", "--ipv4", action="store_true")
    group.add_argument("-6", "--ipv6", action="store_true")
    parser.add_argument("--lapi-url", default="http://localhost:8080/", required=True)
    parser.add_argument(
        "--api-key",
        help="API key to authenticate your bouncer to CrowdSec API",
        required=True,
    )
    parser.add_argument("--next-hop", help="next-hop for your announces", required=True)
    parser.add_argument(
        "-c", "--community", nargs="+", help="BGP communities to add to your announces"
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=int,
        default=10,
        help="interval to wait between calls to the CrowdSec API",
    )
    args = parser.parse_args()
    print(args)
    crowdsec_client = StreamClient(
        lapi_url=args.lapi_url,
        api_key=args.api_key,
        scopes=["ip", "range"],
        interval=args.interval,
    )
    crowdsec_client.run()

    return run(args, crowdsec_client)


if __name__ == "__main__":
    main()
