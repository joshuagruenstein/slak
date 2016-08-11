import os, term, util, net

def list(args, channels, groups, imChannels, users):
    if len(args) == 2 or args[2] == "users":
        for channel in imChannels:
            for user in users:
                if user['id'] == channel['user']:
                    if 'real_name' in user and user['real_name'] != "":
                        print(user['name'] + " <" + user['real_name'] + ">")
                    else:
                        print(user['name'])

    if len(args) == 2 or args[2] == "channels":
        for channel in channels:
            print(channel['name'])

    if len(args) == 2 or args[2] == "groups":
        for group in groups:
            print(group['name'])

    os._exit(0)

def presence(slack, presence):
    try:
        slack.users.set_presence(presence)
        print('Presence set to ' + presence)
    except:
        print('Unable to set presence to \"' + presence + "\"")

    os._exit(0)

def unread(slack,getter):
    unread = net.unread(slack,getter,progress=True)

    print("\n")

    anyUnread = 0
    for name, num in unread.items():
        print(name + ": " + str(num) + " unread")
        anyUnread += num

    if anyUnread == 0:
        print('No unread messages.')
    else:
        print(str(anyUnread) + " unread total.")

    os._exit(0)

def poll(slack, getter):
    print("Polling... I'll let you know if you get anything.")
    lastUnread = {}
    while True:
        unread = net.unread(slack,getter)
        if len(unread) > 0 and unread != lastUnread:
            for name, num in unread.items():
                if num == 1:
                    print("1 new message from " + name)
                    util.notify("1 new message from " + name)
                else:
                    print(str(num) + " new messages from " + name)
                    util.notify(str(num) + " new messages from " + name)
                term.beep()
            lastUnread = unread.copy()

def help():
    print("- Use -l to list channels and users.")
    print("- Chat with somebody like \"slak mntruell\", or \"slak general\".")
    print("   - You can exit a chat by sending \"\exit\".")
    print("- You can check for unread messages with -n.")
    print("- Set your status to away or auto with -a, eg: \"slak -a auto\".")

    os._exit(0)

def update():
    util.gitPull()

    os._exit(0)
