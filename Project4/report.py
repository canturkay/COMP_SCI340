import json

import pandas as pd
import sys


def main():
    with open(sys.argv[1]) as f:
        data = json.load(f)

    json_data = pd.DataFrame(data)
    print(json_data)


if __name__ == '__main__':
    main()
