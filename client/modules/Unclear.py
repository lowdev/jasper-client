# -*- coding: utf-8-*-
from sys import maxint
import random

WORDS = []

PRIORITY = -(maxint + 1)


def handle(text, speaker, mic, profile):
    """
        Reports that the user has unclear or unusable input.

        Arguments:
        text -- user-input, typically transcribed speech
        speaker -- used to interact with the user (output)
        mic -- used to interact with the user (input)
        profile -- contains information related to the user (e.g., phone
                   number)
    """

    messages = ["I'm sorry, could you repeat that?",
                "My apologies, could you try saying that again?",
                "Say that again?", "I beg your pardon?"]

    message = random.choice(messages)

    speaker.clean_and_say(message)


def isValid(text):
    return True
