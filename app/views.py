from django.http import HttpResponse
from . import admin_manager
from . import moment_engine
from datetime import datetime
db = admin_manager.db


def get_timecode():
    year = str(datetime.now().year)
    month = str(datetime.now().month)
    day = str(datetime.now().day)
    hour = str(datetime.now().hour)
    minute = str(datetime.now().minute)
    second = str(datetime.now().second)

    return str(year + "-" + month + "-" + day + "-" + hour + "-" + minute + "-" + second)


def serve_gender_selection_page():
    # Serve gender selection page
    with open("html/pick_gender/index.html", "r") as file:
        content = str(file.read())

    return HttpResponse(content)


def home(request):

    # Client information
    headers = str(request.headers)
    db.reference("visitor_logs").push({
        "headers": headers,
        "time": get_timecode()
    })

    # Validate cookies
    gender = request.COOKIES.get("gender")

    if gender is None:
        return serve_gender_selection_page()
    else:
        if gender != "m" and gender != "f":
            return serve_gender_selection_page()

    # Serve webpage
    with open("html/home/index.html", "r") as file:
        content = str(file.read())

        username, picture, followers, bio, verified, total_user_count = moment_engine.retrieve_moment()

        # Replace Content
        content = content.replace("$$$USERNAME$$$", str(username))
        content = content.replace("$$$PICTURE$$$", str(picture))
        content = content.replace("$$$FOLLOWERS$$$", str(followers))
        content = content.replace("$$$BIO$$$", str(bio))
        content = content.replace("$$$TOTAL-USER-COUNT$$$", str(total_user_count))

        if verified:
            content = content.replace("$$$VERIFIED$$$", "inline-block")
            content = content.replace("$$$NOT-VERIFIED$$$", "none")
        else:
            content = content.replace("$$$VERIFIED$$$", "none")
            content = content.replace("$$$NOT-VERIFIED$$$", "inline-block")

        return HttpResponse(content)


def register(request):
    with open("html/register/index.html", "r") as file:
        content = str(file.read())

        username = str(db.reference("official_instagram").get())
        content = content.replace("$$$USERNAME$$$", username)

        return HttpResponse(content)
