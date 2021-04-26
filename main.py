import csv
from urllib.parse import urlparse
lines = []
words = []
words2 = []
with open('csv0.txt', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['url'])
        p=urlparse(row['url']).path
        #print(p)
        x = p.split('/')
        #print(x)
        words.append(x)
        lines.append(p)
for i in words:
    for j in i:
        if j!='':
           words2.append(j)
print(words2,len(words2))
#Remove duplicates using dict.fromkeys()
final_new_word = list(dict.fromkeys(words2))
print(final_new_word,len(final_new_word))
f = open("demofile.txt", "w")
for i in final_new_word:
    f.write(i + " ")
f.close()

