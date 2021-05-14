# stage3_gen_html.py
studList = "stage3_2a.txt"
courTitle = "cd2021"

# group title initial
grpTitle = studList[:6] + "-" + studList[8] + "g"

# student Account and github Account as inputs
def perWeb(s, g):
    pSite = "<a href=\"https://" + g + ".github.io/" + courTitle + "\">" + s + " web</a>"
    print(pSite)

def perRepo(s, g):
    pSite = "<a href=\"https://github.com/" + g + "/" + courTitle + "\">" + s + " repo</a>"
    print(pSite)
    
def grpWeb(s, g, ord):
    pSite = "<a href=\"https://" + g + ".github.io/" + grpTitle + str(ord) + "\">grp web</a>"
    print(pSite)
    
def grpRepo(s, g, ord):
    pSite = "<a href=\"https://github.com/" + g + "/" + grpTitle + str(ord) + "\">grp repo</a>"
    print(pSite)

# open file, default is read mode, since txt content no chinese char
# no encoding = "UTF-8" is needed
with open(studList) as fh:
    # readlines will read into the whole line and put into list format
    # has \n at the end of each line
    data = fh.readlines()

grpCount = 0
for i in range(len(data)):
    # grpCount is the group order
    grpCount = grpCount + 1
    group = data[i].rstrip("\n").split("\t")
    # use filter to remove vacant string element
    # use [1:] to remove first element
    group = list(filter(None, group))[1:]
    print(grpTitle + str(grpCount) + "<br />")
    for j in range(0, len(group), 2):
        # s is the student number
        s = group[j]
        # g is the github account
        g = group[j+1]
        perWeb(s, g)
        print("|")
        perRepo(s, g)
        print("|")
        grpWeb(s, g, grpCount)
        print("|")
        grpRepo(s, g, grpCount)
        print("<br />")