import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        listaGeneri=DAO.getAllGenres()
        for g in listaGeneri:
            self._view._ddGenre.options.append(
                ft.dropdown.Option(key=g,
                                   text=g.Name,
                                   on_click=self.readGenre))

    def handleCreaGrafo(self, e):
        genreId=self._genere.GenreId
        self._model.buildGraph(genreId)
        self._view.txt_result.controls.append(
            ft.Text("Grafo correttamente creato!")
        )
        self._view.update_page()

    def handleCammino(self,e):
        pass

    def readGenre(self, e):
        self._genere=e.control.data