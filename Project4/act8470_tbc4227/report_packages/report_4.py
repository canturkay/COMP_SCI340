import pandas as pd
import texttable


def get_part4_table(data: pd.DataFrame) -> texttable.Texttable:
    table = texttable.Texttable()

    df = data.groupby(['http_server']).size().reset_index(name='count').sort_values(by=['count'], ascending=False)

    titles = [
        "Web Server",
        "Count"
    ]

    table.set_cols_align(['c'] * len(titles))
    table.header(titles)

    for index, row in df.iterrows():
        table.add_row(build_row(index=index, data=row))

    return table


def build_row(index: str, data: pd.Series) -> list:
    return [data['http_server'], data['count']]