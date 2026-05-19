from database.DAO import DAO
from model.model import Model

modello=Model()
print(DAO.getArtistWPopularity(150, 1)) #funziona
grafo=modello._graph
modello.buildGraph(1)
print(f"Numero nodi: {modello.getNNodi()}")
print(f"Numero archi: {modello.getNArchi()}")
dizPop=modello._dizPopolarita
for a in dizPop.keys:
    print(f"{a}: {dizPop[a]}")