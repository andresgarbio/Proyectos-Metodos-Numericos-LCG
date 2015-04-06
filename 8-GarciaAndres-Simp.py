# -*- coding: utf-8 -*-
"""
Created on Sat May 31 22:16:57 2014

@author: aagarcia

es_numero:
	-cadena: cadena usada para validar que una cadena contiene un valor numerico
ingresar_limites:
	-limite_inferior: limite inferior de un intervalo
	-limite_superior: limite superior de un intervalo
ingresar_precision_solucion:
	-precision: decimales que el usuario pide para sus soluciones
ingresar_funcion:
	-es_despeje: bandera que indica si la funcion a ingresar será la función principal o un despeje
	-funcion: expresión de sympy que el usuario ingresa para buscar sus raíces
	-respuesta: cadena con respuesta de usuario
calcular_integral:
    area: aproximacion integral que se quiere obtener sumando evluaciones del intervalo
    subintervalos: cantidad de trapecios en los que se dividirá la función a integrar
    intervalo: altura del trapecio que se manejará
    valor: iterador, que sirve para determinar como evaluar la próxima iteracion
    limites: lista con los limites de la integral
"""

import sympy, numpy


from sympy import Symbol

""" funcion que comprueba que una cadena contiene un valor numerico
credor original: usuario @Skippy Frand Gouru de Stack Overflow
en el foro "How do I check if a string is a number in Python
http://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-in-python"""

def es_numero(cadena):
    try:
        float(cadena)
        return True
    except ValueError:
        return False
        
#funcion para ingresar y validar un intervalo dado por el usuario
def ingresar_limites():
    
    print"ingresa el intervalo en el que quieres integrar tu función"
    lim_inferior = float(raw_input("desde: "))
    lim_superior = float(raw_input("hasta: "))
    while lim_inferior >= lim_superior:
        print"ingresa el intervalo en el que quieres integrar tu función "
        lim_inferior = float(raw_input("desde: "))
        lim_superior = float(raw_input("hasta: "))
    return [lim_inferior, lim_superior] 

#funcion para insertar y validar expresiones   
def ingresar_funcion():
        
        from sympy.parsing.sympy_parser import parse_expr       
        from sympy import sympify
        
        print("Ahora ingresa tu función")        
        funcion = (sympify(raw_input("f(x) = ")))
        print "¿Es ésta tu funcion?"
        sympy.pprint(funcion)
        respuesta = raw_input("responde si o no: ")
        while respuesta != "si":
            if respuesta == "no":
                print "Ingresa tu función"
                funcion = (parse_expr(raw_input("f(x) = ")))
                print "Es esta tu funcion?"
                sympy.pprint(funcion)
                respuesta = raw_input("responde si o no")    
            else:
                 respuesta = raw_input("responde si o no")
         #se sustituyen los valores para que la expresion sea compatible con matplotlib
        funcion = funcion.subs('pi', 3.14159265359)
        funcion = funcion.subs('e', 2.71828182846)
        return funcion
 
#funcion que evalua los valores de los intervalos x y los suma a la solucion   
def calcular_integral(limites,funcion):
    
    from numpy import arange
    
    area = 0 
    i = 0
    
    subintervalos = float(raw_input("cuantos subintervalos quieres?"))
    intervalo= (limites[1]-limites[0])/subintervalos
    for valor in arange(limites[0],limites[1]+intervalo, intervalo):    
        if (valor != limites[0] and valor != limites[1]):
            if(i % 2):
                area += funcion.subs(x,valor) * 4.0
            else:
                area += funcion.subs(x,valor) * 2.0
        else:
            area += funcion.subs(x,valor) 
        i += 1
    area = (intervalo / 3.0)  * area
    print area

x = Symbol('x')
#funcion principal que le pide los datos al usuario y llama a las demas funciones

print"Bienvenido al programa de integración de Simpson"
limites = ingresar_limites()
funcion = ingresar_funcion()
calcular_integral(limites,funcion)