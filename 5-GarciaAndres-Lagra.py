# -*- coding: utf-8 -*-
"""
Created on Sun Jun  1 19:02:42 2014

@author: aagarcia

Lagrange

diccionario_variables:
    graficar_polinomio:
	-polinomio: expresión sympy que se va a graficar
	-minimo_x: limite inferior del dominio a graficar
	-maximo_x: limite superior del dominio a graficar
	-coord_x: array en el que se guardan intervalos de x para graficar
	-coord_y: array en el que se guardan intervalos de y para graficar
     ingresar_coordenadas:
        puntos: lista con los puntos a interpolar        
        coor_x: valor x para nuevo punto
        coord_y: valor y paa nuevo punto
    interpolar_x:
        i: acumulador
        J: acumulador
        expresion: aquí se almacenan las fracciones que se generan al iterar sobre el conjunto de puntos
        fraccion: el resultado de la interpolacion de cada puntoen la formula sumatoria, es expresion
        numerador: el numerador de la fraccion en la formula sumatoria, es expresion
        denominador:el denominador de la fraccion en la formula sumatoria, es un numero
    interpolar_numero:
        i: acumulador
        J: acumulador
        fraccion: el resultado de la interpolacion de cada puntoen la formula sumatoria con x = a
        numerador: el numerador de la fraccion en la formula sumatoria, es numero
        denominador: interpolar_x: el denominador de la fraccion en la formula sumatoria, es numero
"""
import sympy, numpy

from sympy import Symbol, sympify, expr
x = Symbol('x')

#se genera una lista de puntos para interpolar
def ingresar_coordenadas():
    puntos = []
    num_puntos = int(raw_input("cuantos puntos tienes?"))
    for i in range(num_puntos):
        print"cual es la coordenada x de tu", i +1, "punto"
        coord_x = float(raw_input())
        print"cual es la coordenada y de tu", i + 1,"punto"
        coord_y = float(raw_input())
        puntos.append((coord_x, coord_y))
    return puntos

#genera interpolacion para x
def interpolar_x(lista_puntos):
    
    from sympy import simplify    
    
    expresion = sympify('0')
    #se recorre la lista de puntos
    for i in lista_puntos:
        fraccion = sympify('1')
        numerador = sympify('1')
        denominador = 1.0
        for j in lista_puntos:
            if (j != i):
                #se suma y multiplicade acuerdo a la formula
                numerador *= (x - j[0])
                denominador *= (i[0] - j[0])
                fraccion *= (sympify(x  - j[0])/(i[0]-j[0]))
        fraccion = (numerador/denominador) * i[1]
        expresion += fraccion 
    expresion = simplify(expresion)
    sympy.pprint(expresion)
    return expresion
#genera una interpolacion con respecto a un valor
def interpolar_numero(valor,lista_puntos):
    aproximacion = 0
    #recorre la lista de puntos
    for i in lista_puntos:
        fraccion = 0
        numerador = 1
        denominador = 1
        for j in lista_puntos:
            #se suma y multiplica de acuerto a la formula
            if (j != i):
                numerador *= (valor - j[0])
                denominador *= (i[0] - j[0])
        fraccion = (numerador/denominador) * i[1]
        print fraccion
        aproximacion += fraccion 
    print aproximacion

#si se eligio la interpolacion en cuanto a x, se grafica ese polinomio
def graficar_polinomio(funcion, lista_puntos):
    
    from matplotlib import pyplot
    from sympy import lambdify
    
    from matplotlib import pyplot       
    lista_xy = zip(*lista_puntos)
    [minimo_x, maximo_x] = [min(lista_xy[0]), max(lista_xy[0])]
    coord_x = numpy.linspace(minimo_x,maximo_x,100)
    coord_y = lambdify(x,funcion, "numpy")(coord_x)
    pyplot.plot(coord_x, coord_y)
    pyplot.xlabel('Dominio')
    pyplot.ylabel('Rango')
    pyplot.grid(True)
    pyplot.axhline(linewidth=2, color='black')
    pyplot.axvline(linewidth=2, color='black')
    print "Esta es la gráfica de tu polinomio"
    pyplot.show()
    return funcion

#programa principal en el que se jutnan todas las funciones
print"Bienvenido al interpolador de Lagrange"
lista_puntos = ingresar_coordenadas()
print "¿Quieres un polinomio o aproximar un punto?"
respuesta = raw_input("responde 'x' o introduce el punto: ")
if respuesta == 'x':
    polinomio = interpolar_x(lista_puntos)
    graficar_polinomio(polinomio, lista_puntos)
    
else:
    interpolar_numero(float(respuesta),lista_puntos)



