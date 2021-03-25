import csv

selist=[]
with open('se.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        selist.append(row)

shilist=[]
with open('shiire.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        shilist.append(row)

for se in selist:
    for shi in shilist:
        if se[3] == shi[1]:
            se[3] = shi[0]

#print(selist)

with open('se_switch.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(selist)

print('se_switch.csv を書きました')
