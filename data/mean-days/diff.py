import csv

infile = open("districts.csv")
infile_fl = open("districts_fl.csv")
reader = csv.reader(infile)
reader_fl = csv.reader(infile_fl)


districts = [row[0] for row in reader]
districts_fl = [row[0] for row in reader_fl]

del districts[0]
del districts_fl[0]
districts.sort()
districts_fl.sort()

left = []
left_fl = []
for d in districts:
    if d not in districts_fl:
        left.append(d)

for d in districts_fl:
    if d not in districts:
        left_fl.append(d)

outfile = open("left.txt", "w")
outfile_fl = open("left_fl.txt", "w")

outfile.write('\n'.join(left))
outfile_fl.write('\n'.join(left_fl))

"""
print(len(districts))
print(len(districts_fl))

for i in range(10):
    print(districts[i], districts_fl[i])
"""
