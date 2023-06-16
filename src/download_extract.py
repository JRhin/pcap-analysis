"""A script to download a .7z file from google drive using gdown, and extract its contents.

To change google id just change the id variable inside the '.env' file.
"""

from pathlib import Path
from gdown import download
from tqdm.auto import tqdm
from py7zr import SevenZipFile
from dotenv import dotenv_values


# =========================================================
#                   Needed Functions
# =========================================================

# Function to unzip the .7z file
def extract_pcap(path: Path) -> None:
    """
    Function to extract the pcap file from a .7z compressed file.

    Args:
        -   path (pathlib.Path): The path of the directory containing the .7z files.

    Return:
        -   None
    """
    for zipped_file in tqdm(list(path.glob("*.7z")), desc='Extracting the 7z files'):
        with SevenZipFile(zipped_file) as f:
            f.extractall(path)

    return None


# ============================================================
#                       Main Loop
# ============================================================

def main():
    import argparse
    from argparse import RawDescriptionHelpFormatter

    desc="""A script to download a .7z file from google drive using gdown, and extract its contents.

    To change google id just change the id variable inside the '.env' file.
    """

    # Defining arguments for the argparse
    parser = argparse.ArgumentParser(description=desc, formatter_class=RawDescriptionHelpFormatter  )
    parser.add_argument('-o', '--output', type=str, default='file.7z', help="The name of the dowload output file. Default file.7z .")
    parser.add_argument('-e', '--env', type=str, default='.env', help="The path towards the dotenv file. Default .env .")
    args = parser.parse_args()

    # Defining the needed directories
    current_path = Path('.')
    data_path = current_path/'data/'

    # Get the output path
    output_path = data_path/args.output

    # Load the dotenv file
    config = dotenv_values(args.env)

    # Trying to download the file
    if output_path.is_file():
        answer = input(f'A {output_path.name} already exists. Remove it and proceed? [Y/n]: ')

        match answer:
            case 'y' | 'Y' | '':
                # Download the file
                download(id=config['id'], output=str(output_path), quiet=False)
            case 'n'| 'N':
                pass
            case _:
                raise Exception('Input passed was not a possible choise.')

    # Extract the pcap
    extract_pcap(data_path)


if __name__ == "__main__":
    main()
