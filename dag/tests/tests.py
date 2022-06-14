from dag import DAG
import tempfile
from pathlib import Path

def test_nb_vertices_and_edges():
    edges = [(0, 1),(1,1),(2,3),(1,3)]
    G = DAG(edges)
    assert G.get_number_edges() == 4
    assert G.get_number_vertices() == 4

def test_serialize():
    edges = [(0, 1),(1,1),(2,3),(1,3)]
    G = DAG(edges)
    file_path = Path(tempfile.gettempdir()) / 'graph.hdf5'
    G.serialize(file_path)
    GG = DAG.deserialize(file_path)
    assert GG.get_number_edges() == G.get_number_edges()
    assert GG.get_number_vertices() == G.get_number_vertices()