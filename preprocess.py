import numpy as np

def readFile(filename):
    file = open(filename,"r")
    first_line = file.readline()
    first_line = first_line.split(' ')
    [rows, cols, minf , maxf] = first_line
    rows = int(rows)
    cols = int(cols)
    minf = int(minf)
    maxf = int(maxf)
    lines =  file.readlines()
    array = []
    for i in range(rows):
        array.append([])

    cnt = 0
    for obj in lines:
        line = obj.strip()
        for c in line:
            array[cnt].append(c)
        cnt = cnt + 1
    matrix = np.array(array)
    return (minf,maxf,matrix)
