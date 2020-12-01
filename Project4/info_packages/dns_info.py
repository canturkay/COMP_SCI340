import subprocess


class DNSInfo:
    def __init__(self, ips: list):
        self.urls = ips

    def get_info(self) -> list:
        names = []
        for ip in self.urls:
            res = self.ns_lookup(ip=ip)
            if res:
                for line in res.splitlines():
                    if 'name =' in line:
                        name = line.split('name =')[1].strip(' \t\r\n')[:-1]
                        if name not in names:
                            names.append(name)
                    elif 'Name:' in line:
                        name = line.split('Name:')[1].strip(' \t\r\n')
                        if name not in names:
                            names.append(name)

        return names

    def ns_lookup(self, ip: str, repeat: int = 0) -> str:
        try:
            return subprocess.check_output('nslookup ' + ip,
                                           timeout=2, stderr=subprocess.STDOUT, shell=True).decode("utf-8")
        except:
            if repeat < 2:
                return self.ns_lookup(ip=ip, repeat=repeat+1)
            else:
                return None
