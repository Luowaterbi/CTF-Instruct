#!/bin/bash
export VLLM_WORKER_MULTIPROC_METHOD=spawn
# 定义模型检查点和数据集数组
model=$1
model_path=/path/to/model/$1
checkpoints=($(ls -d ${model_path}/*/ | grep -v 'runs'))
datasets=("humaneval" "mbpp")

# 模型参数
temp=0
max_len=2048
pred_num=1
num_seqs_per_iter=1

# 循环每一个模型检查点和数据集
for checkpoint in "${checkpoints[@]}"
do
    for dataset in "${datasets[@]}"
    do
        checkpoint_name=$(basename "${checkpoint}")
        output_path=../preds_${dataset}/${model}-${checkpoint_name}/T${temp}_N${pred_num}
        if [ -d "${output_path}" ]; then
            echo 'Output path already exists: '$output_path', skipping...'
            continue
        fi
        mkdir -p ${output_path}
        echo 'Output path: '$output_path
        echo 'Model to eval: '$checkpoint
        python generate.py --model ${checkpoint} --dataset ${dataset} --temperature ${temp} \
            --num_seqs_per_iter ${num_seqs_per_iter} --N ${pred_num} --max_len ${max_len} --output_path ${output_path} --num_gpus 8
        python process.py --path ${output_path} --out_path ${output_path}.jsonl --dataset ${dataset}
        python evaluate.py --path ${output_path}.jsonl --dataset ${dataset} --N 1 | tee ${output_path}_pass@k.txt
    done
done