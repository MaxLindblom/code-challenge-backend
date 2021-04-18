"""Wrapper for Sveriges Radio traffic API

Includes two endpoints:
- /messages, for getting relevant traffic messages
- /areas, for listing existing traffic areas
For full documentation:
https://sverigesradio.se/api/documentation/v2/metoder/trafik.html
"""

import requests
import xml.etree.ElementTree as ET

MESSAGES_ENDPOINT = 'http://api.sr.se/api/v2/traffic/messages?pagination=false'
AREAS_ENDPOINT = 'http://api.sr.se/api/v2/traffic/areas?pagination=false'

PRIORITY_MAPPING = {
    '1': 'Mycket allvarlig händelse',
    '2': 'Stor händelse',
    '3': 'Störning',
    '4': 'Information',
    '5': 'Mindre störning'
}

CATEGORY_MAPPING = {
    '0': 'Vägtrafik',
    '1': 'Kollektivtrafik',
    '2': 'Planerad störning',
    '3': 'Övrigt'
}

def messages(area_name=None): 
    """Sends a request to the messages endpoint

    Parameters
    ----------
    area_name : str, optional
        The name of the traffic area to get messages for

    Returns
    -------
    list
        A full list of messages as received from the endpoint
    """

    url = MESSAGES_ENDPOINT if area_name is None else MESSAGES_ENDPOINT + f'&trafficareaname={area_name}'
    r = requests.get(url)
    root = ET.fromstring(r.content)

    msg_list = []
    for msg in root.find('messages').iter('message'): # TODO: include None-check?
        msg_list.append({
            'timestamp': msg.find('createddate').text,
            'priority': PRIORITY_MAPPING[msg.attrib['priority']],
            'title': msg.find('title').text,
            'location': msg.find('exactlocation').text,
            'description': msg.find('description').text,
            'category': CATEGORY_MAPPING[msg.find('category').text]
        })

    return msg_list

def areas(lat=None, lon=None):
    """Sends a request to the areas endpoint

    Parameters
    ----------
    lat : int, optional
        Latitude for the traffic area, if specified
    lon: int, optional
        Longitude for the traffic are, if specificed

    Returns
    -------
    list | str
        The list of traffic areas, or a specific area if lat/lon are specified
    """

    if lat is not None and lon is not None:
        r = requests.get(AREAS_ENDPOINT + f'&latitude={lat}&longitude={lon}')
        root = ET.fromstring(r.content)
        return root.find('area').get('name')

    r = requests.get(AREAS_ENDPOINT)
    root = ET.fromstring(r.content)

    area_list = []
    for area in root.find('areas').iter('area'):
        area_list.append(area.attrib['name'])

    return area_list
