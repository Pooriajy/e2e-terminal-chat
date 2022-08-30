import curses
import time
import os
import requests
import json
from threading import Thread


scr = curses.initscr()
curses.start_color()
# curses.halfdelay(1)
# curses.noecho()


## pair 9: general text and background
## pair 8: splitters text and background


curses.init_pair(9,curses.COLOR_GREEN,curses.COLOR_BLACK)
curses.init_pair(8,curses.COLOR_WHITE,curses.COLOR_BLACK)
# scr.bkgd(' ',curses.color_pair(9)|curses.A_BOLD)

win1 = curses.newwin(scr.getmaxyx()[0]-20,scr.getmaxyx()[1]-10, 2,13)
win2 = curses.newwin(2,200,scr.getmaxyx()[0]-1,10)
stat_panel = curses.newwin(1,scr.getmaxyx()[1],1,int(scr.getmaxyx()[1]/2)-24)
user_panel = curses.newwin(scr.getmaxyx()[0]-10,11,1,1)
user_spliter_panel = curses.newwin(scr.getmaxyx()[0]-1,1,0,10)
user_horiz_spliter_panel = curses.newwin(1,1000,scr.getmaxyx()[0]-2,10)



stat_panel.addstr("this is a test stat", curses.A_BLINK)
stat_panel.refresh()
win2.addstr("Press Enter to START!",curses.A_COLOR)
win2.getstr()

user_spliter_panel.bkgd(' ',curses.color_pair(8))
user_spliter_panel.addch("#")
user_spliter_panel.refresh()
user_horiz_spliter_panel.bkgd(' ',curses.color_pair(8))
user_horiz_spliter_panel.refresh()
# scr.clear()
scr.refresh()
server = 'http://127.0.0.1:8080'
LastID = 0





def getMsg():
    r = requests.get(server+"/get_messages/").content
    r = r.decode().replace("'",'"')
    try:
        js = json.loads(r)
    except:
        return 0
    return js


def getLastMsg():
    try:
        r = requests.get(server+"/get_last_message/").content
        r = r.decode().replace("'",'"')
        js = json.loads(r)
        return js
    except:
        pass


def updater():
    txtMode = curses.A_NORMAL
    name = "random user"
    while(True):
        c = win2.getstr()
        if(c == b'/q'):
            break
        if c.startswith(b'/txt'):
            mode = c.decode().split(" ")[1]

            if mode == 'bold':
                txtMode = curses.A_BOLD
            elif mode == 'dim':
                txtMode = curses.A_DIM
            elif mode == 'normal':
                txtMode = curses.A_NORMAL

        if c == b'/refresh':
            win1.addstr(str(getMsg()))

        if c.startswith(b'/name'):
            name = c.decode().split(" ")[1]

        else:
            if c !=b'':
                data = {"msg":c.decode(), "sender":name}
                x = requests.post(server+"/recv/",str(json.dumps(data)))
                # win1.addstr("You: ")
                # win1.addstr(c+b"\n",txtMode)

        # win2.refresh()
        # win1.refresh()
        win2.clear()
        win2.addstr(">> ")
        scr.refresh()

def displayer():
    ## get history
    # win1.getch()
    stat_panel.addstr("Connected to the Server!",curses.A_BOLD)
    stat_panel.refresh()

    curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)

    user_panel.addstr("akbar\npooria\nmamad",curses.A_BOLD+curses.color_pair(1))
    user_panel.refresh()


    try:
        for i in range(1,scr.getmaxyx()[0]):
            user_spliter_panel.addstr("|")
            user_spliter_panel.refresh()
    except:
        pass


    try:
        for i in range(1,scr.getmaxyx()[1]):
            user_horiz_spliter_panel.addstr("#")
            user_horiz_spliter_panel.refresh()
    except Exception as e:
        pass

    # try:
    #     for i in range(1,scr.getmaxyx()[0]):
    #         user_horiz_spliter_panel.addstr("#")
    #         user_horiz_spliter_panel.refresh()
    # except:
    #     pass



    s = ""
    LastID = 0
    history = getMsg()
    try:
        for i in history:
            s = s+ i['sender']+": "+i['msg']+"\n"
            LastID = int(i['id'])
    except:
        pass
    win1.addstr(s,curses.color_pair(1)+curses.A_BOLD)
    while(True):
        time.sleep(1)
        js = getLastMsg()
        try:
            if js['id'] > LastID:
                win1.addstr(js['sender'] + ": " + js['msg'] + "\n",curses.color_pair(1)+curses.A_BOLD)
                LastID += 1
            win1.refresh()
        except:
            win1.addstr("No Messages!\n")
            win1.refresh()



t1 = Thread(target=updater)
t2 = Thread(target=displayer)
t2.daemon = True
t2.start()
t1.start()
t1.join()
