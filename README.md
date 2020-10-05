# Sample rest_api_demo

This repository contains boilerplate code for a RESTful API based on Flask and Flask-RESTPlus.

The code of this demo app is described in an article of the blog:
http://michal.karzynski.pl/blog/2016/06/19/building-beautiful-restful-apis-using-flask-swagger-ui-flask-restplus/

> Don't forget start the env with `source ./venv/bin/activate`

## Run the application

``` language:shellscript

# create virtaul environment
virtualenv -p `which python3` venv

# Start the python virtual environment
source venv/bin/activate

# install requirements
pip install -r requirements.txt

#  set up the app for development and start it
python setup.py develop

# Start the server with
python rest_api_demo/app.py

```

### For samples of API definition: 

[got to url](http://localhost:8888/api)

### For samples of Authorization: 

[got to url](http://localhost:8888/login)

Test the authorization with [it](http://localhost:8888/)

Get off in good terms with [it](http://localhost:8888/logout)
