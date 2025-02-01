import os
import pandas as pd
import json
import pickle
from tqdm import tqdm
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig
from openai import OpenAI
from args import *
from prompt_library_v2 import *
from keys import *
import time
from data_utils import *
from config_args import *
from utils import *
from model_args import LlamaModel

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
config, args = load_config(inference=True)

if args.model == "llama-8b":
    torch.manual_seed(0)


    model_name = "Llama-3.1-8B-Instruct"
    llama_model = LlamaModel(model_name, config)

    clear_vram()


def assemble_prompt_no_predicate(claim, question_list, grounded_answer_list):
    context = ""
    for question, answer in zip(question_list, grounded_answer_list):
        if question is None or answer is None:
            continue
        context = context+"\n"+answer
       
    full_prompt = prompt % (claim, context)
    
    return context, full_prompt

def assemble_prompt(claim, ans):
    """
    context = predicates + "\n"

    for question, answer in zip(question_list, grounded_answer_list):
        if question is None or answer is None:
            continue
        context = context + "\n" + question + "\n" + answer
    # print(context)
    full_prompt = prompt % (claim, context)
    #print(full_prompt)
    """
    ans= " ".join(ans.split())
    temp_str= claim+ "\n\n"+ "Evidence:"+ "\n" + ans
    #print(temp_str)
    #print("=="*30)
    #print(prompt)
    full_prompt = prompt.format(temp_str)
    #print(full_prompt)
    
    return full_prompt

if args.model == "gpt-4o":
    client = OpenAI(api_key = OPENAI_KEY)


def query_multiple(id_list, claim_list, label_list, ans_list):
    out = []
    i=args.start
    for uid, claim, label, ans in tqdm(
        zip(id_list, claim_list, label_list, ans_list),
        total=len(claim_list),
        ):
        full_prompt= assemble_prompt(claim, ans)
        
        #print(full_prompt)
        
        if args.model == "gpt-4o":
            
        
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": full_prompt}],
                max_tokens=args.max_token,
                temperature=args.temperature,
                )
            response = completion.choices[0].message.content
            print(uid)
            print("==="*30)
            #print(response)
            out.append({"id": uid, "label": label, "claim": claim, "grounded_answers": ans, "agg_response": response, })
                #decomp_result=pd.DataFrame(out)
            i+=1
            #if (i%3==0):
            #    time.sleep(60)
                
                
        if args.model == "llama-8b":
            

            response = llama_model.get_response(full_prompt)
            
            print("Succesful "+ str(i))
            i+=1
            
            #print(response[0]['content'])
            #print(full_prompt)
            """
            inputs = tokenizer(full_prompt, return_tensors="pt", truncation=True, max_length=5000).to(device)
            #print(inputs['input_ids'].size())
            try:
                inputs = tokenizer(full_prompt, return_tensors="pt").to(device)
                outputs = model.generate(**inputs, max_new_tokens=1024)

            except:
                inputs = tokenizer(full_prompt, return_tensors="pt",truncation=True, max_length=5000).to(device)
                outputs = model.generate(**inputs, max_new_tokens=512)

            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            #print(claim)
            print(response)
            res = response.split(full_prompt)[1:][0]
            print(res)
            """
            
            """
            
            response = ollama.generate(model="mistral",
                           #system="Act like a journalist. Based on the evidence paragraph, label each claim as [TRUE] or [HALF-TRUE] or [FALSE], following the examples provided. Print only the label within square brackets and a justification of the label. Print in the structure demonstrated in the following examples.",
                           prompt= full_prompt)
            #print(claim)
            print(response['response'])
            """

            out.append({"id": uid, "label": label, "claim": claim, "grounded_answers": ans, "agg_response": response[0]['content'], })

            with open(f"./PoliResult/out/aggregate/temp_{args.start}_{args.sample}_sample_{args.model}_aggregate_{args.prompt_strategy}_{args.grounding_source}_{args.version}.json","w", ) as f:
                json.dump(out, f)
            
            torch.cuda.empty_cache()
    return out



