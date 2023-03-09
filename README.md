# Welcome to the Tables Scraper!

## The App's Purpose
This app enables you to pull the tables from a given web-source (currently only wabetainfo) 
and conduct simple modifications on the data extracted from specific columns in those tables.

## Running the App Locally
### Steps:
1. Clone the repo
2. Run `pip install -r requirements.txt`
3. Run the app either via your IDE or by using the command `python app.py`

## Running the App on Docker
### Steps:
1. Clone the repo 
2. Access the repo's path via terminal
3. Run the following commands:

`docker build -t <name:version> .` e.g. `docker build tablesscraper:1.0 .`
   
`docker run -d -p <chosen_machine's_port:app's_port> <name:version> ` e.g. `docker run -d -p 5000:5000 tablesscraper:1.0`

To stop the container run `docker stop <first 4 container's characters>`

## Endpoints
###GET endpoints:

---
home page

`http://127.0.0.1:5000`

---
pull all non-previously-seen versions from the web source and updates local records:
`http://127.0.0.1:5000/back_fill_versions/wabetainfo`

---
show all local records:

`http://127.0.0.1:5000/versions_and_sources`

---

show all versions of a specific source (e.g. wabetainfo)

`http://127.0.0.1:5000/versions/<source>` e.g. `http://127.0.0.1:5000/versions/wabetainfo`

---

### POST endpoint - Update a Record
`curl -X POST -H "Content-type: application/json" -d "{\"version_to_update\" : \"<version>\", \"tested_value\" : \"<value>\"}" "http://127.0.0.1:5000/versions/<source_name>/update"`

### DELETE endpoint - Delete a Record
`curl -X DELETE -H "Content-type: application/json" -d "{\"version_to_delete\" : \"<version>\"}" http://127.0.0.1:5000/versions/<source_name>/delete`