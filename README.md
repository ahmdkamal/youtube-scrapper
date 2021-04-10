## The Goal

You will send url for a playlist or channel on YouTube, and it will save its content in db

- views
- title
- thumbnail
- duration
- url
- image path (after downloading it)

<b>NOTE :::</b> Videos' thumbnail are downloaded in the background

### Architecture

Using Controller, Service Pattern

### Prerequisite

Docker should be installed locally

## How to run the application

- copy `.env.example` in same path to be `.env`
  - change its content to what you need
- run in terminal `docker-compose up -d`

### How to access

call in postman or curl `POST http://localhost:YOUR_APP_PORT_IN_ENV/youtube/scrap` with form data has key called `url`
(check collection)

### What is used

- `mongodb` data can be considered as non-structured so I used mongo db

- `Flask` a light-weight framework to have apis
  - `flask_pymongo` to establish connection to mongo
  - `wtforms` to validate request
    
- `python-dotenv` to load environment variables

- `requests` to call external URL

- `bs4` a module in Python to scrap the content of url
    - I found the videos inside a variable in script tag, so I had to search for it in string and print its value to a file 
      and load it again as json


#### Example
    eg. for woking urls
    https://www.youtube.com/watch?v=cnZfPPiivwk&list=RDMMcnZfPPiivwk