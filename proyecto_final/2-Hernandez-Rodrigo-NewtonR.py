"""
NAME
       2-Hernandez-Rodrigo-NewtonR.py
VERSION
        [1.0]
AUTHOR
        Rodrigo Daniel Hernandez Barrera <<rodrigoh@lcg.unam.mx>>
DESCRIPTION
        Programa que encuentra las raices para una ecuacion dada por el usuario, utilizando el metodo de Aproximaciones
        sucesivas, se grafica la funcion asi como el punto (solucion)

USAGE
        Desde terminal y en el directorio donde esta guardado el archivo, utilizar el comando:

            2-Hernandez-Rodrigo-NewtonR.py

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
        solucion:
            -x_n: valor de x para la n iteración
            -x_nmas1: valor de x para n + 1 iteracion
            -diferencia: guarda la diferencia entre el valor de xmas1 y x
            -diferencia_xmas1: guarda la diferencia entre los valores de la siguiente iteeracion
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


# Funcion que aplica la formula del metodo para cada uno de los valores de x calculados y los intercambia mientras itera
# mientras la diferencia entre el valor x_n y x_
def solucion(intervalo, precision):
    formula = x - (funcion / funcion.diff(x))
    x_n = round(((intervalo[1] + intervalo[0]) / 2), precision)
    x_nmas1 = round(formula.subs(x, x_n), precision)
    diferencia = x_nmas1 - x_n
    while abs(diferencia) > (10 ** (-(precision + 1))):
        x_n = x_nmas1
        x_nmas1 = round(formula.subs(x, x_nmas1), precision)
        diferencia = x_nmas1 - x_n
        if round(x_n, precision) == round(x_nmas1, precision):
            soluciones.append(x_nmas1)
            break


import sympy

# Main function que declara la lista que contendra las soluciones y le pide los datos al usuario, pasandolos
# como parametro en la llamada de todas las funciones
x = Symbol('x')
soluciones = []

print("Bienvenid@ al buscador de raices con el metodo Newton-Raphson")

print("Ingresa la función")
funcion = funcion()

print("La derivada de su funcion es: ")
sympy.pprint(funcion.diff(x))

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
    print("No se encontraron cambios de signo y por lo tanto no hay raices entre estos intervalos: ", limites_de_busqueda)

for intervalo in cambios_de_signo:
    solucion(intervalo, precision)

if soluciones:
    print("Las raices de tu ecuacion son: ")
    for solucion in soluciones:
        print(round(solucion, precision))
else:
    print("No se encontraron raices")
graficar(funcion, limites_de_busqueda, soluciones)
