"""
NAME
       3-Hernandez-Rodrigo-RegulaF.py
VERSION
        [1.0]
AUTHOR
        Rodrigo Daniel Hernandez Barrera <<rodrigoh@lcg.unam.mx>>
DESCRIPTION
        Programa que encuentra las raices para una ecuacion dada por el usuario, utilizando el metodo de Aproximaciones
        sucesivas, se grafica la funcion asi como el punto (solucion)

USAGE
        Desde terminal y en el directorio donde esta guardado el archivo, utilizar el comando:

            3-Hernandez-Rodrigo-RegulaF.py

        Requiere previa instalacion de la libreria SymPy desde terminal, de ser necesario consulte el citio web:
        https://programminghistorian.org/es/lecciones/instalar-modulos-python-pip
DICCIONARIO DE VARIABLES
        limites:
            -limite_inferior: limite inferior del intervalo donde se buscaran las soluciones
            -limite_superior: limite superior del intervalo donde se buscaran las soluciones
        funcion:
           -funcion: guarda la funcion ingresada por el usuario convertida con sympify a un tipo que pueda ser
            usado por la libreria SymPy
        graficar:
            -funcion: expresión sympy que se va a graficar
            -minimo_x: limite inferior del dominio a graficar
            -maximo_x: limite superior del dominio a graficar
            -coord_x: guarda los intervalos de x para graficar
            -coord_y: guarda los intervalos de y para graficar
        tabular:
            -lista_iterables: guarda las datos de x y f(x) que seran tabulados
        cambio_de_signo:
            -cambio_de_signo: guarda los intervalos en los que se encuentran soluciones
            -a: valor en el rango de x usado para encontrar raices
            -b: valor en el rango de y para explorar para encontrar raices
        formula:
            x_n: guarda el valor de x de cada iteracion y lo regresa con return
        _pivote:
            f_x: calcula la f(x) para el valor de x_0
            pivote: guarda el pivote y lo regresa con return

        solucion
            x_0: guarda el primer valor x_0 utilizando los intervalos donde existe cambio de signo
            x_nmas1: guarda la siguiente iteracion que aplica la formula al dato x_n
            diferencia: guarda la diferencia entre los valores x_nmas1 y x_n para verificar que se llegue a la precision
                        de decimales deseada
        Funcion principal:
            -soluciones:guarda las soluciones que se encuentran a lo largo del proceso
            -precision: guarda los decimales de precision con los que se desea trabajar
            -funcion: variable que contiene la ecuacion para la cual se desea buscar sus raices
            -limites de busqueda: guarda los limites inferior y superior donde se desea buscar las raices
            -intervalos_iterables: objeto de numpy que guarda los limites recorribles para poder tabular x y f(x)
            -intervalos_iterables2: objeto de numpy que guarda los limites recorribles para poder obtener los intervalos donde existe solucion
            -cambio_de_signo: guarda los intervalos donde se sabe hay un cambio de signo y por lo tanto una posible solucion
"""


import numpy

from sympy import Symbol, lambdify, sympify


# Funcion para ingresar y valida los limites donde el usuario quiere buscar sus soluciones
def limites():
    lim_inferior = float(input("limite inferior: "))
    lim_superior = float(input("limite superior: "))
    while lim_inferior >= lim_superior:
        print("El limite inferior es mayor o igual al limite superior, por favor ingresa unos limites validos")
        lim_inferior = float(input("limite inferior: "))
        lim_superior = float(input("limite superior: "))
    return [lim_inferior, lim_superior]


# Funcion para insertar la funcion y el despeje
def funcion():
    from sympy.parsing.sympy_parser import parse_expr

    funcion = (sympify(input("f(x) = ")))

    variable = parse_expr(funcion)

    funcion_final = variable.subs('pi', 3.14159265359)
    funcion_final = funcion_final.subs('e', 2.71828182846)

    return funcion_final


# Funcion que grafica la ecuacuion que ingreso el usuario
def graficar(funcion, limites_exploracion, soluciones):
    from matplotlib import pyplot

    [minimo_x, maximo_x] = limites_exploracion
    coord_x = numpy.linspace(minimo_x, maximo_x, 100)
    coord_y = lambdify(x, funcion, "numpy")(coord_x)
    pyplot.plot(coord_x, coord_y)
    pyplot.xlabel('x')
    pyplot.ylabel('y')
    pyplot.grid(True)
    pyplot.axhline(linewidth=1, color='black')
    pyplot.axvline(linewidth=1, color='black')
    for solucion in soluciones:
        pyplot.scatter(x=[solucion], y=[0])
    pyplot.show()
    return funcion


