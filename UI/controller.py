import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        generi = self._model.getAllGenre()

        for g in generi:
            self._view._ddGenre.options.append(ft.dropdown.Option(g))
        self._view.update_page()


    def fillDDArtist(self):
        self._view._ddArtist.options.clear()
        artisti = self._model.getAllArtistGenre()

        for artist in artisti:
            self._view._ddArtist.options.append(ft.dropdown.Option(
                key = artist.ArtistId,
                text = artist.Name,
            ))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        self._model.buildGraph(self._view._ddGenre.value)
        self.fillDDArtist()


    def handleCammino(self,e):
        pass