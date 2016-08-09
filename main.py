from slacker import Slacker
from threading import Thread
import time, readline, sys
import struct, fcntl, termios

slack = Slacker('xoxp-9885641827-13134927984-63631444180-69a5d4ffa9')

getMessages = None
sendMessage = None
users = {}

def printMessage(message,user=False):
    if user is False:
        print("\r" + "\033[93m {}\033[00m".format("Me: ") + message)
    else:
        print("\r" + "\033[91m {}\033[00m".format(user+": ") + message)

def initReadWrite():
    global slack, getMessages, sendMessage, users

    channelRaw = slack.channels.list().body['channels']
    channels = [x for x in channelRaw if x['is_archived'] == False]

    groupRaw = slack.groups.list().body['groups']
    groups = [x for x in groupRaw if x['is_archived'] == False and "mpdm-" not in x['name']]

    me = slack.users.profile.get().body['profile']
    userRaw = slack.users.list().body['members']
    for user in userRaw:
        if 'real_name' in user:
            if me['real_name'] == user['real_name']:
                users[user['id']] = False
            else:
                users[user['id']] = user['real_name']

    for channel in channels:
        if channel['name'] == sys.argv[1]:
            correctChannel = channel['id']
            getMessages = lambda x: slack.channels.history(correctChannel,oldest=x).body['messages']
            sendMessage = lambda x: slack.chat.post_message(correctChannel,x,as_user=True)

    for group in groups:
        if group['name'] == sys.argv[1]:
            correctGroup = group['id']
            getMessages = lambda x: slack.groups.history(correctGroup,oldest=x).body['messages']
            sendMessage = lambda x: slack.chat.post_message(correctGroup,x,as_user=True)

    imChannels = slack.im.list().body['ims']
    for channel in imChannels:
        for user in userRaw:
            if user['id'] == channel['user'] and user['name'] == sys.argv[1]:
                correctIM = channel['id']
                getMessages = lambda x: slack.im.history(correctIM,oldest=x).body['messages']
                sendMessage = lambda x: slack.chat.post_message(correctIM,x,as_user=True)

    if sendMessage == None:
        for channel in imChannels:
            for user in userRaw:
                if user['id'] == channel['user']:
                    if 'real_name' in user and user['real_name'] != "":
                        print(user['name'] + " <" + user['real_name'] + ">")
                    else:
                        print(user['name'])
        for channel in channels:
            print(channel['name'])
        for group in groups:
            print(group['name'])

        return False

    return True

if not initReadWrite():
    sys.exit()

lastRead = None

def printMessages(messages, printMe=False):
    global lastRead
    for message in reversed(messages):
        if not 'subtype' in message:
            if users[message['user']] == False:
                if printMe:
                    printMessage(message['text'],False)
            else:
                printMessage(message['text'],users[message['user']])
        lastRead = message['ts']

def updateThread():
    while True:
        (rows,cols) = struct.unpack('hh', fcntl.ioctl(sys.stdout, termios.TIOCGWINSZ,'1234'))

        text_len = len(readline.get_line_buffer())+2

        sys.stdout.write('\x1b[2K')
        sys.stdout.write('\x1b[1A\x1b[2K'*int(text_len/cols))
        sys.stdout.write('\x1b[0G')

        printMessages(getMessages(lastRead))
        sys.stdout.write("\033[93m {}\033[00m".format("Me: ") + readline.get_line_buffer())
        sys.stdout.flush()
        time.sleep(0.5)

printMessages(getMessages(0), printMe=True)
thread = Thread(target=updateThread)
thread.start()

def transformMsg(message):
    temp = message

    temp = temp.replace(":shrug:","¯\_(ツ)_/¯")

    return temp

while True:
    message = input()

    message = transformMsg(message)

    if len(message) > 0:
        sendMessage(message)
