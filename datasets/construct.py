import json
# import tiktoken
import tqdm

# encoding = tiktoken.encoding_for_model("gpt-4-turbo")
PROMPT = """Refine a code generation task, initially presented as #Original_Sample#, which is a JSON dict including three keys: a task instruction, and the output generated from  the instruction.
Your task is to produce a #Modified_Sample# by altering the original task instruction in a way that significantly changes the output, yet with minimal adjustments to the instruction itself.

## Requirements:
1. **Minimal Instruction Change**: Achieve the code change with minimal alterations to the instruction. The difference will be assessed through evaluated by the Rouge score, indicating the high similarity in wording, sentence structure, and length to the original.
2. **No Trival Changes to Instruction**: Ensure the modification to the instruction is semantic-relevant. Do not make trivial changes like adding or removing a word, changing the order of words, or replacing synonyms.
3. **Maximal Code Change**: Your adjustments should lead to considerable changes in the output, impacting aspects like algorithms, data structures, data and control flows, or boundary conditions. The difference will be assessed through both the Rouge score and AST score, indicating the output's functionality, implementation, and naming should substantially diverge from the original.
4. **Encourage Trival Code Change**: The code output should be significantly different. Change every aspect of the code, including the function name, variable names.

## Format:
1. Your output should be a #Modified_Sample# dict in **JSON format** as the #Original_Sample# is.
2. Using **markdown code snippet syntax** in the instruction and the output.
3. Ensure all characters are **properly escaped** in the JSON string.

## Examples:
{seeds}

## Question:
- Original_Sample:
"""


def encode_prompt(data: dict):
    import random
    from seed import SEEDS_LEN, format_seeds

    formatted_seeds = format_seeds(random.sample(range(SEEDS_LEN), k=4))
    prompt = PROMPT.format(seeds=formatted_seeds)

    prompt += (
        json.dumps(data, indent=2)
        + "\n(Your output here)\n- Reasoning:\n"
        + "- Modified_Sample:\n"
    )
    return prompt


def read_data(file):
    if file.endswith(".json"):
        with open(file, "r") as f:
            data = json.load(f)
    elif file.endswith(".jsonl"):
        with open(file, "r") as f:
            data = [json.loads(line) for line in f]
    else:
        raise ValueError("Invalid file format")
    return data


def calcu_ratio_from_input_to_output():
    """
    根据seed计算从input到output的token ratio
    """
    from seed import SEEDS
    ratios = []
    for s in SEEDS:
        ori = s["Original_Sample"]
        ori_text = json.dumps(ori, indent=2)
        reasonings = s["Reasoning"]
        modi = s["Modified_Sample"]
        output_text = "\n- Reasoning:\n" + json.dumps(reasonings, indent=2) + "\n- Modified_Sample:\n" + json.dumps(modi, indent=2)
        ratios.append(len(encoding.encode(output_text))/len(encoding.encode(ori_text)))
    return sum(ratios)/len(ratios)


if __name__ == "__main__":
    # ds = read_data("../data/evol_instruct-decontaminated.jsonl")
    ds = read_data("oss_instruct.json")
    # ratio = calcu_ratio_from_input_to_output()
    # print(f"ratio from input to output: {ratio}")
    prompts = []
    for i in range(3):
        writer = open(f"ctf_oss_prompts_{i}.jsonl", "w")
        prompts.append(writer)

    # input_tokens = []
    # output_tokens = []
    for i, d in tqdm.tqdm(enumerate(ds), total=len(ds)):
        prompt = encode_prompt(d)
        # input_tokens.append(len(encoding.encode(prompt)))
        data = {"id":i, "query": prompt}
        prompts[i%3].write(json.dumps(data) + "\n")
    
        # prompts.write(json.dumps(data) + "\n")
        # d_tokens = len(encoding.encode(json.dumps(d)))
        # output_tokens.append(d_tokens*ratio)
    # print(f"sum of input tokens: {sum(input_tokens)}")
    # print(f"sum of output tokens: {sum(output_tokens)}")
