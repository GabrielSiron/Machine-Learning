import json
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
# abrindo o arquivo json
with open('Sarcasm_Headlines_Dataset.json', 'r') as f:
    datastore = json.load(f)

sentences = []
labels = []
urls = []

# iterando no json e obtendo as informações
for item in datastore:
    sentences.append(item['headline'])
    labels.append(item['is_sarcastic'])
    urls.append(item['article_link'])

# preprocessando o dataset e definindo o conjunto
# de treino e de teste
training_size = 20000
sentences_training = np.array(sentences[0:training_size])
sentences_test = np.array(sentences[training_size:])
labels_training = np.array(labels[0:training_size])
labels_test = np.array(labels[training_size:])

vocab_size = 2000
max_length = 10
# criando o tokenizer e definindo os dados para teste
# (isolando os dados de treino para verificaçao de acurácia)
tokenizer = Tokenizer(num_words = vocab_size, oov_token="<OOV>")
tokenizer.fit_on_texts(sentences_training)
sentences_training = tokenizer.texts_to_sequences(sentences_training)
training_padded = pad_sequences(sentences_training, maxlen=max_length)

# criando o tokenizer para o conjunto de teste
sentences_test = tokenizer.texts_to_sequences(sentences_test)
test_padded = pad_sequences(sentences_test, maxlen=max_length)

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, 2, input_length=max_length),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(24, activation="relu"),
    tf.keras.layers.Dense(1, activation="sigmoid")
])

model.compile(loss="binary_crossentropy", optimizer="adam", metrics=['accuracy'])

num_epochs = 30

history = model.fit(training_padded, labels_training, epochs=num_epochs,
            validation_data=(test_padded, labels_test), verbose=2)

sentences = [
    "I wish you good luck on that",
    "i believe you because i love you"
]

sequences = tokenizer.texts_to_sequences(sentences)

padded = pad_sequences(sequences, maxlen=max_length)

print(model.predict(padded))