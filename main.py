import json
from typing import Dict, Union

from decrypter import TdataReader

if __name__ == '__main__':
    import argparse

    #tdata_path = r"D:\Telegram Desktop\tdata"
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str,required=True, help='Path / directory')
    parser.add_argument('-o', type=str, help='')
    args = parser.parse_args()


    reader = TdataReader(args.i)
    parsed_tdata = reader.read()

    if args.o is None:
        for account in parsed_tdata.accounts.values():
            print(account.get_info())
            print(parsed_tdata.proxy)
    else:
        for account in parsed_tdata.accounts.values():
            json_data = json.dumps([account.get_info(), parsed_tdata.proxy])
            with open(args.o, 'w') as json_file:
                json_file.write(json_data)


