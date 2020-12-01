import texttable
import pandas as pd

def get_part1_table(data: pd.DataFrame):
    table = texttable.Texttable()
    table.add_row([
      "Domain Name",
      "Scan Time",
      "IPv4",
      "IPv6",
        "Server",
        "Insecure HTTP",
        "Redirect to HTTPS",
        "HSTS",
        "TLS",
        "Root CA",
        "RDNS Names",
        "Min. RTT",
        "Max. RTT",
        "Locations"
    ]);

    for index, row in data.iterrows():
        table.add_row(build_row(row))


def build_row(index: str, data: pd.Series) -> list:
    res = [index]

    return res

