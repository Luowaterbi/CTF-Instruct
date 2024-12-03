import json
from tqdm import tqdm
import numpy as np
from scipy.special import softmax
from transformers import AutoTokenizer, AutoModelForCausalLM
from vllm import LLM, SamplingParams
import sys
import random


if __name__ == "__main__":
    model_name_or_path = "XCoder-Complexity-Scorer"
    dataset_name = sys.argv[1]
    ds = json.load(open(dataset_name))
    llm = LLM(model_name_or_path, tensor_parallel_size=8)
    sampling_params = SamplingParams(max_tokens = 2, logprobs = 20)
    prompt = "You are a helpful assistant. Please identify the complexity score of the following user query. \n##Query: {instruction}  \n##Complexity: "
    inputs = [prompt.format_map(dict(instruction = d["instruction"])) for d in ds]
    outputs = llm.generate(inputs, sampling_params)
    
    error_cnt = 0
    for d, output in zip(ds, outputs):
        if "ori" in d:
            del d["ori"]
        try:
            logprobs_list = output.outputs[0].logprobs[0]
        except IndexError:
            error_cnt += 1
            d['c_score'] = 2.0
            continue
        
        score_logits = []
        scores = []
        for i, k in enumerate([16,17,18,19,20,21]):
            if k in logprobs_list:
                score_logits.append(logprobs_list[k].logprob)
                scores.append(i)

        score_logits = np.array(score_logits)
        score_npy = softmax(score_logits, axis=0)
        score_npy = score_npy * np.array(scores)
        score_npy = np.sum(score_npy, axis=0)
        
        d['c_score'] = float(score_npy)
    
    print("Final error cnt:", error_cnt)
    ds = sorted(ds, key=lambda x:x["c_score"], reverse=True)
    json.dump(ds, open(dataset_name.replace(".json", "_with_c_score.json"), "w"), indent=4)