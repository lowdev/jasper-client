import jasperpath
import logging

class Requester(object):
    def __init__(self, speaker, speech_recognizer, mic):
        self._logger = logging.getLogger(__name__)
        self.mic = mic
        self.speaker = speaker
        self.speech_recognizer = speech_recognizer

    def make_a_request(self):
        self.speaker.play_wav_file(jasperpath.data('audio', 'beep_hi.wav'))
        audio_data = self.mic.listen()
        text = self.speech_recognizer.transcribe(audio_data)
        self.speaker.play_wav_file(jasperpath.data('audio', 'beep_lo.wav'))
	
        return text
