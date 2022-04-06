from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.channels import InviteToChannelRequest
from pprint import pprint
import time, os, sys, csv, configparser

config = configparser.ConfigParser()
config.read('config.txt')

api_id = int(config['USER']['api_id'])
api_hash = config['USER']['api_hash']
phone = config['USER']['phone']
find_in_group = config['USERS']['userlist'].split(',')

client = TelegramClient(phone, api_id, api_hash)

async def main():

    chats = []
    groups = []
    gr_title = 'test_grp_2'

    # add group
    new_group = await client(CreateChannelRequest(
        title=gr_title, 
        about='testing api', 
        megagroup=True))

    result = await client(GetDialogsRequest(
                offset_date=None,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=200,
                hash=0))
    chats.extend(result.chats)

    for chat in chats:
        # print(chat.title)
        try:
            if chat.megagroup == True:
                groups.append(chat)
        except:
            continue
    
    for group in groups:
        # print(group.title)
        if group.title == gr_title:
            print("===========================")
            dest_group = group

    print('Choose a group to scrape: ')
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

    target_group = groups[int(gr_index)]
    print('-----------------')
    print(type(target_group), type(dest_group))

    print('Fetching Members...')
    all_members = []
    all_members = await client.get_participants(target_group)

    # find users in group
    found_in_group = []
    for user in [name.username for name in all_members]:
        if user in find_in_group:
            found_in_group.append(user)
    print(found_in_group)

    # target_group_entity = InputPeerChannel(new_group.id,new_group.access_hash)

    # add users to group
    await client(InviteToChannelRequest(dest_group.title, found_in_group))


with client:
    client.loop.run_until_complete(main())
