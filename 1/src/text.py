d1 = []
with open("predInfo3.5.txt", 'r', encoding='utf8') as f:
    d1 = f.readlines()
d2 = []
with open("predInfo3.0.txt", 'r', encoding='utf8') as f:
    d2 = f.readlines()
d3 = []
with open("predInfoT3.0.txt", 'r', encoding='utf8') as f:
    d3 = f.readlines()
d4 = []
with open("predInfoT3.5.txt", 'r', encoding='utf8') as f:
    d4 = f.readlines()

with open("merged.txt", 'w', encoding='utf8') as f:
    for i in range(d1.__len__()):
        f.write("\n")
        f.write("p:3.5  t:0: " + d1[i])
        f.write("p:3.0  t:0: " + d2[i])
        f.write("p:3.5  t:1: " + d3[i])
        f.write("p:3.0  t:1: " + d4[i])
