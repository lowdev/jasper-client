# -*- coding: utf-8-*-
"""
    The Mic class handles all interactions with the microphone.
"""
import logging
import tempfile
import wave
import audioop
import pyaudio
import math
import collections
from audiodata from AudioData

class Mic:

    speechRec = None
    speechRec_persona = None
    RATE = 16000
    CHUNK = 1024

    def __init__(self, active_stt_engine):
        """
        Initiates the pocketsphinx instance.

        Arguments:
        acive_stt_engine -- performs STT while Jasper is in active listen mode
        """
        self._logger = logging.getLogger(__name__)
        self.active_stt_engine = active_stt_engine
        self._logger.info("Initializing PyAudio. ALSA/Jack error messages " +
                          "that pop up during this process are normal and " +
                          "can usually be safely ignored.")
        self._audio = pyaudio.PyAudio()
        self._logger.info("Initialization of PyAudio completed.")

        self.format = pyaudio.paInt16
        self.SAMPLE_WIDTH = pyaudio.get_sample_size(self.format)

        self.energy_threshold = 300 # minimum audio energy to consider for recording
        self.dynamic_energy_threshold = True
        self.dynamic_energy_adjustment_damping = 0.15
        self.dynamic_energy_ratio = 1.5
        self.pause_threshold = 0.8 # seconds of non-speaking audio before a phrase is considered complete
        self.phrase_threshold = 0.3 # minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops)
        self.non_speaking_duration = 0.5 # seconds of non-speaking audio to keep on both sides of the recording

    def adjust_for_ambient_noise(self, duration = 1):
        """
        Adjusts the energy threshold dynamically using audio from ``source`` (an ``AudioSource`` instance) to account for ambient noise.
        Intended to calibrate the energy threshold with the ambient energy level. Should be used on periods of audio without speech - will stop early if any speech is detected.
        The ``duration`` parameter is the maximum number of seconds that it will dynamically adjust the threshold for before returning. This value should be at least 0.5 in order to get a representative sample of the ambient noise.
        """
        stream = self._audio.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.RATE,
                                  input=True,
                                  frames_per_buffer=self.CHUNK)

        assert self.pause_threshold >= self.non_speaking_duration >= 0

        seconds_per_buffer = (self.CHUNK + 0.0) / self.RATE
        elapsed_time = 0

        # adjust energy threshold until a phrase starts
        while True:
            elapsed_time += seconds_per_buffer
            if elapsed_time > duration: break
            buffer = stream.read(self.CHUNK)
            energy = audioop.rms(buffer, self.SAMPLE_WIDTH) # energy of the audio signal

            # dynamically adjust the energy threshold using assymmetric weighted average
            damping = self.dynamic_energy_adjustment_damping ** seconds_per_buffer # account for different chunk sizes and rates
            target_energy = energy * self.dynamic_energy_ratio
            self.energy_threshold = self.energy_threshold * damping + target_energy * (1 - damping)

    def listen(self, timeout = None):
        """
        Records a single phrase from ``source`` (an ``AudioSource`` instance) into an ``AudioData`` instance, which it returns.
        This is done by waiting until the audio has an energy above ``recognizer_instance.energy_threshold`` (the user has started speaking), and then recording until it encounters ``recognizer_instance.pause_threshold`` seconds of non-speaking or there is no more audio input. The ending silence is not included.
        The ``timeout`` parameter is the maximum number of seconds that it will wait for a phrase to start before giving up and throwing an ``speech_recognition.WaitTimeoutError`` exception. If ``timeout`` is ``None``, it will wait indefinitely.
        """

        stream = self._audio.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.RATE,
                                  input=True,
                                  frames_per_buffer=self.CHUNK)

        seconds_per_buffer = (self.CHUNK + 0.0) / self.RATE
        pause_buffer_count = int(math.ceil(self.pause_threshold / seconds_per_buffer)) # number of buffers of non-speaking audio before the phrase is complete
        phrase_buffer_count = int(math.ceil(self.phrase_threshold / seconds_per_buffer)) # minimum number of buffers of speaking audio before we consider the speaking audio a phrase
        non_speaking_buffer_count = int(math.ceil(self.non_speaking_duration / seconds_per_buffer)) # maximum number of buffers of non-speaking audio to retain before and after

        # read audio input for phrases until there is a phrase that is long enough
        elapsed_time = 0 # number of seconds of audio read
        while True:
            frames = collections.deque()

            # store audio input until the phrase starts
            while True:
                elapsed_time += seconds_per_buffer
                if timeout and elapsed_time > timeout: # handle timeout if specified
                    raise WaitTimeoutError("listening timed out")

                buffer = stream.read(self.CHUNK)
                if len(buffer) == 0: break # reached end of the stream
                frames.append(buffer)
                if len(frames) > non_speaking_buffer_count: # ensure we only keep the needed amount of non-speaking buffers
                    frames.popleft()

                # detect whether speaking has started on audio input
                energy = audioop.rms(buffer, self.SAMPLE_WIDTH) # energy of the audio signal
                if energy > self.energy_threshold: break

                # dynamically adjust the energy threshold using assymmetric weighted average
                if self.dynamic_energy_threshold:
                    damping = self.dynamic_energy_adjustment_damping ** seconds_per_buffer # account for different chunk sizes and rates
                    target_energy = energy * self.dynamic_energy_ratio
                    self.energy_threshold = self.energy_threshold * damping + target_energy * (1 - damping)

            # read audio input until the phrase ends
            pause_count, phrase_count = 0, 0
            while True:
                elapsed_time += seconds_per_buffer

                buffer = stream.read(self.CHUNK)
                if len(buffer) == 0: break # reached end of the stream
                frames.append(buffer)
                phrase_count += 1

                # check if speaking has stopped for longer than the pause threshold on the audio input
                energy = audioop.rms(buffer, self.SAMPLE_WIDTH) # energy of the audio signal
                if energy > self.energy_threshold:
                    pause_count = 0
                else:
                    pause_count += 1
                if pause_count > pause_buffer_count: # end of the phrase
                    break

            # check how long the detected phrase is, and retry listening if the phrase is too short
            phrase_count -= pause_count
            if phrase_count >= phrase_buffer_count: break # phrase is long enough, stop listening

        # obtain frame data
        for i in range(pause_count - non_speaking_buffer_count): frames.pop() # remove extra non-speaking frames at the end
        frame_data = b"".join(list(frames))

        return AudioData(frame_data, source.RATE, source.SAMPLE_WIDTH)

    def __del__(self):
        self._audio.terminate()

    def getScore(self, data):
        rms = audioop.rms(data, 2)
        score = rms / 3
        return score

    def activeListen(self, THRESHOLD=None, LISTEN=True, MUSIC=False):
        """
            Records until a second of silence or times out after 12 seconds

            Returns the first matching string or None
        """

        options = self.activeListenToAllOptions(THRESHOLD, LISTEN, MUSIC)
        if options:
            return options[0]

    def activeListenToAllOptions(self, THRESHOLD=None, LISTEN=True,
                                 MUSIC=False):
        """
            Records until a second of silence or times out after 12 seconds

            Returns a list of the matching options or None
        """

        LISTEN_TIME = 12
        THRESHOLD = self.energy_threshold

        # prepare recording stream
        stream = self._audio.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.RATE,
                                  input=True,
                                  frames_per_buffer=self.CHUNK)

        frames = []
        # increasing the range # results in longer pause after command
        # generation
        lastN = [THRESHOLD * 1.2 for i in range(30)]

        for i in range(0, self.RATE / self.CHUNK * LISTEN_TIME):

            data = stream.read(self.CHUNK)
            frames.append(data)
            score = self.getScore(data)

            lastN.pop(0)
            lastN.append(score)

            average = sum(lastN) / float(len(lastN))

            # TODO: 0.8 should not be a MAGIC NUMBER!
            if average < THRESHOLD * 0.8:
                break

        # save the audio data
        stream.stop_stream()
        stream.close()

        with tempfile.SpooledTemporaryFile(mode='w+b') as f:
            wav_fp = wave.open(f, 'wb')
            wav_fp.setnchannels(1)
            wav_fp.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
            wav_fp.setframerate(self.RATE)
            wav_fp.writeframes(''.join(frames))
            wav_fp.close()
            f.seek(0)
            return self.active_stt_engine.transcribe(f)
