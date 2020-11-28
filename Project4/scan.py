import time
import subprocess
import json
import sys

print(sys.argv)
def everything():
    websites = []

    with open(sys.argv[1]) as f:
        for line in f:
            websites.append(line.split('\n')[0])

    website_scans = {}
    # get scan information for websites and create dictionaries
    for w in websites:
        single_website = {}
        single_website["scan_time"] = time.time()
        ips = get_ip_info(w)

        single_website["ipv4_addresses"] = ips[0]
        single_website["ipv6_addresses"] = ips[1]

        website_scans[w] = single_website

    #write_to_file(website_scans)
    print(website_scans)

def write_to_file(content):
    json_object = json.dumps(content)
    file_name = sys.argv[2]
    with open(file_name, "w") as f:
        json.dump(json_object, f, sort_keys=True, indent=4)


def get_ip_info(ws:str):
    pdr = '208.67.222.222'
    result = subprocess.check_output(["nslookup", pdr, "8.8.8.8"],
                                     timeout=2).decode("utf-8")
    ips = result.split("Name:")[1].split(":", 1)[1].splitlines()
    ips_rev = [i.strip(" \r\n\t") for i in ips]
    ipv4_addresses = []
    ipv6_addresses = []
    for i in ips_rev:
        if i != '':
            if ':' in i and i[0].isnumeric():
                ipv6_addresses.append(i)
            if '.' in i and i[0].isnumeric():
                ipv4_addresses.append(i)
    return (ipv4_addresses, ipv6_addresses)
