"Los datos de pruebas de las funciones son con "
"la fuente, entrada y salida del ejercicio 1 de la guía 5"

import math

def getProbsEnt(msgEnt):
    alfEnt = getAlf(msgEnt)
    lenEnt = len(alfEnt)
    probsEnt = [0] * lenEnt

    for elem in msgEnt:
        probsEnt[alfEnt.index(elem)] += 1 / len(msgEnt)
    return probsEnt

def getEntropEnt(probs):
    entrop = 0
    for elem in probs:
        entrop += elem * math.log2(1 / elem)
    return entrop

def getAlf(msg):
    alf = []
    for elem in msg:
        if elem not in alf:
            alf.append(elem)
    return alf

def getMatCanal(msgEnt, msgSal):

    #En esta matriz las FILAS suman 1 xq es la probabilidad de que
    #se de la salida j SABIENDO que se dio la entrada i

    alfEnt = getAlf(msgEnt)
    alfSal = getAlf(msgSal)
    filas = len(alfEnt)
    cols = len(alfSal)
    matCanal = [[0 for _ in range(cols)] for _ in range(filas)]  # Inicializo la matriz con 0s

    for i in range(len(msgEnt)):
        matCanal[alfEnt.index(msgEnt[i])][alfSal.index(msgSal[i])] += 1

    # Normalizo por filas
    for i in range(len(matCanal)):
        fila = matCanal[i]
        suma = sum(fila)
        if suma != 0:
            matCanal[i] = [elem / suma for elem in fila]

    return matCanal

def getProbSal(matCanal, probsEnt):
    cantSal = len(matCanal[0])
    vecProbsSal = [0] * cantSal

    for i in range(cantSal):
        for j in range(len(matCanal)):
            vecProbsSal[i] += matCanal[j][i] * probsEnt[j]
    return vecProbsSal

def getProbsPost(matCanal, probsEnt, probsSal):

    #En esta matriz las COLUMNAS suman 1, porque es la probabilidad 
    # de que se da una entrada i SABIENDO que se dio la salida j

    filas = len(matCanal)       # cantidad de entradas
    cols = len(matCanal[0])     # cantidad de salidas
    probsPost = [[0 for _ in range(cols)] for _ in range(filas)]

    for j in range(filas):
        for i in range(cols):
            probsPost[j][i] = (matCanal[j][i] * probsEnt[j]) / probsSal[i]

    return probsPost

#P(Ai,Bj) = P(Ai/Bj)*P(Bj) = P(Bj/Ai)*P(Ai)
def getMatSimult(matCanal,probsEnt):
    
    #Esta matriz suma 1 entre todos sus elementos xq 
    #Cada posicion es un suceso posible de todos los
    #que pueden ocurrir.

    filas = len(matCanal)       # cantidad de entradas
    cols = len(matCanal[0])     # cantidad de salidas
    matSimult = [[0 for _ in range(cols)] for _ in range(filas)]

    for i in range(filas):
        for j in range(cols):
            matSimult[i][j] = matCanal[i][j]*probsEnt[i]
    return matSimult

def getEntropPost(probsPost,probsSal):
    
    #Una entropía por cada salida

    entropsPost = [0]*len(probsSal)

    for j in range(len(probsPost[0])): #Cantidad de salidas
        for i in range(len(probsPost)): #Cantidad de entradas
            entropsPost[j] += probsPost[i][j]*math.log2(1/probsPost[i][j])

    return entropsPost

def getEntropPostMed(vecEntropsPost,probsSal): #creo que esta mal??? verificar dsps
    
    #Esta entropia posterior media se conoce como Equivocación, o ruido del canal

    entropPostMed = 0

    for i in range (len(vecEntropsPost)):
        entropPostMed += vecEntropsPost[i]*probsSal[i]
    return entropPostMed

def getInfoMutua(entropPriori,entropPostMed):
    return entropPriori - entropPostMed

def getEntropAfin(matSimult):
    entropAfin = 0

    for i in range(len(matSimult)):
        for j in range(len(matSimult[0])):
            entropAfin += matSimult[i][j]*math.log2(1/matSimult[i][j])
    return entropAfin

