from django.conf import settings
import os
from ctransformers import AutoModelForCausalLM
# from transformers import AutoTokenizer, AutoModelForCausalLM
# import torch


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

        # model_name = 'llama-2-7b-chat.ggmlv3.q4_K_S.bin'
        # model_name = '/Volumes/Personal/Python/ai_agent/summarizer/ai_model/llama-2-7b-chat.ggmlv3.q4_K_S.bin'
        # tokenizer = AutoTokenizer.from_pretrained(model_name)
        # model = AutoModelForCausalLM.from_pretrained(model_name, device_map='auto')

        #llm = AutoModelForCausalLM.from_pretrained('llama-2-7b-chat.ggmlv3.q4_K_S.bin',  model_type='llama')
        #print(llm("AI is going to"))

        # inputs = tokenizer(prompt, return_tensors='pt')
        # Generate text
        ''' outputs = model.generate(
            inputs['input_ids'].to('cuda'),  # Send input to GPU if available
            max_length=100,  # Maximum length of the output
            num_return_sequences=1,  # Number of responses
            temperature=0.7,  # Adjust creativity level
            top_p=0.9,  # Nucleus sampling
        ) '''
        # Decode and print the output
        # generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # print(generated_text)



        llm = AutoModelForCausalLM.from_pretrained(
            model_path_or_repo_id = '/Volumes/Personal/Python/ai_agent/summarizer/libs/',  
            model_type = 'llama', 
            model_file = 'llama-2-7b-chat.ggmlv3.q4_K_S.bin',
            local_files_only = True)
        
        print(llm('What are the planets in Solar System'))

        return response

# x = Validator.call_llama(Validator)
# print(x)

prompt = 'What are the planets in Solar System'
x = Validator.call_llama(Validator, prompt)
print(x)

