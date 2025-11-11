import math

def getProbsEnt(msgEnt):
    alfEnt = getAlf(msgEnt)
    lenEnt = len(alfEnt)
    probsEnt = [0] * lenEnt

    for elem in msgEnt:
        probsEnt[alfEnt.index(elem)] += 1 / len(msgEnt)
    return probsEnt

def calcEntropPriori(probs):
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

def formatoFloats(lst):
    return [round(x, 5) for x in lst]

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
    print(formatoFloats(probsEnt))

    probsSal = getProbSal(matCanal, probsEnt)
    print("\nProbabilidades de salida del canal:")
    print(formatoFloats(probsSal))

    probsPost = getProbsPost(matCanal,probsEnt,probsSal)
    print("\nProbabilidades a posteriori de la entada: ")
    for fila in probsPost:
        print(formatoFloats(fila))
