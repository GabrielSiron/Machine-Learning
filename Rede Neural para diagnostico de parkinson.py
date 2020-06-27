from sklearn.neural_network import MLPClassifier
import numpy as np

'''
Esse programa implementa, atraves da biblioteca
sklearn uma aplicacao de Machine Learning  com 
Redes Neurais para diagnostico de parkinson
'''

# o link para download: https://archive.ics.uci.edu/ml/datasets/Parkinsons
dataset = open('C:\\Users\\Sironz\\Desktop\\Rede Neural Hello World\\parkinson.txt', 'r')

dados = []

#tratando os dados para ficarem utilizaveis

for linha in dataset:
    linha = linha.split(',')
    linha.pop(0) #removo essa posicao pois representa a identificacao do paciente (inutil para a classificacao)
    linha = [float(i) for i in linha]
        
    dados.append(linha)

np.random.shuffle(dados)
pctTeste = 70 / 100  # 0.7

dadosTeste = dados[:int(pctTeste * len(dados))]
dadosTreino = dados[int(pctTeste * len(dados)):]

rotulosTeste = []
for teste in dadosTeste:
    rotulosTeste.append(teste.pop(-7))

rotulosTreino = []
for treino in dadosTreino:
    rotulosTreino.append(treino.pop(-7))

# modifique os hiperparametros da rede se necessario
redeNeural = MLPClassifier(solver='adam',
                           alpha=1e-2,
                           hidden_layer_sizes=(20, 12),
                           random_state=1,
                           max_iter=500)

redeNeural.fit(dadosTreino, rotulosTreino)

saidaTeste = redeNeural.predict(dadosTeste)

acertos, total = 0, 0

for i in range(len(saidaTeste)):
    if saidaTeste[i] == rotulosTeste[i]:
        acertos += 1
        print("Acertou!")
    else:
        print("...")
    total += 1

print("O percentual de acertos foi: {}".format(100*acertos/total))
