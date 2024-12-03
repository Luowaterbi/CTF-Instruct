import argparse
import pprint
import sys
import os
import re
from tqdm import tqdm
import torch
from transformers import LlamaTokenizer, AutoModelForCausalLM, GenerationConfig, BitsAndBytesConfig
# from human_eval.data import read_problems, stream_jsonl
from generate_utils import read_from_jsonl
from vllm import LLM
from vllm import SamplingParams
import json

if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

try:
    if torch.backends.mps.is_available():
        device = "mps"
except:
    pass


def construct_prompt(dataset,):
    problems = read_from_jsonl(dataset)
    task_ids = sorted(problems.keys())
    prompts = [problems[task_id]['prompt'].strip() for task_id in task_ids]
    prompt_batch = [prompt.replace('    ', '\t') for prompt in prompts]
    return task_ids, prompt_batch


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--model', type=str, default='bigcode/starcoder', help="")
    parser.add_argument('--dataset', type=str, default='mbpp', help="")
    parser.add_argument('--output_path', type=str, help="")
    parser.add_argument('--temperature', type=float, default=0.8, help="")
    parser.add_argument('--top_p', type=float, default=1, help="")
    parser.add_argument('--N', type=int, default=200, help="")
    parser.add_argument('--max_len', type=int, default=512, help="")
    parser.add_argument('--num_gpus', type=int, default=4, help="")
    parser.add_argument('--decoding_style', type=str, default='sampling', help="")
    parser.add_argument('--num_seqs_per_iter', type=int, default=50, help='')

    args = parser.parse_args()

    argsdict = vars(args)
    print(pprint.pformat(argsdict))

    task_ids, prompt_batch = construct_prompt(args.dataset)
    num_samples = len(prompt_batch)
    print("Number of samples: {}".format(num_samples))

    print(f"model: {args.model}")
    if "sc2-7b" in args.model:
        args.num_gpus = 4
        print("Using 4 GPUs for sc2-7b")
    llm = LLM(model=args.model, tensor_parallel_size=args.num_gpus, max_model_len=8192)
    stop = ["</s>", "\n\n\n\n", "<|EOT|>"]
    if args.dataset == "ds1000":
        stop += ["```"]

    sampling_params = SamplingParams(temperature=args.temperature, top_p=args.top_p, max_tokens=args.max_len, stop=stop, n=args.num_seqs_per_iter)

    print(f"Loaded {args.model}.")
    if args.decoding_style == 'sampling':
        loops = int(args.N / args.num_seqs_per_iter)
    else:
        loops = 1

    print(f"Need {loops} Loops.")
    for _ in tqdm(range(loops), total=loops, leave=False, ncols=0):
        with torch.no_grad():
            completions = llm.generate(prompt_batch, sampling_params)
        for i, completion in enumerate(completions):
            gen_seqs = [completion.outputs[i].text for i in range(args.num_seqs_per_iter)]
            if gen_seqs is not None:
                output_file = args.output_path + '/{}.jsonl'.format(i)
                f = open(output_file, 'a')
                for gen_seq in gen_seqs:
                    code = gen_seq.replace('\t', '    ')
                    completion_seq=dict(
                        {'task_id': task_ids[i],
                         'completion': code,
                         'all_code': prompt_batch[i] + code,
                         }
                    )
                    f.write(json.dumps(completion_seq) + '\n')


if __name__ == '__main__':
    main()