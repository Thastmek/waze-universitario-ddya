from sys import stdin


class Graph:
    def __init__(self, size: int) -> None:
        self.adj_matrix = [[0.0] * size for _ in range(size)]
        self.size = size
        self.vertex_data = [''] * size
        self.bloqueados = [False] * size

    def add_edge(self, u: int, v: int, weight: float) -> None:
        if 0 <= u < self.size and 0 <= v < self.size:
            self.adj_matrix[u][v] = weight
            self.adj_matrix[v][u] = weight

    def add_vertex_data(self, vertex: int, data: str) -> None:
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data

    def buscar_indice(self, nombre: str) -> int:
        pos = -1
        i = 0
        while i < self.size:
            if self.vertex_data[i] == nombre:
                pos = i
            i += 1
        return pos

    def dijkstra(self, inicio: int, fin: int) -> list:
        dist = [float('inf')] * self.size
        dist[inicio] = 0.0
        visitado = [False] * self.size
        padre = [-1] * self.size

        i = 0
        while i < self.size:
            menor = float('inf')
            u = None

            j = 0
            while j < self.size:
                if not visitado[j] and dist[j] < menor:
                    menor = dist[j]
                    u = j
                j += 1

            if u is not None:
                visitado[u] = True

                v = 0
                while v < self.size:
                    if self.adj_matrix[u][v] != 0 and not visitado[v] and not self.bloqueados[v]:
                        nueva = dist[u] + self.adj_matrix[u][v]
                        if nueva < dist[v]:
                            dist[v] = nueva
                            padre[v] = u
                    v += 1
            i += 1

        camino = []
        if dist[fin] != float('inf'):
            actual = fin
            while actual != -1:
                camino = [actual] + camino
                actual = padre[actual]
        return camino



def leer() -> str:
    linea = stdin.readline()
    while linea != "" and linea.strip() == "":
        linea = stdin.readline()
    return linea.strip()


def es_num(texto: str) -> bool:
    if texto == "" or texto == ".":
        return False
    puntos = 0
    i = 0
    while i < len(texto):
        if texto[i] == ".":
            puntos += 1
        elif texto[i] < "0" or texto[i] > "9":
            return False
        i += 1
    return puntos <= 1


def valida(partes: list) -> bool:
    if len(partes) != 3:
        return False
    if not es_num(partes[2]):
        return False
    return float(partes[2]) > 0 and partes[0] != partes[1]



def ajustar(a: str, b: str, peso: float) -> float:
    extra = 10.0 / 60.0
    extra_pap = 20.0 / 60.0

    total = peso + extra
    if a == "PAPELERIA" or b == "PAPELERIA":
        total += extra_pap
    return total


def armar_grafo(conexiones: list) -> Graph:
    nombres = []
    i = 0
    while i < len(conexiones):
        partes = conexiones[i].upper().split()
        if valida(partes):
            if partes[0] not in nombres:
                nombres.append(partes[0])
            if partes[1] not in nombres:
                nombres.append(partes[1])
        i += 1

    g = Graph(len(nombres))
    i = 0
    while i < len(nombres):
        g.add_vertex_data(i, nombres[i])
        i += 1

    i = 0
    while i < len(conexiones):
        partes = conexiones[i].upper().split()
        if valida(partes):
            u = g.buscar_indice(partes[0])
            v = g.buscar_indice(partes[1])
            g.add_edge(u, v, ajustar(partes[0], partes[1], float(partes[2])))
        else:
            print(f"  [!] Conexión {i + 1} inválida, se ignora: '{conexiones[i]}'")
        i += 1

    return g



def a_seg(minutos: float) -> int:
    return int(minutos * 60 + 0.5)


def texto_tiempo(seg: int) -> str:
    mins = seg // 60
    return f"{mins} min {seg - mins * 60} seg"


def texto_min(seg: int) -> str:
    cent = int(seg * 100 / 60 + 0.5)
    ent = cent // 100
    dec = cent - ent * 100
    if dec < 10:
        return f"{ent}.0{dec}"
    return f"{ent}.{dec}"


def tiempo_total(g: Graph, camino: list) -> int:
    total = 0
    i = 0
    while i < len(camino) - 1:
        total += a_seg(g.adj_matrix[camino[i]][camino[i + 1]])
        i += 1
    return total



def buscar_camino(g: Graph, origen: str, destino: str) -> list:
    o = g.buscar_indice(origen)
    d = g.buscar_indice(destino)
    camino = []

    if o == -1:
        print(f"  [!] Zona no válida: {origen}")
    elif d == -1:
        print(f"  [!] Zona no válida: {destino}")
    elif g.bloqueados[o]:
        print(f"  [!] El punto de origen {origen} está bloqueado")
    elif g.bloqueados[d]:
        print(f"  [!] El punto de destino {destino} está bloqueado")
    elif o == d:
        print(f"  Ya te encuentras en {origen}")
    else:
        camino = g.dijkstra(o, d)
        if len(camino) == 0:
            print("  [!] No existe ruta posible")
    return camino


