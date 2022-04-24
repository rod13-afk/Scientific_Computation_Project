"""
NAME
       8-Hernandez-Rodrigo-Romberg.py
VERSION
        [1.0]
AUTHOR
        Rodrigo Daniel Hernandez Barrera <<rodrigoh@lcg.unam.mx>>
DESCRIPTION
        Programa que encuentra las raices para una ecuacion dada por el usuario, utilizando el metodo de Aproximaciones
        sucesivas, se grafica la funcion asi como el punto (solucion)

USAGE
        Desde terminal y en el directorio donde esta guardado el archivo, utilizar el comando:

            python3 8-Hernandez-Rodrigo-Romberg.py

        Requiere previa instalacion de la libreria SymPy desde terminal, de ser necesario consulte el citio web:
        https://programminghistorian.org/es/lecciones/instalar-modulos-python-pip
DICCIONARIO DE VARIABLES
        limites:
            -limite_inferior: valor usado para denotar el limite inferior de un rango
            -limite_superior: valor usado para denotar el limite superior de un rango
        funcion:
            -funcion: expresión de sympy que el usuario ingresa para buscar sus raíces
        solve:
             -variables: diccionario con los valores de las iteraciones
        crear_J:
            cambio_J: suma de las evaluaciones de funcion en cuanto a la siguiente iteración de J
        crear_I_asterisco:
            nuevos_I: lsita con los valores de I para la siguiente iteracion

"""

from sympy import Symbol


# Funcion para ingresar y valida los limites donde el usuario quiere buscar sus soluciones
def limites_de_la_integral():
    print("Ingresa el intervalo en el que quieres integrar tu función")
    lim_inferior = float(input("limite inferior: "))
    lim_superior = float(input("limite superior: "))
    if lim_inferior >= lim_superior:
        raise ValueError("El limite inferior es mas grande que el limite superior, por favor ingrese limites correctos")
    return lim_inferior, lim_superior


# Funcion para insertar la funcion con la que se va a trabajar
def funcion():
    from sympy.parsing.sympy_parser import parse_expr
    from sympy import sympify

    print("Ingresa tu funcion")
    funcion = sympify(input("y' = "))

    variable = parse_expr(funcion)

    funcion_final = variable.subs('pi', 3.14159265359)
    funcion_final = funcion_final.subs('e', 2.71828182846)

    return funcion_final


# Funcion con funciones con el objetivo de iterar hasta encontrar las soluciones
def solve(funcion, limites, decimales):

    # Funcion que genera los primeros datos, en el metodo de Romberg la primera iteracion tiene un patron de resolucion
    # diferente al resto de las iteraciones
    def primeros_calculos(variables):
        variables['c'] = limites[1] - limites[0]
        variables['bandas'] = 1
        variables['J'] = 0.5 * (funcion.subs(x, limites[0]) + funcion.subs(x, limites[1]))
        variables['I'] = [[variables['J'] * variables['c']]]
        print(variables['I'][-1])
        return variables

    # Funcion que crea el resto de iteraciones y regresa el diccionario que contiene las variables que iteran como I y J
    def all_calculos(variables):

        # Funcion que genera los valores de J
        def crear_J(variables):
            cambio_J = 0
            intervalo = ((1.0 / variables['bandas']) * variables['c'])
            n = intervalo + limites[0]
            while n < limites[1]:
                cambio_J += funcion.subs(x, n)
                n = (2.0 * intervalo) + n
            variables['J'] = variables['J'] + cambio_J
            return variables

        # Funcion que genera los valores de I* y los guarda en una lista que se imprime para mostrar los resultados en
        # I y las I*
        def crear_I_asterisco(variables):
            nuevos_I = []
            nuevos_I.append((1.0 / variables['bandas']) * variables['c'] * variables['J'])

            i = 1
            for j in range(variables['num_I']):
                siguiente_I = (((4.0 ** i) - 1) ** -1) * ((nuevos_I[-1] * (4 ** i)) - (variables['I'][-1][j]))
                nuevos_I.append(siguiente_I)
                i += 1
            variables['I'].append(nuevos_I)
            print(nuevos_I)

            return variables

        variables['bandas'] = variables['bandas'] * 2
        variables = crear_J(variables)
        variables['num_I'] += 1
        variables = crear_I_asterisco(variables)
        return variables

    # Codigo que declara el diccionario y sus variables,
    variables = {'c': 0.0, 'bandas': 1.0, 'J': 0.0, 'I': [[0.0]], 'num_I': 0}
    variables = primeros_calculos(variables)
    variables = all_calculos(variables)
    x_n = variables['I'][-1][-2]
    x_nmas1 = variables['I'][-1][-1]
    diferencia = x_nmas1 - x_n
    while abs(diferencia) > (10 ** (-decimales)):
        variables = all_calculos(variables)
        x_n = variables['I'][-1][-2]
        x_nmas1 = variables['I'][-1][-1]
        diferencia = x_nmas1 - x_n
    resultado = round(x_nmas1, decimales)
    print("\nLa solucion a la integral es: " + str(resultado))


x = Symbol('x')

print("Bienvenid@ al metodo de integracion numerica de Romberg")
limites = limites_de_la_integral()
funcion = funcion()
decimales = int(input("Ingresa los decimales de precision con los que quieres tu resultado: "))
solve(funcion, limites, decimales)
