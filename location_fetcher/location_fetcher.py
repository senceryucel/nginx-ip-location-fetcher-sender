import requests

class LocationFetcher:
    def __init__(self, configs) -> None:
        _generated_fields = configs["generated_fields"]
        self.generated_fields = [] 
        for field in _generated_fields.keys():
            if _generated_fields[field]:
                self.generated_fields.append(field)
        self.fields = ""
        for c, field in enumerate(self.generated_fields):
            if c == len(self.generated_fields) - 1:
                self.fields += field
            self.fields += f"{field},"


    def fetch_location(self, ip):
        resp = requests.get(f"http://ip-api.com/json/{ip}?fields={self.fields}")
        return resp