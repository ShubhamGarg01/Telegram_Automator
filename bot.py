import sys
import csv
import random
import time
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
SLEEP_TIME = 10
api_id = 5567609
api_hash = '0f8926366db5ac5b0471cda73fb269cd'
phone = '+91-8955090918'
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

chats = []
last_date = None
chunk_size = 20
groups=[]
 
result = client(GetDialogsRequest(offset_date=last_date,offset_id=0,offset_peer=InputPeerEmpty(),limit=chunk_size,hash = 0))
chats.extend(result.chats)
for chat in chats:
    groups.append(chat)


print('Choose a group to scrape members from:')
i=0
for g in groups:
    print(str(i) + '- ' + g.title)
    i+=1
g_index = input("Enter a Number: ")
target_group=groups[int(g_index)]
print('Fetching Members...')
all_participants = []
all_participants = client.get_participants(target_group, aggressive=True)
print('Saving In file...')
with open("members.csv","w",encoding='UTF-8') as f:
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
    for user in all_participants:
        if user.username:
            username= user.username
        else:
            username= ""
        if user.first_name:
            first_name= user.first_name
        else:
            first_name= ""
        if user.last_name:
            last_name= user.last_name
        else:
            last_name= ""
        name= (first_name + ' ' + last_name).strip()
        writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])      
print('Members scraped successfully.')
input_file = 'members.csv'
users = []
with open(input_file, encoding='UTF-8') as f:
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)
mode = int(input("Enter 1 to send by user ID or 2 to send by username: "))
print("Enter the number")
messages = ["How are you?", "Hi", "do you want to gotrained?"]
for i in range(len(messages)):
    print(f"{i} - {messages[i]}")
msg = int(input())    
for user in users:
    if mode == 2:
        if user['username'] == "":
            continue
        receiver = client.get_input_entity(user['username'])
    elif mode == 1:
        receiver = InputPeerUser(user['id'],user['access_hash'])
    else:
        print("Invalid Mode. Exiting.")
        client.disconnect()
        sys.exit()
    message = messages[msg]
    try:
        print("Sending Message to:", user['name'])
        client.send_message(receiver, message.format(user['name']))
        print("Waiting {} seconds".format(SLEEP_TIME))
        time.sleep(SLEEP_TIME)
    except PeerFloodError:
        print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
        client.disconnect()
        sys.exit()
    except Exception as e:
        print("Error:", e)
        print("Trying to continue...")
        continue
client.disconnect()
print("Done. Message sent to all users.")
