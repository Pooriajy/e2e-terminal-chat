import requests
import cruses

scr = cruses.initscr()

scr.noecho()


server = 'http://127.0.0.1:8080/'


r = requests.get(server+"get_messages/")

data = r.content.decode()

data = data.split("\n")
del data[-1]
a = []
for i in data:
    i = i.replace("(","").replace(")","").replace("'","")
    d = i.split(",")
    a.append([d[0],d[1],d[2]])


print(a[0][1])
