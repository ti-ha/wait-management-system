# Setup on local machines (*NOT CSE*)
The following instructions are for running the system on your local machine.
They will not work on CSE Servers (Scroll down to the next heading for CSE
specific instructions)

## Backend Setup
To setup, you must have Python 3.9 installed. Get it here:
https://www.python.org/downloads/release/python-3911/


### Windows

In the working directory, run the following:
```
$ chmod +x ./install
$ ./install
``` 
to install dependencies. This will
automatically install a virtual environment and allocate the correct packages to
that virtual environment, then build the frontend, before printing an OK
message.

Then, in a separate terminal, run the following command in the working directory
to run the server:

```
$ source venv/Scripts/activate
$ python app.py
```

If you use a different command to run your installation of Python 3.9
for any reason, substitute it for `python` in the command above.

### Mac

In the working directory, run the following:
```
$ chmod +x ./install
$ ./install
``` 
to install dependencies. This will
automatically install a virtual environment and allocate the correct packages to
that virtual environment, then build the frontend, before printing an OK
message.

Then, in a separate terminal, run the following command in the working directory
to run the server:

```
$ source venv/bin/activate
$ python app.py
```

If you use a different alias to run your installation of Python 3.9
for any reason, substitute it for `python` in the command above.

________________________________________________________________________________
## Running the Frontend (Win/MacOS/Linux)

Make sure you have the latest version of node installed.

Ensure you are in the frontend folder. (cd `frontend`)

Run `npm install`.
Once that is completed, run `npm start`.

The frontend will be running on http://localhost:3000

________________________________________________________________________________
# Setup (CSE)

Setup for CSE has been streamlined for submission purposes to remove the chances
of an error occurring preventing markers from properly evaluating the codebase.

## Step 1
In the working directory, run the following:
```
$ chmod +x ./install
$ ./install
``` 
to install dependencies. This will
automatically install a virtual environment and allocate the correct packages to
that virtual environment, then build the frontend, before printing an OK
message.

## Step 2
In the working directory, run the following:
```
$ chmod +x ./run
$ ./run
```

And wait. CSE Servers are not by any means fast; The server will take a while to
get started. Once the server is ready, it will automatically open a browser with
the app landing page.

# Database configuration

For the purposes of marking, we have included two `.db` files in the root
directory of the project. To use either one, simply rename it to `wms_db.db` and
restart the Python server.

`wms_db_empty.db` Contains a complete menu, and three users, but no order data,
and matches the `wms_db.db` working file included in the repository.

`wms_db_with_orderdata.db` Contains all of the data in `wms_db_empty.db` in
addition to historical user data.

# Sample user credentials

We have added one of each Staff member type to the system so you can log in and
test functionality.

## Manager
firstname: Manager

lastname: One

password: Manager

## Wait Staff
firstname: WaitStaff

lastname: One

password: waitstaff

## Kitchen Staff
firstname: KitchenStaff

lastname: One

password: kitchenstaff