# NBD Lab Project

In this repository there is the solution to the Networking for Big Data Laboratory Project.

The Lab Project was about analysing a trace of packets retrieved from the traffic trace of 10/04/2019.

The dataset was provided by the Mawi Project and can be found [here](https://drive.google.com/drive/folders/1YMwwPoekwJrw_-UYkZYUkTFqC8bqAy0F).

## The analysis

General analysis:

- Extract general info from your trace using capinfos.
- Time Evaluation between Sequential and Parallel reading.
- Extract the IP which generates the highest amount of sender traffic, evaluate the bit rate (0.1 sec) for the 6 IP addresses mostly used as endpoint.
- Top 5 Destination IP (received bytes) and Top 5 Source IP (sent bytes).
- Evaluate the bit rate considering all the trace with 3 different sampling rate.
- GeoLocal Reference of the 5 sessions with the highest amount of traffic generated.
- 10 mostly used protocols.
- Port Scanner evaluation (10 Ports mostly used).
- Inter Arrival Time box plot between TCP and UDP Sessions.
- Topology analysis over TCP and UDP network.

Classification between TCP and UDP protocols:

- Our candidate features
  - Unsupervised: KMeans.
  - Supervised: Naive Bayes (baseline), SVM, xgBoost.
- Abacus Signatures
  - Supervised: Naive Bayes (baseline), SVM, xgBoost.

The results of the analysis is reported inside the `main_notebook.ipynb` notebook.

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

## Team

- [Mario Edoardo Pandolfo](https://github.com/JRhin)
- [Gabriele Pelliccioni](https://github.com/gabrielepelliccioni13)
- [Giuseppe di Poce](https://github.com/giuseppedipoce)
