import time
import os
import torch
from transformers import ( 
    AutoTokenizer, 
    AutoModelForCausalLM,
    BitsAndBytesConfig,
    pipeline,
    )
#from peft import LoraConfig, PeftModel
#from trl import SFTTrainer, SFTConfig

from utils import *


class LlamaModel:
    def __init__(self, model_name, config):
        self.config = config
        self.verbose = config['verbose']
        self.model_path = os.path.join(config['hf_model_folder'], model_name)
        if 'bitsandbytes' in config:
            self.bnb_config = BitsAndBytesConfig(**config['bitsandbytes'])
            self.dtype = self.bnb_config.bnb_4bit_compute_dtype
        else:
            self.bnb_config = None
            self.dtype = torch.float16

        # Check if we can load the model on a GPU
        self.device_map, self.device_type = get_device_map()
        if self.device_type == "cuda" and 'bitsandbytes' in config and self.verbose:
            check_bf16_compatibility(config['bitsandbytes'])

        # Load base model
        if self.bnb_config:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                quantization_config=self.bnb_config,
                device_map=self.device_map,
            )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                torch_dtype=self.dtype,
                device_map=self.device_map,
            )

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.padding_side = "right"

    def init_pipeline(self):
        # Create inference pipeline
        self.pipeline = pipeline(
            task="text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            torch_dtype=self.dtype,
        )

        # Set terminators
        self.terminators = [
            self.pipeline.tokenizer.eos_token_id,
            self.pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]



    def get_response(self, query, max_tokens=1028, temperature=0.1, top_p=0.9):

        # Initialize pipeline
        if not hasattr(self, 'pipe'):
            self.init_pipeline()
        
        print("Prompting the model...")
        start_time = time.time()

        # Prepare prompt in conversation format
        conversation = [{"role": "system", "content": "You are a journalist's assistant."}]
        prompt = conversation + [{"role": "user", "content": query}]
        # prompt = self.pipeline.tokenizer.apply_chat_template(
        #     prompt, tokenize=False, add_generation_prompt=True
        # )

        #print("Prompting the model...")
        start_time = time.time()

        

        # Generate response
        with torch.autocast(self.device_type):
            outputs = self.pipeline(
                prompt,
                max_new_tokens=max_tokens,
                eos_token_id=self.terminators,
                do_sample=True,
                temperature=temperature,
                top_p=top_p,
            )

        end_time = time.time()
        execution_time = end_time - start_time
        if self.verbose:
            print("Execution time:", execution_time)


        response = outputs[0]["generated_text"][len(prompt):]
        return response


        

        