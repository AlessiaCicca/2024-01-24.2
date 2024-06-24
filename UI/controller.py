import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_grafo(self, e):
        metodo = self._view.dd_metodo.value
        if metodo is None:
            self._view.create_alert("Selezionare un metodo")
            return
        anno = self._view.dd_anno.value
        if anno is None:
            self._view.create_alert("Selezionare un Anno")
            return
        s= self._view.txt_s.value
        if s == "":
            self._view.create_alert("Inserire un valore numerico ")
            return
        if float(s) <0:
            self._view.create_alert("Inserire un valore numerico maggiore di 0")
            return
        grafo = self._model.creaGrafo(metodo, int(anno), float(s))
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene "
                                                      f"{self._model.getNumNodes()} nodi."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene "
                                                      f"{self._model.getNumEdges()} archi."))

        self._view.update_page()

    def handle_redditizi(self,e):
        lista=self._model.getAnalisi()
        for (id,grado,ricavo) in lista:
            self._view.txt_result.controls.append(ft.Text(f"Prodotto {id} Archi Entranti={grado} Ricavo={ricavo}"))
        self._view.update_page()

    def fillDD(self):
        ann="201"
        for i in range(5,9):
            anno=ann+str(i)
            self._view.dd_anno.options.append(ft.dropdown.Option(
                               text=anno))
        metodi=self._model.getMetodi
        for metodo in metodi:
            self._view.dd_metodo.options.append(ft.dropdown.Option(
                text=metodo))
