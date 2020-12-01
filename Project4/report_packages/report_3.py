import pandas as pd
import texttable


def get_part3_table(data: pd.DataFrame) -> texttable.Texttable:
    table = texttable.Texttable()

    df = data.groupby(['root_ca']).size().reset_index(name='count').sort_values(by=['count'], ascending=False)

    titles = [
        "Root Certificate Authority",
        "Count"
    ]

    table.set_cols_align(['c'] * len(titles))
    table.header(titles)

    for index, row in df.iterrows():
        table.add_row(build_row(index=index, data=row))

    return table


def build_row(index: str, data: pd.Series) -> list:
    return [data['root_ca'], data['count']]