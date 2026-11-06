from datetime import datetime
from sys import stdin


class Graph:
    def __init__(self, size):
        self.adj_matrix = [[0.0] * size for _ in range(size)]
        self.size = size
        self.vertex_data = [''] * size

    def add_edge(self, u, v, weight):
        if 0 <= u < self.size and 0 <= v < self.size:
            self.adj_matrix[u][v] = weight
            self.adj_matrix[v][u] = weight  

    def add_vertex_data(self, vertex, data):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data

    def dijkstra(self, start_vertex_data, end_vertex_data):
        start_vertex = -1
        end_vertex = -1
        idx = 0
        while idx < self.size:
            if self.vertex_data[idx] == start_vertex_data:
                start_vertex = idx
            if self.vertex_data[idx] == end_vertex_data:
                end_vertex = idx
            idx += 1

        if start_vertex == -1 or end_vertex == -1:
            return None, None, "Zona no válida"

        distances = [float('inf')] * self.size
        distances[start_vertex] = 0.0

        visited = [False] * self.size
        parents = [-1] * self.size

        paso = 0
        while paso < self.size:
            min_distance = float('inf')
            u = None
            
            i = 0
            while i < self.size:
                if not visited[i] and distances[i] < min_distance:
                    min_distance = distances[i]
                    u = i
                i += 1

            if u is None or min_distance == float('inf'):
                paso = self.size
            else:
                visited[u] = True

                v = 0
                while v < self.size:
                    if self.adj_matrix[u][v] != 0 and not visited[v]:
                        alt = distances[u] + self.adj_matrix[u][v]
                        if alt < distances[v]:
                            distances[v] = alt
                            parents[v] = u
                    v += 1

            paso += 1

        if distances[end_vertex] == float('inf'):
            return None, None, "No existe ruta posible"

        path_idx = []
        current = end_vertex
        while current != -1:
            path_idx.append(current)
            current = parents[current]

        path_idx_rev = []
        l = len(path_idx) - 1
        while l >= 0:
            path_idx_rev.append(path_idx[l])
            l -= 1

        path = []
        k = 0
        while k < len(path_idx_rev):
            path.append(self.vertex_data[path_idx_rev[k]])
            k += 1

        return path, distances[end_vertex], None


def construir_waze():
    vertices = [
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "L", 
        "ADMISIONES", "BIBLIOTECA", "CANCHAS", "COLISEO", 
        "ENTRADA", "HARBYS", "HUERTA", "MICROHONDAS", "PAPELERIA", 
        "REGIO", "RESTAURANTE", "TIENDA_C"
    ]
    
    g = Graph(len(vertices))
    
    i = 0
    while i < len(vertices):
        g.add_vertex_data(i, vertices[i])
        i += 1

    conexiones = [
        ("ENTRADA", "A", 0.90),
        ("A", "B", 0.40),
        ("B", "C", 0.25),
        ("C", "TIENDA_C", 0.67),
        ("B", "TIENDA_C", 0.5),
        ("C", "E", 0.83),
        ("A", "BIBLIOTECA", 0.15),
        ("BIBLIOTECA", "PAPELERIA", 0.35),
        ("PAPELERIA", "E", 0.50),
        ("PAPELERIA", "D", 0.40),
        ("E", "REGIO", 0.5),
        ("D", "REGIO", 0.33),
        ("REGIO", "RESTAURANTE", 0.67),
        ("A", "G", 0.95),
        ("G", "ENTRADA", 1.17),
        ("G", "F", 0.25),
        ("F", "D", 1.80),
        ("D", "MICROHONDAS", 0.67),
        ("REGIO", "MICROHONDAS", 0.33),
        ("I", "E", 0.80),
        ("I", "RESTAURANTE", 1.5),
        ("RESTAURANTE", "H", 1.60),
        ("RESTAURANTE", "HARBYS", 2.20),
        ("I", "H", 0.45),
        ("H", "COLISEO", 1.5),
        ("COLISEO", "HARBYS", 0.42),
        ("L", "F", 0.33),
        ("L", "MICROHONDAS", 0.25),
        ("L", "RESTAURANTE", 0.17),
        ("L", "HARBYS", 0.50),
        ("HARBYS", "CANCHAS", 0.25),
        ("HARBYS", "HUERTA", 0.33),
        ("A", "I", 4.0),
        ("B", "E", 0.50),
        ("ADMISIONES", "A", 0.17),
        ("ADMISIONES", "PAPELERIA", 0.33),
        ("ADMISIONES", "B", 1.0),
        ("ADMISIONES", "E", 0.60),
        ("PAPELERIA", "F", 0.50),
        ("PAPELERIA", "G", 0.83),
    ]

    extra_general = 10.0 / 60.0
    extra_papeleria = 20.0 / 60.0

    c_idx = 0
    while c_idx < len(conexiones):
        u_str = conexiones[c_idx][0]
        v_str = conexiones[c_idx][1]
        peso = conexiones[c_idx][2]
        
        u = -1
        v = -1
        s_i = 0
        while s_i < g.size:
            if g.vertex_data[s_i] == u_str:
                u = s_i
            if g.vertex_data[s_i] == v_str:
                v = s_i
            s_i += 1
        
        p_ajustado = float(peso) + extra_general
        if u_str == "PAPELERIA" or v_str == "PAPELERIA":
            p_ajustado += extra_papeleria
            
        g.add_edge(u, v, p_ajustado)
        c_idx += 1

    return g, vertices


