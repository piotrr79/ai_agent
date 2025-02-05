from openai import OpenAI
from env import EnvReader

class Connector:
    """ Connector class """

    def __init__(self):
        self
    
    def call_gpt(self):
        """ Call GPT

            Returns:
                String

            @ToDo - Pass user input along file with data to GPT to generate summary for email content
            @ToDo - Log request Id. message, file, etc for asynchronous processing (if needed)
        """
        response = []

        client = OpenAI(
        organization=EnvReader.get_api_organisation(self),
        project=EnvReader.get_project_id(self),
        api_key=EnvReader.get_api_key(self)
        )
        
        stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say this is a test"}], # @ToDo - Email Template generation content
        stream=True)
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                # print(chunk.choices[0].delta.content, end="")
                # print(chunk.choices[0].delta.content)
                response.append(chunk.choices[0].delta.content)

        return response

x = Connector.call_gpt(Connector)
# print(x)