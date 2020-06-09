# README

### Implementation Overview

`Flask` is used as the backend framework because of its lightweight-ness
and customizability for api servers.

`mongodb` is used as the db because we are dealing with unstructured data.

`docker-compose` is used for easy setup.

<br>

### Setup
Navigate to a desired folder and clone this repo.
```
git clone https://github.com/hesingon/ascenda_assignment.git
```
Go to the repo directory, build and run the project using with docker-compose.
```
cd ascenda_assignment
docker-compose build
docker-compose up
```
At this point, the api should be accessible at `localhost:5000/find_hotels`

Either `hotel_id` or `destination_id` can be passed in a parameter. 
e.g.
```
http://localhost:5000/find_hotels?hotel_id=iJhz
```
```
http://localhost:5000/find_hotels?destination_id=5432
```
Note that the two should not be passed together. If they are both 
present, the server will only handle `hotel_id`

<br>

### Configuration & Settings
You can do a few configurations by changing `configs/settings.py`. 

`HOTEL_UPDATE_INTERVAL` represents, when server receives a request for a single
hotel, how much time in minutes the server should check the supplier 
urls again for any updates of the hotel.

`DESTINATION_UPDATE_INTERVAL` similarly represents the time in minutes
for updating all hotels in the same destination.

`SUPPLIERS_ENDPOINTS` are the list of supplier endpoints from which
the server will check for updates of hotels periodically.

<br>

### Design Consideration for Performance

1. Whenever server receives a request, it queries db first. If db
does not contain info for that hotel, or it realized that the hotel
was last updated a long time ago, it will query all the supplier
endpoints to get and merge the latest info. 
We check for updates for a configurable interval (e.g. every 3 hours
or 1 day).

2. The querying of multiple supplier APIs is done in a multi-threaded
manner with `aiohttp` to minimise request latency.
 
<br>

### More possible improvement
1. We can include `redis` as an in-memory db on top of mongodb that 
allows fast retrieval of the more frequently read destinations.
