getMessages = None
sendMessage = None
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
    global getMessages, sendMessage

    for channel in channels:
        if channel['name'] == name:
            correctChannel = channel['id']
            getMessages = lambda x: slack.channels.history(correctChannel,oldest=x).body['messages']
            sendMessage = lambda x: slack.chat.post_message(correctChannel,x,as_user=True)

    for group in groups:
        if group['name'] == name:
            correctGroup = group['id']
            getMessages = lambda x: slack.groups.history(correctGroup,oldest=x).body['messages']
            sendMessage = lambda x: slack.chat.post_message(correctGroup,x,as_user=True)

    for channel in imChannels:
        for user in userRaw:
            if user['id'] == channel['user'] and user['name'] == name:
                correctIM = channel['id']
                getMessages = lambda x: slack.im.history(correctIM,oldest=x).body['messages']
                sendMessage = lambda x: slack.chat.post_message(correctIM,x,as_user=True)
