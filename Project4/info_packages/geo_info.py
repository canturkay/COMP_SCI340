import maxminddb


class GeoInfo:
    def __init__(self):
        self.reader = maxminddb.open_database('GeoLite2-City_20201103/GeoLite2-City.mmdb')

    def get_info(self, ips: list) -> list:
        locations = []

        for ip in ips:
            location = self.reader.get(ip)
            city = None
            province = None
            country = None

            if "country" in location and "en" in location["country"]["names"]:
                country = location["country"]["names"]["en"]
            elif "registered_country" in location and "en" in location["registered_country"]["names"]:
                country = location["registered_country"]["names"]["en"]
            elif "continent" in location and "en" in location["continent"]["names"]:
                country = location["continent"]["names"]["en"]

            if "subdivisions" in location and len(location["subdivisions"]) > 0 and \
                    "en" in location["subdivisions"][0]["names"]:
                province = location["subdivisions"][0]["names"]["en"]

            if "city" in location and "en" in location["city"]["names"]:
                city = location["city"]["names"]["en"]

            location_text = ""

            if city:
                location_text = city
            if province:
                if len(location_text) > 0:
                    location_text += ', '
                location_text += province
            if country:
                if len(location_text) > 0:
                    location_text += ', '
                location_text += country

            if location_text not in locations:
                locations.append(location_text)

        return locations
