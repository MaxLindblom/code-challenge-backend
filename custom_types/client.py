"""Client class for registered users"""

from sr_api.traffic import areas


class Client():
    """Class for representing subscribing clients"""

    def __init__(self, lat, lon, *, email=None, phone=None):
        self.email = email
        self.phone = phone
        self.lat = lat
        self.lon = lon
        self.set_traffic_area()

    def set_traffic_area(self):
        """Sets traffic area for the client based on latitude and longitude

        Returns
        -------
        str
            The traffic area that was set for the client
        """
        self.traffic_area = areas(self.lat, self.lon)
        return self.traffic_area

    def to_json(self):
        """Converts the client object to json

        Returns
        -------
        dict
            Json representation of the client
        """
        return {
            "email": self.email,
            "phone": self.phone,
            "lat": self.lat,
            "lon": self.lon,
            "traffic_area": self.traffic_area
        }
