import subprocess


class TLSInfo:
    def __init__(self, url: str):
        self.url = url

    def get_info(self):
        response = self.get_nmap()
        result = []
        if 'TLSv1.0' in response:
            result.append('TLSv1.0')
        if 'TLSv1.1' in response:
            result.append('TLSv1.1')
        if 'TLSv1.2' in response:
            result.append('TLSv1.2')

        print(self.url, result)
        return result

    def get_nmap(self):
        req = "nmap --script ssl-enum-ciphers -p 443 " + self.url
        return subprocess.check_output(req,
                                   timeout=12, stderr=subprocess.STDOUT, shell=True).decode("utf-8")