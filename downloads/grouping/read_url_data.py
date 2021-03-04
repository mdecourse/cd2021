#https://nfulist.herokuapp.com/?semester=1092&courseno=0764&column=True
'''
2021 spring:
0741 1a
0764 2a
0776 2b
2384 5j
'''
# for read data from url
import urllib.request
# for execution through proxy
import os
# for converting 2d list into 1d
from itertools import chain 
 
proxy = 'http://[2001:288:6004:17::69]:3128'
 
os.environ['http_proxy'] = proxy 
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy

# read data from url
with urllib.request.urlopen('https://nfulist.herokuapp.com/?semester=1092&courseno=0776&column=True') as response:
   html = response.read().decode('utf-8')

# split data with "</br>" into list, up to here we get the student list of the cd2021 2a
Udata = html.split("</br>")
#print("total:" + str(len(Udata)))

# set group as vacent list
group = []
# open w2_a_list.txt which copied from http://c.kmol.info:8000/o616appencye at 2021/03/04 15:00
with open("w2_b_list.txt") as file: 
    content = file.readlines()
for i in range(len(content)):
    data = content[i].rstrip("\n").split("\t")
    group.append(data)
#print(group)

# converting 2d list into 1d 
# using chain.from_iterables 
flatten_group= list(chain.from_iterable(group)) 
for stud in Udata:
    if stud not in flatten_group:
        print(stud)