# Funcion que tabula los datos en x y f(x) usando el intervalo dado por el usuario
def tabulador(intervalos_iterables, funcion_final):
    from tabulate import tabulate
    lista_intervalos = list(intervalos_iterables)
    entrada_salida = []
    for i in lista_intervalos:
        x = i
        y = funcion_final.subs('x', i)
        entrada_salida.append((x, y))
    print(tabulate(entrada_salida, headers=['x', 'y'], tablefmt='fancy_grid'))


# Funcion que busca cambios de signo, comparando valores f(x) y los guarda para enviarlos de regreso y usarlos para
# buscar las soluciones, si alguno de los intervalos da 0, se guarda como solucion
def cambio_de_signo(intervalos_iterables2, funcion):
    cambio_de_signo = []
    a = intervalos_iterables2.__next__()
    for i in intervalos_iterables2:
        b = i
        if (funcion.subs(x, a) * funcion.subs(x, b)) <= 0:
            if (funcion.subs(x, a) * funcion.subs(x, b)) < 0:
                cambio_de_signo.append((a, b))
            elif not funcion.subs(x, a):
                soluciones.append(a)
        a = b
    return cambio_de_signo


# Funcion que aplica la formula del metodo
def formula(a, b):
    x_n = round((((a * funcion.subs(x, b)) - (b * funcion.subs(x, a))) / ((funcion.subs(x, b)) - (funcion.subs(x, a)))),
                precision)
    return x_n


# Funcion calcula el pivote inicial
def _pivote(x_0, funcion):
    f_x = funcion.subs(x, x_0)
    if ((funcion.subs(x, intervalo[0])) * f_x) < 0:
        pivote = intervalo[0]
    elif ((funcion.subs(x, intervalo[1])) * f_x) < 0:
        pivote = intervalo[1]
    return pivote


# Funcion que itera hasta que encuentra la solucion con la precision de decimales deseada, adewmas intercambia el pivote
# cuando se criterio de f(x_n) * f(x_nmas1) < 0
def solucion(intervalo, precision, funcion):
    global x_n
    x_0 = formula(intervalo[0], intervalo[1])
    pivote = _pivote(x_0, funcion)
    x_nmas1 = formula(x_0, pivote)
    diferencia = x_nmas1 - x_0
    if round(x_0, precision) == round(x_nmas1, precision):
        soluciones.append(x_nmas1)
    while abs(diferencia) > (10 ** (-precision)):
        if ((funcion.subs(x, x_0) * funcion.subs(x, x_nmas1)) < 0) and pivote == intervalo[1]:
            pivote = funcion.subs(x, x_nmas1)
        x_n = formula(x_nmas1, pivote)
        x_nmas1 = formula(x_n, pivote)
        diferencia = x_nmas1 - x_n
        if round(x_n, precision) == round(x_nmas1, precision):
            soluciones.append(x_nmas1)


# Main function que declara la lista que contendra las soluciones y le pide los datos al usuario, pasandolos
# como parametro en la llamada de todas las funciones
x = Symbol('x')
soluciones = []

print("Bienvenid@ al buscador de raices con el metodo Regula falsi")

print("Ingresa la función")
funcion = funcion()

precision = input("Ingrese los decimales de precisión para las soluciones: ")
precision = int(precision)

print("Ingresa el rango en x para el cual quieres encontrar todas las soluciones")
limites_de_busqueda = limites()

intervalos_iterables = (n for n in numpy.arange(limites_de_busqueda[0], limites_de_busqueda[1] + 0.1, 1))
tabulador(intervalos_iterables, funcion)

intervalos_iterables2 = (n for n in numpy.arange(limites_de_busqueda[0], limites_de_busqueda[1] + 0.1, 1))
cambios_de_signo = cambio_de_signo(intervalos_iterables2, funcion)

if cambios_de_signo:
    print("Los intervalos en las que se encontro cambio de signo son: ", cambios_de_signo,
          "la formula se aplicara a todos y se imprimiran las raices encontradas\n")
else:
    print("No se encontraron cambios de signo y por lo tanto no hay raices entre estos intervalos: ",
          limites_de_busqueda)

for intervalo in cambios_de_signo:
    solucion(intervalo, precision, funcion)

if soluciones:
    print("Las raices de tu ecuacion son: ")
    for solucion in soluciones:
        print(round(solucion, precision))
else:
    print("No se encontraron raices")
graficar(funcion, limites_de_busqueda, soluciones)
