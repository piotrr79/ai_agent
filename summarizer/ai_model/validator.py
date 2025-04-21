from pathlib import Path
from ctransformers import AutoModelForCausalLM

class Validator:
    """ Connector class """

    def __init__(self):
       pass
    
    def call_llama(self, prompt):
    #def call_llama(self):
        """ Call Llama

            Returns:
                String

        """

        response = []
        
        app_dir = Path(__file__).resolve().parent.parent.parent.parent

        llm = AutoModelForCausalLM.from_pretrained(
            model_path_or_repo_id = str(app_dir) + '/ai_agent/summarizer/libs/', 
            model_type = 'llama', 
            model_file = 'llama-2-7b-chat.ggmlv3.q4_K_S.bin',
            local_files_only = True)
        
        output = llm(prompt, max_new_tokens=60, temperature=0.5)

        # output.replace("?\n ", "")
        # output.replace("\n\n", "")
        
        response.append(output.replace("?\n ", ""))      

        return response

# prompt = 'How many planets are in Solar System'
prompt = 'Does the text attached contains sensitive data, even fictional. Please answer with Yes or No: Jessica Thompson, born on July 14, 1982, is a marketing analyst living at 4827 Willow Creek Dr, Apt 3B, Springfield, IL 62704. She works for BluePeak Strategies Inc. and can be reached at (217) 555-9321 or via email at jessica.thompson82@examplemail.com. Her online credentials include the username "jthompson82" and the password "PurpleSunset!92" (for demo purposes only). Jessica holds a dummy credit card number 4111 1111 1111 1111, with an expiration date of 09/26 and CVV 321. Her fictional social security number is 123-45-6789. Outside of work, she enjoys baking, running, and collecting vintage postcards, and shares her home with her golden retriever, Milo.'
x = Validator.call_llama(Validator, prompt)
print(x)

