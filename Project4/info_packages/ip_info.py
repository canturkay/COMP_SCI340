import subprocess


def ns_lookup(ws: str, ipv6: bool = False, repeat: int = 0) -> str:
    req = "nslookup"
    if ipv6:
        req += " -type=AAAA"

    req += ' ' + ws
    req += " 208.67.222.222"
    try:
            return subprocess.check_output(req,
                                            timeout=3, stderr=subprocess.STDOUT, shell=True).decode("utf-8")
    except Exception as ex:
        if repeat < 2:
            return ns_lookup(ws=ws, ipv6=ipv6, repeat=repeat+1)
        else:
            return None


def get_ipv4_info(ws: str) -> str:
    res = ns_lookup(ws)
    if res:
        return get_addresses(res, ipv4=True)

    return []


def get_ipv6_info(ws: str) -> str:
    res = ns_lookup(ws, ipv6=True)
    if res:
        return get_addresses(res, ipv6=True)

    return []


def get_addresses(lookup_res: str, ipv4: bool = False, ipv6: bool = False) -> list:
    if "Name" not in lookup_res:
        return []

    res = []

    address_lines = lookup_res.split("Name:")[1:]
    for address_line in address_lines:
        if ':' in address_line:
            addresses = address_line.split(":", 1)[1].splitlines()
            ips_rev = [i.strip(" \r\n\t") for i in addresses]

            for address in ips_rev:
                if address != '':
                    if ':' in address and address[0].isnumeric() and ipv6 and address not in res:
                        res.append(address)
                    if '.' in address and address[0].isnumeric() and ipv4 and address not in res:
                        res.append(address)

    return res


def get_ip_info(ws: str) -> tuple:
    return get_ipv4_info(ws=ws), get_ipv6_info(ws=ws)
