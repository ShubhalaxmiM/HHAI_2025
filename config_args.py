import torch
import argparse

from utils import *


def parse_command_line_args(inference=False, training=False):
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
    "--dataset",
    type=str,
    default="politihop",
    help="specify dataset [politihop]",
    )


    parser.add_argument(
    "--prompt_strategy",
    type=str,
    default="fewshot",
    help="prompt strategy [blind, direct, logic, fewshot, direct_label, no_questions]",
    )

    parser.add_argument("--version", type=str, default="V1.0", help="specify version")

    parser.add_argument(
    "--model",
    type=str,
    default="gpt-4o",
    help="specify llama model [llama-8b, gpt-4o]",
    )
    
    #parser.add_argument("--pipeline_step", type= str, help= "decompose, grounding, aggregate")

    #parser.add_argument(
    #    "--device_map",
    #    type=str,
    #    default="auto",
    #    help="specify device map [auto, balanced, balanced_low_0, sequential]",
    #)
    parser.add_argument(
    "--temperature", type=float, default=0.5, help="temperature for GPT-3.5"
    )
    parser.add_argument(
    "--max_token", type=int, default=2048, help="specify number of max new token"
    )


    parser.add_argument(
    "--sample", type=int, default=10, help="number of rows to test code on, enter <= 150"
    )

    parser.add_argument(
    "--start", type=int, default=0, help="starting row index,enter <= 151"
    )


    parser.add_argument(
    "--grounding_source", 
    type=str, 
    default="ruling_comments", 
    help="specify grounding source [google_search, ruling_comments]"
    )

    

    # Parse basic arguments
    parser.add_argument('--config-file',     type=str,  default="/home/shubhalaxmi/FactChecking/peft_config.yaml")
    parser.add_argument('--hf-model-folder', type=str,  default="/home/shubhalaxmi/huggingface_models/")
    parser.add_argument('--verbose',         type=bool, action=argparse.BooleanOptionalAction, default=True)
    
    
    if inference:
        parser.add_argument('--prompt-dir', type=str, default="/home/shubhalaxmi/FactChecking/prompt_library_v2.py")
        parser.add_argument('--testing',    type=bool, action=argparse.BooleanOptionalAction, default=True)

    if training:
        parser.add_argument('--output-dir',   type=str,  default="/mnt/huggingface-models/trained-models")
        parser.add_argument('--dataset-size', type=int,  default=-1)
        parser.add_argument('--bf16',         type=bool, action=argparse.BooleanOptionalAction, default=True)
        parser.add_argument('--fp16',         type=bool, action=argparse.BooleanOptionalAction, default=False)

    

    #args= parser.parse_args()
    
    return parser.parse_args()


def read_config_file(config_path):
    config = load_yaml(config_path)
    if 'bitsandbytes' in config:
        config['bitsandbytes']['bnb_4bit_compute_dtype'] = getattr(
            torch, config['bitsandbytes']['bnb_4bit_compute_dtype'])
    return config


def merge_args_in_config(args, config, inference=False, training=False):
    config['verbose'] = args.verbose
    config['hf_model_folder'] = args.hf_model_folder

    if inference:
        if 'inference' not in config:
            config['inference'] = {}
        config['inference']['prompt_dir'] = args.prompt_dir
        config['inference']['testing'] = args.testing
    
    if training:
        config['dataset_size'] = args.dataset_size
        if 'training' not in config:
            config['training'] = {}
        config['training']['output_dir'] = args.output_dir
        config['training']['bf16'] = args.bf16
        config['training']['fp16'] = args.fp16
    
    return config


def load_config(inference=True, training=False):
    args = parse_command_line_args(inference=inference, training=training)
    config = read_config_file(args.config_file)
    config = merge_args_in_config(args, config, inference=inference, training=training)

    return config, args

"""

def get_basic_config():
    return {
        'verbose' : True,
        'hf_model_folder' : "/home/enrico/.cache/huggingface",
        'inference' : {
            'prompt_dir' : "./results/test_prompts",
        }
    }

"""