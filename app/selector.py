from . import admin_manager
import random
db = admin_manager.db

default_frequency = 0


def select_weighted_username(probabilities, weights):
    return str(random.choices(probabilities, weights=weights, k=1)[0])


def new(previous_username):
    # Data
    user_list = db.reference("users").get()
    frequencies = {}
    max_frequency = default_frequency

    # Parse frequencies
    for each in user_list:
        current_frequency = default_frequency

        if "frequency" in user_list[str(each)]:
            current_frequency = user_list[str(each)]["frequency"]

        # Match with max-frequency
        if current_frequency > max_frequency:
            max_frequency = current_frequency

        # Update list
        frequencies.update({
            str(each): current_frequency
        })
    max_frequency += 1

    # Generate chance list
    chance_list = {}

    for each in frequencies:
        chance_list.update({
            str(each): max_frequency - frequencies.get(each)
        })

    # Generate probabilities and weights list
    probabilities = []
    weights = []

    for each in chance_list:
        probabilities.append(str(each))
        weights.append(chance_list.get(each))

    # Select random weighted item
    selected_username = select_weighted_username(probabilities, weights)

    # Prevent selection of previous user
    if len(probabilities) > 1:
        while selected_username == str(previous_username).replace(".", ":"):
            selected_username = select_weighted_username(probabilities, weights)

    # Generate final user object
    selected_user = user_list[selected_username]

    # Return
    return selected_user["username"], selected_user["picture"], selected_user["followers"], selected_user["bio"], selected_user["verified"], len(user_list)
