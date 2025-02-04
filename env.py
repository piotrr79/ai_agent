import sys
import os
from decouple import config
# Tell syspath where to import modules from other folders in root direcotry
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class EnvReader():
    """ Get runtime params from env """
    
    def __init__(self):
        self

    def get_api_key(self):
        """ Get api key 

            Returns:
                Key string
        """
        if os.environ.get('OPENAI_API_KEY') is not None:   
            self.value = os.environ['OPENAI_API_KEY']
        else:
            self.value = config('OPENAI_API_KEY')
        
        return self.value

    def get_api_organisation(self):
        """ Get product page url from env 

            Returns:
                Api organisation string
        """
        if os.environ.get('OPENAI_ORGANIZATION') is not None:   
            self.value = os.environ['OPENAI_ORGANIZATION']
        else:
            self.value = config('OPENAI_ORGANIZATION')
        
        return self.value

    def get_project_id(self):
        """ Get project id

            Returns:
                Project id string
        """
        if os.environ.get('PROJECT_ID') is not None:   
            self.value = os.environ['PROJECT_ID']
        else:
            self.value = config('PROJECT_ID')
        
        return self.value