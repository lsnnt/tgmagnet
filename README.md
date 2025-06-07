This project dedicated to a telegram bot which can download magnet links and upload it to a server.
# Running the bot
1) Clone and cd to repo using
```
git clone https://github.com/lsnnt/tgmagnet && cd tgmagnet
```
2) To run the bot first set the necessary variables
token should be your telegram bot token and path should be where the torrents are going to be downloaded
https://github.com/lsnnt/tgmagnet/blob/581d0cf96b1de5ed5741cb2df344941ed062336c/main.py#L9-L10
https://github.com/lsnnt/tgmagnet/blob/581d0cf96b1de5ed5741cb2df344941ed062336c/main.py#L133
4) Then install the necessary dependency using
```
pip3 install -r requirements.txt
```
4) Then run the bot using
```
python3 main.py
```
Ctrl+C to exit
If you want to run the bot in background
```
nohup python3 main.py & disown
```

### I recommend to host it on a VPS with at least 2GB RAM
This is bandwith hungry as it first  downloads the torrent and upload it to the server and then provide link to access the file.
However if you want to only download the file download using aria2c or transmission-cli

