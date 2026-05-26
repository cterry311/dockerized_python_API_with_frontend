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

## LLM integration

LLM integration was achieved using the docker model runner, the docker composer has a service running on port 8002
the following endpoints are availible <br>
/chat <br>
/housing<br>
the /chat endpoint expects the context of the converation in openAI format, it will get the models response, the /housing endpoint expects a json body descricing aspects of the house in question, and it will return a response containing  the following keys, price, which is the predicted price, and confidence, which is the models confidence in it's prediction.
also note that the model should not be trusted at all in it's predictions, it is an LLM doing regression, so take it's predictions with a grain of salt

### housing system prompt
the following prompt was provided to the model in order for it to do housing predictions
<code>you are a housing price predictor, you will predict housing prices based on user input. you will get input from the user in json format
            you will respond in json format, and example reply is as follows '{"price": 20000, "confidence":0.6}', you will always respond with the fields price, and confidence. each is a numerical value, where price is the value of the home, and confidence is a float between 0 and 1.
            you will not respond in anything other than a json format and will only reply with the housing price predictions</code>