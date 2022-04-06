from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from pprint import pprint
import time, os, sys, csv, configparser

config = configparser.ConfigParser()
config.read('config.txt')

api_id = int(config['USER']['api_id'])
api_hash = config['USER']['api_hash']
phone = config['USER']['phone']

print(api_id, api_hash, phone)
print(type(api_id), type(api_hash), type(phone))


client = TelegramClient(phone, api_id, api_hash)

async def main():
    chats = []
    groups = []

    result = await client(GetDialogsRequest(
                offset_date=None,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=200,
                hash=0))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.megagroup == True:
                groups.append(chat)
        except:
            continue
    
    # for chat in chats:
    #     if chat.group == True:
    #         groups.append(chat)
    # pprint([t.title for t in groups])
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

    print('Fetching Members...')
    all_members = []
    all_members = await client.get_participants(target_group)

    print('Saving in file...')
    with open('members.csv', 'w', encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=',', lineterminator='\n')
        writer.writerow(['username', 'user_id', 'access_hash', 'first_name', 
                         'last_name', 'group_name', 'group_id'])
        
        for user in all_members:
            # print(dir(target_group))
            # break
            writer.writerow([user.username, user.id, 
                             user.access_hash, user.first_name,
                             user.last_name, target_group.username, target_group.id])
    print('Members scraped successfully')

with client:
    client.loop.run_until_complete(main())

# # me = client.get_me()
# # print(me)
