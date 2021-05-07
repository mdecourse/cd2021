# open file, default is read mode, since txt content no chinese char
# no encoding = "UTF-8" is needed
import random

# number of group menber to draw
num = 2

# check if data is "" or not
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
    # use mem to count the total number of each group
    mem = 0
    # final group data
    fgroup = []
    # count from the second group member, eliminate the first element
    sgroup = group[1:]
    # get only the odd index number
    igroup = [i for i in range(len(sgroup)) if i % 2 == 1]
    for j in igroup:
        # index starts from 0 which is j-1 when j=1
        if notVacant(sgroup[j-1]) == True:
            mem += 1
            fgroup.append(sgroup[j-1])
    print("group " + str(i+1) + ":" + str(mem))
    # shuffle the fgroup list
    random.shuffle(fgroup)
    # draw num of member from final group list: fgroup
    for k in range(num):
        try:
            print(fgroup[k])
        except:
            # num is greater than total number of this group
            print("no such member")
    # seperator
    print("-"*20)
# the following will use group data to generate needed html