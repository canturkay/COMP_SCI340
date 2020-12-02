import pandas as pd
import texttable


def get_part5_table(data: pd.DataFrame) -> texttable.Texttable:
    table = texttable.Texttable()

    df = pd.DataFrame(data)

    df['TLSv1.0'] = df['tls_versions'].str.contains('TLSv1.0', na=False, regex=False)
    df['TLSv1.1'] = df['tls_versions'].str.contains('TLSv1.1', na=False, regex=False)
    df['TLSv1.2'] = df['tls_versions'].str.contains('TLSv1.2', na=False, regex=False)
    df['TLSv1.3'] = df['tls_versions'].str.contains('TLSv1.3', na=False, regex=False)
    df['SSLv2'] = df['tls_versions'].str.contains('SSLv2', na=False, regex=False)
    df['SSLv3'] = df['tls_versions'].str.contains('SSLv3', na=False, regex=False)

    df.loc[df['ipv6_addresses'].str.len() == 0, 'ipv6_enabled'] = 0.0
    df.loc[df['ipv6_addresses'].str.len() != 0, 'ipv6_enabled'] = 1.0

    filters = ['TLSv1.0', 'TLSv1.1', 'TLSv1.2', 'TLSv1.3', 'SSLv2', 'SSLv3', 'insecure_http', 'redirect_to_https',
               'hsts', 'ipv6_enabled']
    res = []
    for index in filters:
        res.append(get_percentage(data=df, index=index, length=len(data)))

    titles = ['TLSv1.0', 'TLSv1.1', 'TLSv1.2', 'TLSv1.3', 'SSLv2', 'SSLv3', 'Insecure HTTP', 'Redirect to HTTPS',
              'HTTP Strict Transport Security', 'IPv6 Enabled']

    table.set_cols_width([7, 7, 7, 7, 7, 7, 10, 10, 10, 10])
    table.set_cols_align(['c'] * len(titles))
    table.header(titles)
    table.add_row(res)

    return table


def get_percentage(data: pd.DataFrame, index: str, length: int) -> float:
    df_new = data.groupby([index]).size().reset_index(name='count').sort_values(by=[index], ascending=False)

    return str(int(data[index].sum() / length * 100)) + " %"
