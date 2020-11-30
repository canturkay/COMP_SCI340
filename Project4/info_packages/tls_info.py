import subprocess


class TLSInfo:
    def __init__(self, url: str):
        self.url = url

    def get_info(self):
        try:
            response = self.get_nmap()
        except Exception as ex:
            print("nmap error", ex)
            response = ""

        result = []

        if 'TLSv1.0' in response:
            result.append('TLSv1.0')
        if 'TLSv1.1' in response:
            result.append('TLSv1.1')
        if 'TLSv1.2' in response:
            result.append('TLSv1.2')

        try:
            response = self.get_openssl()
        except Exception as ex:
            print("openssl error", ex)
            response = ""

        if 'New, TLSv1.3, Cipher' in response:
            result.append('TLSv1.3')

        print(self.url, result)
        return result

    def get_nmap(self):
        req = "nmap --script ssl-enum-ciphers -p 443 " + self.url
        return subprocess.check_output(req,
                                   timeout=15, stderr=subprocess.STDOUT, shell=True).decode("utf-8")

    def get_openssl(self):
        req = "echo | openssl s_client -tls1_3 -connect " + self.url + ":443"
        return subprocess.check_output(req,
                                   timeout=15, stderr=subprocess.STDOUT, shell=True).decode("utf-8")