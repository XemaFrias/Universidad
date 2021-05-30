file= open("california_housing.csv")
#La primera linea es de nombre atributos
line= file.readline().strip("\n").split(",")
#la segunda ya tiene la informacion que queremos
line= file.readline().strip("\n").split(",")
for i in range (9):
	line[i]= float(line[i])
#usamos copy() para evitar que se propaguen los cambios	
maximo= line.copy()
minimo= line.copy()

while len(line)>1:
	for i in range(9):
		line[i]= float(line[i])
		if line[i]> maximo[i]:
			maximo[i]= line[i]
		elif line[i]< minimo[i]:
			minimo[i] = line [i]
	line= file.readline().strip("\n").split(",")
file.close()

file= open("california_housing.csv")
salida = open("datos_tratados.csv","w")
#Escribimos la linea de nombres de atributos
line= file.readline()
salida.write(line)
#Pasamos a normalizar los datos
line= file.readline().strip("\n").split(",")
while len(line) > 1:
	output=""
	for i in range (9):
		line[i]= float(line[i])
		#funcion para normalizar
		line[i]= (line[i]-minimo[i])/(maximo[i]-minimo[i])
		line[i]= str(line[i])
	#Comprimimos la lista en un string separado por comas	
	output= ','.join(line)
	output += "\n"	
	salida.write(output)
	line= file.readline().strip("\n").split(",")
salida.close()
file.close()

