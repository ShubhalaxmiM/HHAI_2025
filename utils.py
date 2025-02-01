import yaml
import json
import torch
import gc
#from collections import Counter
import math
import numpy as np
#from scipy.spatial.distance import jensenshannon
#from nltk.corpus import wordnet31 as wn31
import string
#import torchtext
#from torchtext.data import get_tokenizer

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def dump_yaml(file_path, config):
    with open(file_path, 'w') as file:
        yaml.dump(config, file)


def load_json(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

def get_device_map():
    if torch.cuda.is_available():
        print(f"Using GPU {torch.cuda.get_device_name(0)}")
        device_map = {"": 0} # Use GPU 0
        device_type = "cuda"
    else:
        print('No GPU available, using the CPU instead.')
        device_map = None
        device_type = "cpu"
    return device_map, device_type

def check_bf16_compatibility(config):
    if config['bnb_4bit_compute_dtype'] == torch.bfloat16 and config['load_in_4bit']:
        major, _ = torch.cuda.get_device_capability()
        if major >= 8:
            print("="*80)
            print("Your GPU supports bfloat16, you are getting accelerate training with bf16= True")
            print("="*80)

def print_vram_info():
    free_memory, total_memory = torch.cuda.mem_get_info()

    free_memory_gb = free_memory / 1024**3
    total_memory_gb = total_memory / 1024**3

    print(f"Free Memory: {free_memory_gb:.2f}/{total_memory_gb:.2f} GB")


def clear_vram(variable=None):
    if variable != None:
        del variable
    gc.collect()
    torch.cuda.empty_cache()