def query_multiple_noq(id_list, claim_list, label_list, context_list):
    out = []
    i=0
    for uid, claim, label, ctxt in tqdm(
        zip(id_list, claim_list, label_list, context_list),
        total=len(claim_list),
        ):

        
        full_prompt= assemble_prompt(claim, ctxt)
        #print(full_prompt)

        if args.model == "gpt-4o":

            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": full_prompt}],
                max_tokens=args.max_token,
                temperature=args.temperature,
                )
            response = completion.choices[0].message.content
            print(uid)
            print("==="*30)
            #print(response)
            out.append({"id": uid, "label": label, "claim": claim, "context": ctxt, "agg_response": response, })
                #decomp_result=pd.DataFrame(out)
            i+=1
            if (i%3==0):
                time.sleep(60)
        

        if args.model == "llama-8b":
            

            response = llama_model.get_response(full_prompt)
            
            print("Successful "+ str(i))
            i+=1
            out.append({"id": uid, "label": label, "claim": claim, "grounded_answers": ctxt, "agg_response": response[0]['content'], })

            with open(f"./PoliResult/out/aggregate/temp_{args.start}_{args.sample}_sample_{args.model}_aggregate_{args.prompt_strategy}_{args.grounding_source}_{args.version}.json","w", ) as f:
                json.dump(out, f)
            
            torch.cuda.empty_cache()



    return out
        
        
        
if __name__ == "__main__":
    
    """Set Prompt"""
    
    if args.prompt_strategy == "direct":
        prompt = aggregate
    
    if args.prompt_strategy == "fewshot":
        prompt = aggregate
    elif args.prompt_strategy == "no_questions":
        prompt = aggregate
    elif args.grounding_source== "google_search":
        prompt = aggregate
    
    elif args.prompt_strategy == "journalist_questions":
        prompt = aggregate
    elif args.prompt_strategy == "novice_questions":
        prompt = aggregate

    if args.model == 'llama-8b':
        prompt= llama_aggregate

    if not os.path.exists(f"./PoliResult/out/aggregate"):
        os.makedirs(f"./PoliResult/out/aggregate")
        
    
    
    if args.prompt_strategy== 'no_questions':
        df = pd.read_pickle(f"./PoliResult/out/grounding/closed_final_150_sample_{args.model}_grounded_direct_ruling_comments_{args.version}.pkl"
        )
        #print(df.columns)
        df= df.loc[args.start:args.start+args.sample]
        #print(df)
        id_list = df["id"]
        claim_list = df["claim"]
        label_list = df["label"]
        #ans_list = df["grounded_answers"]

    if args.prompt_strategy== 'no_questions':
        context_list= df['context']
        out_noq= query_multiple_noq(id_list, claim_list, label_list, context_list)

        with open(f"./PoliResult/out/aggregate/final{args.start}_start_{args.sample}_sample_{args.model}_aggregate_{args.prompt_strategy}_{args.version}.json",
            "w",
        ) as f:
            json.dump(out_noq, f)

        print("Finished aggregation!")

    if args.model== 'llama-8b':
        df = pd.read_pickle(f"./PoliResult/out/grounding/closed_final_150_sample_{args.model}_grounded_{args.prompt_strategy}_{args.grounding_source}_{args.version}.pkl"
        )
        df= df.loc[args.start:args.start+args.sample]
        #print(df)
        id_list = df["id"]
        claim_list = df["claim"]
        label_list = df["label"]
        ans_list = df["grounded_answers"]

        out = query_multiple(id_list, claim_list, label_list, ans_list)
        
        with open(f"./PoliResult/out/aggregate/final{args.start}_start_{args.sample}_sample_{args.model}_aggregate_{args.prompt_strategy}_{args.version}.json",
            "w",
        ) as f:
            json.dump(out, f)

        print("Finished aggregation!")

    if args.grounding_source=='google_search' and args.model=='gpt-4o':
        df = pd.read_pickle(f"./PoliResult/out/grounding/final{args.start}_start_150_sample_{args.model}_grounded_{args.prompt_strategy}_google_search_{args.version}.pkl"
        )
        #print(df.columns)
        df= df.loc[args.start:args.start+args.sample]
        #print(df)
        id_list = df["id"]
        claim_list = df["claim"]
        label_list = df["label"]
        context_list= df['grounded_answers']

        out_noq= query_multiple_noq(id_list, claim_list, label_list, context_list)

        with open(f"./PoliResult/out/aggregate/final{args.start}_start_{args.sample}_sample_{args.model}_aggregate_{args.prompt_strategy}_google_search_{args.version}.json",
            "w",
        ) as f:
            json.dump(out_noq, f)

        print("Finished aggregation!")

        
        
            
