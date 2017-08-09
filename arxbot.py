from lib import arx
import subprocess

my_token = "401765530:AAHFC0qWJLre7c5iJGWT1T6PykJrDk7FGZM"
chat_id = "-1001132498844"

arx.check_for_new("log", "list", "for_bot")

def send_to_bot(chat, token, message):
    st = "curl --data \"chat_id=" + chat + "&text=" + message + "\" https://api.telegram.org/bot" + token + "/sendMessage"
    result = subprocess.check_output([st], shell = True).split(",")
    if result[0] == "{\"ok\":true":
        return True
    else:
        return False

def post_new(file):
    try: 
        query = open(file, "r")
        qs = query.readlines()
        query.close()
    except:
        print "No log yet."
        return 0

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
