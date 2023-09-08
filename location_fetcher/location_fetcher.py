import requests
import json

class LocationFetcher:
    def __init__(self, configs) -> None:
        _generated_fields = configs["generated_fields"]
        self.generated_fields = [] 
        # Generating fields to fetch from API
        for field in _generated_fields.keys():
            if _generated_fields[field]:
                self.generated_fields.append(field)
        self.fields = ""
        for c, field in enumerate(self.generated_fields):
            if c == len(self.generated_fields) - 1:
                self.fields += field
            else:
                self.fields += f"{field},"
        print(self.fields)


    def fetch_location(self, ip):
        resp = requests.get(f"http://ip-api.com/json/{ip}?fields={self.fields}")
        
        # If request is not successful, it returns an empty list and throws below exception
        try:
            data = json.loads(resp.content.decode())
        except json.decoder.JSONDecodeError:
            return False
        
        # For mail subject
        city = data["city"]
        lat = data["lat"]
        lon = data["lon"]
        _key = ""
        data_to_send_mail = ""
        for key in data.keys():
            if key == "status":
                continue
            elif key == "continent":
                _key = "Continent"
            elif key == "continentCode":
                _key = "Continent Code"
            elif key == "country":
                _key = "Country"
            elif key == "countryCode":
                _key = "Country Code"
            elif key == "region":
                _key = "Region"
            elif key == "regionName":
                _key = "Region Name"
            elif key == "city":
                _key = "City"
            elif key == "zip":
                _key = "Zip"
            elif key == "district":
                _key = "District"
            elif key == "lat":
                _key = "Latitude"
            elif key == "lon":
                _key = "Longitude"
            elif key == "timezone":
                _key = "Timezone"
            elif key == "offset":
                _key = "Offset"
            elif key == "isp":
                _key = "ISP"
            elif key == "org":
                _key = "Organization"
            elif key == "as":
                _key = "AS"
            elif key == "asname":
                _key = "AS Name"
            elif key == "reverse":
                _key = "Reverse"
            elif key == "mobile":
                _key = "Mobile"
            elif key == "proxy":
                _key = "Proxy"
            elif key == "hosting":
                _key = "Hosting"
            elif key == "query":
                _key = "IP Address"
            
            data_to_send_mail += f"{str(_key)} ----> {data[key]}\n"

        return data["countryCode"], city, lat, lon, data_to_send_mail
    
            
        
    