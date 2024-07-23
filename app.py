import json
from datetime import datetime
from file_watcher import file_watcher
from location_fetcher import location_fetcher
from gmail_sender import gmail_sender

def main():
    with open("configs.json", "r") as config_file:
        configs = json.load(config_file)
   
    wanted_country = configs["general"]["wanted_country"]
    limit = configs["general"]["limit_to_send_mail"]

    ip_fetcher_config = configs["ip_fetcher"]
    gmail_sender_config = configs["gmail_sender"]

    _file_watcher = file_watcher.FileWatcher()
    _location_fetcher = location_fetcher.LocationFetcher(configs=ip_fetcher_config)
    _gmail_sender = gmail_sender.GmailSender(configs=gmail_sender_config)
    
    outside_of_country_list = []
    is_running = True

    while is_running:
        try:
            # Watching the file
            ip_address, timestamp, user_agent = _file_watcher.watch_file()
            # If data arrives, fetch the location
            data = _location_fetcher.fetch_location(ip_address)
            # If data is empty, continue to watch file
            if not data:
                continue

            country, city, lat, lon, data_to_send_mail = data

            # Formatting the timestamp and user_agent to increase readability
            timestamp = datetime.strptime(timestamp, "%d/%b/%Y:%H:%M:%S %z")
            timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S %Z")
            user_agent = user_agent.replace('"', '')
            
            if wanted_country and country != wanted_country:
                outside_of_country_list.append(data_to_send_mail)
                if len(outside_of_country_list) >= limit:
                    # TODO: Format data to send
                    message_subject = f"Summary of Last {limit} Requests"
                    message_body = "\n".join([f"{c}- {str(data)}\nTimestamp: {timestamp}\nUser Agent: {user_agent}" for c, data in enumerate(outside_of_country_list)])
                    outside_of_country_list = []
                else:
                    continue
            else:
                message_subject = f"{city} - {lat}, {lon}"
                message_body = f"Timestamp: {timestamp}\nUser Agent: {user_agent}\n{data_to_send_mail}"
            
            _gmail_sender.send_message(message_subject, message_body)
        
        except KeyboardInterrupt:
            is_running = False    
        except Exception as e:
            print(e)
            continue

if __name__ == "__main__":
    main()
