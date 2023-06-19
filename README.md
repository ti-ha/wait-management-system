# capstone-project-3900w18cromanticcheese

## Running the Server
To setup, you must have the latest version of python 3 installed.

## Windows

Run `. venv/Scripts/activate` in the working directory to initialise the virtual environment.

Then run `python app.py` to start the Flask application. 
The server will be running on http://localhost:5000

## Mac/UNIX

Run `source venv/Scripts/activate` in the working directory to initialise the virtual environment.

Then run `python app.py` to start the Flask application. 
The server will be running on http://localhost:5000

________________________________________________________________________________
## Running the Frontend

Make sure you have the latest version of node installed.

Ensure you are in the frontend folder. (cd `frontend`)

Run `npm install`.
Once that is completed, run `npm start`.

The frontend will be running on http://localhost:3000

## Creating the database

Make sure you have the latest version of PostgreSQL installed and the virtual environment running

### Windows

Open psql.exe and run the following command:
```
$   \i 'C:/%PATHTOREPO%/create_db.sql'
```

### Mac/UNIX

In the working directory, run the following:
```
$   initdb /usr/local/var/postgres
$   pg_ctl -D /usr/local/var/postgres start
$   psql -U postgres -f %PATHTOREPO%/create_db_.sql
```

## Running the database

With the virtual environment running, run `python init_db.py` in the working directory
