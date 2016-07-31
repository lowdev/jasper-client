# -*- coding: utf-8-*-
import wolframalpha
import Unclear

WORDS = []

PRIORITY = 1

def handle(text, speaker, requester, profile):
    """
        Request on wolfram alpha :-).

        Arguments:
        text -- user-input, typically transcribed speech
        speaker -- used to interact with the user (output)
        requester -- used to interact with the user (input)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    
    client = wolframalpha.Client(profile['wolfram-alpha_app_id'])
    res = client.query(text)
    for pod in res.pods:
        print("text : " + pod.title)
        speaker.clean_and_say(pod.text)
        #return

    Unclear.handle(text, speaker, requester, profile)


def isValid(text):
    return True
