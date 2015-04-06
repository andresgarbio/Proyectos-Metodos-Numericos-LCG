# -*- coding: utf-8 -*-
"""
Created on Thu May 15 00:05:56 2014

@author: aagarcia

Aproximaciones Sucesivas

Diccionario de variables por funcion:

-x: simbolo para expresiones
-soluciones: lista de soluciones encontradas

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
graficar_funcion:
	-funcion: expresión sympy que se va a graficar
	-minimo_x: limite inferior del dominio a graficar
	-maximo_x: limite superior del dominio a graficar
	-coord_x: array en el que se guardan intervalos de x para graficar
	-coord_y: array en el que se guardan intervalos de y para graficar
explorar:
	ingresar_precision_rangos:
		-resolucion: numero de intervalos en los que el usuario quiere dividir el dominio para 	explorar raíces
	tabular:
		-i: acumulador
		-generador: generador de nuevos valores de x a tabular
	encontrar_intervalos_soluciones:
		-intervalos_solucion: lista en la que guardan intervalos en los que se encuentran soluciones
		-a: valor en el rango de x usado para encontrar raices
		-b: valor en el rango de y para explorar para encontrar raices
		-i: acumulador
	-resolucion:
	-limites_exploracion:
	-funcion:  funcion que se usará para explorar
	-resolucion: intervalos entre los que el usuario divide una sección del dominio para buscar soluciones
	-generador_exploratorio_1: generador que genera valores f(x) para tabular
	-generador_exploratorio_2: generador que genera valores f(x) para encontrar_intervalos
	-intervalos_solucion: lista con intervalso en los que se encuentran raices de la funcion

encontrar:
	encontrar_solucion:
		checar_criterio:
			-criterio: bandera que indica que se cumplió el criterio de convergencia
			-punto: valor de x para el cual se va a evaluar el criterio de convergencia
			-despeje: expresion para aproximar raices
			-respuesta: cadena que da la respuesta del usuario
		-intervalo:iterador 
		-intervalos_solucion: lista que contiene intervalso para soluciones
		-punto_medio: valor para empezar la iteración
		-despeje: expresion para aproximar raices
		-x_n: valor de x para la n iteración
		-x_nmas1: valor de x para n+ 1 iteracion
   
"""
import sympy, numpy
from sympy import Symbol, lambdify, sympify


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
    lim_inferior = float(raw_input("desde: "))
    lim_superior = float(raw_input("hasta: "))
    while lim_inferior >= lim_superior:
        print"ingresa bien tus limites! vamos otra vez"
        lim_inferior = float(raw_input("desde: "))
        lim_superior = float(raw_input("hasta: "))
    return [lim_inferior, lim_superior]  

#funcion para que el usuario ingrese la precision decimal deseada
def ingresar_precision_solucion():
    precision = raw_input("¿Para cuántos decimales de precisión quieres que se calculen tus soluciones?\ndefault: 5\n")
    while (not es_numero(precision)) or (int(precision) < 1 ):
        if precision == "default": precision = 5  
        else: precision = raw_input("Ingresa default o una resolucion razonable") 
    #se aumenta la precision para que los resultados contengan los digitos deseados y uno redondeado
    return int(precision) + 1
    
#funcion para insertar y validar expresiones
def ingresar_funcion(es_despeje = False):
        
        from sympy.parsing.sympy_parser import parse_expr       
        #entre ingresar una funcion o un despeje, solo cambia el prompt
        if es_despeje == True:
            funcion = (sympify(raw_input("g(x) = ")))
        else:
            funcion = (sympify(raw_input("f(x) = ")))
        print "¿Es ésta tu funcion?"
        sympy.pprint(funcion)
        respuesta = raw_input("responde si o no: \n")
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
 
