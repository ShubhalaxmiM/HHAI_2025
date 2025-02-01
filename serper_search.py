import os
import json
import logging
import random
import pandas as pd
from tqdm import tqdm
from args import *
from keys import SERPER_DEV_KEY

from SERP import SERPER







def serper_search(keywords_data):
    
    searcher = SERPER(api_key=SERPER_DEV_KEY)
    

    with open(f'./PoliResult/out/grounding/final_serp_{args.sample}_dict.jsonl', 'w') as f:
        pass

    #print(dataset)                                             
    count = 0
    samples = []
    for datapoint in tqdm(keywords_data,total=len(keywords_data)):
        print("datapoint")
        print(datapoint)
        
        queries = datapoint["keywords"]
        print(queries)
        filter_date = datapoint["date"]
        result_dict = {}
        #for query in queries:
            #try:
        query = ','.join(queries)
        results = searcher.fetch_results(query, filter_date)
        print(datapoint['id'])
        result_dict[query] = results
        count+=1
            #except Exception as e:
        logging.info("Unable to fetch results for query", query)
        datapoint["google_search"] = result_dict
        #print(result_dict)
        samples.append(datapoint)
        with open(f'./PoliResult/out/grounding/temp_serp_150_dict.jsonl', 'a') as f:
            f.write(json.dumps(datapoint))
            f.write('\n')

    print(count,len(keywords_data))

    return samples

    

if __name__ == "__main__":
    with open("./PoliResult/out/decompose/claim_150_keyword_extraction.json", 'r') as f:
        keywords_data= json.load(f)
    #print(question_df)

    samples= serper_search(keywords_data)


    with open(f'./PoliResult/out/grounding/final_serp_150_dict.jsonl', 'w') as f:
        json.dump(samples, f)



