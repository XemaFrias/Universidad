file=open("aleatorizados_datos.csv")
datosTest=open("datosTest.csv","w")
datosValid=open("datosValid.csv","w")
datosEntre=open("datosEntre.csv","w")

line= file.readline()
for i in range(10200):
	line= file.readline()
	datosEntre.write(line)
for i in range(3400):
	line= file.readline()
	datosValid.write(line)
for i in range(3400):
	line= file.readline()
	datosTest.write(line)	
file.close()
datosTest.close()
datosValid.close()
datosEntre.close()	

