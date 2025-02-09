## Generate email wtemplate ith email library or just as html
import json
from .connector import Connector

class EmailGenerator:
    """ EmailGenerator class """

    def __init__(self):
        self

    def generate_email_content(self):
        """ Generate email content

            Returns:
                JSON
        """
        gtp_response = Connector.call_gpt(self)
        response = EmailGenerator.generate_template(self)
        response.update({"Body" : ' '.join([str(item) for item in gtp_response]) })
        
        return json.dumps(response, indent = 1)

    def generate_template(self):
        """ Generate email template

            Returns:
                Dict
        """
        response = {}

        response.update({"Title" : "Email Title"})
        response.update({"Name" : "Name Surname"})
        response.update({"To" : "email@email.email"})
        response.update({"Cc" : "cc@email.email"})
        response.update({"Footer" : "Email Signature"})

        return response
    
# x = EmailGenerator.generate_email_content(EmailGenerator)
# print(x)