import term
import threading
import time

getMessages = None
sendMessage = None
markRead    = None
channels    = None
groups      = None
imChannels  = None

userRaw     = None
users       = {}

def initFields(slack):
    global channels, groups, imChannels, users, userRaw

    channels = [x for x in slack.channels.list().body['channels'] if x['is_archived'] == False]
    groups = [x for x in slack.groups.list().body['groups'] if x['is_archived'] == False and "mpdm-" not in x['name']]
    imChannels = slack.im.list().body['ims']

    me = slack.users.profile.get().body['profile']
    userRaw = slack.users.list().body['members']
    for user in userRaw:
        if 'real_name' in user:
            if me['real_name'] == user['real_name']:
                users[user['id']] = False
            else:
                users[user['id']] = user['real_name']


def initReadWrite(slack, name):
    global getMessages, sendMessage, markRead

    for channel in channels:
        if channel['name'] == name:
            correctChannel = channel['id']
            markRead = lambda x: mark(slack,correctChannel,x,"CHANNEL")
            getMessages = lambda x: slack.channels.history(correctChannel,oldest=x).body['messages']
            sendMessage = lambda x: slack.chat.post_message(correctChannel,x,as_user=True)
            return True

    for group in groups:
        if group['name'] == name:
            correctGroup = group['id']
            markRead = lambda x: mark(slack,correctGroup,x,"GROUP")
            getMessages = lambda x: slack.groups.history(correctGroup,oldest=x).body['messages']
            sendMessage = lambda x: slack.chat.post_message(correctGroup,x,as_user=True)
            return True

    for channel in imChannels:
        for user in userRaw:
            if user['id'] == channel['user'] and user['name'] == name:
                correctIM = channel['id']
                markRead = lambda x: mark(slack,correctIM,x,"IM")
                getMessages = lambda x: slack.im.history(correctIM,oldest=x).body['messages']
                sendMessage = lambda x: slack.chat.post_message(correctIM,x,as_user=True)
                return True

    return False

def unread(slack,getter,progress=False):
    totalToScan = len(channels) + len(groups) + len(imChannels)
    totalScanned = 0

    unread = {}

    for channel in channels:
        unreads = slack.channels.info(channel['id']).body['channel']['unread_count']

        if unreads != 0:
            unread[channel['name']] = unreads

        totalScanned += 1
        if progress:
            term.progress(totalScanned, totalToScan)

    for group in groups:
        unreads = slack.groups.info(group['id']).body['group']['unread_count']

        if unreads != 0:
            unread[group['name']] = unreads

        totalScanned += 1

        if progress:
            term.progress(totalScanned, totalToScan)

    for im in imChannels:
        unreads = getter.get('im.history',
            params={
                "channel" : im['id'],
                "count"   : 1,
                "unreads" : 1
            }
        ).body['unread_count_display']

        if im['user'] == "USLACKBOT":
            continue

        if unreads != 0:
            unread[users[im['user']]] = unreads

        totalScanned += 1

        if progress:
            term.progress(totalScanned, totalToScan)

    return unread


lastMarked = 0
def mark(slack, channel, ts, channelType):
    global lastMarked

    if time.time()-lastMarked < 5:
        return

    lastMarked = time.time()

    if channelType == "CHANNEL":
        slack.channel.mark(channel,ts)
    elif channelType == "GROUP":
        slack.group.mark(channel,ts)
    else:
        slack.im.mark(channel,ts)
