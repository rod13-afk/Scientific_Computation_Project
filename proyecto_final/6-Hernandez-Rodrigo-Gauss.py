"""
NAME
       6-Hernandez-Rodrigo-Gauss.py
VERSION
        [1.0]
AUTHOR
        Rodrigo Daniel Hernandez Barrera <<rodrigoh@lcg.unam.mx>>
DESCRIPTION
        Programa que encuentra las raices para una ecuacion dada por el usuario, utilizando el metodo de Aproximaciones
        sucesivas, se grafica la funcion asi como el punto (solucion)

USAGE
        Desde terminal y en el directorio donde esta guardado el archivo, utilizar el comando:

            python3 6-Hernandez-Rodrigo-Gauss.py

        Requiere previa instalacion de la libreria SymPy desde terminal, de ser necesario consulte el citio web:
        https://programminghistorian.org/es/lecciones/instalar-modulos-python-pip
DICCIONARIO DE VARIABLES
        criterio:
            criterio: bandera que guarda el criterio y lo cambia a verdadero en caso de que la dominancia diagonal
                        se cumpla
            diagonal: guarda la suma de los coeficientes de las diagonales
            no_diagonal: guarda la suma de los coeficientes que no son la diagonal.

        ecuaciones: guarda la cantidad de ecuaciones que usara el programa
        variables: guarda la cantidad de variables que usara el programa
        redondeo: guarda la cantidad de decimales para redondear el resultado
        matrix: matriz donde se guardan los coeficientes de las ecuaciones
        x: variable que guarda el resultado de aplicar la formula en cada iteracion
        constantes: vector solucion que guarda las soluciones de las ecuaeiones dadas por el usuario
        resultados_temporales: guarda todos los resultados obtenidos en cada iteracion


"""


# Funcion que hace los calculos para determinar si la suma de la diagonal de la matriz es mayor a la suma de los otros
# elementos
def criterio(matriz, ecuaciones, variables):
    criterio = False
    diagonal = 0
    no_diagonal = 0

    for i in range(0, ecuaciones):
        for j in range(0, variables):
            if i == j:
                diagonal += matriz[i][j]
            else:
                no_diagonal += matriz[i][j]
    if abs(no_diagonal) < abs(diagonal):
        criterio = True

    return criterio


import numpy

# Obtencion de los datos necesarios para crear la matriz de coeficientes
print('Bienvenid@ al programa de resolucion de sistemas de ecuaciones lineales con Gauss-Seidel')
ecuaciones = int(input('Ingresa la cantidad de ecuaciones: '))
variables = int(input('Ingresa la cantidad de variables: '))
redondeo = int(input('Ingresa los decimales de precision con los que quieres tus resultados: '))

# Se declara la matriz de coeficientes y el vector que almacenara los resultados
matrix = numpy.zeros((ecuaciones, variables))
x = numpy.zeros((ecuaciones))

# Se declara el vector que va a almacenar las constantes a las que estan igualadas las ecuaciones, tambien se declara
# un vector que servira para calcular el error relativo y la lista que va a almacenar ese error.
constantes = numpy.zeros((variables))
comp = numpy.zeros((variables))
error = []

# Dos for anidados que se utilizan para almacenar los coeficientes de las ecueciones en la matriz y los valores
# constantes a los que estan igualadas
print('Introduce la matriz de coeficientes y el vector solución')
for r in range(0, ecuaciones):
    for c in range(0, variables):
        matrix[(r), (c)] = float(input("Valor en a[" + str(r + 1) + str(c + 1) + "]: "))
    constantes[(r)] = float(input('Solucion de la ecuacion ' + str(r + 1) + ': '))

tolerancia = 0.000000001
iteraciones = 20

# Se llama a la funcion de criterio para checar que las ecuaciones esten en el orden correcto
criterio = criterio(matrix, ecuaciones, variables)
if criterio:
    print("\nEl criterio de dominancia diagonal se cumple, puede procederse con la busqueda de soluciones")
else:
    print("El criterio de dominancia diagonal no se cumple, ordene sus ecuaciones para que la suma de la diagonal sea "
          "mayor a la del resto de coeficientes")
    exit()
# Se declara una lista que almacena todos los valores que surgen con cada iteracion, la iteracion se hace con un par de
# ciclos for, se aplica la formula y el resultado se guarda en la lista
resultados_temporales = []
k = 0
while k < iteraciones and criterio:
    suma = 0
    k = k + 1
    for r in range(0, ecuaciones):
        suma = 0
        for c in range(0, variables):
            if c != r:
                suma = suma + matrix[r, c] * x[c]
        x[r] = (constantes[r] - suma) / matrix[r, r]
        resultados_temporales.append(x[r])

    del error[:]
    # Se utilizan dos ciclos for similares a los anteriores para calcular el error relativo
    for r in range(0, ecuaciones):
        suma = 0
        for c in range(0, variables):
            suma = suma + matrix[r, c] * x[c]
        comp[r] = suma
        dif = abs((comp[r] - constantes[r]) / comp[r])
        error.append(dif)
    if all(i <= tolerancia for i in error):
        break

# Se imprimen los resultados con la precision de decimales indicada por el usuario y se imprime el error
print("\nLos resultados a tus variables son los siguientes:\n")
longitud = len(resultados_temporales)
del resultados_temporales[0:longitud - variables]
contador = 1
for resultado in resultados_temporales:
    print("x_" + str(contador) + " = " + str(round(resultado, redondeo)))
    contador += 1
# print(resultados_temporales)
print("Error relativo:", error[0])
