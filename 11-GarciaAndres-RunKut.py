# -*- coding: utf-8 -*-
"""
Runge Kutta

@author: aagarcia

Runge Kutta

ingresar_funcion:
	-es_despeje: bandera que indica si la funcion a ingresar será la función principal o un despeje
	-funcion: expresión de sympy que el usuario ingresa para buscar sus raíces
	-respuesta: cadena con respuesta de usuario
 generar_yn:
    x_n: aproximación iterativa de x
    y_n: aproximación iterativa de y
    
    k_1: valor k1 del metodo runge kutta
    k_2: valor k2 del metodo runge kutta
    k_3: valor k3 del metodo runge kutta
    k_4: valor k4 del metodo runge kutta
     
 solucion_diferencial:
    valor: iterador
    valor_xy: valor inicial de la funcion en un punto, que es iterado

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
        #se sustituyen los valores para que la expresion sea compatible con matplotlib
        funcion = funcion.subs('pi', 3.14159265359)
        funcion = funcion.subs('e', 2.71828182846)
        return funcion
      
def generar_yn(funcion, intervalo, valores_xy):
    
    x_n = valores_xy[0]
    y_n = valores_xy[1]
    #en base a los valores de la n iteracion, se generan los valore k de runge kutta
    k_1 = intervalo * funcion.subs([(x,x_n ), (y, y_n)])
    k_2 = intervalo * funcion.subs([(x,x_n + (intervalo * 0.5) ), (y, y_n + (k_1*0.5) )])
    k_3 = intervalo * funcion.subs([(x,x_n + (intervalo * 0.5) ), (y, y_n + (k_2*0.5) )])
    k_4 = intervalo * funcion.subs([(x,x_n + intervalo), (y, y_n + k_3)])  
    #se calcula y utilizando los valores k
    y_n = y_n +  ((1/6.0) *( k_1 + 2*k_2 + 2*k_3 + k_4))
    

    return [(x_n + intervalo), y_n]
    
#esta funcion transforma los valores iniciales en la respuesta a traavés de la iteración
#se avanza sobre el intervalo hasta llegar al valor para el que se bucaba la solucion
def solucion_diferencial(funcion, intervalo, valores_iniciales, solucion_x):

    from numpy import arange
     
    valores_xy = valores_iniciales
    
     
    for valor in arange(valores_iniciales[0],solucion_x,intervalo):
         valores_xy = generar_yn(funcion, intervalo, valores_xy)
    print"Tu respuesta es", valores_xy[1]
         
     
     
    
x = Symbol('x')
y = Symbol('y')

valores_iniciales = [0.0,0.0]

#funcion principal que le pide los datos al usuario y llama a las demas funciones

print"Bienvenido al método Runge Kutta!"
funcion = ingresar_funcion()
intervalo = float(raw_input("Ingresa tu intervalo(h)\n"))
print("ingresa los valores iniciales de tu funcion y(a) = b")
valores_iniciales[0] = float(raw_input("a: "))
valores_iniciales[1] = float(raw_input("b: "))
solucion_x = float(raw_input("para que valor x quieres tu solucion?"))
solucion_diferencial(funcion,intervalo,valores_iniciales, solucion_x)






