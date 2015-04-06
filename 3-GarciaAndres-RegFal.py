# -*- coding: utf-8 -*-
"""
Created on Thu May 15 00:05:56 2014

Aproximaciones Sucesivas

Diccionario de variables por funcion:

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
	-funcion:  funcion que se usará para explorar
	-resolucion: intervalos entre los que el usuario divide una sección del dominio para buscar soluciones
	-generador_exploratorio_1: generador que genera valores f(x) para tabular
	-generador_exploratorio_2: generador que genera valores f(x) para encontrar_intervalos
	-intervalos_solucion: lista con intervalso en los que se encuentran raices de la funcion

encontrar:
        encontrar_solucion:
            pivote: valor de x que se mantendrá fijo mientras el otro se aproxima a la raiz
            x_n: primer valor iterado
            x_nmas1: valor iterado consecutivamente después de x_n
            error: diferencia entre valores iterados uno despues del otro
            precision: cantidad de decimales exactos que desea el usuario
            regula:
                -a: limite dinamico de un intervalo
                -b: limite estatico durante la aproximacion (pivote)
        -intervalo:lista que contiene los límites dentro de donde buscar la raiz
        -precision:cantidad de decimales exactos que desea el usuario



@author: aagarcia
"""
import sympy, numpy


from sympy import Symbol, lambdify, sympify

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
#funcion para ingresar y validar un intervalo dado por el usuario
def ingresar_limites():
    lim_inferior = float(raw_input("desde: "))
    lim_superior = float(raw_input("hasta: "))
    while lim_inferior >= lim_superior:
        print"ingresa bien tus limites! vamos otra vez"
        lim_inferior = float(raw_input("desde: "))
        lim_superior = float(raw_input("hasta: "))
    return [lim_inferior, lim_superior]  
#funcion para ingresar precision decimal
def ingresar_precision_solucion():
    precision = raw_input("¿Para cuántos decimales de precisión quieres se calcule tus soluciones?\n")
    while (not es_numero(precision)) or (int(precision) < 1 ):
        if precision == "default": precision = 5  
        else: precision = raw_input("Ingresa default o una resolucion razonable\n") 
    return int(precision) 
#funcion para insertar y validar expresioneS
def ingresar_funcion():
        
        from sympy.parsing.sympy_parser import parse_expr       
        
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
# funcion para graficar la funcion a explorar        
def graficar_funcion():
    
    from matplotlib import pyplot       
    
    print "Escribe tu función"
    funcion = ingresar_funcion() 
    print "Ingresa el rango en que te interesa buscar soluciones"
    [minimo_x, maximo_x] = ingresar_limites()
    coord_x = numpy.linspace(minimo_x,maximo_x,100)
    coord_y = lambdify(x,funcion, "numpy")(coord_x)
    pyplot.plot(coord_x, coord_y)
    pyplot.xlabel('Dominio')
    pyplot.ylabel('Rango')
    pyplot.grid(True)
    pyplot.axhline(linewidth=2, color='black')
    pyplot.axvline(linewidth=2, color='black')
    print "Esta es la gráfica de tu función"
    print "Cuando hayas encontrado un rango que contenga las soluciones que quieras..."
    print "recuérdalo, y cierra la gráfica para continuar"
    pyplot.show()
    return funcion
    
#funcion que tabula x en el rango deseado y encuentra intervalos que contienen raíces
def explorar(funcion):

    """El usuario ingresa los limites para los que quiere encontrar soluciones, con que intervalos quiere hacer los saltos exploratorios
    Se tabula la exploracion para el usuario y se agregan los intervalos que contienen raices a una lista  
    """
    #funcion para ingresar en cuantos 'pedazos' se dividirá el intervalo a explorar
    def ingresar_precision_rangos():
        print"Este programa divide el rango dado por el usuario en 10 intervalos"
        print"para explorar soluciones, si estás conforme escribe default,"
        print"si quieres mas precision, introduce la precision que quieras (ej. 100) "
        resolucion = raw_input()
        while (not es_numero(resolucion)) or (float(resolucion) < 1 ):
            if resolucion == "default": resolucion = 10  
            else: resolucion = raw_input("Ingresa default o una resolucion razonable\n") 
        return float(resolucion)
    #funcion que genera una tabulación para que el usuario vea el cambio de signo
    def tabular(generador):
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
        p = generador.next() 
        for i in generador:
            q = i
            if (funcion.subs(x,p)*funcion.subs(x,q)) <= 0:
                if (funcion.subs(x,p)*funcion.subs(x,q)) < 0:                
                    intervalos_solucion.append((p,q))
                elif not funcion.subs(x,p):
                    soluciones.append(p)
            p = q
        return intervalos_solucion
    """El usuario ingresa los limites para los que quiere encontrar soluciones, con que intervalos quiere hacer los saltos exploratorios
    Se tabula la exploracion para el usuario y se agregan los intervalos que contienen raices a una lista  
    """             
    print "Ingresa el rango en x para el cual quieres encontrar todas las soluciones"
    limites_exploracion = ingresar_limites()
    resolucion = ingresar_precision_rangos()
    generador_exploratorio_1 =(n for n in numpy.arange(limites_exploracion[0],limites_exploracion[1]+(1.0/resolucion), (limites_exploracion[1]-limites_exploracion[0])/resolucion))
    tabular(generador_exploratorio_1)
    generador_exploratorio_2 =(n for n in numpy.arange(limites_exploracion[0],limites_exploracion[1]+(1.0/resolucion), (limites_exploracion[1]-limites_exploracion[0])/resolucion))
    intervalos_solucion = encontrar_intervalos_soluciones(generador_exploratorio_2, funcion) 
    return intervalos_solucion

"""
Esta funcion toma la lista de intervalos en los que se encuentran las soluciones, 
y regresa las soluciones
"""   
def encontrar(intervalos_solucion, precision, funcion):
    """esta funcion itera usando la regla falsa y cambia el pivote si hay un cambio de signo en f(x)"""                          
    def encontrar_solucion(intervalo, precision):
        
        def regula(a,b):
            return round((((a * funcion.subs(x,b))-(b * funcion.subs(x,a)))/((funcion.subs(x,b))-(funcion.subs(x,a)))), precision)
        
        pivote = intervalo[1]
        x_n = round(regula(intervalo[0], pivote), precision)
        x_nmas1 = round(regula(intervalo[0], pivote), precision)
        error = x_nmas1 - x_n
        if round(x_n, precision) == round(x_nmas1,precision):
            soluciones.append(x_nmas1)
        while abs(error) > (10**(-precision)):
            x_nmas1 = regula(x_nmas1, pivote)
            x_n = x_nmas1
            error = x_nmas1 - x_n
            if round(x_n, precision) == round(x_nmas1,precision):
                soluciones.append(x_nmas1)
                            
    print"Ahora vamos a encontrar tus soluciones"
    for intervalo in intervalos_solucion:
        encontrar_solucion(intervalo, precision)
    return precision
    
x = Symbol('x')
soluciones = []

print "Bienvenido al buscador de raíces por aproximaciones sucesivas..."
precision = ingresar_precision_solucion()
funcion = graficar_funcion()
intervalos_solucion = explorar(funcion) 
if intervalos_solucion: 
    encontrar(intervalos_solucion, precision, funcion)
if soluciones:
    print "Aqui van tus soluciones: " 
    for solucion in soluciones:
        print round(solucion, precision)
else:
    print "no se encontraron soluciones"
