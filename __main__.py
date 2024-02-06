import time
import telebot
import requests
import mimetypes
import libtorrent as lt
import os
import subprocess
# import magnetlinkdownloader


headers3 = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.pw.live/',
    'client-id': '5eb393ee95fab7468a79d189',
    'client-version': '2.6.8',
    'Client-Type': 'WEB',
    'randomId': '1652ef6f-ce31-42b4-ae39-0176ce983e09',
    'Origin': 'https://www.pw.live',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'Connection': 'keep-alive',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDg4MzI2MTkuOTU0LCJkYXRhIjp7Il9pZCI6IjYyZDkxM2UyMjc2NWM4MDNiZjJlODJkMSIsInVzZXJuYW1lIjoiOTc5ODczNDczOSIsImZpcnN0TmFtZSI6IiIsImxhc3ROYW1lIjoiIiwib3JnYW5pemF0aW9uIjp7Il9pZCI6IjVlYjM5M2VlOTVmYWI3NDY4YTc5ZDE4OSIsIndlYnNpdGUiOiJwaHlzaWNzd2FsbGFoLmNvbSIsIm5hbWUiOiJQaHlzaWNzd2FsbGFoIn0sInJvbGVzIjpbIjViMjdiZDk2NTg0MmY5NTBhNzc4YzZlZiJdLCJjb3VudHJ5R3JvdXAiOiJJTiIsInR5cGUiOiJVU0VSIn0sImlhdCI6MTcwNTYzNTgxOX0.tr2vLaFihRVJNHagoN5UGiJXnTT2Cim49Z30hqn5H9M',
}

class nnt:
    def get_content_type(file_path):
        content_type, encoding = mimetypes.guess_type(file_path)
        return content_type
    def upload(file_location):
        params3 = {
            'name': file_location,
            'extension': file_location.split('.')[-1],
            'type': 'ASK_DOUBT',
        }
        response3 = requests.get('https://api.penpencil.co/v1/files/signed-url', params=params3, headers=headers3)
        headers4 = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.pw.live/',
            'Origin': 'https://www.pw.live',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'Connection': 'keep-alive',
            'Content-Type': nnt.get_content_type(file_location),
        }
        with open(file_location, 'rb') as file:
            response4 = requests.put(
                url=response3.json()['data']['uploadUrl'],
                headers=headers4,
                data=file,
                stream=True,
                  # Use stream to upload in chunks
            )
            if response4.status_code == 200:
                # return 'Success file uploaded to s3'
                with open('logs.txt','a') as fg:
                    fg.writelines(file_location+" >> "+str(response3.json()['data']['uploadUrl'].split('?')[0])+"\n")
                return "url is  "+response3.json()['data']['uploadUrl'].split('?')[0]
            else:
                return "error uploading file contact admin"

bot = telebot.TeleBot('6612044510:AAFdyJSzrmCwPSSm6SC56pp12eDyyYV0Ofc')
should_stop = False
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'याहा आप टाेरेंट फाइल डाउनलाेड कर सकते हैं। फाइल का magnet लिंक भेजें।')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global should_stop
    ses = lt.session()

    # try:
    magnet_link = message.text
    h = lt.add_magnet_uri(ses, magnet_link, {'save_path': '/home/nnt/torrents/'})
    s = h.status()  # Initialize s before the while loop
    # file_directoryorfile = '/home/nnt/torrents/' + s.name
    while not s.is_seeding:
        s = h.status()
        state_str = ['लािन मे है', 'जाचा जा राहा है', 'मेतादाता दोनलोद किया जा राहा है', 'दोनलोद', 'खतम', 'खतम', 'न']
        bot.send_message(message.chat.id, 'डाउनलाेड हाे रहा है: ' + str(s.progress * 100) + '% ' + state_str[s.state])
        time.sleep(6)
    bot.send_message(message.chat.id, 'डाउनलाेड समाप्त हाे गया है।')
    bot.send_message(message.chat.id, 'अपलाेड कर रहे है...')
    # torrent_directory = '/home/nnt/torrents/'
    # get only the files in the torrent directory
    # run find {torrent_directory} command and get the output
    output = subprocess.check_output('find /home/nnt/torrents/', shell=True).decode('utf-8').split("\n")
    for a in range(0,len(output)):
        try:
            bot.send_message(message.chat.id, nnt.upload(output[a]))
            # 
        except IsADirectoryError as a:
            bot.send_message(message.chat.id, str(a))
        
        # finally:
        #     os.system("rm -rf /home/nnt/torrents/*")
    os.system("rm -rf /home/nnt/torrents/*")
@bot.message_handler(commands=['stop'])
def stop_Message(message):
    global should_stop
    should_stop = True
    bot.send_message(message.chat.id, "Stopping the bot")
    
bot.infinity_polling()