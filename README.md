# semantic-vid
![Semantic-vid home](https://github.com/mvenditto/semantic-vid/blob/master/docs/images/semantic-vid_0.png)
## Dependencies
- Firefox 63.0 (64 bit) (not tested on Chrome)
  - [CORS plugin](https://addons.mozilla.org/it/firefox/addon/cors-everywhere/) may be needed
- Python3
  - flaks
  - flask-cors
  - requests
- [Stardog Knowledge Graph](https://www.stardog.com/docs/)
## Environment Setup
1. [Install and configure Stardog](https://www.stardog.com/docs/)
2. Setup the db (and set username:passwd=admin:admin, or change it in source) :
 ```bash
  # start stardog server (localhost:5820)
  /opt/stardog/bin/stardog-server  start
  # create the new db
  /opt/stardog/bin/stardog-admin db create -P -n semantic-vid_3 ontology/travel_extended.ttl
  # add the data
  /opt/stardog/bin/stardog data add -P semantic-vid_3 ontology/indiv.ttl
  # add the rules
  /opt/stardog/bin/stardog data add -P semantic-vid_3 ontology/rules.ttl
 ```
 3. Install python3 dependencies:
 ```bash
 sudo pip3 install flask flask-cors requests
 ```
 4. Run semantic-vid server
 ```bash
 # start flask (localhost:5000)
 python3 -m flask run # @ the root of the project
 ```
 5. Visit [http://localhost:5000/](http://localhost:5000/)
