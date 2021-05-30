library(RSNNS)


## funcion que calcula el error cuadratico medio
MSE <- function(pred,obs) {sum((pred-obs)^2)/length(obs)}


#CARGA DE DATOS
# se supone que los ficheros tienen encabezados
# trainSet <- read.csv("Train.csv",dec=".",sep=",",header = T)
# validSet <- read.csv( "Valid.csv",dec=".",sep=",",header = T)
# testSet  <- read.csv("Test.csv",dec=".",sep=",",header = T)

trainSet <- read.table("trainParab.txt")
validSet <- read.table( "testParab.txt")
testSet <- read.table( "testParab.txt")


salida <- ncol (trainSet)   #num de la columna de salida





#SELECCION DE LOS PARAMETROS
a <- 10 #NUMERO DE NEURONAS DE LA PRIMERA CAPA
b <- 10 #NUMERO DE NEURONAS DE LA SEGUNDA CAPA
topologia        <- c(a,b) #PARAMETRO DEL TIPO c(A,B,C,...,X) A SIENDO LAS NEURONAS EN LA CAPA OCULTA 1, B LA CAPA 2 ...
razonAprendizaje <- 0.05 #NUMERO REAL ENTRE 0 y 1
ciclosMaximos    <- 500 #NUMERO ENTERO MAYOR QUE 0

#Colocamos bucles anidados para automatizar el cambio de los hiperparámetros 
#ESTE BUCLE CAMBIA EL VALOR DE LA RAZON DE APRENDIZAJE
for (i in 1:19){
  topologia[1] <- a
  #ESTE BUCLE CAMBIA EL NUMERO DE NEURONAS DE LA PIMERA CAPA
  for (j in 1:11){
    topologia[2] <- b
    #ESTE BUCLE CAMBIA EL NUMERO DE NEURONAS DE LA SEGUNDA CAPA
    for (k in 1:11){
      #EJECUCION DEL APRENDIZAJE Y GENERACION DEL MODELO
      set.seed(1)
      model <- mlp(x= trainSet[,-salida],
                   y= trainSet[, salida],
                   inputsTest=  validSet[,-salida],
                   targetsTest= validSet[, salida],
                   size= topologia,
                   maxit=ciclosMaximos,
                   learnFuncParams=c(razonAprendizaje),
                   shufflePatterns = F
      )
      
      # #GRAFICO DE LA EVOLUCION DEL ERROR
      plotIterativeError(model)
      # 
      # # DATAFRAME CON LOS ERRORES POR CICLo: de entrenamiento y de validacion
      # iterativeErrors <- data.frame(MSETrain= (model$IterativeFitError/ nrow(trainSet)),
      #                               MSEValid= (model$IterativeTestError/nrow(validSet)))
      # 
      # # 
      #SE OBTIENE EL NUMERO DE CICLOS DONDE EL ERROR DE VALIDACION ES MINIMO 
      nuevosCiclos <- which.min(model$IterativeTestError)
      # 
      #ENTRENAMOS LA MISMA RED CON LAS ITERACIONES QUE GENERAN MENOR ERROR DE VALIDACION
      set.seed(1)
      model <- mlp(x= trainSet[,-salida],
                   y= trainSet[, salida],
                   inputsTest=  validSet[,-salida],
                   targetsTest= validSet[, salida],
                   size= topologia,
                   maxit=nuevosCiclos,
                   learnFuncParams=c(razonAprendizaje),
                   shufflePatterns = F
      )
      #GRAFICO DE LA EVOLUCION DEL ERROR
      plotIterativeError(model)
      
      iterativeErrors <- data.frame(MSETrain= (model$IterativeFitError/ nrow(trainSet)),
                                    MSEValid= (model$IterativeTestError/nrow(validSet)))
      
      #CALCULO DE PREDICCIONES
      prediccionesTrain <- predict(model,trainSet[,-salida])
      prediccionesValid <- predict(model,validSet[,-salida])
      prediccionesTest  <- predict(model, testSet[,-salida])
      
      #CALCULO DE LOS ERRORES
      errors <- c(TrainMSE= MSE(pred= prediccionesTrain,obs= trainSet[,salida]),
                  ValidMSE= MSE(pred= prediccionesValid,obs= validSet[,salida]),
                  TestMSE=  MSE(pred= prediccionesTest ,obs=  testSet[,salida]))
      errors
      
      
      
      
      
      #SALIDAS DE LA RED
      outputsTrain <- data.frame(pred= prediccionesTrain,obs= trainSet[,salida])
      outputsValid <- data.frame(pred= prediccionesValid,obs= validSet[,salida])
      outputsTest  <- data.frame(pred= prediccionesTest, obs=  testSet[,salida])
      
      
      
      
      #GUARDANDO RESULTADOS
      modelo <- paste0("nnet","-",topologia[1],"-",topologia[2],"-",razonAprendizaje,".rds")
      saveRDS(model,modelo)
      errores <- paste0("finalErrors","-",topologia[1],"-",topologia[2],"-",razonAprendizaje,".csv")
      write.csv2(errors,errores)
      erroresIter <- paste0("iterativeErrors","-",topologia[1],"-",topologia[2],"-",razonAprendizaje,".csv")
      write.csv2(iterativeErrors,erroresIter)
      train <- paste0("netOutputsTrain","-",topologia[1],"-",topologia[2],"-",razonAprendizaje,".csv")
      write.csv2(outputsTrain,train)
      valid <- paste0("netOutputsValid","-",topologia[1],"-",topologia[2],"-",razonAprendizaje,".csv")
      write.csv2(outputsValid,valid)
      test <- paste0("netOutputsTest","-",topologia[1],"-",topologia[2],"-",razonAprendizaje,".csv")
      write.csv2(outputsTest, test) 
      
      #AUMENTAMOS EN 5 EL NUMERO DE NEURONAS DE LA SEGUNDA CAPA
      topologia[2] <- topologia[2] + 5
    }
    topologia[1] <- topologia[1] + 5
  }
  razonAprendizaje <- razonAprendizaje + 0.05
}
