"""Client class for registered users"""

from sr_api.traffic import areas

class Client:

    def __init__(self, lat, lon, *, email=None, phone=None):
        if email is not None:
            self.email = email
        elif phone is not None:
            self.phone = phone
        self.lat = lat
        self.lon = lon
        self.set_traffic_area(lat, lon)
        
    def set_traffic_area(self, lat, lon):
        """Sets traffic area for the specified latitude and longitude
        
        Parameters
        ----------
        lat : int
            Latitude for the client
        lon: int
            Longitude for the client

        Returns
        -------
        str
            The traffic area that was set for the client
        """
        self.traffic_area = areas(lat, lon)
        return self.traffic_area