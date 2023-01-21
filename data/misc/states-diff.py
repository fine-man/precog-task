import csv

infile = open("states.csv")
infile_fl = open("states_fl.csv")
reader = csv.reader(infile)
reader_fl = csv.reader(infile_fl)


states = [row[0] for row in reader]
states_fl = [row[0] for row in reader_fl]

del states[0]
del states_fl[0]
states.sort()
states_fl.sort()

left = []
left_fl = []
for d in states:
    if d not in states_fl:
        left.append(d)

for d in states_fl:
    if d not in states:
        left_fl.append(d)

outfile = open("state_left.txt", "w")
outfile_fl = open("state_left_fl.txt", "w")

outfile.write('\n'.join(left))
outfile_fl.write('\n'.join(left_fl))

"""
print(len(states))
print(len(states_fl))

for i in range(10):
    print(states[i], states_fl[i])
"""
