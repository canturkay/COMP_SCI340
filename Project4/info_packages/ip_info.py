import subprocess


def ns_lookup(ws: str, ipv6: bool = False) -> str:
    req = []
    req.append("nslookup")
    if ipv6:
        req.append("-type=AAAA")

    req.append(ws)
    req.append("208.67.222.222")

    return subprocess.check_output(req,
                                   timeout=2, stderr=subprocess.STDOUT, shell=True).decode("utf-8")


def get_ipv4_info(ws: str) -> str:
    res = ns_lookup(ws)
    addresses = get_addresses(res, ipv4=True)

    return addresses


def get_ipv6_info(ws: str) -> str:
    res = ns_lookup(ws, ipv6=True)
    addresses = get_addresses(res, ipv6=True)

    return addresses


def get_addresses(lookup_res: str, ipv4: bool = False, ipv6: bool = False) -> list:
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


def get_ip_info(ws: str) -> tuple:
    return get_ipv4_info(ws=ws), get_ipv6_info(ws=ws)
