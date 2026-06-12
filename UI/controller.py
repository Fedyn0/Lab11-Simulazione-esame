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

        influenza = 0
        artista = None

        for key, value in self._model.getInfluenza().items():
            if value > influenza:
                influenza = value
                artista = key

        self._model.getTop5Archi()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo contiene {len(self._model._graph.nodes())} nodi e {len(self._model._graph.edges())} archi."))
        self._view.txt_result.controls.append(
            ft.Text(f"Artista più influente: {artista.Name}, con influenza: {influenza}"))

        for i in self._model.getTop5Archi():
            self._view.txt_result.controls.append(
                ft.Text(f"{i[0].Name} -> {i[1].Name}: {i[2]["weight"]}")
            )

        self._view.update_page()

    def handleCammino(self,e):
        bestPath = self._model.getBestPath(self._view._ddArtist.value)

        artista = self._model._artisti[int(self._view._ddArtist.value)]

        self._view.txt_result.controls.append(
            ft.Text(f"Per l'artista {artista} è stato trovato il seguente percorso:")
        )

        for i in bestPath:
            self._view.txt_result.controls.append(
                ft.Text(i)
            )

        self._view.update_page()