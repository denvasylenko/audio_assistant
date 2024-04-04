import os
import time
from AudioRecorder import AudioRecorder
import pyaudio

class CommandRecorder:
    """
    The CommandRecorder class is designed to record audio commands, with functionality to automatically stop recording
    if a specified duration of silence is detected. This class uses an AudioRecorder instance for capturing audio data,
    providing a higher-level interface specifically for command recording scenarios.

    Attributes:
        save_path (str): Path to the directory where command recordings will be saved.
        silence_limit (int): Duration in seconds to wait for silence before stopping the recording.
        recorder (AudioRecorder): An instance of AudioRecorder for handling low-level audio recording operations.
        command_audio_path (str): Full file path where the current command recording will be saved.

    Parameters:
        save_path (str): The directory where command recordings should be saved.
        silence_limit (int): The maximum duration of silence (in seconds) that should be tolerated before
                             automatically stopping the recording. Defaults to 3 seconds.
        rate (int): The sample rate for the audio recording. Defaults to 16000 Hz.
        channels (int): The number of channels in the audio recording (1 for mono, 2 for stereo). Defaults to 1.
        format (pyaudio.PaFormat): The format of the audio data (e.g., pyaudio.paInt16). Defaults to pyaudio.paInt16.
    """
    def __init__(self, save_path, silence_limit=3, rate=16000, channels=1, format=pyaudio.paInt16):
        self.save_path = save_path
        self.silence_limit = silence_limit
        self.recorder = AudioRecorder(rate, channels, format)
        self.command_audio_path = os.path.join(self.save_path, "command.wav")

    def start_command_recording(self):
        """
        Initiates the recording of an audio command. The recording process continues until either a command is captured
        or the silence limit is reached, indicating that no further audio is being provided by the user.

        The method automatically handles the starting, buffering, and stopping of the audio recording, as well as
        saving the captured audio to a predefined file path.

        Returns:
            str: The path to the saved audio file containing the recorded command.
        """
        print("Start command recording.")
        self.recorder.start_recording()
        command_start_time = time.time()

        while True:
            data = self.recorder.read_data()
            if data:  # Check for actual audio data to ensure the recorder is capturing audio.
                if time.time() - command_start_time > self.silence_limit:
                    print("Stopping command recording due to silence.")
                    break

        self.recorder.save_audio(self.command_audio_path)
        self.recorder.stop_recording()
        return self.command_audio_path

    def stop_mic(self):
        """
        Safely terminates the audio recording session and releases the resources associated with the PyAudio instance.

        This method should be called to ensure proper cleanup of the audio system resources once recording operations
        are complete.
        """
        self.recorder.stop_mic()
