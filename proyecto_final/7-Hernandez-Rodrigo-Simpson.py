"""
NAME
       7-Hernandez-Rodrigo-Simpson.py
VERSION
        [1.0]
AUTHOR
        Rodrigo Daniel Hernandez Barrera <<rodrigoh@lcg.unam.mx>>
DESCRIPTION
        Programa que resuelve integrales por el metodo de Simpson 1/3, dada la integral, sus limites, el numero de bandas,
        y los decimales de precision.
USAGE
        Desde terminal y en el directorio donde esta guardado el archivo, utilizar el comando:

            7-Hernandez-Rodrigo-Simpson.py

        Requiere previa instalacion de la libreria SymPy desde terminal, de ser necesario consulte el citio web:
        https://programminghistorian.org/es/lecciones/instalar-modulos-python-pip
DICCIONARIO DE VARIABLES
    funcion:

        -funcion: guarda la funcion ingresada por el usuario convertida con sympify a un tipo que pueda ser
        usado por la libreria SymPy

    limites:
        limite_inferior: almacena el limite inferior de la integral
	    limite_superior: almacena el limite superior de la integral

    solve:
        a: almacena el limite inferior
        b: almacena el limite superior
        h: guarda el intervalo dado por la resta de 'b' con 'a' dividida entre el total de bandas
        intervalo = guarda el valor del limite inferior, que con cada iteracion se le suma el valor de 'h'
        A = es el area bajo la curva, es decir la solucion a la integral

"""


from sympy import Symbol


# Ingresa la funcion y sustituye los valores de 'pi' y 'e'
def funcion():
    from sympy.parsing.sympy_parser import parse_expr
    from sympy import sympify

    print("\nIngresa tu funcion")
    funcion = sympify(input("   y' = "))

    variable = parse_expr(funcion)

    funcion_final = variable.subs('pi', 3.14159265359)
    funcion_final = funcion_final.subs('e', 2.71828182846)

    return funcion_final


# Funcion para ingresar los limites de la integral. Se valida que el limite superior sea mayor al inferior, si esto es
# falso se regresa un ValueError con un mensaje representativo
def limites():
    print("\nIngresa el intervalo de la integral")
    limite_inferior = float(input("   limite inferior: "))
    limite_superior = float(input("   limite superior: "))
    if limite_inferior >= limite_superior:
        raise ValueError("El limite inferior es mas grande que el limite superior, por favor hagalo de nuevo")
    return limite_inferior, limite_superior


# Funcion que recibe los limites de la integral, los almacena en variables y los utiliza para avanzar desde el limite
# inferior hasta el superior de acuerdo al intervalo 'h' que es calculado previamente. Dentro de un for se decide cual
# operacion realizar y se guarda el valor en A, que es nuestra area de resultado.
def solve(limits_of_integration, funcion, bandas, decimales):
    from numpy import arange

    a = limits_of_integration[0]
    b = limits_of_integration[1]

    h = (b - a) / bandas

    A = 0.0
    for i, intervalo in enumerate(arange(a, b + h, h)):
        if intervalo != a and intervalo != b:
            if i % 2:
                A += funcion.subs(x, intervalo) * 4.0
            else:
                A += funcion.subs(x, intervalo) * 2.0
        else:
            A += funcion.subs(x, intervalo)
    A = (h / 3.0) * A
    resultado = round(A, decimales)
    print("\nLa solucion a la integral es: " + str(resultado))


# Main function que le pide los datos al usuario, pasandolos como parametro en la llamada de las funciones
x = Symbol('x')
print("Bienvenid@ al programa de integración de Simpson")
limits_of_integration = limites()
funcion = funcion()
bandas = float(input("\nIngresa el numero de bandas con el que quieres trabajar: "))
decimales = int(input("Ingresa los decimales de precision para el resultado: "))
solve(limits_of_integration, funcion, bandas, decimales)
