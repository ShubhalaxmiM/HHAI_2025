import os
import pandas as pd
import json
import re
from tqdm import tqdm
import time
#import replicate
import torch
from openai import OpenAI
from args import *
#from prompt_library_politihop import *
from prompt_library_v2 import *
from keys import *
#from config_args import *
#from utils import *
#from model_args import LlamaModel

#import ollama

if args.model == "gpt-4o":
    client = OpenAI(api_key = OPENAI_KEY)


def query_multiple(id_list, claim_list, date_list, label_list):
    out = []
    i=0
    for uid, claim, date, label in tqdm(
        zip(id_list, claim_list, date_list, label_list), total=len(claim_list)
    ):
        full_prompt = prompt.format(claim)
        
        print(full_prompt)
        
        #i+=1
        #if(i==3):
         #   break
        if args.model == "gpt-4o":
                
                completion = client.chat.completions.create(
                model="chatgpt-4o-latest",
                messages=[{"role": "system", "content": full_prompt}],
                max_tokens=args.max_token,
                temperature=0.5,
                )
                #print("temp "+ str(args.temperature))
                response = completion.choices[0].message.content
                #print(claim)
                print(response)

                keywords= response.split("/")
                keywords = [item for item in keywords if item!= " "+date]
                print(keywords)
                out.append({"id": uid, "label": label, "claim": claim, "date": date, "keywords": keywords,})

    return out


if __name__ == "__main__":
    
    
        """Set Prompt"""
       
        prompt= keyword_extract
        
    
            
        if not os.path.exists(f"./PoliResult/out/decompose"):
            os.makedirs(f"./PoliResult/out/decompose")
    
        df = pd.read_csv(f"./data/Dataset_150.csv")
        
        sample= args.sample
        start= args.start
        df= df.loc[start:sample]
        id_list = df["TUD_ID"]
        claim_list = df["statement"]
        date_list = df["statement_date"]
        label_list = df["annotated_label"]


        out= query_multiple(id_list, claim_list, date_list, label_list)

        with open(f"./PoliResult/out/decompose/claim_150_keyword_extraction.json",
                    "w",) as f:
            json.dump(out, f)
                    
        
        #result= pd.read_json("./PoliResult/out/decompose/final{args.start}_start_{args.sample}_sample_{args.model}_decompose_{args.prompt_strategy}_{args.version}.json")
        #result.to_csv("./PoliResult/out/decompose/final{args.start}_start_{args.sample}_sample_{args.model}_decompose_{args.prompt_strategy}_{args.version}.csv")
        print("Finished extract keywords")



    
