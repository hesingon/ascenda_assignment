# Developer's Guide

### MongoDB setup
Spin up mongodb as a docker image <br>
```
docker run -d -p 27017-27019:27017-27019 --name mongodb mongo:latest
```
To connect to the instance <br>
```
docker exec -it mongodb bash
mongo
```
[Reference](https://www.thepolyglotdeveloper.com/2019/01/getting-started-mongodb-docker-container-deployment/)

