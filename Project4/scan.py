import json
import sys
import time

from info_packages.dns_info import DNSInfo
from info_packages.geo_info import GeoInfo
from info_packages.http_info import HttpInfo
from info_packages.ip_info import get_ip_info
from info_packages.rtt_info import RTTInfo
from info_packages.tls_info import TLSInfo


def main():
    websites = []

    with open(sys.argv[1]) as f:
        for line in f:
            websites.append(line.split('\n')[0])

    geo_info = GeoInfo()

    website_scans = {}
    # get scan information for websites and create dictionaries
    for ws in websites:
        print("Scanning ", ws)

        single_website = {}

        single_website["scan_time"] = time.time()

        single_website["ipv4_addresses"], single_website["ipv6_addresses"] = get_ip_info(ws)

        http_info = HttpInfo(ws=ws)
        single_website["http_server"], single_website["insecure_http"], \
            single_website["redirect_to_https"], single_website["hsts"] = http_info.get_info()

        tls_info = TLSInfo(url=ws)

        single_website['tls_versions'], single_website['root_ca'] = tls_info.get_info()

        dns_info = DNSInfo(ips=single_website["ipv4_addresses"])

        single_website['rdns_names'] = dns_info.get_info()

        rtt_info = RTTInfo(ips=single_website["ipv4_addresses"])

        single_website['rtt_range'] = rtt_info.get_info()

        single_website['geo_locations'] = geo_info.get_info(ips=single_website["ipv4_addresses"])

        website_scans[ws] = single_website

    geo_info.reader.close()

    write_to_file(website_scans)


def write_to_file(content):
    json_object = json.dumps(content, sort_keys=True, indent=4)
    print(json_object)
    file_name = sys.argv[2]
    with open(file_name, "w") as f:
        json.dump(content, f, sort_keys=True, indent=4)


if __name__ == '__main__':
    main()
