from file_watcher import file_watcher
from location_fetcher import location_fetcher
from gmail_sender import gmail_sender
import json

if __name__ == "__main__":
    config_file = open("configs.json", "r")
    configs = json.load(config_file)
   
    wanted_country =  configs["general"]["wanted_country"]

    _file_watcher = file_watcher.FileWatcher(configs=configs["file_watcher"])
    _location_fetcher = location_fetcher.LocationFetcher(configs=configs["ip_fetcher"])
    _gmail_sender = gmail_sender.GmailSender(configs=configs["gmail_sender"])
    outside_of_country_list = []
    limit = 10

    while True:
        ip_address, timestamp, user_agent = _file_watcher.watch_file()
        resp = _location_fetcher.fetch_location(ip_address).decode()
        try:
            resp_dict = json.loads(resp)
        except json.decoder.JSONDecodeError as empty:
            continue
        city = resp_dict["city"]
        district = resp_dict["district"]
        lat = resp_dict["lat"]
        lon = resp_dict["lon"]
        if wanted_country:
            country = resp_dict["countryCode"]
            if country == wanted_country:
                _gmail_sender.send_message(f"{city}/{district} /// {lat},{lon}", (resp_dict))
            else:
                outside_of_country_list.append(resp_dict)
                if len(outside_of_country_list) >= limit:
                    summary_data_to_send = ""
                    for c, data in enumerate(outside_of_country_list):
                        summary_data_to_send += f"{c}- ", str(data) + "\n"
                    _gmail_sender.send_message(f"Summary of Last {limit} Requests", summary_data_to_send)
                    outside_of_country_list = []
        else:
            _gmail_sender.send_message(f"{city}/{district} /// {lat},{lon}", (resp_dict))
        