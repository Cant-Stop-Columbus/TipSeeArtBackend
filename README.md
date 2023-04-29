## Windows users
For Windows, you may need to preface the below commands with `python -m`
Ex: `python -m uvicorn main:app --reload`

### Installing pip on Windows
Assuming you have python and curl installed, run the following commands
`curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`
`python get-pip.py`

## Downloading required packages
`pip install -r requirements.txt`

## Alembic Database Management Commands
Creates the tables in your database
### Generate a new migration based on changes to models in api/models
`alembic revision --autogenerate`
### Run all new migrations
`alembic upgrade head`

## Running the Api
`uvicorn main:app --reload`

## Swagger
Append `/docs` to the end of the URL for the Swagger page
Ex: `http://localhost:8000/docs`