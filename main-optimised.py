import time
import telebot
import requests
import mimetypes
import libtorrent as lt
import os
import subprocess

path = "YOUR_PATH_HERE"
token = "YOUR_TELEGRAM_BOT_TOKEN HERE"
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
                return file_location+" >> "+str(response3.json()['data']['uploadUrl'].split('?')[0])+"\n"
            else:
                return "error uploading file contact admin"

bot = telebot.TeleBot(token)
should_stop = False
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'You can get link of files here paste the magnet link here and get its uploaded link')

def track_torrent_status(h, message):
    state_str = [
        'in Queue', 'Checking', 'Downloading metadata',
        'Downloading', 'Completed', 'Completed', 'No'
    ]
    
    # Initial status
    s = h.status()
    progresstimes = 0
    while not s.is_seeding:
        s = h.status()
        progress = s.progress * 100
        bot.send_message(message.chat.id, f'Downloading: {progress:.2f}% {state_str[s.state]}')
        if(progress==0):
            progresstimes+=1
        if(progresstimes==10):
            bot.send_message(message.chat.id, "We could not download the torrent in reasonable time check if there are enough seeders")
            return False
        time.sleep(6)  # Avoid spamming, sleep for a reasonable time
        
    bot.send_message(message.chat.id, 'Download Completed')
    
# Helper function to handle upload tasks
def upload_torrent_files(message, path):
    try:
        output = subprocess.check_output(f'find {path}', shell=True).decode('utf-8').split("\n")
        
        for file in output:
            if file:  # Avoid processing empty file paths
                try:
                    # Assuming nnt.upload() uploads the file
                    bot.send_message(message.chat.id, nnt.upload(file))
                    # Cleanup after upload
                    os.system(f"rm -rf \"{path}/{file}\"")
                except IsADirectoryError as e:
                    bot.send_message(message.chat.id, f"Error: {e}")
    except subprocess.CalledProcessError as e:
        bot.send_message(message.chat.id, f"Error finding files: {e}")
        
# Main handler for processing the torrent
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global should_stop
    ses = lt.session()
    
    magnet_link = message.text
    try:
        # Add the magnet URI and save the torrent to the specified path
        h = lt.add_magnet_uri(ses, magnet_link, {'save_path': path})
        
        # Track the torrent download status
        track_torrent_status(h, message)
        
        # Notify the user that uploading is starting
        bot.send_message(message.chat.id, 'Uploading...')
        
        # Handle the upload process
        upload_torrent_files(message, path)
        
        # Final cleanup step
        os.system(f"rm -rf <ENTER PATH HERE>") 
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")
@bot.message_handler(commands=['stop'])
def stop_Message(message):
    global should_stop
    should_stop = True
    bot.send_message(message.chat.id, "Stopping the bot")
    
bot.infinity_polling()
