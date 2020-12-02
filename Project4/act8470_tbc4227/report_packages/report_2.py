import pandas as pd
import texttable


def get_part2_table(data: pd.DataFrame) -> texttable.Texttable:
    table = texttable.Texttable()

    titles = [
        "Domain Name",
        "Minimum RTT",
        "Maximum RTT"
    ]

    table.set_cols_align(['c'] * len(titles))
    table.header(titles)

    for index, row in data.sort_values(by=['rtt_min']).iterrows():
        table.add_row(build_row(index=index, data=row))

    return table


def build_row(index: str, data: pd.Series) -> list:
    return [index, data['rtt_min'], data['rtt_max']]