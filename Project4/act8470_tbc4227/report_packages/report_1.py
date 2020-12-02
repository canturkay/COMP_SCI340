from datetime import datetime

import pandas as pd
import texttable


def get_part1_table(data: pd.DataFrame) -> texttable.Texttable:
    table = texttable.Texttable()
    table.set_cols_width([
        15,
        15,
        17,
        25,
        8,
        10,
        13,
        6,
        10,
        20,
        25,
        5,
        5,
        20,
    ])

    titles = [
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
    ]

    table.set_cols_align(['c'] * len(titles))
    table.header(titles)

    for index, row in data.iterrows():
        table.add_row(build_row(index=index, data=row))

    return table


def build_row(index: str, data: pd.Series) -> list:
    res = [index, datetime.utcfromtimestamp(data['scan_time'])]

    fields = [
        'ipv4_addresses',
        'ipv6_addresses',
        'http_server',
        'insecure_http',
        'redirect_to_https',
        'hsts',
        'tls_versions',
        'root_ca',
        'rdns_names',
        'rtt_min',
        'rtt_max',
        'geo_locations'
    ]

    for field in fields:
        field_data = data[field]
        if isinstance(field_data, bool):
            res.append('YES' if data[field] else 'NO')
        elif isinstance(field_data, list):
            res.append('\n'.join(field_data))
        else:
            res.append(data[field])

    return res
