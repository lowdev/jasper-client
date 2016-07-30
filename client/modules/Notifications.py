# -*- coding: utf-8-*-
import re
import facebook


WORDS = ["FACEBOOK", "NOTIFICATION"]


def handle(text, speaker, requester, profile):
    """
        Responds to user-input, typically speech text, with a summary of
        the user's Facebook notifications, including a count and details
        related to each individual notification.

        Arguments:
        text -- user-input, typically transcribed speech
        speaker -- used to interact with the user (output)
        requester -- used to interact with the user (input)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    oauth_access_token = profile['keys']['FB_TOKEN']

    graph = facebook.GraphAPI(oauth_access_token)

    try:
        results = graph.request("me/notifications")
    except facebook.GraphAPIError:
        speaker.clean_and_say("I have not been authorized to query your Facebook. If you " +
                "would like to check your notifications in the future, " +
                "please visit the Jasper dashboard.")
        return
    except:
        speaker.clean_and_say(
            "I apologize, there's a problem with that service at the moment.")

    if not len(results['data']):
        speaker.clean_and_say("You have no Facebook notifications. ")
        return

    updates = []
    for notification in results['data']:
        updates.append(notification['title'])

    count = len(results['data'])
    speaker.clean_and_say("You have " + str(count) +
            " Facebook notifications. " + " ".join(updates) + ". ")

    return


def isValid(text):
    """
        Returns True if the input is related to Facebook notifications.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bnotification|Facebook\b', text, re.IGNORECASE))
