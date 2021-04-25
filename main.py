"""Main class containing all exposed endpoints"""
from typing import Optional
import asyncio
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from custom_types.client import Client
import database.connector as db
import sr_api.traffic as traffic


class ClientIn(BaseModel):
    """Class structure for client sent in requests"""
    email: Optional[str] = None
    phone: Optional[str] = None
    lat: int
    lon: int


class ClientOut(BaseModel):
    """Class structure for client sent in response"""
    email: Optional[str] = None
    phone: Optional[str] = None
    lat: int
    lon: int
    traffic_area: str


app = FastAPI()


@app.post("/clients", response_model=ClientOut)
async def register_client(client: ClientIn):
    """Registers a client

    Parameters
    ----------
    client: ClientIn
        The client to register

    Returns
    -------
    ClientOut
        The client, if registered succesfully
    """

    _check_client(client)
    new_client = Client(client.lat, client.lon,
                        email=client.email, phone=client.phone)
    added = db.add_client(new_client)
    if added is None:
        raise HTTPException(
            status_code=400, detail="Could not register client")
    if new_client == added:
        return new_client.to_json()


@app.put("/clients", response_model=ClientOut)
async def update_geolocation(client: ClientIn):
    """Updates geolocation info for a client

    Parameters
    ----------
    client: ClientIn
        Client containing new geolocation data

    Returns
    -------
    ClientOut
        The updated client
    """

    _check_client(client)
    existing_client = Client(client.lat, client.lon,
                             email=client.email, phone=client.phone)
    if db.get_client(existing_client) is None:
        raise HTTPException(status_code=400, detail="Client doesn't exist")
    updated = db.update_client(existing_client)
    return updated.to_json()


@app.delete("/clients", response_model=ClientOut)
async def delete_client(client: ClientIn):
    """Unsubscribes a client from the service

    Parameters
    ----------
    client: ClientIn
        Client to be removed

    Returns
    -------
    ClientOut
        The client that was removed
    """

    _check_client(client)
    existing_client = Client(client.lat, client.lon,
                             email=client.email, phone=client.phone)
    if db.get_client(existing_client) is None:
        raise HTTPException(status_code=400, detail="Client doesn't exist")
    removed = db.remove_client(existing_client)
    if removed is None:
        raise HTTPException(
            status_code=400, detail="Could not unsubscribe client")
    if existing_client == removed:
        return removed.to_json()


def _check_client(client):
    if client.email is None and client.phone is None:
        raise HTTPException(
            status_code=400, detail="Must provide either email or phone number")


def _construct_message(msg):
    """Formats a message from a dictionary

    Parameters
    ----------
    msg: dict
        The message in dict form

    Returns
    -------
    str
        A stringified version of the message
    """

    date = datetime.fromisoformat(msg['timestamp'].split('.')[0])
    msg_string = f"Nytt trafikmeddelande för {msg['title']}, "
    msg_string += f"{date.month}/{date.day} {date.hour}:{date.minute}. "
    msg_string += f"{msg['priority']}, {msg['category']}: {msg['description']} "
    if msg['location'] is not None:
        msg_string += f"Exakt plats: {msg['location']}."
    return msg_string


def _send_message(msg, email, phone):
    """Sends a message to a client

    Parameters
    ----------
    msg: dict
        A message in dict form with string values
    email: str
        Email adress to send message to. Can be None
    phone: str
        Phone number to send SMS to. Can be None
    """

    msg_string = _construct_message(msg)
    if email is not None:
        with open('sent_messages.txt', 'a+') as f:
            f.writelines(
                [f"Sent to email {email}:\n", msg_string, "\n"])
            f.close()
    if phone is not None:
        with open('sent_messages.txt', 'a+') as f:
            f.writelines(
                [f"Sent to phone number {phone}:\n", msg_string, "\n"])
            f.close()


def _handle_area_clients(client_list, current_poll, msg):
    """Performs necessary actions for all clients for an area

    Parameters
    ----------
    client_list: list
        A list of all relevant clients
    current_poll: datetime
        Timestamp for current poll
    msg: str
        The message to potentially send
    """

    for client in client_list:
        client_date = client[-1]
        if (current_poll - client_date).total_seconds() / (60 * 24) > 1:
            db.remove_client(
                Client(client[2], client[3], email=client[0], phone=client[1]))
        else:
            _send_message(msg, client[0], client[1])


async def server():
    """Runs the server and all business logic"""
    last_poll = datetime.now() - timedelta(minutes=10)
    print('Server booted up, polling API every 10 minutes.')
    while True:
        current_poll = datetime.now()
        clients = db.get_all_clients()
        recipients = {}
        for client in clients:
            recipients.setdefault(client[4], []).append(client)
        for area, client_list in recipients.items():
            messages = traffic.messages(area)
            for msg in messages:
                # We don't need microseconds
                msg_datestring = msg['timestamp'].split('.')[0]
                poll_diff = (
                    (last_poll - datetime.fromisoformat(msg_datestring))
                    .total_seconds()
                )
                if poll_diff < 0:
                    # New message(s) for the area found!
                    _handle_area_clients(client_list, current_poll, msg)

        last_poll = current_poll
        # We don't need to poll more often than every 10 minutes
        await asyncio.sleep(10*60)

if __name__ == '__main__':
    asyncio.run(server())
