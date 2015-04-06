# -*- coding: utf-8 -*-
"""
Created on Sat May 31 22:16:57 2014

@author: aagarcia
Romberg

es_numero:
	-cadena: cadena que es evaluada para si es un valor numérico
ingresar_limites:
	-limite_inferior: valor usado para denotar el limite inferior de un rango
	-limite_superior: valor usado para denotar el limite superior de un rango
ingresar_precision_solucion:
	-precision: cantidad de decimales que el usuario pide para su respuesta
ingresar_funcion:
	-despeje: bandera que indica si la funciona ingresar será la función principal o un despeje
	-funcion: expresión de sympy que el usuario ingresa para buscar sus raíces
	-respuesta: cadena para que el usuario de su respuesta
 aproximar_integral:
     -bandeo: diccionario con los valores de la iteracion más reciente
generar_J:
    cambio_J: suma de las evaluaciones de funcion en cuanto a la siguiente iteración de J
generar_refinamientosI:
    nuevos_I: lsita con los valores de I para la siguiente iteracion

"""

import sympy, numpy


from sympy import Symbol

""" funcion que comprueba que una cadena contiene un valor numerico
credor original: usuario @Skippy Frand Gouru de Stack Overflow
en el foro "How do I chech if a string is a number in Python
http://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-in-python"""

def es_numero(cadena):
    try:
        float(cadena)
        return True
    except ValueError:
        return False
#ingresar y validar los limites para la integral
def ingresar_limites():
    
    print"ingresa el intervalo en el que quieres integrar tu función"
    lim_inferior = float(raw_input("desde: "))
    lim_superior = float(raw_input("hasta: "))
    while lim_inferior >= lim_superior:
        print"ingresa el intervalo en el que quieres integrar tu función "
        lim_inferior = float(raw_input("desde: "))
        lim_superior = float(raw_input("hasta: "))
    return [lim_inferior, lim_superior] 

#ingresar y validar la funcion para la que se va a evaluar la integral    
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
        funcion = funcion.subs('pi', 3.14159265359)
        funcion = funcion.subs('e', 2.71828182846)
        return funcion
        
#el usuario ingresa con que precision decimal quiere su solucion aproximada
def ingresar_precision_solucion():
    precision = raw_input("¿Para cuantos decimales de precision quieres se calcule tus soluciones?")
    while (not es_numero(precision)) or (int(precision) < 1 ):
        if precision == "default": precision = 5  
        else: precision = raw_input("Ingresa default o una resolucion razonable") 
    return int(precision) 


#esta funcion itera el diccionario bandeo, generando nuevas corecciones hasta dar con una respuesta determinada
def aproximar_integral(funcion, limites, precision):
    #genera la primera iteracion de bandeo, I1
    def primer_bandeo(bandeo):
        bandeo['c'] = limites[1]-limites[0]
        bandeo['bandas'] = 1
        bandeo['J'] = 0.5 *(funcion.subs(x,limites[0]) + funcion.subs(x,limites[1]))
        bandeo['I'] = [[bandeo['J']*bandeo['c']]]
        print bandeo['I'][-1]
        return bandeo
    #genera las subsecuentes  iteraciones de bandeo y las aproximaciones I 
    def doblar_bandeo(bandeo):
        #genera la siguiente iteracion de J
        def generar_J(bandeo): 
            cambio_J = 0
            intervalo = ((1.0/bandeo['bandas'])*bandeo['c'])
            n = intervalo + limites[0]
            while(n < limites[1]):
                cambio_J += funcion.subs(x,n)
                n = (2.0 * intervalo) + n
            bandeo['J'] = bandeo['J'] + cambio_J
            return bandeo
         #genera una lista  con la siguiente iteración de I y la agrega a bandeo I   
        def generar_refinamientosI(bandeo):
            nuevos_I = []
            nuevos_I.append((1.0/bandeo['bandas'])*bandeo['c']*bandeo['J'])
            
            i = 1
            for j in range(bandeo['num_I']):
                siguiente_I = (((4.0**i)-1)**-1)*((nuevos_I[-1]*(4**i))-(bandeo['I'][-1][j])) 
                nuevos_I.append(siguiente_I) 
                i +=1
            bandeo['I'].append(nuevos_I)
            print nuevos_I
            
            return bandeo
              
        bandeo['bandas'] = bandeo['bandas'] * 2
        bandeo = generar_J(bandeo)
        bandeo['num_I'] += 1
        bandeo = generar_refinamientosI(bandeo)
        return bandeo
    
    #la funcion inicial inicializa bandeo y genera un loop que continua iterando hasta llegar a la solucion esperada
    bandeo = {'c': 0.0, 'bandas': 1.0, 'J': 0.0,'I' : [[0.0]],'num_I':0}
    bandeo = primer_bandeo(bandeo)
    x_n = bandeo['I'][-1][0]
    bandeo = doblar_bandeo(bandeo)
    x_n = bandeo['I'][-1][-2]
    x_nmas1 = bandeo['I'][-1][-1]
    error = x_nmas1 - x_n
    while(abs(error) > (10**(-precision))):                    
        bandeo = doblar_bandeo(bandeo)
        x_n = bandeo['I'][-1][-2]
        x_nmas1 = bandeo['I'][-1][-1]
        error = x_nmas1 - x_n
    print"La solucion a la integral es:", x_nmas1
        
        
            
        
x = Symbol('x')

print"Bienvenido al programa de integración de Romberg"
limites = ingresar_limites()
funcion = ingresar_funcion()
precision = ingresar_precision_solucion()
aproximar_integral(funcion, limites, precision)


