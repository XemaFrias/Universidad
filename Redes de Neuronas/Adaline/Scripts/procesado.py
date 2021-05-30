#Open the data file
f = open("california_housing.csv","rt")
attributes = f.readline().strip().split(",")

#Read first line of data
aux = f.readline().strip().split(",")
max = list(aux)
min = list(aux)

for i in range(9):
	max[i] = float(max[i])
	min[i] = float(min[i])
#Get max and min of each attribute
while len(aux) > 1:
	for i in range(9):
		aux[i] = float(aux[i])
		if aux[i] > max[i]:
			max[i] = aux[i]
		elif aux[i] < min[i]:
			min[i] = aux[i]
	aux = f.readline().strip().split(",")

f.close()
f = open("california_housing.csv","rwt")
new = open("data.csv","a")

aux = f.readline()
new.write(aux)
aux = f.readline().strip().split(",")

str1 = ""
count = 0
while len(aux) > 1:
	count += 1
	print(count)
	for i in range(9):
		aux[i] = float(aux[i])
		aux[i] = (aux[i] - min[i])/(max[i] - min[i])
		if i != 8:
			str1 += str(aux[i]) + ","
		else:
			str1 += str(aux[i])
	aux = f.readline().strip().split(",")
	new.write(str1 + "\n")
	str1 = ""
new.close()
