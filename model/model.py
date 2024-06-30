import copy

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self.getMetodi=DAO.getMetodi()[0]
        self.dizioMetodi=DAO.getMetodi()[1]
        self.grafo = nx.DiGraph()
        self._idMap = {}

    def creaGrafo(self, metodo,anno,s):
        metodoCode=self.dizioMetodi[metodo]
        self.nodi = DAO.getNodi(metodoCode,anno)
        self.grafo.add_nodes_from(self.nodi)
        self.addEdges(s)
        for v in self.nodi:
            self._idMap[v.Product_number] = v
        return self.grafo

    def getNumNodes(self):
        return len(self.grafo.nodes)

    def getNumEdges(self):
        return len(self.grafo.edges)

    def addEdges(self, s):
        self.grafo.clear_edges()
        for nodo1 in self.grafo:
            for nodo2 in self.grafo:
                if nodo1 != nodo2 and self.grafo.has_edge(nodo1, nodo2) == False:
                   prezzoMinimo=float(nodo1.prezzo) + float(nodo1.prezzo)*s
                   if nodo2.prezzo>prezzoMinimo:
                        self.grafo.add_edge(nodo1, nodo2)

    def getAnalisi(self):
        dizio={}
        lista=[]
        for nodo in self.grafo:
            dizio[nodo.Product_number]=self.grafo.in_degree(nodo)
        dizioOrdinato=list(sorted(dizio.items(), key=lambda item:item[1], reverse=True))
        contatore=0
        for (nodoId,grado) in dizioOrdinato:
            if contatore <5:
                nodo=self._idMap[nodoId]
                lista.append((nodoId,grado, nodo.prezzo))
                contatore+=1
        return lista

    def getBestPath(self):
        self._soluzione = []
        self._costoMigliore = 0
        for nodo in self.grafo.nodes:
            if self.grafo.in_degree(nodo)==0:
                parziale = [nodo]
                self._ricorsione(parziale)
        return self._costoMigliore, self._soluzione

    def _ricorsione(self, parziale):
        if self.grafo.out_degree(parziale[-1])==0:
            if len(parziale) > self._costoMigliore:
                self._soluzione = copy.deepcopy(parziale)
                self._costoMigliore = len(parziale)

        for n in self.grafo.successors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale)
                parziale.pop()

