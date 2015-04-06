# -*- coding: utf-8 -*-
"""
Created on Fri May 30 21:44:28 2014

@author: aagarcia
"""

#Esta funcion construye una lista de listas , las listas anidadas dentro de la
#lista principal seran las ecuaciones del sistema, cada ecuacion tiene n
#elementos(variables) mas una constante y hay n ecuaciones
def generar_matriz(n):
    def ingresar_ecuaciones():
        ecuaciones = [range(n+1) for x in range(n)]
        for ecuacion in ecuaciones:
            for cociente in ecuacion:
                if cociente < n:
                    print "Ingresa el", cociente + 1,"° cociente de la", ecuaciones.index(ecuacion) +1, "° ecuacion"
                    ecuacion[cociente] = float(raw_input())
                else:
                    print "Ingresa la constante de la", ecuaciones.index(ecuacion)+1, "° ecuacion"
                    ecuacion[cociente] = float(raw_input())
        print "Esta es la matriz de tus ecuaciones:"
        for ecuacion in ecuaciones:
            print ecuacion
        return ecuaciones
    
    def checar_criterio(sistema_ecuaciones):

        import copy
        
        matriz = copy.deepcopy(sistema_ecuaciones)     
        peso_diag = 0
        peso_otro = 0
        criterio = False         
        
        for renglon in matriz: renglon.pop()
        diag_matriz = diag(abs(array(matriz)))
        peso_diag = sum(diag_matriz)
        peso_otro = abs(matrix((matriz))).sum()
        peso_otro = peso_otro - peso_diag
        if peso_diag > peso_otro:
            criterio = True
        return criterio
        
    sistema_ecuaciones = ingresar_ecuaciones()    
    while not checar_criterio(sistema_ecuaciones):
        print"El orden de tus ecuaciones no cumple el criterio de convergencia para este intervalo"
        respuesta = raw_input("Quieres arriesgarte? responde si/no?")
        while respuesta != "si" and  respuesta != "no":
            respuesta = raw_input("Quieres arriesgarte? responde si/no?")
        if respuesta == "si":
            return sistema_ecuaciones
        else:
            sistema_ecuaciones = ingresar_ecuaciones() 
    print"Enhorabuena, tu sistema cumple el criterio de convergencia!"
    return sistema_ecuaciones

def encontrar_soluciones(ecuaciones, precision):
    
    def iteracion(aproximadores, soluciones):
        soluciones_iteracion = soluciones
        for aproximacion in aproximadores: 
            soluciones_iteracion[aproximacion[0]] = ((aproximacion[1])-(sum(array(soluciones) * array(aproximacion[3]))))/(aproximacion[2])
            soluciones_iteracion[aproximacion[0]] = round(soluciones_iteracion[aproximacion[0]], precision)            
        return soluciones_iteracion
        
    valores_diagonales = diag(array(ecuaciones))
    valores_constantes = [ecuacion.pop() for ecuacion in ecuaciones]
    val_no_diagonales = (array(ecuaciones) - diag(diag(array(ecuaciones)))).tolist()
    indice = range(n)
    aproximadores = zip(indice,valores_constantes,valores_diagonales,val_no_diagonales) 
    soluciones_n = [0]*(n)
    solucion_n = soluciones_n[0]
    soluciones_n = iteracion(aproximadores, soluciones_n)
    solucion_n = soluciones_n[0]
    soluciones_n = iteracion(aproximadores, soluciones_n)
    i = 0
    while(round(solucion_n, precision) != round(soluciones_n[0], precision)):
        if i > 10*n:
            print"no converge"
            break
        solucion_n = soluciones_n[0]
        soluciones_n = iteracion(aproximadores, soluciones_n)
        i += 1
    else:
        print"Tus soluciones son:"
        print soluciones_n

    

               
from numpy import array, diag, matrix  
    
print"Bienvenido al solucionador de sistemas de ecuaciones lineales"
print"por medio del método de Gauss Siedel ordena tus ecuaciones en la forma: "
print" a11X1 + a12X2 + a13X3 + ... + a1nXn = b1"
print" a21X1 + a22X2 + a23X3 + ... + a2nXn = b2"
print" a31X1 + a32X2 + a33X3 + ... + a3nXn = b3"
print" ..."
print" an1X1 + an2X2 + an3X3 + ... + annXn = bn"
n = int(raw_input("¿Cuantas variables tienes?\n"))
precision = int(raw_input("¿Para cuántos decimales de precisión quieres que se calculen tus soluciones?\n"))
ecuaciones = generar_matriz(n)
encontrar_soluciones(ecuaciones, precision)


    
    

                    