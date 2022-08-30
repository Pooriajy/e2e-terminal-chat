import web
import sqlite3
import json
urls = (
    '/get_messages/','getMessages',
    '/get_last_message/','getLastMessage',
    '/recv/','recv',
    '/(.*)', 'hello'
)
app = web.application(urls, globals())
conn = sqlite3.connect('data.db',check_same_thread=False)
cur = conn.cursor()




class hello:
    def GET(self,name):
        return 'hello '+name


class getLastMessage:
    def GET(self):
        cur.execute("select * from messages order by id DESC LIMIT 1")
        m = cur.fetchone()
        t = {'id':m[0],'sender':m[2],'msg':m[1]}
        return t


class getMessages:
    def GET(self):
        cur.execute("select * from messages")
        s=[]
        msg = cur.fetchall()
        for i in msg:
            s.append({'id':i[0],'sender':i[2],'msg':i[1]})
        return s

class recv:
    def POST(self):
        data = web.data().decode()
        js = json.loads(data)
        cur.execute("select count(*) from messages")
        id = int(cur.fetchone()[0]) + 1

        msg = js['msg']
        sender = js['sender']
        cur.execute("insert into messages values ({0},'{2}','{1}')".format(id,sender,msg))
        conn.commit()

        return '200 OK'






if __name__ == "__main__":
    app.run()
