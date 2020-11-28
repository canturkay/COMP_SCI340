import json
import subprocess
import sys
import time


def main():
    websites = []

    with open(sys.argv[1]) as f:
        for line in f:
            websites.append(line.split('\n')[0])

    website_scans = {}
    # get scan information for websites and create dictionaries
    for ws in websites:
        single_website = {}
        single_website["scan_time"] = time.time()

        single_website["ipv4_addresses"] = get_ipv4_info(ws)
        single_website["ipv6_addresses"] = get_ipv6_info(ws)

        website_scans[ws] = single_website

    # write_to_file(website_scans)
    print(website_scans)


def write_to_file(content):
    json_object = json.dumps(content)
    file_name = sys.argv[2]
    with open(file_name, "w") as f:
        json.dump(json_object, f, sort_keys=True, indent=4)


def ns_lookup(ws: str, ipv6: bool = False) -> str:
    req = []
    req.append("nslookup")
    if ipv6:
        req.append("-type=AAAA")

    req.append(ws)
    req.append("8.8.8.8")

    return subprocess.check_output(req,
                                   timeout=2, stderr=subprocess.STDOUT, shell=True).decode("utf-8")


def get_ipv4_info(ws: str) -> str:
    res = ns_lookup(ws)
    addresses = get_addresses(res, ipv6=False)

    return addresses


def get_ipv6_info(ws: str) -> str:
    res = ns_lookup(ws, ipv6=True)
    addresses = get_addresses(res, ipv4=False)

    return addresses


def get_addresses(lookup_res: str, ipv4: bool = True, ipv6: bool = True) -> list:
    address_line = lookup_res.split("Name:")[1]

    if ':' not in address_line:
        return []

    addresses = address_line.split(":", 1)[1].splitlines()
    ips_rev = [i.strip(" \r\n\t") for i in addresses]

    res = []

    for address in ips_rev:
        if address != '':
            if ':' in address and address[0].isnumeric() and ipv6:
                res.append(address)
            if '.' in address and address[0].isnumeric() and ipv4:
                res.append(address)

    return res


if __name__ == '__main__':
    main()
