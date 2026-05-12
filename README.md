## using this app
setup command
<code>docker compose up --build</code>

run command
<code>docker compose up</code>

this application allows the user to save and view records in mong, as well as accsess a model for iris classification

### ports used
- 3000, front end user interface, web page
- 8000, back end api, used for interfacing with mongo
- 8001, model api, it serves predictions to the back end api
- 27017, mongo database


## architecture

&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; |---> Health Checks<br>
WebInterface --->  FrontEnd ---> BackEnd ---> ModelAPI<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; |---> Mongo

## docker model runner

a model was loaded using docker model runner, the model was gemma4, code for making requests to it is in the file, front_end/dockerModelRunnerTest.js

the request is made to port 12434, it's response to the test query of "what is docker in one sentance", was "Docker is a platform that allows developers to package applications and all their dependencies into portable, isolated units called containers, ensuring they run consistently across any environment."