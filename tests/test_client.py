from custom_types.client import Client


def test_client():
    phone_client = Client(60, 18, phone='23232323')
    assert phone_client.phone == '23232323'
    assert phone_client.email is None

    email_client = Client(60, 18, email='example@domain.com')
    assert email_client.phone is None
    assert email_client.email == 'example@domain.com'

    email_phone_client = Client(
        60, 18, email='some@thing.com', phone='99999999')
    assert email_phone_client.email == 'some@thing.com'
    assert email_phone_client.phone == '99999999'


def test_set_traffic_area():
    phone_client = Client(61, 18, phone='23232323')
    assert phone_client.traffic_area == 'Gävleborg'
    phone_client.lat = 60
    phone_client.lon = 18
    phone_client.set_traffic_area()
    assert phone_client.traffic_area == 'Uppland'