def main():
    fec = datetime.now().strftime("%Y-%m-%d")
    hor = datetime.now().strftime("%H:%M")

    g, vertices = construir_waze()

    print("+------------------------------------------------+")
    print(f"|{'WAZE UNIVERSITARIO':^48}|")
    print("+------------------------------------------------+")
    print(f"| FECHA: {fec:<39} |")
    print(f"| HORA : {hor:<39} |")
    print("+------------------------------------------------+")
    print()

    zonas_str = ""
    z_idx = 0
    while z_idx < len(vertices):
        if z_idx == 0:
            zonas_str = vertices[z_idx]
        else:
            zonas_str = zonas_str + ", " + vertices[z_idx]
        z_idx += 1

    print(f"Zonas habilitadas: {zonas_str}")
    print("-" * 50)

    origen = ""
    while origen not in vertices:
        print("¿Dónde te encuentras?:")
        linea = stdin.readline()
        if linea:
            origen = linea.strip().upper()
            if origen not in vertices:
                print("  [!] Zona no válida. Intenta de nuevo.")
                print()

    destino = ""
    while destino not in vertices:
        print("¿A dónde vas?:")
        linea = stdin.readline()
        if linea:
            destino = linea.strip().upper()
            if destino not in vertices:
                print("  [!] Zona no válida. Intenta de nuevo.")
                print()

    camino, tiempo_total, error = g.dijkstra(origen, destino)

    print()
    print("+------------------------------------------------+")
    if error:
        print(f"| ESTADO: {error:<38} |")
    else:
        ruta_str = ""
        r_idx = 0
        while r_idx < len(camino):
            if r_idx == 0:
                ruta_str = camino[r_idx]
            else:
                ruta_str = ruta_str + " -> " + camino[r_idx]
            r_idx += 1
        
        seg_totales = int(tiempo_total * 60)
        mins = seg_totales // 60
        segs = seg_totales % 60
        
        entero_t = int(tiempo_total)
        decimal_t = int((tiempo_total - entero_t) * 100)
        dec_str = f"0{decimal_t}" if decimal_t < 10 else str(decimal_t)
            
        tiempo_formateado = f"{mins} min {segs} seg ({entero_t}.{dec_str} min)"

        print(f"| Ruta óptima : {ruta_str:<33} |")
        print(f"| Tiempo est. : {tiempo_formateado:<33} |")
        print(f"| Salida prog.: {hor:<33} |")
    print("+------------------------------------------------+")


main()
