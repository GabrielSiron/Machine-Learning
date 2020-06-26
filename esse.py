import idx2numpy as de
import numpy as np
import cv2
import math

class Knn:

    def distEuclidiana(self, dado, teste):
        soma = 0
        for item in range(len(dado)):
            for j in range(28):
                soma += 0.001*math.pow(int(dado[item][j]) - int(teste[item][j]), 2)

        return math.sqrt(soma)

    def votMajor(self, rotuloTeste, comp, k, qtdRotulos):

        classific = np.zeros((qtdRotulos))
        
        for i in range(k):
            valor = min(comp)
            rotulo = comp[valor]
            comp.pop(valor)
            if i != k-1:
                classific[rotulo] += 1
            else:
                return classific
            
    def knn(self, amostra, base, rotulos):

        n = {}
        lista = []
        for j in range(len(base)):
            dist = self.distEuclidiana(amostra[:len(amostra) - 1], base[j])
            lista.append(dist)
            n.update({dist: rotulos[j]})

        return n


arquivoImagem = 'train-images.idx3-ubyte'
arquivoRotulo = 'train-labels.idx1-ubyte'

imagens = de.convert_from_file(arquivoImagem)
rotulos = de.convert_from_file(arquivoRotulo)

limiteTreino = 300
limiteTeste = 100

imagensTreinos = imagens[:limiteTreino, :, :]
rotulosTreinos = rotulos[:limiteTreino]
imagensTestes  = imagens[limiteTreino:limiteTreino+limiteTeste, :, :]
rotulosTestes  = rotulos[limiteTreino:limiteTreino+limiteTeste]

classificador = Knn()

allVizinhos = {}

i=0
soma=0

for teste in imagensTestes:

    allVizinhos = classificador.knn(teste, imagensTreinos, rotulosTreinos)
    kVizinhos = list(classificador.votMajor(rotulosTestes[i], allVizinhos, 3, 10))
    print(kVizinhos.index(max(kVizinhos)), rotulosTestes[i], sep = " - ", end = ' ')
    if kVizinhos.index(max(kVizinhos)) == rotulosTestes[i]:
        soma += 1
        print("acertou!")
    else:
        print("...")
    i += 1

print(100*soma/i)
