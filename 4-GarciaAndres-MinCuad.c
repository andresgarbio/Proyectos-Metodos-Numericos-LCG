/*
 * minimos_cuadrados.c
 *  punto:estructura de datos que guarda c y y
 * 	matriz: estructura de datos, lista de listas de puntos
 * 	num_puntos= variable que indica el numero de puntos
 * 	i = acumulador
 *	L: fin nulo de una lista de puntos
 *	char respuesta: cadena que almacena la respuesta de un usuario
 * 	lista: lista de puntos
 * 	nodo: puntero al punto que se va a agregar
 * 	promedios: vector que contiene los promedios para x y y de una lista de puntos
 * 	promedio_x: promedio de x de una lista
 *  promedio_y: promedio de y de una lista
 * 	numerador: numerador en la formula para coeficiente de pearson
 * 	denominador: denominadpr en la formula para coeficiente de pearson
 * 	sumatoria_x: sumatoria de x de una lista
 * 	sumatoria_y: sumatoria de y de una lista
 * 	nueva_matriz: nueva matriz en donde se ingresan lso datos
 *  matriz_sumar: matriz en la que se suman los renglones
 * 	matriz_multiplicar: matriz en la que se multiplica un renglon por un factor determinado
 * 	matriz_liberada: matriz cuyos punteros se van a liberar
 *	
 *  
 * 		
 */


#include <stdio.h>
#include <math.h>
#include <stdlib.h>

typedef struct _punto{
		int numero;
		float x;
		float y;
		struct _punto* sig;
} punto;

typedef struct _matriz{
		int* dimension;
		float** entrada;
} matriz;

