import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._genere=None
        self._artist=None

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        if self._genere is None:
            self._view.txt_result.controls.append(
                ft.Text("Selezionare prima un genere musicale!", color="red")
            )
            self._view.update_page()
            return
        v=self._view._txtInMinV.value
        if v=="":
            self._view.txt_result.controls.append(
                ft.Text("Inserire un numero minimo di vendite!", color="red")
            )
            self._view.update_page()
            return
        try:
            minV=int(v)
        except ValueError:
            self._view.txt_result.controls.append(
                ft.Text("Il numero minimo di vendite deve essere un intero positivo!", color="red")
            )
            self._view.update_page()
            return
        if minV<0:
            self._view.txt_result.controls.append(
                ft.Text("Il numero minimo di vendite deve essere un intero positivo!", color="red")
            )
            self._view.update_page()
            return
        self._model.buildGraph(self._genere, minV)
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato!\n"
                    f"Numero di vertici: {self._model.getNNodes()}\n"
                    f"Numero di archi: {self._model.getNEdges()}")
        )
        self.fillDDArtist()
        self._view.update_page()

    def handleAnalizza(self, e):
        if self._model.getNNodes()==0:
            self._view.txt_result.controls.append(
                ft.Text("Creare prima il grafo!", color="red")
            )
            self._view.update_page()
            return
        if self._model.getNEdges()==0:
            self._view.txt_result.controls.append(
                ft.Text("Non ci sono archi nel grafo", color="red")
            )
            self._view.update_page()
            return
        self._view.txt_result.controls.append(
            ft.Text(f"Top influencer: {self._model.getTopArtist()}\n"
                    f"Artisti collegati:")
        )
        for a, peso in self._model.getListArtists():
            self._view.txt_result.controls.append(
                ft.Text(f"{a}, peso arco: {peso}"))
        self._view.update_page()

    def handleCammino(self,e):
        self._view.txt_result.controls.clear()
        if self._model.getNNodes() == 0:
            self._view.txt_result.controls.append(
                ft.Text("Creare prima il grafo!", color="red")
            )
            self._view.update_page()
            return
        if self._model.getNEdges()==0:
            self._view.txt_result.controls.append(
                ft.Text("Non ci sono archi nel grafo", color="red")
            )
            self._view.update_page()
            return
        if self._artist is None:
            self._view.txt_result.controls.append(
                ft.Text("Selezionare un artista di partenza!", color="red")
            )
            self._view.update_page()
            return
        txtM = self._view._txtInM.value
        if txtM == "":
            self._view.txt_result.controls.append(
                ft.Text("Inserire una lunghezza massima!", color="red")
            )
            self._view.update_page()
            return
        try:
            m = int(txtM)
        except ValueError:
            self._view.txt_result.controls.append(
                ft.Text("M deve essere un intero positivo!", color="red")
            )
            self._view.update_page()
            return
        if m <= 0:
            self._view.txt_result.controls.append(
                ft.Text("M deve essere un intero positivo!", color="red")
            )
            self._view.update_page()
            return
        path, score=self._model.getBestPath(self._artist, m)
        self._view.txt_result.controls.append(
            ft.Text(f"Cammino migliore trovato, con punteggio totale {score}:")
        )
        for i in range(len(path)):
            a=path[i]
            self._view.txt_result.controls.append(
                ft.Text(f"{a.Name} - {a.ArtistId}, {a.nTracce} tracce totali vendute, peso arco: {self._model.getPesoArco(i)}")
            )
        self._view.update_page()

    def fillDDGenre(self):
        generi=self._model.getAllGenres()
        generiOpt=list(map(lambda x: ft.dropdown.Option(text=x.Name,
                                                        key=x.GenreId,
                                                        data=x,
                                                        on_click=self.readDDGenre), generi))
        self._view._ddGenre.options=generiOpt
        self._view.update_page()

    def readDDGenre(self, e):
        self._genere=e.control.data

    def fillDDArtist(self):
        artisti=self._model.getAllNodes()
        artistiOpt=list(map(lambda x: ft.dropdown.Option(text=x.Name,
                                                        key=x.ArtistId,
                                                        data=x,
                                                        on_click=self.readDDArtist), artisti))
        self._view._ddArtist.options=artistiOpt
        self._view.update_page()

    def readDDArtist(self, e):
        self._artist=e.control.data
