"""Main class containing all exposed endpoints"""
from fastapi import FastAPI, HTTPException
from custom_types.client import Client
import database.connector as db
from pydantic import BaseModel
from typing import Optional

class ClientIn(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    lat: int
    lon: int

app = FastAPI()

@app.post("/clients", response_model=Client)
async def register_client(client: ClientIn):
    """Registers a client

    Parameters
    ----------
    client: ClientIn
        The client to register

    Returns
    -------
    Client
        The client, if registered succesfully
    """

    _check_client(client)
    new_client = Client(client.lat, client.lon, email=client.email, phone=client.phone)
    added = db.add_client(new_client)
    if added is None:
        raise HTTPException(status_code=400, detail=f"Could not register client")
    elif new_client == added:
        return new_client

@app.put("/clients", response_model=Client)
async def update_geolocation(client: ClientIn):
    """Updates geolocation info for a client

    Parameters
    ----------
    client: ClientIn
        Client containing new geolocation data

    Returns
    -------
    Client
        The updated client
    """

    _check_client(client)
    existing_client = Client(client.lat, client.lon, email=client.email, phone=client.phone)
    if db.get_client(existing_client) is None:
        raise HTTPException(status_code=400, detail="Client doesn't exist")
    updated = db.update_client(existing_client)
    return updated

@app.delete("/clients", response_model=Client)
async def delete_client(client: ClientIn):
    """Unsubscribes a client from the service

    Parameters
    ----------
    client: ClientIn
        Client to be removed

    Returns
    -------
    Client
        The client that was removed
    """

    _check_client(client)
    existing_client = Client(client.lat, client.lon, email=client.email, phone=client.phone)
    if db.get_client(existing_client) is None:
        raise HTTPException(status_code=400, detail="Client doesn't exist")
    removed = db.remove_client(existing_client)
    if removed is None:
        raise HTTPException(status_code=400, detail=f"Could not unsubscribe client")
    elif existing_client == removed:
        return removed

def _check_client(client):
    if client.email is None and client.phone is None:
        raise HTTPException(status_code=400, detail="Must provide either email or phone number")
