import firebase_admin
from firebase_admin import credentials
from firebase_admin import db as database

db = database

# Initialize Admin
cred = credentials.Certificate("credential.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "[YOUR-DATABASE-URL]" #TODO: Add your database url here
})
