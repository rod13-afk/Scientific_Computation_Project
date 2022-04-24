"""
NAME
       9-Hernandez-Rodrigo-Euler.py
VERSION
        [1.0]
AUTHOR
        Rodrigo Daniel Hernandez Barrera <<rodrigoh@lcg.unam.mx>>
DESCRIPTION
        Programa que resuelve ecuaciones diferenciales por el metodo de Euler, dada la funcion, el intervalo de busqueda,
        los valores iniciales e imprime el resultado para una cierta x con los decimales de precision proporcionados.
USAGE
        Desde terminal y en el directorio donde esta guardado el archivo, utilizar el comando:

            9-Hernandez-Rodrigo-Euler.py

        Requiere previa instalacion de la libreria SymPy desde terminal, de ser necesario consulte el citio web:
        https://programminghistorian.org/es/lecciones/instalar-modulos-python-pip
DICCIONARIO DE VARIABLES
    funcion:

        -funcion: guarda la funcion ingresada por el usuario convertida con sympify a un tipo que pueda ser
        usado por la libreria SymPy

    calculator:
        x_n: primero guarda el valor inicial de 'x' y despues los valores de 'x' generados en la funcion 'calculator'
        y_n: primero guarda el valor inicial de 'y' y despues los valores de 'y' generados en la funcion 'calculator'

    solve:
        valores_de_x_y: valores de 'x' y 'y' que van cambiando con cada iteracion del for
        resultado: guarda el resultado final de 'y'
"""

from sympy import Symbol


# Ingresa la funcion y sustituye los valores de 'pi' y 'e'
def funcion():
    from sympy.parsing.sympy_parser import parse_expr
    from sympy import sympify

    print("Ingresa tu funcion")
    funcion = sympify(input("y' = "))

    variable = parse_expr(funcion)

    funcion_final = variable.subs('pi', 3.14159265359)
    funcion_final = funcion_final.subs('e', 2.71828182846)

    return funcion_final


# Funcion que en un inicio recibe los valores iniciales de 'x' y 'y', los utiliza en la funcion arange en un for para ir
# avanzando el valor de 'x' con respecto al intervalo (h) introducido. Llama a la funcion 'calculator' enviando como
# parametros los valores de 'x' y 'y' y los recibe de vuelta pero modificados luego de pasar por las formulas, esto
# ocurre hasta que se llegue al valor de x deseado. Finalmente imprime el resultado.
def solve(funcion, ancho_de_banda, valores_iniciales, valor_final_x, decimales):
    from numpy import arange

    valores_de_x_y = valores_iniciales

    for intervalo in arange(valores_iniciales[0], valor_final_x, ancho_de_banda):
        valores_de_x_y = calculator(funcion, ancho_de_banda, valores_de_x_y)
    resultado = round(valores_de_x_y[1], decimales)
    print("El resultado de y(" + str(valor_final_x) + ") = " + str(resultado))


# Funcion que sustituye en la formula de metodo Euler los valores iniciales y despues los valores salientes de cada
# iteracion, tambien calcula el valor de la 'y', este valor es el que regresa la funcion, junto con x + h
def calculator(funcion, h, valores_de_x_y):
    x_n = float(valores_de_x_y[0])
    y_n = float(valores_de_x_y[1])

    y_n = y_n + (h * funcion.subs([(x, x_n), (y, y_n)]))

    return (x_n + h), y_n


# Main function que declara la lista que contendra a los valores iniciales y
# le pide los datos al usuario, pasandolos como parametro en la llamada de las funciones
x = Symbol('x')
y = Symbol('y')
valores_iniciales = [0.0, 0.0]

print("Bienvenid@ al metodo de Euler")
funcion = funcion()
ancho_de_banda = float(input("Ingresa la 'h' con la que quieres trabajar: "))
decimales = int(input("Ingresa los decimales de precision con los que quieres tu resultado: "))
print("Ingresa los valores de las variables con los que quieres comenzar:")
valores_iniciales[0] = float(input("x inicial: "))
valores_iniciales[1] = float(input("y inicial: "))
valor_final_x = float(input("Ingresa el valor de 'x' para el que quieres la solucion: "))
solve(funcion, ancho_de_banda, valores_iniciales, valor_final_x, decimales)