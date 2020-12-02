import os
import signal
import subprocess


class TLSInfo:
    def __init__(self, url: str):
        self.url = url

    def get_info(self) -> tuple:
        try:
            response = self.get_nmap()
        except Exception as ex:
            # print("nmap error", ex)
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
            # print("openssl error", ex)
            response = ""

        if 'New, TLSv1.3, Cipher' in response:
            result.append('TLSv1.3')

        ca_arg = None
        if response is not None and len(result) > 0:
            lines = response.splitlines()
            ca_line = None
            for line in lines:
                if 'depth=' in line:
                    ca_line = line
                    break

            if ca_line is not None:
                for arg in ca_line.split(','):
                    if ' O = ' in arg:
                        ca_arg = arg.split(' O = ')[1]
                        break

        return result, ca_arg

    def get_nmap(self, repeat: int = 0) -> str:
        try:
            req = "nmap --script ssl-enum-ciphers -p 443 " + self.url
            return subprocess.check_output(req,
                                       timeout=10, stderr=subprocess.STDOUT, shell=True).decode("utf-8")
        except Exception as ex:
            if repeat < 1:
                return self.get_nmap(repeat=repeat+1)
            else:
                return ""

    def get_openssl(self, repeat: int = 0) -> str:
        try:
            req = "echo | timeout 2 openssl s_client -connect " + self.url + ":443"

            return subprocess.check_output(req, shell=True, input="", timeout=2, stderr=subprocess.STDOUT).decode("utf-8")
        except Exception as ex:
            if repeat < 1:
                return self.get_openssl(repeat=repeat+1)
            else:
                return ""
