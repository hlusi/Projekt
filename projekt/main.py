import os
data = open('data.txt','r')
text = data.read()
file_status = os.stat('data.txt')
print(file_status)
# kontroluju velikost souboru
if file_status.st_size < 1:
    print('Soubor muze byt prazdny')
else: print('zadana data maji spravnou delku')

# konrojulu datovy typ
x = 'dgtjy'
if type(text) == type(x):
   text = text
else:
    text = str(text)

# upravovani delky textu
padded = text + ((16 - len(text) % 16) * chr(16 - len(text) % 16))
print(padded)

#prevod dat do vhodne datove struktury
text_v_bytech = str.encode(padded)

print(text_v_bytech)
print(len(text_v_bytech))









