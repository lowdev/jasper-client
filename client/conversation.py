# -*- coding: utf-8-*-
import logging
import signal
import os
from snowboy import snowboydecoder

class Conversation(object):

    def __init__(self, requester, brain):
        self._logger = logging.getLogger(__name__)
        self.requester = requester
        self.brain = brain
        self.interrupted = False

    def signal_handler(self, signal, frame):
        self.interrupted = True

    def interrupt_callback(self):
        return self.interrupted

    def startListenningActively(self):
        text = requester.make_a_request()

        if text:
            self.brain.query(text)
        else:
            self.brain.say("Pardon?")

    def handleForever(self):
        """
        Delegates user input to the handling function when activated.
        """
        self._logger.info("Starting to handle conversation")

        TOP_DIR = os.path.dirname(os.path.abspath(__file__))
        MODEL_FILE = os.path.join(TOP_DIR, "snowboy/model.pmdl")

        signal.signal(signal.SIGINT, self.signal_handler)

        print("A moment of silence, please...")
        self.mic.adjust_for_ambient_noise()

        detector = snowboydecoder.HotwordDetector(MODEL_FILE, sensitivity=0.5)
        print('Listening... Press Ctrl+C to exit')

        # main loop
        detector.start(detected_callback=self.startListenningActively,
               interrupt_check=self.interrupt_callback,
               sleep_time=0.03)

        detector.terminate()
