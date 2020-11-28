import json
import sys
import time

from info_packages.http_info import HttpInfo
from info_packages.ip_info import get_ip_info


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

        single_website["ipv4_addresses"], single_website["ipv6_addresses"] = get_ip_info(ws)

        http_info = HttpInfo(ws=ws)

        website_scans[ws] = single_website

    # write_to_file(website_scans)
    print(website_scans)


def write_to_file(content):
    json_object = json.dumps(content)
    file_name = sys.argv[2]
    with open(file_name, "w") as f:
        json.dump(json_object, f, sort_keys=True, indent=4)





if __name__ == '__main__':
    main()
