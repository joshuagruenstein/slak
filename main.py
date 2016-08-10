import slacker
from threading import Thread
import time, sys

import flags, net, term, util

authToken = util.getToken()
slack = slacker.Slacker(authToken)

if sys.argv[1] == "-h":
    flags.help()
elif sys.argv[1] == "-u":
    flags.update()
elif sys.argv[1] == "-p":
    if len(sys.argv) < 3:
        print("No presence provided.")
        sys.exit()
    flags.presence(slack, sys.argv[2])
else:
    net.initFields(slack)

if sys.argv[1] == "-l":
    flags.list(sys.argv, net.channels, net.groups, net.imChannels,
               slack.users.list().body['members'])
elif sys.argv[1] == "-n":
    flags.unread(slack,slacker.BaseAPI(token=authToken),
                 net.channels,net.groups,net.imChannels,net.users)

net.initReadWrite(slack,sys.argv[1])

if not net.sendMessage:
    print("Invalid input. Get help with \"slak -h\".")
    sys.exit()

lastRead = 0

def updateThread():
    global lastRead

    while True:
        term.resetTermLine()

        val = term.printMessages(net.getMessages(lastRead), net.users, printMe=(lastRead==0))
        if val != None: lastRead = val

        term.resetPrompt()
        time.sleep(0.5)

thread = Thread(target=updateThread)
thread.start()

while True:
    message = input()

    message = util.transformMsg(message)

    if len(message) > 0:
        net.sendMessage(message)
