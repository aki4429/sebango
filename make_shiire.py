import csv

bango=[]
shiire={} #仕入れコードとidの辞書
result =[]

with open('bango.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        bango.append(row)

with open('shiire.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        shiire[row[1]]=row[0]


for ba in bango:
    if ba[3] in shiire:
        s_id = shiire[ba[3]]
    else:
        s_id = ''
    
    result.append([ba[0], ba[1], ba[2], s_id])

with open('result.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(result)

