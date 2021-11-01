#!/usr/bin/python3

fileName = "norm_class_rate2.csv"

label_list = []

class_file = open(fileName, "r")
for line in class_file:
    line = line.strip().split(',')
    label_list.append(line)



#break new line
size = len(label_list)
print('{')
print('\"undefined\": 0.5,')
last_size = size - 1
for x in label_list[:last_size]:
    print('\"' + x[0] + '\" :' + x[1] + ',')

print('\"' + label_list[last_size][0] + '\" :' + label_list[last_size][1] )

print('}')
