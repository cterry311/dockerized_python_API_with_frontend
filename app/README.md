this is an API project built in python

it runs using fastapi

run the following command to install all dependencies
pip install -r requirements.txt

use this command to run the project locally

uvicorn api:app --host 0.0.0.0 --port 8000

run these commands to setup the project on docker

docker build -t app_name_here

use this command to run the project on docker
docker run -p 8000:8000 app_name_here

the service will run on port 8000
details about the service can be found at http://localhost:8000/docs


AI was used in this project to get details about how fastapi works, specifcally how to respond with customized response objects and how to read the response body of the request, it was also used to understand how the curl command line tool works and what parameters it needs, https://chatgpt.com/share/69d1956f-3f90-83e8-a313-5a1ab584467b


Repo Link https://github.com/cterry311/FirstPythonAPI.git