import argparse

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
    help="specify llama model [llama-8b, llama-13b, llama-30b, text-davinci, gpt-4o]",
)

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


args = parser.parse_args()

print(args)
