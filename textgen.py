from RNN2 import  VOCABULARY, model, SEQ_LENGTH, char_to_int
import numpy as np

original_text = []
predicted_text = []



def handle_submit():
    global predicted_text
    global original_text

    inp = list(text)

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
        next_word.append(chr[index])
        inp_text.append(index)
        inp_text = inp_text[1:]
        next_char = chr[index]

    predicted_text = predicted_text + [''.join(next_word)]
    print(" " + ''.join(next_word), end='|')

text = '.KH'

text.on_submit(handle_submit())
#handle_submit
from tabulate import tabulate

original_text = original_text.split()
predicted_text.insert(0,"")
predicted_text.pop()

table = []
for i in range(len(original_text)):
    table.append([original_text[i], predicted_text[i]])
print(tabulate(table, headers = ['Actual Word', 'Predicted Word']))