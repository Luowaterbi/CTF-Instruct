#!/bin/bash
export VLLM_WORKER_MULTIPROC_METHOD=spawn

model=ctfcoder
model_path=/path/to/ctfcoder
datasets=("humaneval" "mbpp")

# 模型参数
temp=0
max_len=2048
pred_num=1
num_seqs_per_iter=1

# 循环每一个模型检查点和数据集
for dataset in "${datasets[@]}"
do
    output_path=../preds_${dataset}/${model}/T${temp}_N${pred_num}
    mkdir -p ${output_path}
    echo 'Output path: '$output_path
    python generate.py --model ${model_path} --dataset ${dataset} --temperature ${temp} \
        --num_seqs_per_iter ${num_seqs_per_iter} --N ${pred_num} --max_len ${max_len} --output_path ${output_path} --num_gpus 8
    python process.py --path ${output_path} --out_path ${output_path}.jsonl --dataset ${dataset}
    python evaluate.py --path ${output_path}.jsonl --dataset ${dataset} --N 1 | tee ${output_path}_pass@k.txt
done

cd LiveCodeBench
python -m lcb_runner.runner.main \
    --model ${model} \
    --local_model_path ${model_path} \
    --use_cache --scenario codegeneration \
    --evaluate \
    --num_process_evaluate 100 \
    --continue_existing_with_eval \
    --release_version release_v3 \
    --stop "###,<|EOT|>" && \
python -m lcb_runner.evaluation.compute_scores --eval_all_file output/${model}/Scenario.codegeneration_10_0.2_eval_all.json --start_date 2024-01-01

