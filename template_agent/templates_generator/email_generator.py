## Generate email wtemplate ith email library or just as html
import json
from .connector import Connector

class EmailGenerator:
    """ EmailGenerator class """

    def __init__(self):
        self


    def generate_email_content(self, prompt, title, name, surname, to, cc, signature):
        """ Generate email content

            Returns:
                JSON
        """
        gtp_response = Connector.call_gpt(self, prompt)
        response = EmailGenerator.generate_template(self, title, name, surname, to, cc, signature)
        response.update({"Body" : ' '.join([str(item) for item in gtp_response]) })
        
        return json.dumps(response, indent = 1)
    

    def generate_email_template(self, prompt_response, title, name, surname, to, cc, signature):
        """ Generate email template

            Returns:
                JSON
        """
        response = EmailGenerator.generate_template(self, title, name, surname, to, cc, signature)
        response.update({"Body" : ' '.join([str(item) for item in prompt_response]) })
        
        return json.dumps(response, indent = 1)


    def generate_template(self, title, name, surname, to, cc, signature):
        """ Generate email template

            Returns:
                Dict
        """
        response = {}

        response.update({"Title" : title})
        response.update({"Name" : name + ' ' + surname})
        response.update({"To" : to})
        response.update({"Cc" : cc})
        response.update({"Footer" : signature})

        return response
    
    def stringify_ai_response(self, prompt_response):
        """ Stringify ai repsonse

            Returns:
                JSON
        """
        response = {}
        response.update({"Body" : ' '.join([str(item) for item in prompt_response]) })
        
        return json.dumps(response, indent = 1)
    
# x = EmailGenerator.generate_email_content(EmailGenerator)
# print(x)