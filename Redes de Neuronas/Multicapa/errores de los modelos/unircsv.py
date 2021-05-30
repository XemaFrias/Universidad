if __name__ == '__main__':
    f1 = open("errores.csv","w")
    f1.write("Capa1,Capa2,Razon,TrainMSE,ValidMSE,TestMSE\n")
    for i in range(10): #Itera sobre la razon de aprendije
        for j in range(4): #Itera sobre la primera capa de neuronas
            for k in range(4): #Itera sobre la segunda capa de neuronas
                f2 = open("csv/finalErrors-"+str((j+1)*10)+"-"+str((k+1)*10)+"-"+str((i*0.1)+0.05)+".csv")
                f2.readline()
                str1 = str((j+1)*10)+","+str((k+1)*10)+","+str(str((i*0.1)+0.05))+","
                for i in range(3):
                    str2 = f2.readline().replace("\r\n","").split(";")
                    str1 += str(str2[1]).replace(",",".").replace("/n","")
                    if i != 2:
                        str1 += ","
                str1 += "\n"
                f1.write(str1)
