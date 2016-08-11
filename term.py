import sys, struct, fcntl, termios, readline, shutil

def resetPrompt():
    sys.stdout.write("\033[93m {}\033[00m".format("Me: ") + readline.get_line_buffer())
    sys.stdout.flush()

def resetTermLine():
    (rows,cols) = struct.unpack('hh', fcntl.ioctl(sys.stdout, termios.TIOCGWINSZ,'1234'))

    text_len = len(readline.get_line_buffer())+2

    sys.stdout.write('\x1b[2K')
    sys.stdout.write('\x1b[1A\x1b[2K'*int(text_len/cols))
    sys.stdout.write('\x1b[0G')

def printMessage(message,user=False):
    if user is False:
        print("\r" + "\033[93m {}\033[00m".format("Me: ") + message)
    else:
        print("\r" + "\033[91m {}\033[00m".format(user+": ") + message)

def progress(count, total, suffix=''):
    bar_len = shutil.get_terminal_size((80, 20))[0] - 9

    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s\r' % (bar, percents, '%'))
    sys.stdout.flush()

def printMessages(messages, users, printMe=False):
    retVal = None

    for message in reversed(messages):
        if not 'subtype' in message:
            if users[message['user']] == False:
                if printMe:
                    printMessage(message['text'],False)
            else:
                printMessage(message['text'],users[message['user']])
        retVal = message['ts']

    return retVal

def beep():
    sys.stdout.write('\007')
    sys.stdout.flush()
