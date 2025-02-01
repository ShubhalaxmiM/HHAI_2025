import json

from crawler import Crawler
import tqdm
from boilerpy3 import extractors
import os
from relevance import FactCheckFilter
import random
from args import *
# random.seed(77)


with open(f"./PoliResult/out/grounding/final_filtered_serp_150_dict.json") as fp:
    source_dataset = json.load(fp)
    
filter = FactCheckFilter("fact_checkers 1.json")
crawler = Crawler(extractors.ArticleExtractor())

point_count = 0

readable_corpus = {}
samples = source_dataset

corpus ={}
qrels = {}
global_corpus_count = 0 

#Set environment values


for datapoint in tqdm.tqdm(samples,total=len(samples)):
    qrels[point_count] = {}
    evidences = {}
    snippets = {}
    count = 0
    claim_url = "https://www.politifact.com/"

    #Collect referencing links
    if("sources" in datapoint.keys() and datapoint["sources"]):
        for link in datapoint["sources"]:
            is_present = False
            if('description' in link.keys()):
                    snippets[count] = ("",link['description'])
                    is_present = True
            if("link" in link.keys() and link["link"] and filter.is_not_fact_checker(claim_url,link["link"])):
                url = link["link"].rstrip(' ')
                url = url.lstrip(' ')
                evidences[url]  = count
                is_present=True
            if(is_present):
                link['corpus_index'] = count
                count+=1
    
    queries = datapoint['filtered_search_results']
    for query,value in queries.items():
        values_non_fact_check = [link for link in value if filter.is_not_fact_checker(claim_url,link['link'])]
        top_k = min(len(values_non_fact_check),5)
        for link in values_non_fact_check[:top_k]:
            evidences[link['link']] = count
            if('snippet' in link.keys()):
                snippets[count] = (link['link'],link['snippet'])
            link['corpus_index'] = count
            count+=1

    results = crawler.crawl_links(evidences)
    # results_all = all_crawler.crawl_links(evidences)
    
    corpus_index_map = {}
    for i in range(count):
        evidence = {'title':''}
        insert = False
        if(i in snippets):
            insert = True
            evidence['snippet'] = snippets[i][1]
            evidence['url'] = snippets[i][0]
        else:
            evidence['snippet'] = ''
        if(i in results):
            insert = True
            evidence['text'] = results[i][1]
            evidence['url'] = results[i][0]
        # if(i in results_all):
        #     insert = True
        #     evidence['text_all'] = results_all[i][1]
        else:
            evidence['text'] = ''
        
        if(insert):
            corpus[global_corpus_count] = evidence
            qrels[point_count][global_corpus_count] = 1
            corpus_index_map[i]=global_corpus_count
            global_corpus_count+=1
            with open(f"./PoliResult/out/grounding/test/corpus_crawled_150_backup.json", 'a') as f:
                f.write(json.dumps({'id':global_corpus_count,'text':evidence}))
                f.write('\n')
    with open(f"./PoliResult/out/grounding/test/qrels_crawled_150_backup.json", 'a') as f:
        f.write(json.dumps({"id":point_count,"qrel":qrels[point_count]}))
        f.write('\n')
            

    for query,value in queries.items():
        for link in value:
            if(link and 'corpus_index' in link.keys()):
                corpus_count = link['corpus_index']
                if(corpus_count in corpus_index_map):
                    link['corpus_index'] = corpus_index_map[corpus_count]
                else:
                    del link['corpus_index']
    
    if("sources" in datapoint.keys() and datapoint["sources"]):
        for link in datapoint["sources"]:
            if("link" in link.keys() and link["link"] and 'corpus_index' in link.keys()):
                corpus_count = link['corpus_index']
                if(corpus_count in corpus_index_map):
                    link['corpus_index'] = corpus_index_map[corpus_count]
                else:
                    del link['corpus_index']
    with open(f"./PoliResult/out/grounding/test/test_crawled_150_backup.json", 'a') as f:
        f.write(json.dumps(datapoint))
        f.write('\n')

    
    point_count+=1


print("global",global_corpus_count,"point",point_count)

with open(f"./PoliResult/out/grounding/test/qrels_crawled_150.json",'w+') as fp:
    json.dump(qrels,fp)

with open(f"./PoliResult/out/grounding/test/corpus_crawled_150.json",'w+') as fp:
    json.dump(corpus,fp)    

with open(f"./PoliResult/out/grounding/test/test_crawled_150.json",'w+') as fp:
    json.dump(samples,fp)

with open(f"./PoliResult/out/grounding/test/error_log.json",'w+') as fp:
    json.dump(crawler.error_log,fp)







