# -*- coding: utf-8-*-
import datetime
import re
from client.app_utils import getTimezone
from semantic.dates import DateService

WORDS = ["TIME"]


def handle(text, speaker, requester, profile):
    """
        Reports the current time based on the user's timezone.

        Arguments:
        text -- user-input, typically transcribed speech
        speaker -- used to interact with the user (output)
        requester -- used to interact with the user (input)
        profile -- contains information related to the user (e.g., phone
                   number)
    """

    tz = getTimezone(profile)
    now = datetime.datetime.now(tz=tz)
    service = DateService()
    response = service.convertTime(now)
    speaker.clean_and_say("It is %s right now." % response)


def isValid(text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\btime\b', text, re.IGNORECASE))
