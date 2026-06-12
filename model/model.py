import copy
import operator

import networkx as nx

from database.DAO import DAO
from model.Artist import Artist


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._artisti = {}
        self._popolarita = {}
        self._influenza = {}
        self._bestPath = []

    def getBestPath(self, artist):

        self._bestPath = []

        parziale = [self._artisti[int(artist)]]

        self._ricorsione(parziale, -1)

        return self._bestPath


    def _ricorsione(self, parziale, lastWeight):

        if len(parziale) > len(self._bestPath):
            self._bestPath = copy.deepcopy(parziale)

        nodo_corrente = parziale[-1]

        for i in self._graph.out_edges(nodo_corrente,data=True):
            peso = i[2]['weight']

            if peso > lastWeight:
                if i[1] not in parziale:
                    parziale.append(i[1])
                    self._ricorsione(parziale, peso)
                    parziale.pop()


    def buildGraph(self, genre):
        self._graph.clear()
        nodes = DAO.getAllArtistByGenre(genre)
        self._graph.add_nodes_from(nodes)

        for artist in nodes:
            self._artisti[artist.ArtistId] = artist

        print(f"Sono stati aggiunti {len(nodes)} vertici al grafo")

        lista_popolarita = DAO.getPopolarita(self._artisti, genre)

        for artista, pop in lista_popolarita:
            self._popolarita[artista] = pop

        self.addEdges(self._artisti, genre)

        print(f"Sono stati aggiunti {len(self._graph.edges)} archi al grafo")



    def getAllGenre(self):
        return DAO.getAllGenre()

    def getAllArtistGenre(self):
        return self._graph.nodes

    def addEdges(self, artisti, genre):
        edges = DAO.getArchi(artisti,genre)

        for u, v in edges:
            pop_u = self._popolarita[u]
            pop_v = self._popolarita[v]
            peso = pop_u + pop_v

            if pop_u > pop_v:
                self._graph.add_edge(u, v, weight=peso)

            elif pop_u < pop_v:
                self._graph.add_edge(v, u, weight=peso)

            else:
                self._graph.add_edge(u, v, weight=peso)
                self._graph.add_edge(v, u, weight=peso)

    def getInfluenza(self):
        for artista in self._graph.nodes:
            pesoEntranti = self._graph.in_degree(artista, weight='weight')
            pesoUscenti = self._graph.out_degree(artista, weight='weight')
            self._influenza[artista] = pesoUscenti - pesoEntranti
        return self._influenza

    def getTop5Archi(self):
        return sorted(self._graph.edges(data= True), key = lambda x: x[2]['weight'], reverse = True)[:5]