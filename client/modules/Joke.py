# -*- coding: utf-8-*-
import random
import re
from client import jasperpath

WORDS = ["JOKE", "KNOCK KNOCK"]


def getRandomJoke(filename=jasperpath.data('text', 'JOKES.txt')):
    jokeFile = open(filename, "r")
    jokes = []
    start = ""
    end = ""
    for line in jokeFile.readlines():
        line = line.replace("\n", "")

        if start == "":
            start = line
            continue

        if end == "":
            end = line
            continue

        jokes.append((start, end))
        start = ""
        end = ""

    jokes.append((start, end))
    joke = random.choice(jokes)
    return joke


def handle(text, speaker, requester, profile):
    """
        Responds to user-input, typically speech text, by telling a joke.

        Arguments:
        text -- user-input, typically transcribed speech
        speaker -- used to interact with the user (output)
        requester -- used to interact with the user (input)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    joke = getRandomJoke()

    speaker.clean_and_say("Knock knock")

    def firstLine(text):
        speaker.clean_and_say(joke[0])

        def punchLine(text):
            speaker.clean_and_say(joke[1])

        punchLine(requester.make_a_request())

    firstLine(requester.make_a_request())


def isValid(text):
    """
        Returns True if the input is related to jokes/humor.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bjoke\b', text, re.IGNORECASE))
