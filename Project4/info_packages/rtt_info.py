import subprocess
import math

class RTTInfo:
    def __init__(self, ips: list):
        self.ips = ips

    def get_info(self) -> list:
        min_val = float('inf')
        max_val = float('-inf')

        for ip in self.ips:
            response = self.get_rtt_message(ip=ip)

            if response and "real" in response:
                duration_text = response.split('real')[1].splitlines()[0].strip(' \t\r\n')
                try:
                    duration_val = float(duration_text[2:-1])
                    min_val = min(min_val, duration_val)
                    max_val = max(max_val, duration_val)
                except:
                    pass

        if math.isinf(min_val) or math.isinf(max_val):
            return None
        else:
            return [min_val, max_val]

    def get_rtt_message(self, ip: str, repeat: int = 0):
        try:
            req = 'sh -c "time echo -e \'\\x1dclose\\x0d\' | telnet ' + ip + ' 443"'
            return subprocess.run(req,timeout=3, shell=True, capture_output=True).stderr.decode("utf-8")
        except Exception as ex:
            if repeat < 3:
                return self.get_rtt_message(ip=ip, repeat=repeat+1)
            else:
                return None