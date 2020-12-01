import json
import sys

import pandas as pd
import numpy as np

from report_packages.report_1 import get_part1_table
from report_packages.report_2 import get_part2_table
from report_packages.report_3 import get_part3_table


def main():
    with open(sys.argv[1]) as f:
        data = json.load(f)

    df = pd.DataFrame(data).transpose()

    df.rtt_range = df.rtt_range.replace(np.nan, 0)

    df[['rtt_min', 'rtt_max']] = df.rtt_range.to_list()

    part_1_table = get_part1_table(data=df)
    part_2_table = get_part2_table(data=df)
    part_3_table = get_part3_table(data=df)
    write_to_file(content=part_1_table.draw() + '\n' +  part_2_table.draw() + '\n' +  part_3_table.draw(), file_name=sys.argv[2])


def write_to_file(content: str, file_name: str):
    with open(file_name, "w") as f:
        f.write(content)


if __name__ == '__main__':
    main()
