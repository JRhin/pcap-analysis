"""Script to perform the topology analysis of the TCP and UDP networks.

This script assumes a 'pcap.parquet' file inside the 'data/' directory.
"""

import polars as pl
import seaborn as sns
from pathlib import Path
from tqdm.auto import tqdm
import graph_tool.all as gt
import matplotlib.pyplot as plt

# ========================================
#           Needed Functions
# ========================================

def get_graph(dataframe: pl.DataFrame,
              protocol: int) -> gt.Graph:
    """This function create a gt.Graph from a dataframe given a protocol type.

    Args:
        - dataframe (pl.DataFrame): The original polars.DataFrame.
        - protocol (int): The decimal value corrisponding to a protocol.

    Returns:
        -   gt.Graph() : The gt.Graph.
    """
    edges = (dataframe
             .lazy()
             .filter((pl.col('proto')==protocol))
             .select(pl.col('src'), pl.col('dst'), pl.col('len'))
             .collect())

    return gt.Graph(edges.rows(), hashed=True, eprops=[('weight', 'double')])


def get_diameter(graph: gt.Graph) -> int:
    """This function return the diameter of the given gt.Graph.

    Args:
        - graph (gt.Graph): The original gt.Graph.

    Returns:
        - diameter (int): The diameter of the given gt.Graph.
    """
    dist = gt.shortest_distance(graph, directed=True)
    diameter = 0
    for v in tqdm(graph.vertices(), desc=f'Calculating the diameter'):
        sh_paths = set(dist[v])
        sh_paths.remove(2147483647)
        if (temp:=max(sh_paths)) > diameter:
            diameter = temp
    return diameter


# ========================================
#               Main Loop
# ========================================

def main() -> None:
    import argparse
    from argparse import RawTextHelpFormatter

    desc="""Script to perform the topology analysis of the TCP and UDP networks.

    This script assumes a 'pcap.parquet' file inside the 'data/' directory.
    """

    # Define the argparse arguments
    parser = argparse.ArgumentParser(description=desc, formatter_class=RawTextHelpFormatter)
    args = parser.parse_args()

    current_path = Path('.')
    data_path = current_path/'data'
    pcap_path = data_path/'pcap.parquet'

    df = pl.scan_parquet(pcap_path)

    all_edges_df = (df
                    .groupby(['src', 'dst', 'proto'])
                    .agg(pl.col('len').sum())
                    .collect()).with_columns(len=1/pl.col('len')).sort(by='len', descending=True)

    # Plotting the graph for TCP
    print('Plotting the TCP network', end='')
    tcp_g = get_graph(all_edges_df, protocol=6)
    vb, eb = gt.betweenness(tcp_g)
    gt.graph_draw(tcp_g,
                  vertex_fill_color=gt.prop_to_size(vb, 0, 1, power=.1),
                  vertex_size=gt.prop_to_size(vb, 3, 12, power=.2),
                  vorder=vb,
                  output='tcp_network.pdf')
    print(', done.')


    # Plotting the largest component for TCP
    print('Plotting the TCP largest component', end='')
    tcp_lc = gt.extract_largest_component(tcp_g)
    vb, eb = gt.betweenness(tcp_lc)
    gt.graph_draw(tcp_lc,
                  vertex_fill_color=gt.prop_to_size(vb, 0, 1, power=.1),
                  vertex_size=gt.prop_to_size(vb, 3, 12, power=.2),
                  vorder=vb,
                  output='tcp_largest_component.pdf')
    print(', done.')

    # Plotting the graph for UDP
    print('Plotting the UDP network', end='')
    udp_g = get_graph(all_edges_df, protocol=17)
    vb, eb = gt.betweenness(udp_g)
    gt.graph_draw(udp_g,
                  vertex_fill_color=gt.prop_to_size(vb, 0, 1, power=.1),
                  vertex_size=gt.prop_to_size(vb, 3, 12, power=.2),
                  vorder=vb,
                  output='udp_network.pdf')
    print(', done.')

    # Plotting the largest component for UDP
    print('Plotting the UDP largest component', end='')
    udp_lc = gt.extract_largest_component(udp_g)
    vb, eb = gt.betweenness(udp_lc)
    gt.graph_draw(udp_lc,
                  vertex_fill_color=gt.prop_to_size(vb, 0, 1, power=.1),
                  vertex_size=gt.prop_to_size(vb, 3, 12, power=.2),
                  vorder=vb,
                  output='udp_largest_component.pdf')
    print(', done.')

    # Degree Distribution plot
    print('Getting the degree distribution', end='')
    degree_distribution = pl.concat([pl.DataFrame({'Degree': [v.in_degree()+v.out_degree() for v in tcp_g.vertices()],
                                                   'Protocol': 'TCP'}),
                                     pl.DataFrame({'Degree': [v.in_degree()+v.out_degree() for v in udp_g.vertices()],
                                                   'Protocol': 'UDP'})])
    plot = sns.scatterplot(degree_distribution.groupby(['Protocol', 'Degree']).count().to_pandas(),
                           x='Degree',
                           y='count',
                           hue='Protocol',
                           style='Protocol',
                           hue_order=['TCP', 'UDP'])
    plot.set(title='Degree Distribution TCP and UDP',
             xlabel='Degree', ylabel='Frequency',
             xscale='log', yscale='log')
    plot.figure.savefig('degree_distribution.svg')
    sns.despine()
    plt.show()
    print(', done.')

    # Analysing the diameter of the networks
    print(f'The TCP network diameter is {get_diameter(tcp_g)}, while the UDP network diameter is {get_diameter(udp_g)}.')

    # Analysing the clustering coefficient for all the graphs
    print()
    graphs = {'TCP network': tcp_g, 'TCP largest component': tcp_lc, 'UDP network': udp_g, 'UDP largest component': udp_lc}
    for g in graphs:
        print(f'The global clustering coefficient for {g} is: {gt.global_clustering(graphs[g])}')

    # Get the number of components
    print()
    _, tcp_hist = gt.label_components(tcp_g)
    _, udp_hist = gt.label_components(udp_g)
    print(f'TCP number of componets: {len(tcp_hist)}')
    print(f'UDP number of componets: {len(udp_hist)}')
    componets = pl.concat([pl.DataFrame({'components_nodes': tcp_hist,
                                         'Protocol': 'TCP'}),
                           pl.DataFrame({'components_nodes': udp_hist,
                                         'Protocol': 'UDP'})])
    plot = sns.displot(componets.to_pandas(),
                       x='components_nodes',
                       hue='Protocol',
                       col='Protocol',
                       log_scale=(True, True),
                       element='step',
                       stat='frequency')
    plot.fig.subplots_adjust(top=.8)
    plot.fig.suptitle('Node Distribution in components')
    plot.set(xlabel='Nodes in component')
    plot.figure.savefig('components_nodes_distribution.svg')
    sns.despine()
    plt.show()

    # Get number of edges and vertex for each graph
    print()
    for g in graphs:
        print(f'The {g} has {graphs[g].num_vertices()} vertices and {graphs[g].num_edges()} edges.')


    return None



if __name__ == "__main__":
    main()
