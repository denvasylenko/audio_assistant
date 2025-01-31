from openai import OpenAI

class OpenAIAssistant:
    """
    OpenAIAssistant is a class that encapsulates the functionality to interact with OpenAI's API, specifically utilizing
    GPT models for generating summaries or responses based on the input text and user commands. This class simplifies the
    process of sending requests to OpenAI and processing the responses.

    Attributes:
        client (OpenAI): An instance of the OpenAI client configured with the provided API key.

    Parameters:
        openai_key (str): The API key for OpenAI. This key is used to authenticate requests to OpenAI's API.
    """

    def __init__(self, openai_key):
        """
        Initializes the OpenAIAssistant with an API key for OpenAI, setting up the client for further API interactions.

        Args:
            openai_key (str): The API key for OpenAI. This key is necessary to authenticate and authorize requests to
                              the OpenAI API.
        """
        self.client = OpenAI(api_key=openai_key)

    def assist(self, command, text, model="gpt-3.5-turbo-instruct", temperature=0.7, max_tokens=150):
        """
        Generates a response based on the given command and input text by querying OpenAI's GPT model. This method
        constructs a prompt that combines the command and text, sends it to the specified GPT model, and processes the response
        to extract the generated content.

        Args:
            command (str): The command or request that specifies what the assistant is expected to do with the input text.
                           This command guides the model's response generation.
            text (str): The input text to be processed.
            model (str): The identifier of the GPT model to use for generating the response. Defaults to "gpt-3.5-turbo-instruct".
            temperature (float): Controls the randomness in the response generation. Lower values make responses more deterministic.
                                 Defaults to 0.7.
            max_tokens (int): The maximum number of tokens in the generated response. Defaults to 150.

        Returns:
            str: The text generated by the GPT model based on the provided command and input text, formatted as a summary or
                 a response to the command.
        """
        prompt = f"""
        Your task is to assist user by providing accurate information, solutions, and creative content based input on user request.
        
        Request: ```{command}```
        
        Input: ```{text}```
        """
        
        response = self.client.completions.create(
            model=model,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
        summary = response.choices[0].text.strip()
        return summary
