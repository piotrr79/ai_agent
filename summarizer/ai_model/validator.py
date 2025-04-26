from pathlib import Path
from ctransformers import AutoModelForCausalLM

class Validator:
    """ Validator class """

    def __init__(self):
       pass
    
    def call_internal_model(self, prompt: str, tokens: int, temp: float) -> list:
        """ Call Llama

            Returns:
                List
        """

        response = []
        
        app_dir = Path(__file__).resolve().parent.parent.parent.parent

        # @ToDo - move model names to configuration (db or .env) 
        llm = AutoModelForCausalLM.from_pretrained(
            model_path_or_repo_id = str(app_dir) + '/ai_agent/summarizer/libs/', 
            model_type = 'llama', 
            model_file = 'llama-2-7b-chat.ggmlv3.q4_K_S.bin',
            local_files_only = True)
        
        # @ToDo - move max_new_tokens and temperature to configuration (db or .env) 
        output = llm(prompt, max_new_tokens=tokens, temperature=temp)        
        #response.append(output.replace("?\n ", "").replace("\n\n", ""))      
        response.append(output)

        return response

