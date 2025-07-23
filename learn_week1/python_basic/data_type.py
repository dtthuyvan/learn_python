x = 10
y=9.0
print(x+y)

print(2+2*2**2)

print(type('9.0'))

print(19//3)

print(18 % 3, 15 / 3, 16 // 3, 2 ** 3)

x = 4567_898_765_456
print(x)
print(x+1)

print(id(x))

name = 'Alice'
id1 = id(name)
name = 'Emma'
id2 = id(name)
print(id1==id2)

x = 12
id1 = id(x)
x += 5
id2 = id(x)
print(id1 == id2)

l1 = [3, 6]
id1 = id(l1)
l1.append(9)
id2 = id(l1)
print(id1 == id2)

my_string = 'GenAI'
#my_string[0] = 'X'
print(my_string[0])

tech = 'MachineLearning'
print(tech[0:7])

a, b = '1', '2'
print(a + b * 3)

#string[start:stop:step]
print('Python 3!!!'[:7:2])
mac = 'b4:6d:83:77:85:f3'
print(mac[-1] + mac[:2])

text = "AI will shape the future!"
print(text.upper())

print('$300 $400 $200'.count('$'))

buzzwords = ['Deep Learning', 'Neural Networks', 'Generative AI']
result = ' | '.join(buzzwords)
print(result)

filename = "research_paper_v1.docx"
cleaned_filename = filename.removesuffix(".docx")
print(cleaned_filename)

text = 'Python is awesome'
print(text.split())