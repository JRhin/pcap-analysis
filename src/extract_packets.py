"""Script for extracting packets from a .pcap file.

Packets infos from the IP layer are stored in a .jsonl file called 'pcap.jsonl'.

The script assumes that the directory follows this structure:

    root/
    |_ data/

The .pcap file (one or more) must be saved in the 'data/' directory and the script must be launched from the 'root/' directory.

The .jsonl file is going to be saved in the 'data/' directory.

Note: To read the packets sequentially just set n_jobs to 1, by adding '-j 1' or '--jobs 1'.
"""

# Importing the needed libraries
import pyshark
import polars as pl
from time import time
from pathlib import Path
from tqdm.auto import tqdm

from model import Packet

import json
import jsonlines
from joblib import Parallel, delayed



# =========================================================
#                   Needed Functions
# =========================================================

@delayed
def read_packet(packet: pyshark.packet,
                path: Path) -> None:
    """Function to read and store the infos of a packet.

    Args:
        - packet (pyshark.packet): A pyshark.packet to query from.
        - path (pathlib.Path): The path towards the .jsonl file where the function will append the infos.

    Return:
        - None
    """
    # We extract the packets only from the IP level
    if 'IP' in packet:
        pckt = Packet(dsfield_dscp=packet.ip.dsfield_dscp,
                      hdr_len=packet.ip.hdr_len,
                      dsfield=packet.ip.dsfield,
                      dsfield_ecn=packet.ip.dsfield_ecn,
                      len=packet.ip.len,
                      proto=packet.ip.proto,
                      flags_df=packet.ip.flags_df,
                      flags_mf=packet.ip.flags_mf,
                      flags_rb=packet.ip.flags_rb,
                      frag_offset=packet.ip.frag_offset,
                      ttl=packet.ip.ttl,
                      src=packet.ip.src,
                      dst=packet.ip.dst,
                      srcport=packet.udp.srcport if 'UDP' in packet else packet.tcp.srcport if 'TCP' in packet else -1,
                      dstport=packet.udp.dstport if 'UDP' in packet else packet.tcp.dstport if 'TCP' in packet else -1,
                      sniff_timestamp=packet.sniff_timestamp)
        
        # Append the pckt.json() to the .jsonl file
        with jsonlines.open(path, mode='a') as writer:
            writer.write(json.loads(pckt.model_dump_json()))

    return None


def read_pcap(path: Path,
              save_to: Path,
              n_jobs: int = -1,
              verbose: int = 0) -> float:
    """A function used to read in parallel or in sequential the packets of a pcap.

    Args:
        -   path (pathlib.Path):    The path towards the pcap file.
        -   save_to (pathlib.Path): The path where the info are going to be saved.
        -   n_jobs (int):   Needed for the joblib.Parallel() function, it defines the number of workes used to run a function.
                            If it is set to -1 then all available workers are used. Default -1.
        -   verbose (int):  Used by joblib.Parallel() function, used for printing logs of the work status. Default 0.

    Return:
        -   float : The required time for reading all the pcap packets.
    """
    start = time()
    with pyshark.FileCapture(path) as pcap:
        Parallel(n_jobs=n_jobs, require="sharedmem", verbose=verbose)(read_packet(packet=packet, path=save_to) for packet in pcap)
    end = time()
    return end-start



# ============================================================
#                       Main Loop
# ============================================================

def main() -> None:
    import argparse
    from argparse import RawTextHelpFormatter

    desc = """Script for extracting packets from a .pcap file.

    Packets infos from the IP layer are stored in a .jsonl file called 'pcap.jsonl'.

    The script assumes that the directory follows this structure:

        root/
        |_ data/
    

    The .pcap file (one or more) must be saved in the 'data/' directory and the script must be launched from the 'root/' directory.

    The .jsonl file is going to be saved in the 'data/' directory.

    Note: To read the packets sequentially just set n_jobs to 1, by adding '-j 1' or '--jobs 1'.
    """

    # Define the argparse arguments
    parser = argparse.ArgumentParser(description=desc, formatter_class=RawTextHelpFormatter)
    parser.add_argument('-j', '--jobs', type=int, default=-1, help='Number of workers (it sets the n_jobs of joblib.Parallel()). If set to -1 all available workers are used. Default -1.')
    parser.add_argument('-v', '--verbose', type=int, default=0, help='Set the verbose variable for joblib.Parallel(). Default 0.')
    args = parser.parse_args()
   
    # Defines all the needed paths
    current_path = Path('.')
    data_path = current_path/"data/"
    jsonl_path = data_path/"pcap.jsonl"

    assert data_path.exists(), "The 'data/' directory doesn't exist, but required. Run '--help' for more insights."

    # Check if the .json file exists.
    if jsonl_path.is_file():

        # Ask permission to remove the .jsonl file.
        answer = input("A 'pcap.jsonl' file already exists. Remove it and proceed? [Y/n]: ") 
        match answer:
            case 'y' | 'Y' | '':
                # Remove the file
                jsonl_path.unlink(missing_ok=True)
            case 'n' | 'N':
                # Abort
                print('Nothing to do then, abort.')
                return None
            case _:
                raise Exception(f"'{answer}' was not in the options...")

    # Start to read each pcap file
    print()
    for pcap_path in data_path.glob("*.pcap"):
        print(f"Reading pcap {pcap_path}...")
        required_time = read_pcap(path=pcap_path,
                                  save_to=jsonl_path,
                                  n_jobs=args.jobs,
                                  verbose=args.verbose)
        print()
        print(f'Time required for reading all packets of {pcap_path}: {required_time} seconds.')
        print()
        print()

        # We save a .parquet copy
        pl.read_ndjson(jsonl_path).write_parquet(f'{data_path/pcap_path.stem}.parquet')



if __name__ == "__main__":
    main()
