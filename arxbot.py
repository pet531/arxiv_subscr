#This is to post new abstracts to telegram. 

from lib import arx
import subprocess

#SPECIFY YOUR TOKEN AND CHAT HERE
my_token = "your bot's token"
chat_id = "id of the chat you want to post stuff too"

arx.check_for_new("log", "list", "for_bot")

def send_to_bot(chat, token, message):
    st = "curl --data \"chat_id=" + chat + "&text=" + message + "\" https://api.telegram.org/bot" + token + "/sendMessage"
    result = subprocess.check_output([st], shell = True).split(",")
    if result[0] == "{\"ok\":true":
        return True
    else:
        return False

def post_new(file):
    query = open(file, "r")
    qs = query.readlines()
    query.close()
    t = ""
    failed = []
    for x in qs:
        if x.strip() == "$":

            if send_to_bot(chat_id, my_token, t) == False:
                failed.append(t)
                failed.append("$")
            t = ""

        else:
            t = t + x
    query = open(file, "w")
    for x in failed:
        query.write(x.strip())
        query.write("\n")

post_new("for_bot")
