import networkx as nx

from database.DAO import DAO
from model.connessione import Connessione


class Model:
    def __init__(self):
        self._graph=nx.DiGraph() #grafo multiplo, orientato e pesato
        self._artists=DAO.getAllArtistWPopularity()
        self._idMapA={}
        for a in self._artists:
            self._idMapA[a.ArtistId]=a #associa l'artista al suo id
        self._nodes=[]


    def buildGraph(self, genreId):
        print("Costruzione grafo iniziata")
        self._nodes = DAO.getArtistForGenre(genreId, self._idMapA)
        self._graph.add_nodes_from(self._nodes)
        self.aggiungiArchi()

    def aggiungiArchi(self):
        conn=DAO.getConnessioniArtisti(self._idMapA)
        for c in conn:
            a1=c.artista1
            a2=c.artista2
            if a1 in self._nodes and a2 in self._nodes:
                #controllo se entrambi gli artisti della connessione sono nei nodi che ho trovato prima
                peso=a1.popularity+a2.popularity
                if a1.popularity>a2.popularity:
                    self._graph.add_edge(a1, a2, weight=peso)
                    #arco da a1 ad a2 se la popolarità di a1 è maggiore di a2
                if a1.popularity<a2.popularity:
                    self._graph.add_edge(a2, a1, weight=peso)
                if a1.popularity==a2.popularity:
                    self._graph.add_edge(a1, a2, weight=peso)
                    self._graph.add_edge(a2, a1, weight=peso)
                    #archi in entrambe le direzioni se stessa popolarità