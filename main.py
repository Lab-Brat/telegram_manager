from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.functions.channels import CreateChannelRequest, InviteToChannelRequest
import time, sys, configparser

config = configparser.ConfigParser()
config.read('config.txt')

api_id = int(config['USER']['api_id'])
api_hash = config['USER']['api_hash']
phone = config['USER']['phone']
gr_title = config['GROUP']['group_name']
gr_about = config['GROUP']['about']

client = TelegramClient(phone, api_id, api_hash)

async def main():
    chats = []
    groups = []

    # add group
    new_group = await client(CreateChannelRequest(
        title=gr_title, 
        about=gr_about, 
        megagroup=True))

    # extract all group names
    result = await client(GetDialogsRequest(
                offset_date=None,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=200,
                hash=0))
    chats.extend(result.chats)

    # filter out all megagroups
    for chat in chats:
        try:
            if chat.megagroup == True:
                groups.append(chat)
        except:
            continue
    
    # find new group among all groups
    for group in groups:
        # print(group.title)
        if group.title == gr_title:
            dest_group = group

    # list existing groups and take user input
    print('Choose a group to get users from: ')
    for i, group in enumerate(groups):
        print(str(i) + '- ' + group.title)
    gr_index = input("Enter a number: ")
    if gr_index == '':
        print('Ok, skipping')
        time.sleep(1)
        sys.exit()
    else: pass

    print('')
    print('Fetching Members...')
    time.sleep(1)

    # extract members from group
    target_group = groups[int(gr_index)]
    print('Fetching Members...')
    all_members = []
    all_members = await client.get_participants(target_group)

    # print user ids
    for i, user in enumerate(all_members):
        print(f'{i} name: {user.first_name} {user.last_name}')

    # enter and process user ids
    chosen_users_input = input("Enters IDs of chosen users: ")
    chosen_users = []
    for u in chosen_users_input:
        chosen_users.append(all_members[int(u)].id)

    # add users to group
    await client(InviteToChannelRequest(dest_group.title, chosen_users))
    print(f'added {len(chosen_users)} users to group {gr_title}')


with client:
    client.loop.run_until_complete(main())
