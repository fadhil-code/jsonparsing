import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import csv
from urllib.parse import urlparse

words2 = []

window = tk.Tk()
window.title("Python Tkinter Text Box")
window.minsize(600,400)
def readDataset():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )
    filename = fd.askopenfilename(
        title='Open a file',
        filetypes=filetypes)
    #name= fd.askopenfilename()
    label2 = ttk.Label(window, text ="")
    label2.config(text=filename)
    label2.grid(column = 0, row = 3)
    lines = []
    words = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            p=urlparse(row['url']).path
            x = p.split('/')
            words.append(x)
            lines.append(p)
    for i in words:
            for j in i:
                if j!='':
                   words2.append(j)
    final_new_word = list(dict.fromkeys(words2))
    #print(final_new_word,len(final_new_word))
    str2="The dataset filtered...there is "   + str(len(words2)) + " Words"
    label2.config(text=str2)
    label2.grid(column = 0, row = 3)

def save_file():
    final_new_word = []
    final_new_word = list(dict.fromkeys(words2))
    f = fd.asksaveasfile(mode='w', defaultextension=".txt")
    for i in final_new_word:
            f.write(i + " ")       # add whitespace between missions, per the Creating Missions guidelines
            print(i)
    f.close()
    str2="File saved on " +  str(f.name)   +" with ("+ str(len(final_new_word)) + ") Words"
    label3 = ttk.Label(window, text =str2)
    label3.grid(column = 0, row = 5)


label = ttk.Label(window, text = "Enter the path of dataset file and it should be txt file")
label.grid(column = 0, row = 0)
button = ttk.Button(window, text = "Browse", command = readDataset)
button.grid(column= 0, row = 2)

button = ttk.Button(window, text = "Save", command = save_file)
button.grid(column= 0, row = 4)



import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Activation
from keras.optimizers import RMSprop, Adam
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
SEQ_LENGTH = 100
def buildmodel(VOCABULARY):
    model = Sequential()
    model.add(LSTM(256, input_shape = (SEQ_LENGTH, 1), return_sequences = True))
    model.add(Dropout(0.2))
    model.add(LSTM(256))
    model.add(Dropout(0.2))
    model.add(Dense(VOCABULARY, activation = 'softmax'))
    model.compile(loss = 'categorical_crossentropy', optimizer = 'adam')
    return model

def readTXTfile():
    TXTfilelabel2 = ttk.Label(window, text="Please wait while the training process is completed...")
    TXTfilelabel2.grid(column=0, row=9)
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )
    filename = fd.askopenfilename(
        title='Open a file',
        filetypes=filetypes)
    #name= fd.askopenfilename()


    file = open(filename, encoding='utf8')
    raw_text = file.read()
    raw_text = raw_text.lower()
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
    TL=("Text length = " + str(text_length))
    NOCH=("No. of characters = " + str(char_length))

    char_to_int = dict((c, i) for i, c in enumerate(chars))
    input_strings = []
    output_strings = []

    for i in range(len(raw_text) - SEQ_LENGTH):
        X_text = raw_text[i: i + SEQ_LENGTH]
        X = [char_to_int[char] for char in X_text]
        input_strings.append(X)
        Y = raw_text[i + SEQ_LENGTH]
        output_strings.append(char_to_int[Y])

    length = len(input_strings)
    input_strings = np.array(input_strings)
    input_strings = np.reshape(input_strings, (input_strings.shape[0], input_strings.shape[1], 1))
    input_strings = input_strings / float(VOCABULARY)

    output_strings = np.array(output_strings)
    output_strings = np_utils.to_categorical(output_strings)
    print(input_strings.shape)
    print(output_strings.shape)

    model = buildmodel(VOCABULARY)
    folder= fd.askdirectory()
    filepath = str(folder) + "/weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
    checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
    callbacks_list = [checkpoint]

    history = model.fit(input_strings, output_strings, epochs=50, batch_size=128, callbacks=callbacks_list)

    str2="The dataset readed...there is  " + TL + " and " + NOCH
    TXTfilelabel2.config(text=str2)
    TXTfilelabel2.grid(column = 0, row = 9)

    TXTfilelabel3 = ttk.Label(window, text=input_strings.shape)
    TXTfilelabel3.grid(column=0, row=10)
    TXTfilelabel4 = ttk.Label(window, text=output_strings.shape)
    TXTfilelabel4.grid(column=0, row=11)

    TXTfilelabel4 = ttk.Label(window, text="The training is finished you can find the files on: " + str(folder))
    TXTfilelabel4.grid(column=0, row=12)


buildmodellabel = ttk.Label(window, text = "Load the text file to entered as Input in RNN")
buildmodellabel.grid(column = 0, row = 7)

button = ttk.Button(window, text = "Browse", command = readTXTfile)
button.grid(column= 0, row = 8)






window.mainloop()
