# -*- coding: utf-8-*-
import random
import re

WORDS = ["MEANING", "OF", "LIFE"]


def handle(text, speaker, requester, profile):
    """
        Responds to user-input, typically speech text, by relaying the
        meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
        speaker -- used to interact with the user (output)
        requester -- used to interact with the user (input)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    messages = ["It's 42, you idiot.",
                "It's 42. How many times do I have to tell you?"]

    message = random.choice(messages)

    speaker.clean_and_say(message)


def isValid(text):
    """
        Returns True if the input is related to the meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bmeaning of life\b', text, re.IGNORECASE))
