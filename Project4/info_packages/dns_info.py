import subprocess


class DNSInfo:
    def __init__(self, ips: list):
        self.urls = ips

    def get_info(self):
        names = []
        for ip in self.urls:
            res = self.ns_lookup(ip=ip)
            for line in res.splitlines():
                if 'Name:' in line:
                    name = line.split('Name:')[1].strip(' \t\r\n')
                    if name not in names:
                        names.append(name)

        return names

    def ns_lookup(ws: str, ip: str) -> str:
        return subprocess.check_output('nslookup ' + ip,
                                       timeout=2, stderr=subprocess.STDOUT, shell=True).decode("utf-8")
