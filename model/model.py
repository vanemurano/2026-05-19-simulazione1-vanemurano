import copy

import networkx as nx

from database.DAO import DAO
from model.connessione import Connessione


class Model:
    def __init__(self):
        self._graph=nx.DiGraph() #grafo semplice, orientato e pesato
        self._nodes = []
        self._idMapArtists={}
        for a in DAO.getAllArtists():
            self._idMapArtists[a.ArtistId]=a
        self._topArtist=None
        self._bestPath=[]
        self._bestScore=0

    def getAllGenres(self):
        return DAO.getAllGenres()

    def buildGraph(self, genre, minV):
        self._nodes=[]
        self._graph.clear()
        self._nodes=DAO.getAllNodes(genre.GenreId, minV)
        for a1, a2, peso in DAO.getAllEdges(self._idMapArtists):
            if a1 in self._nodes and a2 in self._nodes:
                ricavo1=DAO.getRicavo(a1.ArtistId)
                ricavo2=DAO.getRicavo(a2.ArtistId)
                if ricavo1>ricavo2:
                    self._graph.add_edge(a1, a2, weight=peso)
                if ricavo1<ricavo2:
                    self._graph.add_edge(a2, a1, weight=peso)

    def getNNodes(self):
        return len(self._nodes)

    def getNEdges(self):
        return len(self._graph.edges)

    def getTopArtist(self):
        nodi=list(self._nodes)
        nodi.sort(key=lambda x: self._graph.out_degree(x), reverse=True)
        maxGrado=self._graph.out_degree(nodi[0]) # max grado in uscita
        maxList=[n for n in nodi if self._graph.out_degree(n)==maxGrado]
        # lista con tutti i nodi di grado in uscita massimo
        res=[]
        for a in maxList:
            peso=0
            for nodo in self._graph.successors(a):
                peso+=self._graph[a][nodo]["weight"]
            res.append((a, peso))
        res.sort(key=lambda tupla: tupla[1], reverse=True)
        self._topArtist=res[0][0]
        return self._topArtist

    def getListArtists(self):
        lista=[]
        for n in self._graph.successors(self._topArtist):
            lista.append((n, self._graph[self._topArtist][n]["weight"]))
        lista.sort(key=lambda x: x[1], reverse=True)
        return lista

    def getAllNodes(self):
        return self._nodes

    def getBestPath(self, source, m):
        self._bestPath = []
        self._bestScore = 0
        parziale=[source]
        self._ricorsione(parziale, m, 0)
        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale, m, score):
        # condizione di ottimalità
        if score > self._bestScore:
            self._bestPath = copy.deepcopy(parziale)
            self._bestScore = score
        # condizione terminale
        if len(parziale)>=m:
            return
        for a in self._graph.successors(parziale[-1]):
            if (a.nTracce % 2)!=(parziale[-1].nTracce % 2) and a not in parziale:
                peso=self._graph[parziale[-1]][a]["weight"]
                new_score=score+peso
                parziale.append(a)
                self._ricorsione(parziale, m, new_score)
                parziale.pop() # backtracking

    def getPesoArco(self, i):
        if i==(len(self._bestPath)-1):
            return 0
        return self._graph[self._bestPath[i]][self._bestPath[i+1]]["weight"]
        # peso dell'arco tra il nodo all'indice i e il successivo nella soluzione