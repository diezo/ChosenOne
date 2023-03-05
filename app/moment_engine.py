import base64
from datetime import datetime
import requests
from . import admin_manager
from . import selector

db = admin_manager.db
frequency_update_unit = 10
default_frequency_unit = 0


def pic(picture):
    return base64.b64encode(requests.get(picture).content).decode("utf-8")


def update_frequency(username):
    previous_frequency_raw = db.reference(f"users/{str(username).replace('.', ':')}/frequency").get()
    previous_frequency = default_frequency_unit

    if previous_frequency_raw is not None:
        previous_frequency = int(str(previous_frequency_raw))

    db.reference(f"users/{str(username).replace('.', ':')}/frequency").set(previous_frequency + frequency_update_unit)


def retrieve_moment():
    moment_user = db.reference("moment_user").get()

    if moment_user is not None:
        last_moment = str(moment_user["moment"])
        current_moment = str(get_minute_code())

        # Compare moments
        if last_moment == current_moment:
            # Match
            username = moment_user["username"]
            picture = moment_user["picture"]
            followers = moment_user["followers"]
            bio = moment_user["bio"]
            verified = moment_user["verified"]

            # Calculate total users
            users = db.reference("users").get()
            total_user_count = len(users)

            data = username, pic(picture), followers, bio, verified, total_user_count
            update_frequency(data[0])
            return data
        else:
            data = unmatch_condition(moment_user["username"])
            update_frequency(data[0])
            return data
    else:
        data = unmatch_condition(moment_user["username"])
        update_frequency(data[0])
        return data


def unmatch_condition(previous_username):
    # Unmatch
    print("Creating new user...")
    username, picture, followers, bio, verified, total_user_count = selector.new(previous_username)

    db.reference("moment_user").set({
        "moment": get_minute_code(),
        "username": username,
        "picture": picture,
        "followers": followers,
        "bio": bio,
        "verified": verified
    })

    return username, pic(picture), followers, bio, verified, total_user_count


def get_minute_code():
    year = str(datetime.now().year)
    month = str(datetime.now().month)
    day = str(datetime.now().day)
    hour = str(datetime.now().hour)
    minute = str(datetime.now().minute)
    second = datetime.now().second

    second_value = "1"

    if second > 52.5:
        second_value = "8"
    elif second > 45:
        second_value = "7"
    elif second > 37.5:
        second_value = "6"
    elif second > 30:
        second_value = "5"
    elif second > 22.5:
        second_value = "4"
    elif second > 15:
        second_value = "3"
    elif second > 7.5:
        second_value = "2"

    return str(year + month + day + hour + minute + second_value)
