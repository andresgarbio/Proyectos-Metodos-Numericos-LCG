# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 00:39:21 2014

@author: aagarcia

Euler

ingresar_funcion:
	-es_despeje: bandera que indica si la funcion a ingresar será la función principal o un despeje
	-funcion: expresión de sympy que el usuario ingresa para buscar sus raíces
	-respuesta: cadena con respuesta de usuario
"""
import sympy 

from sympy import Symbol

#funcion para insertar y validar expresiones   
def ingresar_funcion():
        
        from sympy.parsing.sympy_parser import parse_expr       
        from sympy import sympify
        
        print("Ahora ingresa tu función")        
        funcion = sympify(raw_input("y' = "))
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
        funcion = funcion.subs('pi', 3.14159265359)
        funcion = funcion.subs('e', 2.71828182846)
        return funcion

#funcion que genera nuevos valores de x y y de  en base a la ecuacion diferencial y al intervalo     
def generar_yn(funcion, intervalo, valores_xy):
    
    x_n = valores_xy[0]
    y_n = valores_xy[1]
    
    y_n = y_n + (intervalo * funcion.subs([(x,x_n), (y, y_n)]))

    return [(x_n + intervalo), y_n]

#funcion que itera generando nuevos valores para x y hasta llegar al valor para el que se buscaba la solucion        
def solucion_euler(funcion, intervalo, valores_iniciales, solucion_x):

    from numpy import arange
     
    valores_xy = valores_iniciales
    
     
    for valor in arange(valores_iniciales[0],solucion_x,intervalo):
         valores_xy = generar_yn(funcion, intervalo, valores_xy)
    print"Tu respuesta es", valores_xy[1]
         
     
     
    
x = Symbol('x')
y = Symbol('y')

#funcion principal que le pide los datos al usuario y llama a las demas funciones     

valores_iniciales = [0.0,0.0]
print"Bienvenido al programa de resolucion de ecuaciones diferenciales EULER"
funcion = ingresar_funcion()
intervalo = float(raw_input("Ingresa tu intervalo(h)\n"))
print("ingresa los valores iniciales de tu funcion y(a) = b")
valores_iniciales[0] = float(raw_input("a: "))
valores_iniciales[1] = float(raw_input("b: "))
solucion_x = float(raw_input("para que valor x quieres tu solucion?\n"))
solucion_euler(funcion,intervalo,valores_iniciales, solucion_x)