# funcion para graficar la funcion a explorar   
def graficar_funcion():
    
    from matplotlib import pyplot       
    
    print "Escribe tu función"
    funcion = ingresar_funcion() 
    print "Ingresa el rango en x en que te interesa buscar soluciones"
    [minimo_x, maximo_x] = ingresar_limites()
    coord_x = numpy.linspace(minimo_x,maximo_x,100)
    coord_y = lambdify(x,funcion, "numpy")(coord_x)
    pyplot.plot(coord_x, coord_y)
    pyplot.xlabel('Dominio')
    pyplot.ylabel('Rango')
    pyplot.grid(True)
    pyplot.axhline(linewidth=2, color='black')
    pyplot.axvline(linewidth=2, color='black')
    print "Esta es la gráfica de tu función->"
    print "Cuando hayas encontrado un rango que contenga las soluciones que quieras..."
    print "recuérdalo, y cierra la gráfica para continuar"
    pyplot.show()
    return funcion
 
#funcion que tabula x en el rango deseado y encuentra intervalos que contienen raíces
def explorar(funcion):
    
    #funcion para ingresar en cuantos 'pedazos' se dividirá el intervalo a explorar
    def ingresar_precision_rangos():
        print"Este programa divide el rango dado por el usuario en 10 intervalos"
        print"para explorar soluciones, si estás conforme escribe default,"
        print"si quieres mas precision, introduce la precision que quieras (ej. 100) "
        resolucion = raw_input()
        while (not es_numero(resolucion)) or (float(resolucion) < 1 ):
            if resolucion == "default": resolucion = 10  
            else: resolucion = raw_input("Ingresa default o una resolucion razonable") 
        return float(resolucion)
        
    #funcion que genera una tabulación para que el usuario vea el cambio de signo
    def tabular(generador):
         print"generando tabla...."
         print" x         |       y"
         for i in generador: 
             print i , "    |     " ,  funcion.subs(x,i)   
         print"********************************************************"        
         print"Si notas un desvío en los intervalos de la tabulación..."
         print"es un desvio causado por la aritmética punto flotante"
         print"Este desvio aumenta conforme la exploración se hace más precisa"
         print"No te preocupes!"
         print"Este desvio no se reflejará en las raíces de tu función"
         print"********************************************************" 
         
    """funcion que compara valores f(x) , si hay un cambio de signo, se agrega un intervalo para respuestas
    si uno de ellos es cero, se agrega directamente a las respuestas
    """     
    def encontrar_intervalos_soluciones(generador,funcion):
        intervalos_solucion = [] 
        a = generador.next() 
        for i in generador:
            b = i
            if (funcion.subs(x,a)*funcion.subs(x,b)) <= 0:
                if (funcion.subs(x,a)*funcion.subs(x,b)) < 0:                
                    intervalos_solucion.append((a,b))
                elif not funcion.subs(x,a):
                    soluciones.append(a)
            a = b
        return intervalos_solucion
        
    """El usuario ingresa los limites para los que quiere encontrar soluciones, con que intervalos quiere hacer los saltos exploratorios
    Se tabula la exploracion para el usuario y se agregan los intervalos que contienen raices a una lista  
    """       
    print "Ingresa el rango en x para el cual quieres encontrar todas las soluciones"
    limites_exploracion = ingresar_limites()
    resolucion = ingresar_precision_rangos()
    #se usann generadores para tabular y sacar f(x) al buscar raíces porque no requieren memoria como listas
    generador_exploratorio_1 =(n for n in numpy.arange(limites_exploracion[0],limites_exploracion[1]+(1.0/resolucion), (limites_exploracion[1]-limites_exploracion[0])/resolucion))
    tabular(generador_exploratorio_1)
    generador_exploratorio_2 =(n for n in numpy.arange(limites_exploracion[0],limites_exploracion[1]+(1.0/resolucion), (limites_exploracion[1]-limites_exploracion[0])/resolucion))
    intervalos_solucion = encontrar_intervalos_soluciones(generador_exploratorio_2, funcion)
    return intervalos_solucion

