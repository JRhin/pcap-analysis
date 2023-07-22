"""A script that performes an analysis over a pcap package using 'capinfos'.
"""

import polars as pl
from os import system
from pathlib import Path


# ============================================================
#                       Main Loop
# ============================================================

def main() -> None:
    import argparse
    from argparse import RawDescriptionHelpFormatter

    desc = """A script that performes an analysis over a pcap package using 'capinfos'.
    """

    # Defining the parser
    parser = argparse.ArgumentParser(description=desc, formatter_class=RawDescriptionHelpFormatter)
    parser.parse_args()

    # Defining directories
    current_path = Path('.')
    data_path = current_path/"data/"


    for pcap in data_path.glob('*.pcap'):

        print('=================================================================')
        print(f'Getting capture infos about {pcap}')
        print('=================================================================')
        print()

        print("Number of packets  in the capture:")
        print('-----------------------------------------------------------------')
        system(f'capinfos -c {pcap}')
        print()
        print()

        print('The average data reate in bits/sec:')
        print('-----------------------------------------------------------------')
        system(f'capinfos -i {pcap}')
        print()
        print()

        print('The average packet size:')
        print('-----------------------------------------------------------------')
        system(f'capinfos -z {pcap}')
        print()
        print()

        print('General all infos:')
        print('-----------------------------------------------------------------')
        system(f'capinfos -A {pcap}')
        print()
        print()

        print('Generating a capinfos.csv in the current directory...')
        capinfos_csv = data_path/'capinfos.csv'
        system(f'capinfos -TmQ {pcap} > {capinfos_csv}')
        print('Displaying the csv:')
        print('-----------------------------------------------------------------')
        print(pl.read_csv(capinfos_csv).transpose(include_header=True, header_name='Info', column_names=['Value']))


        print('=================================================================')
        print()
        print()
        print()


if __name__ == "__main__":
    main()
