import json
from vosk import Model, KaldiRecognizer

class SpotKeyword:
    """
    The SpotKeyword class utilizes the Vosk speech recognition library to detect specific keywords in audio data. 
    It is designed to process live or pre-recorded audio streams and identify occurrences of a predefined keyword.

    Attributes:
        model (vosk.Model): An instance of the Vosk model used for speech recognition.
        recognizer (vosk.KaldiRecognizer): The speech recognizer that processes audio data using the Vosk model.
        keyword (str): The specific keyword or phrase that this instance is set to detect in audio streams.

    Parameters:
        model_path (str): The file path to the Vosk model directory. This model is used to initialize the speech recognizer.
        keyword (str): The keyword or phrase to be detected in the audio data. The detection process is case-sensitive.
    """

    def __init__(self, model_path, keyword):
        """
        Initializes the SpotKeyword instance with a specified Vosk model and a keyword.

        Args:
            model_path (str): The path to the Vosk model directory used for speech recognition.
            keyword (str): The specific keyword or phrase to detect in audio streams.
        """
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.keyword = keyword

    def process_audio_data(self, data):
        """
        Processes a chunk of audio data through the speech recognizer to check for the presence of the specified keyword.

        This method examines both the final and the partial recognition results to determine if the keyword has been spoken.
        It's suitable for use in real-time applications where immediate keyword detection is required.

        Args:
            data (bytes): A chunk of audio data to be processed. The audio data should be in the format expected by
                          the Vosk model (typically 16kHz, mono, PCM).

        Returns:
            bool: True if the keyword is detected in the audio data; False otherwise.
        """
        if self.recognizer.AcceptWaveform(data):
            # Check the final recognition result for the keyword.
            result_json = self.recognizer.Result()
            result_data = json.loads(result_json)
            if 'text' in result_data and self.keyword in result_data['text']:
                return True
        # Check the partial (in-progress) recognition results for the keyword.
        partial_json = self.recognizer.PartialResult()
        partial_data = json.loads(partial_json)
        partial_text = partial_data.get('partial', '')
        return self.keyword in partial_text
