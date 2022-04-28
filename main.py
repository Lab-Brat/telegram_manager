from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.functions.channels import CreateChannelRequest, InviteToChannelRequest
from telethon.errors.rpcerrorlist import UserPrivacyRestrictedError
import time, sys, configparser

config = configparser.ConfigParser()
config.read('config.txt', encoding='utf-8')

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
    print('')

    # enter and process user ids
    chosen_users_input = input("Enters IDs of chosen users: ").split(',')
    print('')
    for u in chosen_users_input:
        try:
            cu = all_members[int(u)].id
            fname = all_members[int(u)].first_name
            lname = all_members[int(u)].last_name
            await client(InviteToChannelRequest(dest_group.title, [cu]))
            print(f'added {fname} {lname} to group {gr_title}')
        except UserPrivacyRestrictedError:
            print("The user's privacy settings do not allow you to do this. Skipping.")


with client:
    client.loop.run_until_complete(main())
