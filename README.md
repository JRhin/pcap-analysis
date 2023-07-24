# NBD Lab Project

## Directory structure

```
./root
  |_ .env
  |_ README.md
  |_ requirements.txt
  |_ main_notebook.ipynb
  |_ /data/
  |   |_ pcap_all.zip
  |_ /img/
  |   |_ components_nodes_distribution.svg
  |   |_ degree_distribution.svg
  |   |_ tcp_largest_component.svg
  |   |_ tcp_network.svg
  |   |_ udp_largest_components.svg
  |   |_ udp_network.svg
  |_ /src/
      |_ download_extract.py
      |_ capinfos.py
      |_ extract_packets.py
      |_ model.py
      |_ topology_analysis.py
```
## Dependencies

 - Wireshark: to install it just follow the specific guide for your machine that you can find [here](https://www.wireshark.org/download.html).
 - Some python modules: to install them just run in a terminal `pip install -r requirements.txt` from the root directory of the project.

## Setup

1. Clone this repository.

2. **Optional**: It is strongly suggested to create and activate a python virtual environment in the project root folder, then remember to set the environment as kernel for `main_notebook.ipynb` ([here](https://janakiev.com/blog/jupyter-virtual-envs/) a guide).

3. Install the needed dependencies.

4. **Optional**: run in the project root folder `python src/download_extract.py` to retrieve the pcap file and store it in the `data/` directory. This step is mandatory for running `capinfos.py` and `extract_packets.py`.
