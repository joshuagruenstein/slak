import os, sys

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def getToken():
    with open(os.path.join(__location__, 'token'), 'r') as token:
        return token.read().replace('\n', '')

def gitPull():
    return os.system("git -C " + os.path.dirname(sys.argv[0]) + " pull")

def transformMsg(message):
    temp = message

    if r"/exit" in message:
        os._exit(0)

    temp = temp.replace(":shrug:","¯\_(ツ)_/¯")

    return temp
