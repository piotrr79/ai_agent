import sys, json
from openai import OpenAI
from env import EnvReader

class Connector:
    """ Connector class """

    def __init__(self):
        self
    
    def call_gpt(self):
        client = OpenAI(
        organization=EnvReader.get_api_organisation(self),
        project=EnvReader.get_project_id(self),
        )
        
        stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Email generation content / @ToDo"}],
        stream=True)
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="")
