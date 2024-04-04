import os
from SpotKeyword import SpotKeyword
from OpenAITranscriber import OpenAITranscriber
from OpenAIAssistant import OpenAIAssistant
from AudioRecorder import AudioRecorder
from CommandRecorder import CommandRecorder

class Assistant:
    """
    The Assistant class encapsulates the functionality for detecting a specified keyword in audio input,
    recording commands after the keyword detection, transcribing the audio to text, and summarizing the content.
    
    Attributes:
        spot_keyword (SpotKeyword): An instance of the SpotKeyword class for detecting a specific keyword in the audio.
        openAITranscriber (OpenAITranscriber): An instance of the OpenAITranscriber class for converting audio to text.
        openAIAssistant (OpenAIAssistant): An instance of the OpenAIAssistant class for generating response based on recorded command and text.
        recorder (AudioRecorder): An instance of the AudioRecorder class for recording audio.
    
    Args:
        vosk_model_path (str): The file path to the Vosk model used for keyword detection.
        keyword (str): The keyword to listen for in the audio input.
        openai_key (str): The API key for OpenAI used by the OpenAIAssistant and OpenAIAssistant.
    """

    def __init__(self, vosk_model_path, keyword, openai_key):
        self.spot_keyword = SpotKeyword(vosk_model_path, keyword)
        self.openAITranscriber = OpenAITranscriber(openai_key)
        self.openAIAssistant = OpenAIAssistant(openai_key)
        self.recorder = AudioRecorder()

    def start(self):
        """
        Starts the Assistant's audio processing workflow. This method manages the main audio recording,
        detects the specified keyword, records a subsequent command, transcribes both the main audio and the command,
        and finally generates response based on command.

        The workflow is as follows:
        1. Start recording audio continuously and listen for the keyword.
        2. Once the keyword is detected, stop the main recording.
        3. Start recording a command.
        4. If the user doesn't speak for 3 seconds, stop recording the command.
        5. Transcribe audio and the command recording into text.
        6. Generate a response based on the transcribed texts.
        """
        self.recorder.start_recording()  # Begin recording
        keyword_detected = False
        try:
            while not keyword_detected:
                data = self.recorder.read_data()  # Read data from the stream
                keyword_detected = self.spot_keyword.process_audio_data(data)

            print("Keyword detected, stopping recording.")

        finally:
            # Ensure the main recording is stopped and saved
            self.recorder.stop_recording()  
            dir_path = os.path.join(os.getcwd(), 'transcriptions')
            os.makedirs(dir_path, exist_ok=True)
            main_audio_path = os.path.join(dir_path, "sample.wav")
            self.recorder.save_audio(main_audio_path)  
            self.recorder.stop_mic()  # Cleanup the PyAudio instance

            # Handle command recording
            command_recorder = CommandRecorder(dir_path)
            command_audio_path = command_recorder.start_command_recording()
            command_recorder.stop_mic()

        # Transcribe and summarize
        command_transcription = self.openAITranscriber.transcribe_audio(command_audio_path)
        text_transcription = self.openAITranscriber.transcribe_audio(main_audio_path)
        print("Text Transcription:", text_transcription)
        print("Command Transcription:", command_transcription)
        respone = self.openAIAssistant.assist(command=command_transcription, text=text_transcription)
        print("Respone:", respone)
