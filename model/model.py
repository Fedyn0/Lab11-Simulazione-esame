import networkx as nx

from database.DAO import DAO
from networkx import Graph

class Model:
    def __init__(self):
        self._graph = nx.DiGraph()

    def buildGraph(self, genre):
        self._graph.clear()
        nodes = DAO.getAllArtistByGenre(genre)
        self._graph.add_nodes_from(nodes)
        print(f"Sono stati aggiunti {len(nodes)} vertici al grafo")


    def getAllGenre(self):
        return DAO.getAllGenre()

    def getAllArtistGenre(self):
        return self._graph.nodes