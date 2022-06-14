from pathlib import Path
from typing import List, Tuple, Union

import h5py
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


class DAG():
    def __init__(self, edges: Union[np.ndarray, List[Tuple[int, int]]]):
        if isinstance(edges, np.ndarray):
            _graph = nx.from_numpy_array(edges, create_using=nx.MultiDiGraph)
        elif isinstance(edges, list):
            _graph = nx.from_edgelist(edges, create_using=nx.MultiDiGraph)
        else:
            raise ValueError(
                "Can only create a graph from numpy array or List[Tuple[int,int]]")
        # put labels on nodes
        self.graph = nx.relabel_nodes(
            _graph, {a: int(a) for a in _graph.nodes()})

    def get_number_vertices(self) -> int:
        return self.graph.number_of_nodes()

    def get_number_edges(self) -> int:
        return self.graph.number_of_edges()

    def _draw(self):
        _, ax = plt.subplots(figsize=(5, 5))
        ax.set_title('Graph plot')
        nx.draw_networkx(self.graph, pos=nx.spring_layout(self.graph))

    def save_graph_to_png(self, filename : Path = Path('plotgraph.png')):
        self._draw()
        plt.savefig(filename, dpi=300, bbox_inches='tight')

    def _histogram(self):
        degree_histogram = nx.degree_histogram(self.graph)
        plt.bar(range(1, len(degree_histogram)+1), degree_histogram)
        plt.ylabel('frequency')
        plt.xlabel('Node id')
        plt.title('Histogram of vertex out-degrees')

    def draw_histogram(self):
        self._histogram()
        plt.show()

    def save_histogram_to_png(self, filename : Path = Path('histogram.png')):
        self._histogram()
        plt.savefig(filename, dpi=300, bbox_inches='tight')

    def serialize(self, filename: Path = Path('graph-dump.hdf5')):
        try:
            _np_array = nx.to_numpy_array(self.graph)
            f = h5py.File(str(filename), 'w')
            f.create_dataset("graph", data=_np_array)
        finally:
            f.close()

    def deserialize(filepath: Union[str, Path]) -> 'DAG':
        try:
            f = h5py.File(str(filepath), 'r')
            edge_list = f['graph'][()]
            result = DAG(edge_list)
        finally:
            f.close()
        return result
