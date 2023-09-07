from file_watcher import file_watcher
from location_fetcher import location_fetcher
from gmail_sender import gmail_sender
import json

if __name__ == "__main__":
    config_file = open("configs.json", "r")
    configs = json.load(config_file)
    
    _file_watcher = file_watcher.FileWatcher(configs=configs["file_watcher"])
    _location_fetcher = location_fetcher.LocationFetcher(configs=configs["ip_fetcher"])
    _gmail_sender = gmail_sender.GmailSender(configs=configs["gmail_sender"])
    
    while True:
        ip_address, timestamp, user_agent = _file_watcher.watch_file()
        resp = _location_fetcher.fetch_location(ip_address).decode()
        resp_dict = json.loads(resp)
        city = resp_dict["city"]
        district = resp_dict["district"]
        lat = resp_dict["lat"]
        lon = resp_dict["lon"]
        _gmail_sender.send_message(f"{city}/{district} /// {lat},{lon}", (resp_dict))
    