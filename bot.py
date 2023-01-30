# coding: utf-8
import numpy as np
import telebot
import mysql.connector
from datetime import date, timedelta
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import json

# variaveis globais
sentences = []
labels = []
datastore = []

tokenizer = Tokenizer()
max_length = 7
vocab_size = 20

num_epochs = 100

# funcoes
def loadDataset():

    with open('dataset.json', 'r') as f:
        datastore = json.load(f)

    # iterando no json e obtendo as informações
    for item in datastore:
        sentences.append(item['frase'])
        labels.append(item['label'])

def sepDataset(limit):
    training_sentences = np.array(sentences[:limit])
    training_labels = np.array(labels[:limit])
    testing_sentences = np.array(sentences[limit:])
    testing_labels = np.array(labels[limit:])
    
    return training_sentences, training_labels, testing_sentences, testing_labels

def tokenizerWords(training_sentences, training_labels, testing_sentences, testing_labels):
    tokenizer = Tokenizer(num_words = vocab_size, oov_token="<OOV>")
    tokenizer.fit_on_texts(training_sentences)
    training_sentences = tokenizer.texts_to_sequences(training_sentences)
    padding_training = pad_sequences(training_sentences)
    
    testing_sentences = tokenizer.texts_to_sequences(testing_sentences)
    padding_testing = pad_sequences(testing_sentences)

    return padding_training, padding_testing

def neuralNetwork(padding_training, training_labels, padding_testing, testing_labels):
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(vocab_size, 2, input_length=max_length),
        tf.keras.layers.GlobalAveragePooling1D(),
        tf.keras.layers.Dense(24, activation="relu"),
        tf.keras.layers.Dense(3, activation="relu")
    ])

    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=['accuracy'])

    history = model.fit(padding_training, training_labels, epochs=num_epochs,
            validation_data=(padding_testing, testing_labels), verbose=2)

    return model

def processingData(data):
    '''
    Funcao para ajustar o formato da data
    para o aceito pelo MySQL
    '''

    value = data.strip().split('/')
    #dia
    if len(value[0]) == 1:
        value[0] = "0" + value[0]
    #mes
    if len(value[1]) == 1:
        value[1] = "0" + value[1]
    #ano
    if len(value[2]) == 2:
        value[2] = "20" + value[2]
        
    return value[2] + '-' + value[1] + '-' + value[0]

# codigo para o bot do telegram
bot = telebot.TeleBot('1685155091:AAEWDKG2yHaaBu4pMq7imN0IkXqNJMt1k8c')

@bot.message_handler(commands=['semanal'])
def get_list_att_week(message):
    '''
    funcao para pegar as atividades do banco de dados 
    registradas para a semanal atual
    '''
    data_atual = str(date.today())
    data_semana = str((date.today()) + timedelta(days=7))
    sql = "SELECT * FROM att WHERE dia_entrega BETWEEN '" + data_atual + "' AND '" + data_semana + "';"
    cursor.execute(sql)
    reply = "Ola, " + message.from_user.first_name + ". Deixe-me ver..."
    bot.reply_to(message, reply)
    reply = "Achei! Para essa semana, temos:\n"
    
    i = 1
    for (nome, pts, dia_entrega) in cursor:
        reply = reply + str(i) + ' - ' + str(nome) + ", valendo " + str(pts) + " pontos;\n"
        i += 1
    if i == 1:
        reply = reply + "Nada"
    else:
        reply = reply + "😀"
    bot.send_message(message.chat.id, reply)

@bot.message_handler(commands=['diario'])
def get_list_att(message):
    '''
    funcao para pegar as atividades do banco de dados 
    registradas para hoje
    '''
    data_atual = str(date.today())
    sql = "SELECT * FROM att WHERE dia_entrega='" + data_atual + "';"
    cursor.execute(sql)
    reply = "Ola, " + message.from_user.first_name + ". Deixe-me ver..."
    bot.reply_to(message, reply)
    reply = "Achei! Para hoje, temos:\n"
    
    i = 1
    for (nome, pts, dia_entrega) in cursor:
        reply = reply + str(i) + ' - ' + str(nome) + ", valendo " + str(pts) + " pontos;\n"
        i += 1
    if i == 1:
        reply = "Aquieta o cu na cadeira e vai ler um livro que hoje o dia tá livre"
    bot.send_message(message.chat.id, reply)

@bot.message_handler(commands=['add'])
def send_welcome(message):
    '''
    funcao para adicionar no banco de dados
    uma atividade
    '''
    values = message.text[4:len(message.text)].strip().split(',')
    values[2] = processingData(values[2])
    sql = "INSERT INTO att (nome, pts, dia_entrega) VALUES (%s, %s, %s)"
    val = (values[0], values[1], values[2])
    cursor.execute(sql, val)
    db_connection.commit()
    bot.send_message(message.chat.id, "Atividade adicionada com Sucesso! 😀")

try:
	db_connection = mysql.connector.connect(host='localhost', user='root', password='143867', database='ifba')
except mysql.connector.Error as error:
	if error.errno == errorcode.ER_BAD_DB_ERROR:
		print("Database doesn't exist")
	elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("User name or password is wrong")
	else:
		print(error)

cursor = db_connection.cursor()

if __name__ == "__main__":
    # carrega o dataset 
    loadDataset()
    # separa partes para treino e teste
    train_s, train_l, test_s, test_l = sepDataset(limit=11)
    # cria tokens para as palavras e sequencias, para poder
    # usar na rede neural
    pad_train, pad_test = tokenizerWords(train_s, train_l, test_s, test_l)
    neuralNetwork(pad_train, train_l, pad_test, test_l)

    bot.polling()
