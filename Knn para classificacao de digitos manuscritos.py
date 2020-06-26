import idx2numpy as idnp #esse modulo eh usado para conseguir ler arquivos com a extensao .idx-ubyte
import numpy as np
import cv2
import math

'''
Esse programa utiliza algoritmo KNN
para classificar imagens 28x28px em 
digitos manuscritos (de 0 a 9).

O link para o dataset eh esse: http://yann.lecun.com/exdb/mnist/

No proprio dataset, existem divisoes para 
teste e treino. Aqui, optei por usar o
proprio arquivo de treino como teste (o dataset
eh muito grande, possui 60k imagens!)

se quiser, retire os print()
'''

#criacao da classe KNN
class Knn:
    
    
    def distEuclidiana(self, dado, teste):
        
        '''
        Eu optei por usar distancia euclidiana no meu programa.
        Existem outras metricas, mas essa eh a mais comum.
        '''
        soma = 0
        for item in range(len(dado)):
            for j in range(28):
                soma += 0.001*math.pow(int(dado[item][j]) - int(teste[item][j]), 2)

        return math.sqrt(soma)
    
    
    def votMajor(self, rotuloTeste, comp, k, qtdRotulos):
        '''
        eu crio uma array com (nesse caso) 10 posicoes. Cada
        posicao representa um digito manuscrito e, a cada 
        classificacao que o programa realiza, a posicao referente
        ao digito eh incrementada em uma unidade
        '''
        classific = np.zeros((qtdRotulos))
        
        for i in range(k):
            valor = min(comp)
            rotulo = comp[valor]
            comp.pop(valor)
            
            if i != k-1:
                classific[rotulo] += 1
            else:
                return classific #retornar a array
    
    def knn(self, amostra, base, rotulos):
        '''
        eu criei essa funcao (KNN) com o unico intuito de economizar
        codigo no main. ela nao faz nada de especial
        '''
        n = {}
        lista = []
        for j in range(len(base)):
            dist = self.distEuclidiana(amostra[:len(amostra) - 1], base[j])
            lista.append(dist)
            n.update({dist: rotulos[j]})

        return n

# lembre de baixar os arquivos e coloca-los no mesmo diretorio do seu programa 
# ou passe o diretorio completo na string
arquivoImagem = 'train-images.idx3-ubyte'
arquivoRotulo = 'train-labels.idx1-ubyte'

#agora, tanto 'imagens' como 'rotulos' serao objetos numpy.array, facilmente manipulaveis
imagens = idnp.convert_from_file(arquivoImagem)
rotulos = idnp.convert_from_file(arquivoRotulo)

'''
quanto maior os limites, mais preciso seu programa tende a ficar.
No entanto, se voce esta ainda aprendendo, usar 60k de dados de entrada
pode levar muito tempo para processar. Entao, limite seus dados de entrada
para ter um retorno mais rapido.
'''

limiteTreino = 300
limiteTeste = 100

imagensTreinos = imagens[:limiteTreino, :, :]
rotulosTreinos = rotulos[:limiteTreino]
imagensTestes  = imagens[limiteTreino:limiteTreino+limiteTeste, :, :]
rotulosTestes  = rotulos[limiteTreino:limiteTreino+limiteTeste]

# objeto da classe Knn()
classificador = Knn()

# dicionario usado para armazenar os valores das distancias euclidianas
# de cada um dos dados de treino para uma dada amostra
allVizinhos = {}

# variaveis de controle para a precisao do programa
i    = 0
soma = 0

# o parametro do programa. Lembre de testar valores diferentes
# para 'k' e verifique a variacao de precisao
k = 7

for teste in imagensTestes:
    
    allVizinhos = classificador.knn(teste, imagensTreinos, rotulosTreinos)
    
    kVizinhos = list(classificador.votMajor(rotulosTestes[i], allVizinhos, k, 10))
    print(kVizinhos.index(max(kVizinhos)), rotulosTestes[i], sep = " - ", end = ' ')
    if kVizinhos.index(max(kVizinhos)) == rotulosTestes[i]:
        soma += 1
        print("acertou!")
    else:
        print("...")
    i += 1

print("O percentual de acertos é: {}%".format(100*soma/i))
