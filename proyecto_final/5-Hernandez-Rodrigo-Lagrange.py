
"""
NAME
       5-Hernandez-Rodrigo-Lagrange.py
VERSION
        [1.0]
AUTHOR
        Rodrigo Daniel Hernandez Barrera <<rodrigoh@lcg.unam.mx>>
DESCRIPTION
        Programa que encuentra el polinomio que mejor se ajusta los puntos dados por el usuario, esto por el metodo de
        interpolacion de Lagrange, tambien se puede interpolar un valor especifico de x para encontrar su coordenada en y
USAGE
        Desde terminal y en el directorio donde esta guardado el archivo, utilizar el comando:

            python3 5-Hernandez-Rodrigo-Lagrange.py

        Requiere previa instalacion de la libreria SymPy desde terminal, de ser necesario consulte el citio web:
        https://programminghistorian.org/es/lecciones/instalar-modulos-python-pip
DICCIONARIO DE VARIABLES
    graficar_polinomio:
        -polinomio: expresión sympy que se va a graficar
        -minimo_x: limite inferior del dominio a graficar
        -maximo_x: limite superior del dominio a graficar
        -coord_x: array en el que se guardan intervalos de x para graficar
        -coord_y: array en el que se guardan intervalos de y para graficar
    guardar_datos:
        datos: lista que guardara los puntos por los que pasa la grafica del polinomio
        x: guarda la coordenada 'x' de cada punto
        y: guarda la coordenada 'y' de cada punto
    encontrar_polinomio:
        numerador: guarda el numerador de la fraccion en la formula
        denominador: guarda el denominador de la fraccion en la formula
        elemento_de_suma: guarda los elementos fraccionarios que han de sumarse y que se generan en cada iteracion.
        polinomio: guarda el polinomio final producto de la suma de los elementos de suma
    interpolar_numero:
        valor: guarda el numero que quiere interpolarse
        numerador: guarda el numerador de la fraccion en la formula
        denominador: guarda el denominador de la fraccion en la formula
        elemento_de_suma: guarda los elementos numericos que han de sumarse y que se generan en cada iteracion.
        resultado: acumula todos los valores provenientes de cada iteracion, es el resultado final.
    funcion principal
        cantidad_de_datos: guarda la cantidad de datos que se van a utilizar en el programa
        datos_en_xy: guarda los datos ingresados, provenientes de la funcion guardar_datos()
        respuesta: indica lo que desea hacer el usuario, encontrar el polinomio o interpolar un numero
        polinomio: guarda el polinomio resultante
        decision: indica si el usuario quiere hacer algo mas en el programa o salir del mismo
"""

import numpy
import sympy
from sympy import Symbol, sympify

x = Symbol('x')


# Funcion que recibe la cantidad de datos que se van a ingresar, recibe los datos por parte del usuario y los guarda en
# una lista, esta lista es el objeto que regresa la funcion
def guardar_datos(cantidad_de_datos):
    datos = []
    for i in range(cantidad_de_datos):
        print("Dato", i + 1, "del conjunto de las x")
        x = float(input())
        print("Dato", i + 1, "del conjunto de las y")
        y = float(input())
        datos.append((x, y))
    return datos


# Funcion que genera el polinomio, recibe los datos por parte de la funcion 'guardar_datos' y aplica la formula para
# finalmente imprimir el polinomio en 'pretty form'
def encontrar_polinomio(datos_en_xy):
    from sympy import simplify

    polinomio = 0
    # se recorre la lista de puntos
    for i in datos_en_xy:
        elemento_de_suma = 1
        denominador = 1
        numerador = 1
        for j in datos_en_xy:
            if j != i:
                # se suma y multiplicade acuerdo a la formula
                numerador *= (x - j[0])
                denominador *= (i[0] - j[0])
                elemento_de_suma *= (sympify(x - j[0]) / (i[0] - j[0]))
        elemento_de_suma = (numerador / denominador) * i[1]
        polinomio += elemento_de_suma
    polinomio = simplify(polinomio)
    sympy.pprint(polinomio)
    return polinomio


# Funcion que aplica la formula del metodo de Lagrande pero sustituye la variable 'x' por la constante ingresada
def interpolar_numero(datos_en_xy):

    valor = int(input("Ingrese el numero que quiere interpolar en el polinomio: "))
    resultado = 0

    for i in datos_en_xy:
        denominador = 1
        numerador = 1
        for j in datos_en_xy:
            if j != i:
                numerador *= (valor - j[0])
                denominador *= (i[0] - j[0])
        elemento_de_suma = (numerador / denominador) * i[1]
        resultado += elemento_de_suma
    print("f(", valor, ") = ", resultado)


# Funcion que grafica el polinomio y los puntos dados por el usuario
def graficar(polinomio, datos_en_xy):
    from sympy import lambdify
    from matplotlib import pyplot

    datos_xy_descomprimidos = list(zip(*datos_en_xy))
    [minimo_x, maximo_x] = [min(datos_xy_descomprimidos[0]), max(datos_xy_descomprimidos[0])]
    eje_x = numpy.linspace(minimo_x, maximo_x, 100)
    eje_y = lambdify(x, polinomio, "numpy")(eje_x)
    pyplot.plot(eje_x, eje_y)
    pyplot.xlabel('Eje x')
    pyplot.ylabel('Eje y')
    pyplot.grid(True)
    pyplot.axhline(linewidth=1, color='black')
    pyplot.axvline(linewidth=1, color='black')
    for datos in datos_xy_descomprimidos:
        x_axis = datos_xy_descomprimidos[0]
        y_axis = datos_xy_descomprimidos[1]
        pyplot.scatter(x=[x_axis], y=[y_axis])
    pyplot.show()


# Main function que le pide los datos y las decisiones al usuario, pasandolos como parametro en la llamada de las funciones

print("Bienvenid@ al programa de Aproximacion Funcional por el metodo de Lagrange")
cantidad_de_datos = int(input("Ingresa la cantidad de datos (puntos) con los que vas a trabajar: "))
datos_en_xy = guardar_datos(cantidad_de_datos)

respuesta = input("¿Quieres un polinomio o interpolar un numero? responde 'polinomio' o 'interpolar valor': ")
if respuesta == 'polinomio':
    polinomio = encontrar_polinomio(datos_en_xy)
    graficar(polinomio, datos_en_xy)
    decision = input("Si deseas interpolar un numero en el polinomio escribe 'si', si quieres terminar escribe 'no': ")
    if decision == 'si':
        valor = input("Ingrese el numero que quiere interpolar en el polinomio: ")
        variable = sympify(polinomio)
        interpolacion = variable.subs('x', valor)
        print("f(", valor, ") = ", interpolacion)
    else:
        exit()
elif respuesta == 'interpolar valor':
    interpolar_numero(datos_en_xy)
    decision = input("Si deseas calcular el polinomio de tus datos escribe 'si', si quieres terminar escribe 'no': ")
    if decision == 'si':
        encontrar_polinomio(datos_en_xy)
    else:
        exit()
else:
    ValueError("La respuesta es incorrecta, por favor elija 'interpolar valor' o 'polinomio'")
