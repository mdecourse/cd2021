# open file, default is read mode, since txt content no chinese char
# no encoding = "UTF-8" is needed
import random

# draw number of group member
num = 2

def notVacant(data):
    if data == "":
        return False
    else:
        return True
        
with open("stage3_2a.txt") as fh:
    # readlines will read into the whole line and put into list format
    # has \n at the end of each line
    data = fh.readlines()
#print(len(data))
# big group list
bgroup = []
# count from the second group member
sgroup = []
for i in range(len(data)):
    group = data[i].rstrip("\n").split("\t")
    #print(group)
    mem = 0
    # final group data
    fgroup = []
    # count from the second group member
    sgroup = group[1:]
    # get only the odd index number
    igroup = [i for i in range(len(sgroup)) if i % 2 == 1]
    for j in igroup:
        if notVacant(sgroup[j-1]) == True:
            mem += 1
            fgroup.append(sgroup[j-1])
    print("group " + str(i+1) + ":" + str(mem))
    # shuffle the fgroup list
    random.shuffle(fgroup)
    for k in range(2):
        print(fgroup[k])
    print("-"*20)
# the following will use group data to generate needed html