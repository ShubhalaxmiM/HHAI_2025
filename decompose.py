#!/usr/bin/env python
#coding: utf-8


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
from config_args import *
from utils import *
from model_args import LlamaModel

#import ollama

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
config, args = load_config(inference=True)

if args.model == "llama-8b":
    torch.manual_seed(0)


    model_name = "Llama-3.1-8B-Instruct"
    llama_model = LlamaModel(model_name, config)

    clear_vram()
    


if args.model == "gpt-4o":
    client = OpenAI(api_key = OPENAI_KEY)

        
def query_multiple(id_list, claim_list, label_list, context_list, just_list):
    out = []
    i=0
    for uid, claim, label, context, just in tqdm(
        zip(id_list, claim_list, label_list, context_list, just_list), total=len(claim_list)
    ):
        full_prompt = prompt.format(claim)
        
        #print(full_prompt)
        
        #i+=1
        #if(i==3):
         #   break
        if args.model == "gpt-4o":
                
                completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": full_prompt}],
                max_tokens=args.max_token,
                temperature=args.temperature,
                )
                #print("temp "+ str(args.temperature))
                response = completion.choices[0].message.content
                #print(claim)
                print(response)
                out.append({"id": uid, "label": label, "claim": claim, "response": response, "context": context, "justification": just})
                #print(out)
                #decomp_result=pd.DataFrame(out)
                with open(f"./PoliResult/out/decompose/temp{args.start}_start_{args.sample}_sample_{args.model}_decompose_{args.prompt_strategy}_{args.version}.json",
                    "w",) as f:
                    json.dump(out, f)
                    #print("wrote to file")
                print(uid)
                i+=1
                #if (i%3==0):
                #    time.sleep(60)
                
           
        elif args.model == "llama-8b":

            response = llama_model.get_response(full_prompt)

            print(response[0]['content'])

            
            out.append({"id": uid, "label": label, "claim": claim, "response": response[0]['content'], "context": context, "justification": just})

            with open(f"./PoliResult/out/decompose/temp{args.start}_start_{args.sample}_sample_{args.model}_decompose_{args.prompt_strategy}_{args.version}.json",
                    "w",) as f:
                json.dump(out, f)
            print(uid)
        
    return out


def extract_journalist_questions(id_list, claim_list, label_list, context_list, just_list, journalist_list):
    out=[]
    for uid, claim, label, context, just, journalist in tqdm(
        zip(id_list, claim_list, label_list, context_list, just_list, journalist_list), total=len(claim_list)
    ):
        q_list= journalist.split('//')
        q_format= ["Followup Question: {}".format(item.strip()) for item in q_list if item!='']
        q_format= '\n'.join(q_format)
        print(q_format)
        print("==========="*10)

        out.append({"id": uid, "label": label, "claim": claim, "response": q_format, "context": context, "justification": just})

    return out


def extract_novice_questions(id_list, claim_list, label_list, context_list, just_list, novice_list):
    out=[]
    for uid, claim, label, context, just, novice in tqdm(
        zip(id_list, claim_list, label_list, context_list, just_list, novice_list), total=len(claim_list)
    ):
        #print(novice)
        q_list= novice.split('//')
        q_format= ["Followup Question: {}".format(item.strip()) for item in q_list if item!='']
        q_format= '\n'.join(q_format)
        print(q_format)
        print("==========="*10)

        out.append({"id": uid, "label": label, "claim": claim, "response": q_format, "context": context, "justification": just})

    return out

if __name__ == "__main__":
    
    
        """Set Prompt"""
       
        if args.prompt_strategy == "direct":
            prompt = direct_decompose
        
        if args.prompt_strategy == "fewshot":
            prompt = fewshot_decompose
        
    
            
        if not os.path.exists(f"./PoliResult/out/decompose"):
            os.makedirs(f"./PoliResult/out/decompose")
    
        df = pd.read_csv(f"./data/Dataset_150.csv")
        
        sample= args.sample
        start= args.start
        df= df.loc[start:sample]
        id_list = df["TUD_ID"]
        claim_list = df["full_claim"]
        label_list = df["annotated_label"]
        context_list= df['ruling_clean_split']
        just_list = df['justification']
        journalist_list= df['journalist']
        novice_list= df['novice']
        #print(novice_list)

        if args.prompt_strategy == "journalist_questions":
            out= extract_journalist_questions(id_list, claim_list, label_list, context_list, just_list, journalist_list)

        elif args.prompt_strategy == "novice_questions":
            out= extract_novice_questions(id_list, claim_list, label_list, context_list, just_list, novice_list)

        else:
            out= query_multiple(id_list, claim_list, label_list, context_list, just_list)


        with open(f"./PoliResult/out/decompose/final{args.start}_start_{args.sample}_sample_{args.model}_decompose_{args.prompt_strategy}_{args.version}.json",
                    "w",) as f:
            json.dump(out, f)
                    
        
        #result= pd.read_json("./PoliResult/out/decompose/final{args.start}_start_{args.sample}_sample_{args.model}_decompose_{args.prompt_strategy}_{args.version}.json")
        #result.to_csv("./PoliResult/out/decompose/final{args.start}_start_{args.sample}_sample_{args.model}_decompose_{args.prompt_strategy}_{args.version}.csv")
        print("Finished decomposition")