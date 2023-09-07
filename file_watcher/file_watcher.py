import time
class FileWatcher:
    def __init__(self, configs) -> None:
        self.f = open('.log', "r")
    
    def watch_file(self):
        line = self.f.readline()
        if line:
            return line
        else:
            time.sleep(5)