def ver_ruta(g: Graph, origen: str, destino: str) -> None:
    camino = buscar_camino(g, origen, destino)

    if len(camino) > 0:
        ruta = g.vertex_data[camino[0]]
        i = 0
        while i < len(camino) - 1:
            u = camino[i]
            v = camino[i + 1]
            seg = a_seg(g.adj_matrix[u][v])
            print(f"  {i + 1}. {g.vertex_data[u]} -> {g.vertex_data[v]}: {texto_tiempo(seg)}")
            ruta = ruta + " -> " + g.vertex_data[v]
            i += 1

        total = tiempo_total(g, camino)
        print(f"  Ruta óptima : {ruta}")
        print(f"  Tiempo est. : {texto_tiempo(total)} ({texto_min(total)} min)")


def ver_tiempo(g: Graph, origen: str, destino: str) -> None:
    camino = buscar_camino(g, origen, destino)

    if len(camino) > 0:
        total = tiempo_total(g, camino)
        print(f"  Tiempo est. : {texto_tiempo(total)} ({texto_min(total)} min)")


def agregar(g: Graph, a: str, b: str, distancia: str) -> None:
    u = g.buscar_indice(a)
    v = g.buscar_indice(b)

    if u == -1:
        print(f"  [!] Zona no válida: {a}")
    elif v == -1:
        print(f"  [!] Zona no válida: {b}")
    elif u == v:
        print("  [!] No se puede conectar un punto consigo mismo")
    elif not es_num(distancia) or float(distancia) <= 0:
        print(f"  [!] Distancia no válida: {distancia}")
    else:
        peso = ajustar(a, b, float(distancia))
        if g.adj_matrix[u][v] != 0:
            print(f"  Camino actualizado: {a} <-> {b} ({texto_tiempo(a_seg(peso))})")
        else:
            print(f"  Camino agregado: {a} <-> {b} ({texto_tiempo(a_seg(peso))})")
        g.add_edge(u, v, peso)


def bloquear(g: Graph, nombre: str) -> None:
    i = g.buscar_indice(nombre)

    if i == -1:
        print(f"  [!] Zona no válida: {nombre}")
    elif g.bloqueados[i]:
        print(f"  [!] {nombre} ya estaba bloqueado")
    else:
        g.bloqueados[i] = True
        print(f"  Punto bloqueado: {nombre}")


def habilitar(g: Graph, nombre: str) -> None:
    i = g.buscar_indice(nombre)

    if i == -1:
        print(f"  [!] Zona no válida: {nombre}")
    elif not g.bloqueados[i]:
        print(f"  [!] {nombre} no estaba bloqueado")
    else:
        g.bloqueados[i] = False
        print(f"  Punto habilitado: {nombre}")


def ver_zonas(g: Graph) -> None:
    zonas = ""
    i = 0
    while i < g.size:
        if i == 0:
            zonas = g.vertex_data[i]
        else:
            zonas = zonas + ", " + g.vertex_data[i]
        i += 1
    print(f"  Zonas: {zonas}")


def ejecutar(g: Graph, linea: str, num: int) -> None:
    partes = linea.upper().split()
    print(f"[{num}] {linea}")

    if len(partes) == 3 and partes[0] == "RUTA":
        ver_ruta(g, partes[1], partes[2])
    elif len(partes) == 3 and partes[0] == "TIEMPO":
        ver_tiempo(g, partes[1], partes[2])
    elif len(partes) == 4 and partes[0] == "CAMINO":
        agregar(g, partes[1], partes[2], partes[3])
    elif len(partes) == 2 and partes[0] == "BLOQUEAR":
        bloquear(g, partes[1])
    elif len(partes) == 2 and partes[0] == "HABILITAR":
        habilitar(g, partes[1])
    elif len(partes) == 1 and partes[0] == "ZONAS":
        ver_zonas(g)
    else:
        print("  [!] Orden no válida (RUTA, TIEMPO, CAMINO, BLOQUEAR, HABILITAR, ZONAS)")
    print()



def encabezado(fecha: str, caso: int) -> None:
    print("+------------------------------------------------+")
    print(f"|{'WAZE UNIVERSITARIO - CASO ' + str(caso):^48}|")
    print("+------------------------------------------------+")
    print(f"| FECHA     : {fecha:<35}|")
    print("+------------------------------------------------+")


def resolver_caso(fecha: str, conexiones: list, ordenes: list, caso: int) -> None:
    encabezado(fecha, caso)
    g = armar_grafo(conexiones)

    i = 0
    while i < len(ordenes):
        ejecutar(g, ordenes[i], i + 1)
        i += 1


def leer_casos(total: int) -> None:
    caso = 0
    while caso < total:
        fecha = leer()

        n = int(leer())
        conexiones = []
        i = 0
        while i < n:
            conexiones.append(leer())
            i += 1

        m = int(leer())
        ordenes = []
        i = 0
        while i < m:
            ordenes.append(leer())
            i += 1

        resolver_caso(fecha, conexiones, ordenes, caso + 1)
        caso += 1


def main() -> None:
    x = leer()
    if x != "":
        total = int(x)
        leer_casos(total)


main()
