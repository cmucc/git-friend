# by cpreseau
# with starter code copied from
# http://wiki.shellium.org/w/Writing_an_IRC_bot_in_Python
# complete with far too many comments

# Import some necessary libraries.
import socket 

# Some basic variables used to configure the bot	
server = "irc.freenode.net" # Server
channel = "##git-friend-private-channel-do-not-join" # Channel
botnick = "cclub-git-friend" # Your bots nick
hostname = "club.cc.cmu.edu"

# This part is actually specific to git-friend
import os
# This part is actually specific to git-friend and important!!
import subprocess

# 0 means uninitialized, +1 for each state from there
def get_state(nick):
    if not os.path.exists("./" + nick + "/state"):
        return 0;

    f = open("./" + nick + "/state", "r")
    state = f.read(5)
    return int(state)

def set_state(state, nick):
    subprocess.call(["mkdir","-p",nick])
    f = open("./" + nick + "/state", "w")
    f.write(str(state))

def message_callback(nick, channel, msg):
    state = get_state(nick)
    if (state == 0):
        send_msg(nick, "Hello, friend! Let's get our group project done!")
        send_msg(nick, "You should start by making a bare repo for us.")
        send_msg(nick, "Just give me the file path.")
        send_msg(nick, "BTW, my username is git-friend@club.cc.cmu.edu")
        set_state(1, nick)
    elif (state == 1):
        msg = msg.strip()
        print(msg)
        if (os.path.isdir(msg) and subprocess.call(["git","clone",msg,nick + "/repo/"]) == 0):
            send_msg(nick, "Thanks! Could you also make an initial commit with a .gitignore?")
            set_state(2, nick)
        else:
            send_msg(nick, "Uh, that doesn't look right...")
            send_msg(nick, "Are you sure you set the afs permission right?")
            send_msg(nick, "My user name is git-friend@club.cc.cmu.edu")
            send_msg(nick, "Also remember to give me the full path, ie. /afs/andrew.cmu.edu/...")
            send_msg(nick, "If your client interprets anything beginning with a '/' as a command, try prefixing it with a space")
    elif (state == 2):
        d = nick + "/repo"
        subprocess.call(["git","pull"],cwd=d)
        if os.path.exists(nick + "/repo/.gitignore"):
            send_msg(nick, "Great! I'll push what I have so far.")
            subprocess.call(["cp","../speedy_sort.py",d])

            subprocess.call(["git","add","speedy_sort.py"],cwd=d)
            subprocess.call(["git","commit","-m","Added SpeedySort. You do the rest."],cwd=d)
            if subprocess.call(["git","push"],cwd=d) == 0:
                set_state(3, nick)
            else:
                send_msg(nick, "Uh... are you sure I have write permissions?")
        else:
            send_msg(nick, "Uh, I don't see a .gitignore in there?")

    elif (state == 3):
        send_msg(nick, "I think I've already completed my part of this project.")
        send_msg(nick, "You should do the rest")
        set_state(4, nick)

    elif (state == 4):
        send_msg(nick, "Stop talking to me and finish our homework. It's due soon!")

# send a private message
def send_msg(nick, msg):
    ircsock.send("PRIVMSG " + nick + " :" + msg + "\n")

def ping(): # This is our first function! It will respond to server Pings.
	ircsock.send("PONG :pingis\n")	

def sendmsg(chan , msg): # This is the send message function, it simply sends messages to the channel.
	ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n") 

def joinchan(chan): # This function is used to join channels.
	ircsock.send("JOIN "+ chan +"\n")

			
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667)) # Here we connect to the server using the port 6667
ircsock.send("user " + botnick + " " + hostname + " " +  hostname + " " +  hostname + "\n")
ircsock.send("NICK "+ botnick +"\n") # here we actually assign the nick to the bot

joinchan(channel) # Join the channel using the functions we previously defined

while 1: # Be careful with these! it might send you to an infinite loop
	ircmsg = ircsock.recv(2048) # receive data from the server
	ircmsg = ircmsg.strip('\n\r') # removing any unnecessary linebreaks.
	print(ircmsg) # Here we print what's coming from the server

	if ircmsg.find(' PRIVMSG ')!=-1:
		nick = ircmsg.split('!')[0][1:]
		channel = ircmsg.split(' PRIVMSG ')[-1].split(' :')[0]
                msg = ircmsg[ircmsg.rfind(":") + 1:]
		message_callback(nick,channel,msg)

	elif ircmsg.find("PING :") != -1: # if the server pings us then we've got to respond!
		ping()
