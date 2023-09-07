import time, re
class FileWatcher:
    def __init__(self, configs) -> None:
        self.logfile = open('new_access.log', "r")
        self.request_pattern = r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "GET .*" 200 \d+ ".*" "(.*)"'


    def watch_file(self):
        while True:
            line = self.logfile.readline()
            match = re.match(self.request_pattern, line)
            if match:
                print(line)
                ip_address = match.group(1)
                timestamp = match.group(2)
                user_agent = match.group(3)
                return ip_address, timestamp, user_agent
            else:
                time.sleep(5)
