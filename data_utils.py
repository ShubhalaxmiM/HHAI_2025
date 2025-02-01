import pandas as pd
import json
import re
from openai import OpenAI
from keys import OPENAI_KEY
from helper_prompts import *
from args import *


def question_extraction_llama(question_df, prompt_strategy):
    #print("in function")
    if prompt_strategy == 'direct':
        question_df['response'] = question_df['response'].apply(lambda x: (x.split('Followup Question: '))[1::])
        
    elif prompt_strategy == 'fewshot':
        #print("in elif")
        for i in range(len(question_df)):
            #print("in loop")
            s = question_df.loc[i, 'response']
            s= s.split('**\n')[-1]
            s= s.split('\n')
            #print(s)
            question_df.loc[i, 'response']= s

    elif prompt_strategy == 'novice_questions':
        question_df['response'] = question_df['response'].apply(lambda x: (x.split('Followup Question: '))[1::])

    elif prompt_strategy == 'journalist_questions':
        question_df['response'] = question_df['response'].apply(lambda x: (x.split('Followup Question: '))[1::])

    return question_df

def question_extraction_gpt(question_df):
    #print("in function")
    question_df['questions'] = question_df['response'].apply(lambda x: (x.split('Followup Question: '))[1::])

    return question_df

def coref_resolution(question_df):
    #print(question_df.columns)
    client = OpenAI(api_key=OPENAI_KEY)
    
    for i in range(len(question_df)):
        #print(question_df.loc[i, 'response'])
        temp= ''
        for item in question_df.loc[i, 'response']:
            #print(item)
            claim = question_df.loc[i, 'claim']
            full_qa_prompt= rephrase_question_prompt.format(claim, item)
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": full_qa_prompt}],
                max_tokens=100,
                temperature=0.1,
                )
            response = completion.choices[0].message.content
            #print(response)
            temp= temp + response + '\n'
        print(i)  
        question_df.loc[i, 'coref_q']= temp
    
    question_df.to_csv(f"./PoliResult/out/decompose/coref0_start_{args.sample}_sample_{args.model}_decompose_{args.prompt_strategy}_{args.version}.csv")

    return question_df

            

    



def extract_questions(response_list):
    questions= []
    k=0

    if 1>0:
        pass
    

    elif prompt_strategy== 'direct'and args.model== 'llama-7b':
        for r in response_list:
            print(k)
            qa_list= r.split("Followup Question: ")[1::]
            print(qa_list)
            questions.append(qa_list)
            k+=1
            """
            #print(r)
            if "Followup Questions:\n\n" in r:
                qa_list= r.split("Followup Questions:\n\n")[1]
                #print(qa_list)
                qa_list= re.sub(r'[1-9]\.', '',qa_list)
                qa_list= qa_list.split('\n')
                #if '' in qa_list:
                #    qa_list= qa_list.remove('')
                #print("plural")
                print(qa_list)
                questions.append(qa_list)

            elif "Followup Question:" in r:
                #print(r)
                qa_list= r.split("Followup Question:")[1::]
                #if '' in qa_list:
                #    qa_list= qa_list.remove('')
                #print("singular")
                #print(qa_list)
            
                questions.append(qa_list)

            else:
                print(r)
                qa_list= r.split("Followup Questions:\n")[1]
                print(qa_list)
                qa_list= re.sub(r'[1-9].', '',qa_list)
                qa_list= qa_list.split('\n')
                print("plural")
                print(qa_list)
                questions.append(qa_list)
            """
            
            
    return questions
