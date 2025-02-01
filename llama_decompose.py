import os
import torch
from tqdm import tqdm

from utils import *
from config_args import load_config
from model_args import LlamaModel
from prompt_library_v2 import *
from config_args import *
from args import *
import pandas as pd

# Parse command line arguments and config file
config, args = load_config(inference=True)
#print(args)

torch.manual_seed(0)


model_name = "Llama-3.1-8B-Instruct"
llama_model = LlamaModel(model_name, config)

clear_vram()

def query_multiple(id_list, claim_list, label_list, context_list, just_list):
    out = []
    i=0
    #print("===================================================================")
    #print(prompt)
    for uid, claim, label, context, just in tqdm(
        zip(id_list, claim_list, label_list, context_list, just_list), total=len(claim_list)
    ):
        full_prompt = prompt.format(claim)

        response = llama_model.get_response(full_prompt)

        print(response)

        out.append({"id": uid, "label": label, "claim": claim, "response": response, "context": context, "justification": just})

        with open(f"./PoliResult/out/decompose/temp{args.start}_start_{args.sample}_sample_{args.model}_decompose_{args.prompt_strategy}_{args.version}.json",
                  "w",) as f:
                json.dump(out, f)
        print(uid)
        
    return out



if __name__ == "__main__":
    
    
        """Set Prompt"""
       
        if args.prompt_strategy == "direct":
            prompt = direct_decompose
        
        if args.prompt_strategy == "fewshot":
            prompt = fewshot_decompose

        #print(prompt)
    
            
        if not os.path.exists(f"./PoliResult/out/decompose"):
            os.makedirs(f"./PoliResult/out/decompose")
    
        df = pd.read_csv(f"./data/Dataset_150.csv", )
        
        sample= args.sample
        start= args.start
        df= df.loc[start:sample]
        id_list = df["###_id"]
        claim_list = df["full_claim"]
        label_list = df["annotated_label"]
        context_list= df['ruling_clean_split']
        just_list = df['justification']
        journalist_list= df['journalist']
        novice_list= df['novice']

        """
       
       if args.prompt_strategy == "journalist_questions":
            out= extract_journalist_questions(id_list, claim_list, label_list, context_list, just_list, journalist_list)

       elif args.prompt_strategy == "novice_questions":
            out= extract_novice_questions(id_list, claim_list, label_list, context_list, just_list, novice_list)
        """
        out= query_multiple(id_list, claim_list, label_list, context_list, just_list)


        with open(f"./PoliResult/out/decompose/final{args.start}_start_{args.sample}_sample_{args.model}_decompose_{args.prompt_strategy}_{args.version}.json",
                    "w",) as f:
            json.dump(out, f) 
                    
        
        #result= pd.read_json("./PoliResult/out/decompose/final{args.start}_start_{args.sample}_sample_{args.model}_decompose_{args.prompt_strategy}_{args.version}.json")
        #result.to_csv("./PoliResult/out/decompose/final{args.start}_start_{args.sample}_sample_{args.model}_decompose_{args.prompt_strategy}_{args.version}.csv")
        print("Finished decomposition")



