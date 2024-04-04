import pyaudio
import wave

class AudioRecorder:
    """
    AudioRecorder handles audio recording functionalities, including starting and stopping recordings,
    reading data from the microphone, buffering this data, and saving it to a file.

    Attributes:
        rate (int): Sample rate of the audio recording.
        channels (int): Number of channels in the audio recording (1 for mono, 2 for stereo).
        format (pyaudio.paFormat): Audio format as defined by PyAudio. Example: pyaudio.paInt16.
        mic (pyaudio.PyAudio): Instance of PyAudio used to interact with the system's audio interface.
        buffer (list): A list to accumulate audio data frames read from the microphone.
        stream (pyaudio.Stream): The audio stream from which the audio data is being captured.
    """

    def __init__(self, rate=16000, channels=1, format=pyaudio.paInt16):
        """
        Initializes the AudioRecorder with the specified audio parameters.

        Args:
            rate (int): The sample rate of the audio (in Hz).
            channels (int): The number of audio channels (1 for mono, 2 for stereo).
            format (pyaudio.paFormat): The format of the audio data (e.g., pyaudio.paInt16).
        """
        self.rate = rate
        self.channels = channels
        self.format = format
        self.mic = pyaudio.PyAudio()
        self.buffer = []
        self.stream = None

    def start_recording(self, buffer_size=4096):
        """
        Starts the audio recording by opening a stream and beginning to capture data.

        Args:
            buffer_size (int): The number of frames per buffer.
        """
        self.stream = self.mic.open(format=self.format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=buffer_size)
        self.stream.start_stream()

    def read_data(self, buffer_size=4096):
        """
        Reads data from the audio stream and appends it to the internal buffer.

        Args:
            buffer_size (int): The number of frames to read from the stream at once.

        Returns:
            data (bytes): The audio data read from the stream.
        """
        if not self.stream:
            raise RuntimeError("Stream is not started.")
        data = self.stream.read(buffer_size, exception_on_overflow=False)
        self.buffer.append(data)
        return data

    def save_audio(self, filename):
        """
        Saves the audio data accumulated in the buffer to a WAV file.

        Args:
            filename (str): The path and filename where the audio should be saved.
        """
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.mic.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.buffer))
        wf.close()
        print(f"Audio saved to {filename}")

    def stop_recording(self):
        """
        Stops the audio recording by stopping and closing the stream, and clearing the buffer.
        """
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.stream = None
        self.buffer = []

    def stop_mic(self):
        """
        Terminates the PyAudio instance, effectively stopping all audio processing and releasing resources.
        """
        self.mic.terminate()