"""
'encontrar'toma la lista de los intervalos en los que se encuentran las soluciones, 
y regresa las soluciones

"""   
def encontrar(intervalos_solucion, precision):
    """ 'encontrar maneja la lista de intervalos de solucion 
    "encontrar_solucion" se encarga de cada solucion individual
    """           
    def encontrar_solucion(intervalo, precision):
        """Esta funcion checa los criterios de convergencia usando la derivada 
        del punto x_0 a iterar y le permite al usuario ingresar otro despeje """
        def checar_criterio(despeje,punto):
    
            from sympy.mpmath import diff, log, sin, tan, cos

            criterio = False     
            #se evalua el criterio de convergencia y se deja que el usuario decida si continua con el msimo despeje        
            print "g'(",punto,") = ",abs(diff(lambdify(x,sympify(despeje),"sympy"), punto))
            while abs(diff(lambdify(x,sympify(despeje),"sympy"), punto)) > 1.0:
                print"Tu despeje no cumple el criterio de convergencia para este intervalo"
                respuesta = raw_input("Quieres arriesgarte? responde si/no\n")
                while respuesta != "si" and  respuesta != "no":
                    respuesta = raw_input("Quieres arriesgarte? responde si/no?")
                if respuesta == "si":
                    return criterio
                else:
                    despeje = ingresar_funcion(despeje = True)
            print"Tu despeje cumple el criterio de covergencia, solucion garantizada!"
            criterio = True
            return criterio
		
        punto_medio = (intervalo[1]+intervalo[0])/2 
        print"Ingresa un despeje cuyo resultado sea real para x = " , punto_medio
        print"si tu depeje es raiz cuadrada, " 
        print"que tenga el mismo signo que x"
        #se le pide al usuario un despeje y se generan los primeras iteraciones y diferencias
        despeje = ingresar_funcion(es_despeje = True)
        x_n = round(punto_medio, precision) 
        x_nmas1 = round(despeje.subs(x, x_n), precision)
        #se genera una diferencia entre soluciones iteradas consecutivamentecompararla con la precision deseada
        diferencia_n = x_nmas1 - x_n
        #si el criterio de convergencia se cumple se itera hasta llegar a la precision deseada
        if checar_criterio(despeje, x_n) :
            while abs(diferencia_n) > (10**(-precision)):
                x_n = x_nmas1
                x_nmas1 = round(despeje.subs(x, x_nmas1), precision)
                diferencia_n = x_nmas1 - x_n
            print"Guardando solucion...."
            soluciones.append(x_nmas1)
        else:
		#si nos e cumple el criterio, se itera hasta que las diferencias aumenten (se aleje de la solucion)
            diferencia_n = x_nmas1 - x_n
            x_n = x_nmas1
            x_nmas1 = round(despeje.subs(x, x_nmas1), precision)
            diferencia_nmas1 = x_nmas1 - x_n
            #para saber si converge o no, se toma en cuenta que las diferencias entre iteraciones disminuyan cada vez mas
            while abs(diferencia_n) > abs(diferencia_nmas1):
                x_n = x_nmas1                
                x_nmas1 = round(despeje.subs(x, x_nmas1), precision)
                diferencia_n = diferencia_nmas1
                diferencia_nmas1 = x_nmas1 - x_n
                if round(x_n, precision) == round(x_nmas1,precision):
                    print"Guardando solucion...."
                    soluciones.append(x_nmas1)
                    break
            #si los valores empiezan a alejarse de la solucion (si la diferencia entre consecutivos aumenta) se detiene
            else:
                print"No converge"
                
                            
    print"Para encontrar solcuiones, despeja fu funcion f(x)"
    print"y conviertela en una funcion del tipo x = g(x)"
    for intervalo in intervalos_solucion:
        encontrar_solucion(intervalo, precision)
    return precision
    
x = Symbol('x')
soluciones = []

#programa principal que llama a los demás

print "Bienvenido al buscador de raíces por aproximaciones sucesivas!"
precision = ingresar_precision_solucion()
funcion = graficar_funcion()
intervalos_solucion = explorar(funcion)
if intervalos_solucion: 
    encontrar(intervalos_solucion, precision)
if soluciones:
    print "Aqui van tus soluciones: " 
    for solucion in soluciones:
        print round(solucion, precision)
else:
    print "no se encontraron soluciones"
    


                                                        









    






