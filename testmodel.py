from database.DAO import DAO
from model.artist import Artist
from model.genre import Genre
from model.model import Model

modello=Model()
modello.buildGraph(Genre(1, "Rock"), 20)
modello.getBestPath(Artist(90, "Iron Maiden", 140), 4)
