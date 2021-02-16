# coding: utf-8
import os
import telebot
import mysql.connector
from datetime import date, timedelta
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

sentences = [
    'Me diga as atividades diarias',
    'me diga as atividades mensais',
    'me diga as atividades semanais',
    'eu te amo bot'
]

tokenizer = Tokenizer(num_words = 100, oov_token="<OOV>")
tokenizer.fit_on_texts(sentences)
sequences = tokenizer.texts_to_sequences(sentences)
padded = pad_sequences(sequences)

print(tokenizer.word_index)
print(sequences)

# codigo para o bot do telegram
bot = telebot.TeleBot('1685155091:AAEWDKG2yHaaBu4pMq7imN0IkXqNJMt1k8c')
# bot.send_message(-1001338594601, 'O pai ta on ;) Podem começar a interagir')
# conectando ao banco de dados 
# select * from att where dia_entrega between data_inicio and data_final;

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

def processingData(data):
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

@bot.message_handler(commands=['semanal'])
def get_list_att_week(message):
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
        reply = reply + "Nada, seu viado"
    else:
        reply = reply + "😀"
    bot.send_message(message.chat.id, reply)

@bot.message_handler(commands=['diario'])
def get_list_att(message):
    data_atual = str(date.today())
    print(data_atual)
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
    values = message.text[4:len(message.text)].strip().split(',')
    values[2] = processingData(values[2])
    sql = "INSERT INTO att (nome, pts, dia_entrega) VALUES (%s, %s, %s)"
    val = (values[0], values[1], values[2])
    cursor.execute(sql, val)
    db_connection.commit()
    bot.send_message(message.chat.id, "Atividade adicionada com Sucesso! 😀")

'''
@bot.message_handler()
def send_welcome(message):
    if message.text.upper() == "DA UM JEITO NELA AI BOT":
        bot.send_message(message.chat.id, "Pare de encher o saco de Gabriel, Priscila. Senão você vai ter que dar o cu pra ele! ")

# Essa eh a forma de fazer ele obedecer um comando, precedido por '/' no telegram

@bot.message_handler(commands=['today'])
def send_league_data(message):
    bot.reply_to(message, get_league())
'''

bot.polling()
