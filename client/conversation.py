# -*- coding: utf-8-*-
import logging
import signal
import os
from notifier import Notifier
from brain import Brain
from snowboy import snowboydecoder
import jasperpath

class Conversation(object):

    def __init__(self, speaker, speech_recognizer, mic, profile):
        self._logger = logging.getLogger(__name__)
        self.mic = mic
        self.speaker = speaker
        self.speech_recognizer = speech_recognizer
        self.profile = profile
        self.brain = Brain(self.speaker, self.mic, profile)
        self.notifier = Notifier(profile)
        self.interrupted = False

    def signal_handler(self, signal, frame):
        self.interrupted = True

    def interrupt_callback(self):
        return self.interrupted

    def startListenningActively(self):
        threshold = None
        self._logger.debug("Started to listen actively with threshold: %r",
                               threshold)
        self.speaker.play_wav_file(jasperpath.data('audio', 'beep_hi.wav'))
        audio_data = self.mic.listen()
        text = self.speech_recognizer.transcribe(audio_data)
        self.speaker.play_wav_file(jasperpath.data('audio', 'beep_lo.wav'))
        self._logger.debug("Stopped to listen actively with threshold: %r",
                               threshold)

        if text:
            self.brain.query(text)
        else:
            self.speaker.clean_and_say("Pardon?")

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
