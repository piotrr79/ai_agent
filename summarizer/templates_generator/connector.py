from django.conf import settings
from openai import OpenAI

class Connector:
    """ Connector class """

    def __init__(self):
        self
    
    def call_gpt(self, prompt):
        """ Call GPT

            Returns:
                String
                
            @ToDo - Log request Id. message, file, etc, e.g. for asynchronous processing (if needed)
        """
        response = []

        client = OpenAI(
        organization=settings.OPENAI_ORGANIZATION,
        project=settings.PROJECT_ID,
        api_key=settings.OPENAI_API_KEY
        )

        stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}], 
        stream=True)
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                # print(chunk.choices[0].delta.content, end="")
                # print(chunk.choices[0].delta.content)
                response.append(chunk.choices[0].delta.content)

        return response

# x = Connector.call_gpt(Connector)
# print(x)