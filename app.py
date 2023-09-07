from file_watcher import file_watcher
from location_fetcher import location_fetcher
from gmail_sender import gmail_sender
import json

config_file = open("configs.json", "r")
configs = json.load(config_file)

_file_watcher = file_watcher.FileWatcher(configs=configs["file_watcher"])
_location_fetcher = location_fetcher.LocationFetcher(configs=configs["ip_fetcher"])
_gmail_sender = gmail_sender.GmailSender(configs=configs["gmail_sender"])

while True:
    data = _file_watcher.watch_file()
    if not data == "None" or not data == " ":
        print(data)

_location_fetcher.fetch_location("")
_gmail_sender.send_message("11", "1223")
