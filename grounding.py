import os

import pandas as pd
import re
import time
from tqdm import tqdm
from args import *
from keys import *
from openai import OpenAI
import torch
from data_utils import *
from SERP import SERPER
from serper_search import serper_search
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

        
        




def grounding_from_gpt_embeddings(question_list, context_list):
    # models
    client = OpenAI(api_key=OPENAI_KEY)
    qa_prompt=""" 
    Use the below article to answer the subsequent question. Only use information in the article to answer the question.
    Article:
    \\\
    {}
    \\\

    Question: {}
    """
    #print(context_list)
    grounded_answers=[]
    question_answers=[]
    i=0
    for questions in tqdm(question_list, total=len(question_list)):
        temp = ""
        temp_q = ""
        for q in questions:
            #print(qa_prompt.format(context_list[i],q))
        
            full_qa_prompt= qa_prompt.format(context_list[i],q)
            #print(context_list[i])
            #break
            try:
                completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": full_qa_prompt}],
                max_tokens=1024,
                temperature=args.temperature,
                )
                response = completion.choices[0].message.content

            except:
                response= " "
            
            #print(q+ "\n"+ response + "\n")
            temp_q += q+ "\n"+ response
            temp+=(response)
            print(i)
                
            if (i%20==0):
                time.sleep(60)
                    
        #break         
        
        i+=1
        question_answers.append(temp_q)
        grounded_answers.append(temp)
        # print(grounded_answers)
    return grounded_answers, question_answers


def grounding_from_llama_embeddings(question_list, context_list, start):
    

    qa_prompt=""" 
    Use the below article to answer the subsequent question. Only use information in the artice to answer the question.
    Article:{}

    Question: {}
    """
    
    grounded_answers=[]
    i=start
    for questions in tqdm(question_list, total=len(question_list)):
        temp = ""
        #print(questions)
        for q in questions:
            #print("question")
            #print(q)            
            if q=='':
                continue
            full_qa_prompt= qa_prompt.format(context_list[i],q)
            response = llama_model.get_response(full_qa_prompt)

            #print(response[0]['content'])
            temp= temp+ '\n' + response[0]['content']
            #print(temp)

        grounded_answers.append(temp)
        
        dataset.loc[i,'grounded_answers']= temp
        dataset.to_pickle(
    f"./PoliResult/out/grounding/temp{args.start}_start_{args.sample}_sample_{args.model}_grounded_{args.prompt_strategy}_{args.grounding_source}_{args.version}_qaconstraint.pkl"
      )
        print(i)
        i+=1

    return grounded_answers
            

if __name__ == "__main__":
    prompt_strategy= args.prompt_strategy
    
    if not os.path.exists(f"./PoliResult/out/grounding"):
        os.makedirs(f"./PoliResult/out/grounding")


    with open(f"./PoliResult/out/decompose/final0_start_{args.sample}_sample_{args.model}_decompose_{args.prompt_strategy}_{args.version}.json") as fp:
        dataset = pd.read_json(fp)
    
    """
    
    dt= pd.read_csv("./data/datetime.csv")
    for i in range(len(dataset)):
        dataset[i]["published"]= dt.loc[i, 'statement_date']
        #print(dataset[i]["published"])
    """
    """
    
    with open(f"./PoliResult/out/decompose/final0_start_{args.sample}_sample_{args.model}_decompose_{args.prompt_strategy}_{args.version}.json"
         ) as f1:
        df = pd.read_json(f1)
    
    #print(df.columns)    
    sample= args.sample
    start= args.start
    df= df.loc[start:start+sample]
    #print(len(df))
    """

    
    
    
    
    
    
    
    """
    df= coref_resolution(df)
    print("Coreference resolution Complete")
    
    dt= pd.read_csv("./data/datetime.csv")

    #with open(f"./PoliResult/out/decompose/coref0_start_{args.sample}_sample_{args.model}_decompose_{args.prompt_strategy}_{args.version}.json"
     #    ) as f1:
      #  df = pd.read_json(f1)

    df= pd.read_json(f"./PoliResult/out/decompose/coref0_start_{args.sample}_sample_{args.model}_decompose_{args.prompt_strategy}_{args.version}.json")

    for i in range(len(df)):
        df.loc[i, "published"]= dt.loc[i, 'statement_date']

    

    df.to_json(f"./PoliResult/out/decompose/coref0_start_{args.sample}_sample_{args.model}_decompose_{args.prompt_strategy}_{args.version}.json")
    """
      
        
    if args.grounding_source == "google_search":

        #samples= serper_search(dataset)
        #with open(f"./PoliResult/out/grounding/serp_{args.sample}_sample_{args.model}_grounding_{args.prompt_strategy}_{args.version}.json", "w+") as fp:
        #    json.dump(samples, fp)

        with open(f"./PoliResult/out/grounding/scraped_150_full_text.json") as fp:
            evidence_df= pd.read_json(fp)

        dataset = question_extraction_gpt(dataset)
        print("Extracted_questions")
        grounded_answers, question_answers= grounding_from_gpt_embeddings(dataset["questions"], evidence_df["evidence"])
        dataset['grounded_answers']= grounded_answers
        dataset['question_answers']=question_answers
        dataset.to_pickle(f"./PoliResult/out/grounding/final{args.start}_start_{args.sample}_sample_{args.model}_grounded_{args.prompt_strategy}_{args.grounding_source}_{args.version}.pkl"
                    )

        
        
    if args.grounding_source == "ruling_comments" and args.model== "gpt-4o":
        grounded_answers, question_answers= grounding_from_gpt_embeddings(df["questions"], df["context"])
        df['grounded_answers']= grounded_answers
        df['question_answers']=question_answers
        df.to_pickle(f"./PoliResult/out/grounding/final{args.start}_start_{args.sample}_sample_{args.model}_grounded_{args.prompt_strategy}_{args.grounding_source}_{args.version}.pkl"
                    )
    

    elif args.grounding_source == "ruling_comments" and args.model== "llama-8b":
        #print(dataset['response'])
        df = question_extraction_llama(dataset, args.prompt_strategy)
        print("Question Extracion Complete")
    
        grounded_answers= grounding_from_llama_embeddings(df["response"], df["context"], args.start)
        dataset['grounded_answers']= grounded_answers
        dataset.to_pickle(f"./PoliResult/out/grounding/closed_final_{args.sample}_sample_{args.model}_grounded_{args.prompt_strategy}_{args.grounding_source}_{args.version}.pkl"
                    )
        
        
  
    

    
    
    print("Finished Getting Knowledge-grounded answers!")