#Es sin ruido si existe 1 solo elemento !=0 por columna
def checkSinRuido(matCanal):
    i = 0
    while( i < len(matCanal[0])):
        cantAct = 0
        for j in range(len(matCanal)):
            #print("\nElemento actual : " + str(matCanal[j][i]))
            if matCanal[j][i] != 0:
                cantAct += 1
                if cantAct > 1:
                    return False
        i += 1
    return True

#Es determinante si existe 1 solo elemento !=0 por fila
def checkDeterminante(matCanal):
    i = 0
    while( i < len(matCanal[0])):
        cantAct = 0
        for j in range(len(matCanal)):
            #print("\nElemento actual : " + str(matCanal[i][j]))
            if matCanal[i][j] != 0:
                cantAct += 1
                if cantAct > 1:
                    return False
        i += 1
    return True

#producto matricial
def getCanalComp(matA,matB):

    if len(matA[0]) != len(matB): #no se pueden multiplicar las matrices
        return -1
    
    matComp = [[0 for _ in range(len(matB[0]))] for _ in range(len(matA))]

    for i in range(len(matComp)):          # filas de A
        for j in range(len(matComp[0])):   # columnas de B
            for k in range(len(matA[0])):  # recorre columnas de A / filas de B
                matComp[i][j] += matA[i][k] * matB[k][j]
    
    return matComp

if __name__ == "__main__":
    msgEnt = "abcacaabbcacaabcacaaabcaca"
    msgSal = "01010110011001000100010011"

    alfEnt = getAlf(msgEnt)
    alfSal = getAlf(msgSal)

    print("Entrada del canal:", msgEnt)
    print("Salida del canal:", msgSal)
    print("\n")
    print("Alfabeto de entrada:", alfEnt)
    print("Alfabeto de salida:", alfSal)

    matCanal = getMatCanal(msgEnt, msgSal)
    print("\nMatriz del canal:")
    for fila in matCanal:
        print([round(x, 5) for x in fila])

    probsEnt = getProbsEnt(msgEnt)
    print("\nProbabilidades de la entrada del canal:")
    print(probsEnt)

    entropEnt = getEntropEnt(probsEnt)
    print("\nEntropia de entrada: " + str(entropEnt))

    probsSal = getProbSal(matCanal, probsEnt)
    print("\nProbabilidades de salida del canal:")
    print(probsSal)

    matProbsPost = getProbsPost(matCanal,probsEnt,probsSal)
    print("\nProbabilidades a posteriori de la entada: ")
    for fila in matProbsPost:
        print(fila)

    matProbsSimult = getMatSimult(matCanal,probsEnt)
    print("\nProbabilidades de proceso simultaneo: ")
    for fila in matProbsSimult:
        print(fila)

    vecEntropsPost = getEntropPost(matProbsPost,probsSal)
    print("\nEntropias a posteriori: ")
    print(vecEntropsPost)

    entropPostMed = getEntropPostMed(vecEntropsPost,probsSal)
    print("\nEntropia media a posteriori: ")
    print(entropPostMed)

    infoMutua = getInfoMutua(entropEnt,entropPostMed)
    print("\nInformacion mutua del canal: ")
    print(infoMutua)

    entropAfin = getEntropAfin(matProbsSimult)
    print("\nEntropia afin del canal: ")
    print(entropAfin)
    print("\n")

    print("Canal sin ruido" if checkSinRuido(matCanal) else "Canal con ruido")

    print("Canal determinante" if checkDeterminante(matCanal) else "Canal no determinante")

    print("================== GUIA 6 ================")

    matA = [[0.4,0.6,0,0],
            [0.0,0.0,0.5,0.5],
            [0,0,0.7,0.3]]

    matB = [[0.2,0.3,0.5],
            [0,0,1],
            [0,0,1]]

    print("Canal A:")
    for fila in matA:
        print(fila)

    print("Canal B:")
    for fila in matB:
        print(fila)

    canalComp = getCanalComp(matA,matB)
    print("Canal Compuesto: ")
    if (isinstance(canalComp,int)):
        print("No se pueden multiplicar las matrices")
    else:
        for fila in canalComp:
            print(fila)