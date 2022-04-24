"""
NAME
       1-Hernandez-Rodrigo-AproxSu.py
VERSION
        [1.0]
AUTHOR
        Rodrigo Daniel Hernandez Barrera <<rodrigoh@lcg.unam.mx>>
DESCRIPTION
        Programa que encuentra las raices para una ecuacion dada por el usuario, utilizando el metodo de Aproximaciones
        sucesivas, se grafica la funcion asi como el punto (solucion)

USAGE
        Desde terminal y en el directorio donde esta guardado el archivo, utilizar el comando:

            python3 1-Hernandez-Rodrigo-AproxSu.py

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
        criterio:
            -criterio: bandera que denota si el criterio de convergencia se cumplio o no
            -respuesta: guarda la decision del usuario de continuar a pesar de que el depeje no cumpla el criterio
        solucion:
            -x_0: valor intermedio entre los dos limites donde hay solucion
            -x_n: valor de x para la n iteración
            -x_nmas1: valor de x para n + 1 iteracion
            -diferencia: guarda la diferencia entre el valor de xmas1 y x
            -diferencia_xmas1: guarda la diferencia entre los valores de la siguiente iteeracion
        Funcion principal:
            -soluciones:guarda las soluciones que se encuentran a lo largo del proceso
            -precision: guarda los decimales de precision con los que se desea trabajar
            -funcion: variable que contiene la ecuacion para la cual se desea buscar sus raices
            -despeje: contiene el despeje de la funcion
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
def _funcion(despeje=False):
    from sympy.parsing.sympy_parser import parse_expr

    if despeje:
        funcion = (sympify(input("g(x) = ")))
    else:
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


# Funcion que evalua el criterio de convergencia g(x) < 1 usando el despeje y el punto medio entre los intervalos que
# contienen solucion, si el criterio se cumple regresa True, si no se cumple pregunta al usuario si aun asi quiere
# calcular las soluciones, ya que el criterio es suficiente mas no necesario
def criterio(despeje, punto_medio):
    import sys
    import mpmath
    sys.modules['sympy.mpmath'] = mpmath

    criterio = False
    # Se evalua el criterio de convergencia y se deja que el usuario decida si continua con el msimo despeje
    print("g'(", punto_medio, ") = ", despeje.subs(x, punto_medio))
    while despeje.subs(x, punto_medio) > 1.0:
        print("Tu despeje no cumple el criterio de convergencia para el punto x_0: ", punto_medio)
        respuesta = input("Quieres arriesgarte? responde si/no\n")
        while respuesta != "si" and respuesta != "no":
            respuesta = input("Quieres arriesgarte? responde si/no?")
        if respuesta == "si":
            return criterio
        else:
            exit()
    print("Tu despeje cumple el criterio de covergencia para el punto x_0: ", punto_medio)
    criterio = True
    return criterio


# Funcion que genera las soluciones, utiliza el criterio de convergencia, si el criterio se cumple se itera hasta que
# se alcanzan los decimales de precision,
def solucion(intervalo, precision):

    x_0 = (intervalo[1] + intervalo[0]) / 2
    x_n = round(x_0, precision)
    x_nmas1 = round(despeje.subs(x, x_n), precision)
    diferencia = x_nmas1 - x_n
    if criterio(despeje, x_0):
        while abs(diferencia) > (10 ** (-precision)):
            x_n = x_nmas1
            x_nmas1 = round(despeje.subs(x, x_nmas1), precision)
            diferencia = x_nmas1 - x_n
        soluciones.append(x_nmas1)
    else:
        # Si no se cumple el criterio se busca que las diferencias aumenten
        diferencia = x_nmas1 - x_n
        x_n = x_nmas1
        x_nmas1 = round(despeje.subs(x, x_nmas1), precision)
        diferencia_nmas1 = x_nmas1 - x_n

        # Para saber si converge o no, se toma en cuenta que las diferencias entre iteraciones disminuyan cada vez mas
        while abs(diferencia) > abs(diferencia_nmas1):
            x_n = x_nmas1
            x_nmas1 = round(despeje.subs(x, x_nmas1), precision)
            diferencia = diferencia_nmas1
            diferencia_nmas1 = x_nmas1 - x_n
            if round(x_n, precision) == round(x_nmas1, precision):
                soluciones.append(x_nmas1)
                break
        # si los valores empiezan a alejarse de la solucion (si la diferencia entre consecutivos aumenta) se detiene
        else:
            print("No converge")


# Main function que declara la lista que contendra las soluciones y le pide los datos al usuario, pasandolos
# como parametro en la llamada de todas las funciones
x = Symbol('x')
soluciones = []

print("Bienvenid@ al buscador de raíces de Aproximaciones Sucesivas")

precision = input("Ingrese los decimales de precisión para las soluciones: ")
precision = int(precision) + 1

print("Ingresa la función")
funcion = _funcion(despeje=False)

print("Ingresa el despeje ")
despeje = _funcion(despeje=True)

print("Ingresa el rango en x para el cual quieres encontrar todas las soluciones")
limites_de_busqueda = limites()

intervalos_iterables = (n for n in numpy.arange(limites_de_busqueda[0], limites_de_busqueda[1] + 0.1, 1))
tabulador(intervalos_iterables, funcion)

intervalos_iterables2 = (n for n in numpy.arange(limites_de_busqueda[0], limites_de_busqueda[1] + 0.1, 1))

cambios_de_signo = cambio_de_signo(intervalos_iterables2, funcion)
print("Los intervalos en las que se encontro cambio de signo son: ", cambios_de_signo,
      "el despeje se aplicara a todos y se imprimiran las raices encontradas\n")

for intervalo in cambios_de_signo:
    solucion(intervalo, precision)

if soluciones:
    print("Las raices de tu ecuacion son: ")
    for solucion in soluciones:
        print(round(solucion, precision))
else:
    print("No se encontraron raices")
graficar(funcion, limites_de_busqueda, soluciones)
