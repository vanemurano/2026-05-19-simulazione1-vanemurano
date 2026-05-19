import networkx as nx

from database.DAO import DAO
from model.connessione import Connessione


class Model:
    def __init__(self):
        self._graph=nx.DiGraph() #grafo multiplo, orientato e pesato
        self._artists=DAO.getAllArtist()
        self._idMapA={}
        for a in self._artists:
            self._idMapA[a.ArtistId]=a #associa l'artista al suo id

    def buildGraph(self, genreId):
        self._graph.clear()
        print("Costruzione grafo iniziata")
        self._nodes = DAO.getArtistForGenre(genreId, self._idMapA)
        #tutti gli artisti di quel genere
        self._graph.add_nodes_from(self._nodes)
        self.aggiungiArchi(genreId)

    def aggiungiArchi(self, genreId):
        conn=DAO.getConnessioniArtisti(self._idMapA, genreId)
        for c in conn:
            a1=c.artista1
            a2=c.artista2
            pop1=DAO.getArtistWPopularity(a1.ArtistId, genreId)
            pop2=DAO.getArtistWPopularity(a2.ArtistId, genreId)
            if a1 in self._nodes and a2 in self._nodes:
                #controllo se entrambi gli artisti della connessione sono nei nodi che ho trovato prima
                peso=pop1+pop2
                if pop1>pop2:
                    self._graph.add_edge(a1, a2, weight=peso)
                    #arco da a1 ad a2 se la popolarità di a1 è maggiore di a2
                if pop1<pop2:
                    self._graph.add_edge(a2, a1, weight=peso)
                if pop1==pop2:
                    self._graph.add_edge(a1, a2, weight=peso)
                    self._graph.add_edge(a2, a1, weight=peso)
                    #archi in entrambe le direzioni se stessa popolarità

    def getNNodi(self):
        return len(self._nodes)

    def getNArchi(self):
        return len(self._graph.edges)

    def getArchiPesoMaggiore(self):
        archi=list(self._graph.edges)
        listaArchiPesati=[]
        for (a1, a2) in archi:
            peso=self._graph.get_edge_data(a1, a2)["weight"]
            listaArchiPesati.append((a1, a2, peso)) #lista di tuple
        listaArchiPesati.sort(key=lambda x: x[2], reverse=True)
        #ordina in base al terzo elemento della tupla, cioè il peso dell'arco
        return listaArchiPesati[0:5]

    def getArtistaPiuInfluente(self):
        listaA=[]
        for a in self._nodes:
            influenza=self._graph.out_degree(a, weight='weight')-self._graph.in_degree(a, weight='weight')
            #peso archi uscenti - peso archi entranti
            listaA.append((a, influenza)) #tupla artista influenza
        listaA.sort(key=lambda x: x[1], reverse=True) #ordino per influenza
        return listaA[0] #ritorna il primo elemento, quello più influente

    def getDictArtists(self):
        return self._idMapA