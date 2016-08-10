import os, term

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

def unread(slack,getter,channels,groups,imChannels):
    anyUnread = 0;

    totalToScan = len(channels) + len(groups) + len(imChannels)
    totalScanned = 0

    for channel in channels:
        unreads = slack.channels.info(channel['id']).body['channel']['unread_count']

        if unreads != 0:
            print(channel['name'] + ": " + str(unreads) + " unread")
            anyUnread += 1;

        totalScanned += 1
        term.progress(totalScanned, totalToScan)

    for group in groups:
        unreads = slack.groups.info(group['id']).body['group']['unread_count']

        if unreads != 0:
            print(group['name'] + ": " + str(unreads) + " unread")
            anyUnread += 1;

        totalScanned += 1
        term.progress(totalScanned, totalToScan)

    for im in imChannels:
        unreads = getter.get('im.history',
            params={
                "channel" : im['id'],
                "count"   : 1,
                "unreads" : 1
            }
        ).body['unread_count_display']

        if unreads != 0:
            print(group['name'] + ": " + str(unreads) + " unread")
            anyUnread += 1;

        totalScanned += 1
        term.progress(totalScanned, totalToScan)

    print()

    if anyUnread == 0:
        print('No unread messages.')
    else:
        print(str(anyUnread) + " unread total.")

    os._exit(0)

def help():
    print("- Use -l to list channels and users.\n- Chat with somebody like \"slak mntruell\", or \"slak general\".\n   - You can exit a chat by sending \"\exit\".\n- You can check for unread messages with -n.\n- Set your status to away or auto with -a, eg: \"slak -a auto\".")

    os._exit(0)
