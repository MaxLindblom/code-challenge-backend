"""Main class containing all exposed endpoints"""
from fastapi import FastAPI

app = FastAPI()

@app.post("/mail/{email}")
async def register_email(email, lat, lon):
    """Registers a client based on email

    Parameters
    ----------
    email : str
        The email to register
    lat : int
        Lattitude for the client, closest integer
    lon: int
        longitude for the client, closest integer

    Returns
    -------
    """

@app.post("/phone/{phone}")
async def register_phone(phone, lat, lon):
    """Registers a client based on phone number

    Parameters
    ----------
    phone : str
        The phone number to register
    lat : int
        Lattitude for the client, closest integer
    lon: int
        longitude for the client, closest integer

    Returns
    -------
    """


@app.put("/mail/{email}")
async def update_geolocation_email(email, lat, lon):
    """Updates geolocation info for an email

    Parameters
    ----------
    email : str
        The email to update info for
    lat : int
        Lattitude for the client, closest integer
    lon: int
        longitude for the client, closest integer

    Returns
    -------
    """


@app.put("/phone/{phone}")
async def update_geolocation_phone(phone, lat, lon):
    """Updates geolocation info for a phone nubmer

    Parameters
    ----------
    phone : str
        The phone number to update info for
    lat : int
        Lattitude for the client, closest integer
    lon: int
        longitude for the client, closest integer

    Returns
    -------
    """


@app.delete("/mail/{email}")
async def delete_email(email):
    """Unsubscribes an email from the service

    Parameters
    ----------
    email : str
        The email to unsubscribe

    Returns
    -------
    """


@app.delete("/phone/{phone}")
async def delete_phone(phone):
    """Unsubscribes a phone number from the service

    Parameters
    ----------
    phone : str
        The phone number to unsubscribe

    Returns
    -------
    """