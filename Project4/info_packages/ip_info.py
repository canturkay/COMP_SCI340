import subprocess


def ns_lookup(ws: str, ipv6: bool = False, repeat: int = 0) -> str:
    req = []
    req.append("nslookup")
    if ipv6:
        req.append("-type=AAAA")

    req.append(ws)
    req.append("208.67.222.222")
    try:
            return subprocess.check_output(req,
                                            timeout=3, stderr=subprocess.STDOUT, shell=True).decode("utf-8")
    except Exception as ex:
        print(ex)
        if repeat < 3:
            return ns_lookup(ws=ws, ipv6=ipv6, repeat=repeat+1)
        else:
            return None


def get_ipv4_info(ws: str) -> str:
    res = ns_lookup(ws)
    print(res)
    if res:
        return get_addresses(res, ipv4=True)

    return []


def get_ipv6_info(ws: str) -> str:
    res = ns_lookup(ws, ipv6=True)
    if res:
        return get_addresses(res, ipv6=True)

    return []


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
