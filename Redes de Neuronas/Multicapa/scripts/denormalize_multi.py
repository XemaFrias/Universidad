maximo=500001
minimo=14999

f2 = open("netOutputsTest.csv")
valoresObtenidosTest = []

l = len(f2.readlines())
f2.seek(0)

for i in range(l):
    line = f2.readline().strip("\n").split(";")
    valoresObtenidosTest.append(line[1])

valoresObtenidosTestD = []
for i in range(len(valoresObtenidosTest)):
    valoresObtenidosTestD.append(float(valoresObtenidosTest[i])*(maximo-minimo)+minimo)

fn = open("netOutputsTestDenormalized.csv","w")
for i in range(len(valoresObtenidosTest)):
    fn.write(str(valoresObtenidosTest[i]) + "," + str(valoresObtenidosTestD[i]) + "\n")
