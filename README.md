# ChosenOne
Website that updates every 7.5 seconds to display profiles of random instagram users from the database.

## Services used
- **Django Framework** as a webserver
- **Firebase RealtimeDatabase** to store profiles of Instagram Users and Visitor Logs.

## Setup
1. Replace `credential.json` with your own Firebase Admin Service Account Secret.
2. Open `app/admin_manager.py` and replace *databaseURL* with your own Database URL.
3. Add your own **SECURITY_KEY** inside `project/settings.py`.
4. Execute the command below in the project root directory to start the webserver.
> `python3 manager.py runserver 0.0.0.0:80`

## Cold Start Problem
To register initial users for the website, use the *python script* I created to add users to the database. The script can also be used to add new users to the database when required.

### Add users to the Database
Clone the project from the link below and use the `register.py` script to register new users. You must pass the instagram username of the person as the first argument and optionally pass "yes" as the second argument to register the user as **verified**.
> [https://github.com/moonstorage/chosenone-extras](https://github.com/moonstorage/chosenone-extras)