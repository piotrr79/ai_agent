from django.conf import settings
from openai import OpenAI

class Connector:
    """ Connector class """

    def __init__(self):
        pass
    
    def call_gpt(self, prompt: str) -> list:
        """ Call GPT

            Returns:
                String
                
            @ToDo - Consider to log request Id, message, file, etc
        """
        response = []

        client = OpenAI(
        organization=settings.OPENAI_ORGANIZATION,
        project=settings.PROJECT_ID,
        api_key=settings.OPENAI_API_KEY
        )

        # @ToDo - move model name and settings to configuration (db or .env) 
        stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}], 
        stream=True)
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                response.append(chunk.choices[0].delta.content)

        return response