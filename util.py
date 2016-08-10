import os, sys

def getToken():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    with open(os.path.join(__location__, 'token'), 'r') as token:
        return token.read().replace('\n', '')

def transformMsg(message):
    temp = message

    if r"/exit" in message:
        os._exit(0)

    temp = temp.replace(":shrug:","¯\_(ツ)_/¯")

    return temp
