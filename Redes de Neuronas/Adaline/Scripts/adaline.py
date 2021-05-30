from random import uniform

class Adaline():
    def __init__(self, w, variacionW, zita, data):
            self.w = w
            self.zita = zita
            self.alpha = 0.05
            self.data = data
            self.variacionW = variacionW
            self.variacionZ = 0
            self.x = []
            self.y = 0
            self.d = 0
            self.mse = 0
            self.mea = 0
            self.valoresObtenidos = []
            self.valoresReales = []
            self.maximo=500001
            self.minimo=14999

    def train(self):
        #Se procede a recorrer los distintos patrones
        data.seek(0)
        l = len(data.readlines()) - 1
        data.seek(0)
        data.readline()
        for i in range(l):
            self.x = data.readline().strip("\n").split(",")
            self.y = 0
            self.d = 0
            #Se calcula el sumatorio
            for j in range(8):
                self.y +=float(self.x[j])*self.w[j]
            #Se suma el umbral
            self.y += self.zita
            #Se actualiza la salida deseada
            self.d = self.x[8]
            difSalida = float(self.d) - self.y
            for j in range(8):
                self.w[j] += self.alpha*difSalida*float(self.x[j])
            self.zita += self.alpha*difSalida

    def calculate_error(self, save):
        data.seek(0)
        l = len(data.readlines()) - 1
        data.seek(0)
        data.readline()
        for i in range(l):
            self.x = data.readline().strip("\n").split(",")
            self.y = 0
            self.d = 0
            #Se calcula el sumatorio
            for j in range(8):
                self.y +=float(self.x[j])*self.w[j]
            #Se suma el umbral
            self.y += self.zita
            #Se actualiza la salida deseada
            self.d = self.x[8]
            difSalida = float(self.d) - self.y
            self.mse += difSalida**2
            self.mea += abs(difSalida)
            if save != 0:
                self.valoresObtenidos.append(self.y)
                self.valoresReales.append(float(self.d))
        self.mse = self.mse/l
        self.mea = self.mea/l
        print("MSE")
        print(self.mse)
        print("MEA")
        print(self.mea)


    def changeDataSet(self, data):
        self.data = data

    def denormalize(self):
        for i in range(len(self.valoresReales)):
            self.valoresReales[i]= self.valoresReales[i]*(self.maximo-self.minimo)+self.minimo
            self.valoresObtenidos[i]= self.valoresObtenidos[i]*(self.maximo-self.minimo)+self.minimo

if __name__ == "__main__":
    data = open("datosEntre.csv")
    f1 = open("errorEntrenamiento.csv","w")
    f2 = open("errorValidacion.csv","w")
    pesos=[]
    variacionPesos=[]
    for i in range(8):
    	#Inicializamos pesos y umbral con numeros aleatorios entre -1 y 1
        pesos.append(uniform(-1,1))
    print(pesos)
    umbral = uniform(-1,1)
    variacionPesos=pesos.copy()
    tasaAprendizaje=uniform(0,1)
    #Inicializamos Adaline
    adaline = Adaline(pesos, variacionPesos, umbral, data)
    pesosFinales = []
    umbralFinal = 0
    errorMEAMinimo = 9999
    #Comenzamos el entrenamiento
    count = 1
    for i in range(512):
        adaline.train()
        #Se calcula el error del set de entrenamiento
        print("-----Error set de entrenamiento ciclo " + str(i) + "-----")
        adaline.calculate_error(0)
        f1.write(str(adaline.mse) + "\n")
        if adaline.mea < errorMEAMinimo:
            errorMEAMinimo = adaline.mea
            pesosFinales = adaline.w.copy()
            umbralFinal = adaline.zita
            count = 0
        else:
            count+=1
            if count > 10:
                break
        data.close()
        data = open("datosValid.csv")
        adaline.changeDataSet(data)
        print("-----Error set de validacion ciclo " + str(i) + "-----")
        adaline.calculate_error(0)
        f2.write(str(adaline.mse) + "\n")
        data.close()
        data = open("datosEntre.csv")
    if count > 10:
         print("-----Error tras llegar al criterio de parada (el error no se reduce): " + str(errorMEAMinimo) + "-----")
    else:
        print("-----Error tras llegar al criterio de parada (todos los ciclos completados): " + str(errorMEAMinimo) + "-----")
    print()
    print("-----Pesos Elegidos-----")
    print(pesosFinales)
    f = open("pesosFinales.csv","w")
    fstring = "Umbral: " + str(umbralFinal) +"\nPesos: "
    for i in range(len(pesosFinales)):
        fstring += str(pesosFinales[i]) + ","
    f.write(fstring)
    f.close()
    print()
    #Se utiliza el conjunto de test para evaluar la generalizacion del aprendizaje
    adaline.changeDataSet("datosTest.csv")
    adaline.w = pesosFinales.copy()
    adaline.zita = umbralFinal
    print("-------Error del test-------")
    adaline.calculate_error(1)

    data = open("data_grafico.csv","w")
    adaline.denormalize()
    for i in range(len(adaline.valoresReales)):
        data.write(str(adaline.valoresReales[i]) + "," + str(adaline.valoresObtenidos[i]) + "\n")
