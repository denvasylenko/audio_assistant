from openai import OpenAI

class OpenAITranscriber:
    """
    The OpenAITranscriber class interfaces with the OpenAI API to transcribe audio files into text using OpenAI's
    advanced machine learning models. It is specifically designed to leverage the Whisper model for audio
    transcription, offering a simple and effective method for converting speech in audio files to written text.

    Attributes:
        client (OpenAI): An instance of the OpenAI client, configured with the user's API key.

    Parameters:
        openai_key (str): The API key for accessing OpenAI's services. This key is required to authenticate
                          and authorize the transcription requests to the OpenAI API.
    """

    def __init__(self, openai_key):
        """
        Initializes a new instance of the OpenAITranscriber class with the given OpenAI API key.

        Args:
            openai_key (str): The API key for OpenAI, used to authenticate requests to the OpenAI API.
        """
        self.client = OpenAI(api_key=openai_key)

    def transcribe_audio(self, audio_file_path):
        """
        Transcribes the given audio file into text using OpenAI's Whisper model.

        This method opens the specified audio file, sends it to OpenAI for transcription, and then
        returns the transcribed text. It is designed to handle various audio formats and languages
        supported by the Whisper model, making it versatile for different transcription needs.

        Args:
            audio_file_path (str): The path to the audio file that will be transcribed. The file should
                                   be accessible and in a format supported by the Whisper model.

        Returns:
            str: The text transcribed from the audio file. If the transcription is successful, this will
                 contain the spoken content of the audio file as text. If an error occurs, the method
                 may raise an exception or return an error message, depending on the OpenAI API response.
        """
        with open(audio_file_path, "rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcription.text
