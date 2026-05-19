import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._genere=None

    def fillDDGenre(self):
        listaGeneri=DAO.getAllGenres()
        for g in listaGeneri:
            self._view._ddGenre.options.append(
                ft.dropdown.Option(key=g.GenreId,
                                   text=g.Name,
                                   data=g,
                                   on_click=self.readGenre))

    def fillDDArtist(self, e):
        if self._genere is None:
            return
        genere=self._genere
        genreId=genere.GenreId
        diz=self._model.getDictArtists()
        listaArtisti=DAO.getArtistForGenre(genreId, diz)
        self._view._ddArtist.options.clear() #svuotiamo le opzioni precedenti
        self._view._ddArtist.value = None #resettiamo l'eventuale scelta precedente
        for a in listaArtisti:
            self._view._ddArtist.options.append(
                ft.dropdown.Option(key=a.ArtistId,
                                   text=a.Name,
                                   data=a,
                                   on_click=self.readArtist))

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        if self._view._ddGenre.value is None:
            self._view.create_alert("Selezionare un genere musicale!")
            return
        self.fillDDArtist(e)
        genere=self._genere
        genreId=genere.GenreId
        self._model.buildGraph(genreId)
        a, inf=self._model.getArtistaPiuInfluente()
        self._view.txt_result.controls.extend(
            [ft.Text("Grafo correttamente creato:"),
             ft.Text(f"Numero di nodi: {self._model.getNNodi()}"),
             ft.Text(f"Numero di archi: {self._model.getNArchi()}"),
             ft.Text(f"Artista più influente: {a.Name}, con influenza: {inf}"),
             ft.Text("Top 5 archi:")]
        )
        for arco in self._model.getArchiPesoMaggiore(): #lista di tuple arco
            self._view.txt_result.controls.append(ft.Text(
                f"{arco[0].Name} -> {arco[1].Name}: {arco[2]}"
            ))
        self._view.update_page()

    def handleCammino(self,e):
        pass

    def readGenre(self, e):
        self._genere=e.control.data

    def readArtist(self, e):
        self._artist=e.control.data