int main(int argc, char **argv)
{	/*gener una lista de puntos agregando a final*/
	punto* generar_puntos(){
		
		punto* crear_punto(int id_punto){
		
			punto* nuevo_punto;
		
			if(!(nuevo_punto = malloc(sizeof(punto)))){
			puts("Error no hay memoria");
			exit(1);
			}nuevo_punto->numero = id_punto;
			printf("Cual es el valor x para tu %i ° punto? \n", id_punto);
			scanf("%f",&(nuevo_punto->x));
			printf("Cual es el valor y para tu %i °punto? \n", id_punto);
			scanf("%f",&(nuevo_punto->y));
			nuevo_punto->sig = NULL;
			
			return(nuevo_punto);
			
		}
		
		punto* agregar_final(punto* lista, punto* nodo){
	
			punto *p;
			
			if(lista){
				if(lista->x > nodo->x){
						nodo->sig = lista;
						lista = nodo;
						return(lista);
				}for( p = lista;(p->sig); p=(p->sig)){
					if(p->sig->x > nodo->x){
						nodo->sig = p->sig;
						p->sig = nodo;
						return(lista);
					}
				} p->sig = nodo;
			}else{
				lista = nodo;
			}nodo->sig = NULL;
			return(lista);
		} 
		
		punto* reacomodar_ids(punto* lista,int num_puntos){	
			
			punto *p;
			int i;
			
			for(p = lista, i = 0;i < num_puntos; p = p->sig, i++){
				p->numero = i+1;
			}return(lista);
		}
		
		int num_puntos, i;
		punto* L;
		char respuesta;
		
		L = NULL;
			
		puts("Cuantas puntos (x,y) tienes?");
		scanf("%i", &num_puntos);
		while(num_puntos < 2){
			puts("Necesitas mas puntos! Inserta más!");
			scanf("%i", &num_puntos);
		}for( i = 0 ; i < num_puntos ; i++) {
		L = agregar_final(L,crear_punto(i+1));
	}puts("Importó el orden en el que insertaste los puntos?" );
	puts("responde s/n");
	scanf("%c",&respuesta);
	while(respuesta != 'n' && respuesta !='s'){
		scanf("%c",&respuesta);
	}if(respuesta == 'n'){
		L = reacomodar_ids(L, num_puntos);
	}return(L);	
	}
	/*tabula los valores de lista de puntos*/
	void tabular(punto* lista){
		
		punto* p;
		puts("tabulando...");
		puts("  id     |      x         |      y     \n");
		for(p = lista;(p); p=(p->sig)){
			printf("  %i    |   %f       |   %f   \n", p->numero, p->x, p->y);
		}	
	}
	
	/*recorre la lista para sacar el coef de pearson de los datos*/
	void coef_pearson(punto*lista){
		
		float* promediar(punto* lista){
			
			float* promedios;
			float sumatoria_x, sumatoria_y, n;
			punto* p;
		
			sumatoria_x = 0;
			sumatoria_y = 0;
			n = 0;
			if(!(promedios = malloc(2*sizeof(float)))){
			puts("Error no hay memoria");
			exit(1);
			}for(p = lista;(p); p=(p->sig)){
				sumatoria_x += p->x;
				sumatoria_y += p->y;	
				n = p->numero;
			}promedios[0] = sumatoria_x / n;
			promedios[1] = sumatoria_y / n;
			return promedios;
		}
		
		float promedio_x, promedio_y,numerador,denominador_x, pearson, pearson_2, denominador_y, denominador;
		punto* p;
		
		promedio_x = *(promediar(lista));
		promedio_y = *(promediar(lista) + 1);
		numerador = 0;
		denominador_x = 0;
		denominador_y = 0;
		
		/*al recorrer la lista saca valores para numerador y denominador*/
		for(p = lista;(p); p=(p->sig)){
			numerador += ((p->x)-promedio_x) * ((p->y) - promedio_y);
			denominador_x += pow(((p->x)-promedio_x),2) ;
			denominador_y += pow(((p->y)-promedio_y),2);	
		}denominador = denominador_x * denominador_y;
		denominador = pow(denominador,0.5);
		pearson = numerador/denominador;
		printf("Coeficiente de correlacion : %f\n", pearson);
		pearson_2 = pow(pearson,2);
		printf("Coeficiente de determinacion = %f\n", pearson_2);
		
		
		
		
	}
	
	/*liberar un punto de una lista*/
	
	void liberar(punto* lista_puntos){
		
		punto* p, *q;

		for(p = lista_puntos; (p->sig); p = q){
			 q = p->sig;
			 free(p);	
		}		
	}
	/*aloca memoria para una matriz*/
	matriz* crear_matriz(int* dimensiones){

		
			matriz* nueva_matriz;

			int i;
			
			if(!(nueva_matriz = malloc(sizeof(matriz)))){
				puts("Error no hay memoria");
				exit(1);
			}if(!(nueva_matriz->dimension = malloc(sizeof(int*)))){
				puts("Error no hay memoria");
				exit(1);
			}nueva_matriz->dimension = dimensiones;
			if(!(nueva_matriz->entrada = malloc(dimensiones[0]*sizeof(float*)))){
				puts("Error no hay memoria");
				exit(1);
			}for(i = 0 ; i < dimensiones[0]; i++){
				if(!((*((nueva_matriz->entrada)+i))  = calloc(dimensiones[1], sizeof(float)))){
					puts("Error no hay memoria");
					exit(1);
				}
			}
			
			return(nueva_matriz);
			
	}
	/*recorre las entradas de una matriz y las imprime*/
	void imprimir_matriz(matriz* matriz_impresa){
		
		int i;
		int j;
		
		for( i = 0 ; i < matriz_impresa->dimension[0]; i++){
			printf("\n");
			for( j = 0 ; j < matriz_impresa->dimension[1]; j++){
				printf(" %f ", matriz_impresa->entrada[i][j]);
			}printf("\n");
		}
	}
	/* suma dos renglones de una matriz y los igual a uno de ellos*/
	matriz* sumar_renglon(matriz* matriz_sumar, int renglon_a, int renglon_b){
		
		int i;
		
		for(i = 0; i < matriz_sumar->dimension[1] ; i++){
			matriz_sumar->entrada[renglon_a][i] = matriz_sumar->entrada[renglon_a][i] + matriz_sumar->entrada[renglon_b][i];
		}return matriz_sumar;
	}
	
	/*multiplica un renglon de la matriz por un factor y lo iguala al mismo renglon*/
	matriz* multiplicar_renglon(matriz* matriz_multiplicar, int renglon_a, float factor){
		
		int i;
		
		for(i = 0; i < matriz_multiplicar->dimension[1] ; i++){
			matriz_multiplicar->entrada[renglon_a][i] = matriz_multiplicar->entrada[renglon_a][i] * factor;
		}return matriz_multiplicar;
	}
	
	/*libera cada entrada de la matriz y finalmente la matriz */
	void liberar_matriz(matriz* matriz_liberada){
		
		int i;
		
		for(i = 0 ; i < (matriz_liberada->dimension[0]) ; i++){
			free(*(matriz_liberada->entrada + i));
		}free(matriz_liberada->entrada);
		free(matriz_liberada);
	}
	
	/*calcula la sumatoria de x en cierto punto de la nueva matriz*/
	float sumatoria_x(punto* lista_puntos_sumatoria, int renglon, int columna){
		
		punto*p;
		float sumatoria;
		
		sumatoria = 0;
		
		for(p = lista_puntos_sumatoria; (p); p = p->sig){
			/*rl valor de x depende de su posicion i y j en la matriz*/
			 sumatoria += pow(p->x, renglon + columna);
		}return sumatoria;
	}
	
	float sumatoria_y(punto* lista_puntos_sumatoria, int renglon){
		
		punto*p;
		float sumatoria;
		
		sumatoria = 0;
		/*recorre las ultimas entradas de una matriz y las imprime
		 * generando las constantes de la matriz*/
		for(p = lista_puntos_sumatoria; (p); p = p->sig){
			 sumatoria += (pow(p->x, renglon) * (p->y));
		}return sumatoria;
	}
	/*recorre la matriz creaa y permite al usuarion ingresar datos*/
	
	matriz* insertar_datos(matriz* matriz_vacia, punto* lista_puntos_insertar){
		
		int i;
		int j;
		for(i = 0 ; i < (matriz_vacia->dimension[0]) ; i++){
			for(j = 0 ; j < (matriz_vacia->dimension[0]) ; j++){
			matriz_vacia->entrada[i][j] = sumatoria_x(lista_puntos_insertar, i, j);
			}
		}for(j = 0; j < (matriz_vacia->dimension[0]) ; j++){
			matriz_vacia->entrada[j][matriz_vacia->dimension[0]] = sumatoria_y(lista_puntos_insertar,j);
		}return matriz_vacia;
	}
	/*avanza por una matriz y divide las entrdas entre el elemento diagonal*/
	matriz* despeje(matriz* matriz_despejar){
		
		int i;
		int j;
		
		for(i = 0; i < matriz_despejar->dimension[0] ; i++){
			for(j = 0; j < matriz_despejar->dimension[0] ; j++){
				matriz_despejar->entrada[i][j] = matriz_despejar->entrada[i][j] / matriz_despejar->entrada[i][i];
			}	
		}return matriz_despejar;
	}
	
	/*avanza por una matriz y apra cada elemento diagonal, convierte en 0 todos los elementos de la misma columna
	 *y al final queda una matriz diagonal*/
	matriz* resolver_gauss_jordan(matriz* matriz_resolver){
		
		int i;
		int j;
		int k; 
		
		for(i = 0; i < matriz_resolver->dimension[0] ; i++){
			for(j = 0; j < matriz_resolver->dimension[0] ; j++){
				if (i == j){
					for(k = 0; k < matriz_resolver->dimension[0] ; k++){
						if(k != i){ 
							multiplicar_renglon(matriz_resolver, i, -1 *((matriz_resolver->entrada[k][j])/(matriz_resolver->entrada[i][j])));
							matriz_resolver = sumar_renglon(matriz_resolver, k, i);
						}
					}
				}multiplicar_renglon(matriz_resolver, i, (1.0/matriz_resolver->entrada[i][i]));
			}	
		}return matriz_resolver;
	}
	
	/*imprime el polinomio resultante*/
	void imprimir_polinomio(matriz* matriz_resuelta){
		
		int i;
		
		puts("Tu polinomio es:");
		for(i = matriz_resuelta->dimension[0]; i ; i--){
			if (matriz_resuelta->entrada[i-1] > 0){
				printf("+ ");
			}else{
				printf("- ");
			}printf("%f x^%i ", matriz_resuelta->entrada[i-1][matriz_resuelta->dimension[0]], i-1 );
		}	
	}
	/*Este es el programa principal que junta a las funciones anteriores*/
	matriz* matriz_resolucion;
	punto* lista_puntos;
	int grado;
	int tamano[2];
	grado = 0;
	
	puts("Este es el programa de regresiones lineales y cuadráticas");
	lista_puntos = generar_puntos();
	tabular(lista_puntos);
	coef_pearson(lista_puntos);
	puts("De que grado quieres tu polinomio" );
	puts("El grado de tu polinomio debe ser menor que el numero de puntos");
	scanf("%d",&grado);
	while(grado < 1){
		scanf("%d",&grado);
	}grado++;
	tamano[0] = grado;
	tamano[1] = grado + 1;
	matriz_resolucion= crear_matriz(tamano);
	matriz_resolucion = insertar_datos(matriz_resolucion, lista_puntos);
	matriz_resolucion = resolver_gauss_jordan(matriz_resolucion);
	matriz_resolucion = despeje(matriz_resolucion);
	imprimir_polinomio(matriz_resolucion);
	
	liberar_matriz(matriz_resolucion);



	liberar(lista_puntos);
	return 0;
}
