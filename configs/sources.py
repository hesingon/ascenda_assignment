import os

MONGO_HOST = 'db' if os.environ.get('DOCKER_MODE') else 'localhost'
MONGO_PORT = 27017

HOTEL_ID = [
    'iJhz',
    'SjyX',
    'f8c9'
]

ID_IDENTIFIERS = [
    'Id',
    'hotel_id',
    'id'
]

DESTINTATION_IDENTIFIERS = [
    'destination',
    'DestinationId',
    'destination_id'
]
