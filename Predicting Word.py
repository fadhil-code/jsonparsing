import keras
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Activation
from keras.optimizers import RMSprop, Adam
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils


def buildmodel(VOCABULARY):
    model = Sequential()
    model.add(LSTM(256, input_shape=(SEQ_LENGTH, 1), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(256))
    model.add(Dropout(0.2))
    model.add(Dense(VOCABULARY, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    return model


import numpy as np

file = open('saved_models2/1filttered.txt', encoding='utf8')
raw_text = file.read()  # you need to read further characters as well
raw_text = raw_text.lower()
SEQ_LENGTH = 100

chars = sorted(list(set(raw_text)))
print(chars)
bad_chars = ['#', '*', '@', '_', '\ufeff']
for i in range(len(bad_chars)):
    raw_text = raw_text.replace(bad_chars[i], "")

chars = sorted(list(set(raw_text)))
print(chars)

text_length = len(raw_text)
char_length = len(chars)
VOCABULARY = char_length
print("Text length = " + str(text_length))
print("No. of characters = " + str(char_length))

char_to_int = dict((c, i) for i, c in enumerate(chars))

int_to_char = dict((i, c) for i, c in enumerate(chars))

filename = 'saved_models2/weights-improvement-31-2.0081.hdf5'
model = buildmodel(VOCABULARY)
model.load_weights(filename)
model.compile(loss='categorical_crossentropy', optimizer='adam')

original_text = []
predicted_text = []
import ipywidgets as widgets

text = widgets.Text()
display(text)


def handle_submit(sender):
    global predicted_text
    global original_text

    inp = list(text.value)

    last_word = inp[len(original_text):]
    inp = inp[:len(original_text)]
    original_text = text.value
    last_word.append(' ')

    inp_text = [char_to_int[c] for c in inp]
    last_word = [char_to_int[c] for c in last_word]

    if len(inp_text) > 100:
        inp_text = inp_text[len(inp_text) - 100:]
    if len(inp_text) < 100:
        pad = []
        space = char_to_int[' ']
        pad = [space for i in range(100 - len(inp_text))]
        inp_text = pad + inp_text

    while len(last_word) > 0:
        X = np.reshape(inp_text, (1, SEQ_LENGTH, 1))
        next_char = model.predict(X / float(VOCABULARY))
        inp_text.append(last_word[0])
        inp_text = inp_text[1:]
        last_word.pop(0)

    next_word = []
    next_char = ':'
    while next_char != ' ':
        X = np.reshape(inp_text, (1, SEQ_LENGTH, 1))
        next_char = model.predict(X / float(VOCABULARY))
        index = np.argmax(next_char)
        next_word.append(int_to_char[index])
        inp_text.append(index)
        inp_text = inp_text[1:]
        next_char = int_to_char[index]

    predicted_text = predicted_text + [''.join(next_word)]
    print(" " + ''.join(next_word), end='|')


text.on_submit(handle_submit)



from tabulate import tabulate

original_text = original_text.split()
predicted_text.insert(0,"")
predicted_text.pop()

table = []
for i in range(len(original_text)):
    table.append([original_text[i], predicted_text[i]])
print(tabulate(table, headers = ['Actual Word', 'Predicted Word']))