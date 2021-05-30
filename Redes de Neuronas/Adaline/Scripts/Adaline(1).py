from random import uniform


pesos=[]
variacionPesos=[]
for i in range(9):
	#Inicializamos pesos y umbral con números aleatorios entre -1 y 1
	pesos.append(uniform(-1,1))
variacionPesos=pesos.copy()	
tasaAprendizaje=uniform(0,1)
print("Tasa de Aprendizaje de "+ str(tasaAprendizaje))
print( "Pesos y umbral iniciales")
print(pesos)

for x in range(500):
	#print("Inicio del ciclo " +str(x))
	file=open("datosEntre.csv")
	line= file.readline()
	#Una vez inicializados los pesos corremos por los distintos patrones
	for i in range(10200):
		line= file.readline().strip("\n").split(",")
		salidaObtenida=0
		#Rango 8 porque el ultimo atributo es la salida deseada
		for j in range(8):
			salidaObtenida +=float(line[j])*pesos[j]
		#sumamos tambien el umbral
		salidaObtenida+=pesos[8]
		#line[8]contiene el resultado que debemos obtener	
		difSalida= float(line[8])- salidaObtenida
		#Calculamos la variacion de pesos y del umbral
		for j in range(8):
			variacionPesos[j]= tasaAprendizaje*difSalida*float(line[j])
		variacionPesos[8]= tasaAprendizaje*difSalida
		#Por ultimo, updateamos los pesos
		for j in range(9):
			pesos[j] += variacionPesos[j]
	#print("Pesos obtenidos")
	#print(pesos)
	#Con esto habriamos realizado una vuelta de entrenamiento y miramos errores
	erroresEntre=[]
	file.close()
	file=open("datosEntre.csv")
	line= file.readline()
	#Obtenemos los errores en cada patron
	for i in range(10200):
		line= file.readline().strip("\n").split(",")
		salidaObtenida=0
		for j in range(8):
			salidaObtenida +=float(line[j])*pesos[j]
		salidaObtenida+=pesos[8]
		erroresEntre.append(abs(float(line[8])- salidaObtenida))
	#Por ultimo obtenemos el error absoluto medio
	sumaErrorEntre=0
	for i in erroresEntre:
		sumaErrorEntre += i
	sumaErrorEntre= sumaErrorEntre / 10200
	file.close()

	#Ahora usamos nuestro conjunto de validacion
	erroresVali=[]
	file=open("datosValid.csv")
	line= file.readline()
	for i in range(3400):
		line= file.readline().strip("\n").split(",")
		salidaObtenida=0
		for j in range(8):
			salidaObtenida +=float(line[j])*pesos[j]
		salidaObtenida+=pesos[8]
		erroresVali.append(abs(float(line[8])- salidaObtenida))
	sumaErrorVali=0
	for i in erroresVali:
		sumaErrorVali += i
	sumaErrorVali= sumaErrorVali / 3400
	file.close()
	#Para finalizar, esenamos los resultados
	print("Error en entrenamiento \tError en validacion")	
	strFinal= str(sumaErrorEntre)+ "\t" + str(sumaErrorVali)
	print(strFinal)




