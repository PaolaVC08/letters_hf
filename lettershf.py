import os

def leer_matriztxt(ruta_archivo):
    matriz = []
    with open(ruta_archivo, 'r') as f:
        for linea in f:
            linea_limpia = linea.strip()
            if linea_limpia:
                fila = [int(n) for n in linea_limpia.split()]
                matriz.append(fila)
    return matriz

def procesar_patron(matriz):
    vector_plano = [elemento for fila in matriz for elemento in fila]
    vector_bipolar = [-1 if valor == 0 else 1 for valor in vector_plano]
    return vector_bipolar

carpeta_dataset = 'dataset'

# read h.txt, e.txt, o.txt, etc.
archivos_entrenamiento = ['h.txt', 'o.txt', 'e.txt', 'k.txt', 'j.txt', 'i.txt']
patrones_entrenamiento = []

print("cargando patrones")
for nombre_archivo in archivos_entrenamiento:
    ruta_completa = os.path.join(carpeta_dataset, nombre_archivo)
    matriz = leer_matriztxt(ruta_completa)
    vector_bipolar = procesar_patron(matriz)
    patrones_entrenamiento.append(vector_bipolar)
    print(f"Patrón {nombre_archivo} cargado.")

# pesos W
tamano_patron = len(patrones_entrenamiento[0]) # 8*5 = 40
matriz_W = [[0] * tamano_patron for _ in range(tamano_patron)]

# Obtener W con la suma de los pesos por patron
for patron in patrones_entrenamiento:
    for i in range(tamano_patron):
        for j in range(tamano_patron):
            if i == j:
                matriz_W[i][j] = 0
            else:
                matriz_W[i][j] += patron[i] * patron[j]

print("\nMatriz de Pesos W ")
for fila in matriz_W:
    print(fila)
print ("\n")

# FASE DE RECONOCIMIENTO

# target
archivo_target = 'x1.txt' 
ruta_target = os.path.join(carpeta_dataset, archivo_target)

matriz_target = leer_matriztxt(ruta_target)
patron_entrada = procesar_patron(matriz_target)

print(f"Patrón de Entrada U(0): {patron_entrada}")

# Inicio de bucle
max_iteraciones = 50
U_actual = patron_entrada[:] 
iteracion = 0

while True:
    iteracion += 1
    print(f"\nIteración {iteracion} ")
    U_anterior = U_actual[:]

    # Multiplicar U_actual * W
    resultado_multiplicacion = [0] * tamano_patron
    for j in range(tamano_patron):
        suma_total = sum(U_actual[i] * matriz_W[i][j] for i in range(tamano_patron))
        resultado_multiplicacion[j] = suma_total
    
    print(f"Resultado de U*W: {resultado_multiplicacion}")

    # Función de activación
    U_siguiente = []
    for i in range(tamano_patron):
        valor = resultado_multiplicacion[i]
        if valor > 0:
            U_siguiente.append(1)
        elif valor < 0:
            U_siguiente.append(-1)
        else:
            U_siguiente.append(U_anterior[i]) # Mantiene el valor si es 0
    
    U_actual = U_siguiente
    print(f"Nuevo Estado U({iteracion}): {U_actual}")

    # Condición de stop
    if U_actual == U_anterior:
        print("\nLa red ha alcanzado un estado estable")
        break
    
    if iteracion >= max_iteraciones:
        print("\nLa red no convergió en el máximo de iteraciones.")
        break

print(f"\nresultado final: El patrón de entrada converge a: {U_actual}")

# resultado a una matriz
print("\nResultado final en matriz")
for i in range(0, tamano_patron, 5):
    fila = U_actual[i:i+5]
    fila_visual = ['1' if val == 1 else '.' for val in fila]
    print(" ".join(fila_visual))
