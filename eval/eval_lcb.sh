cd LiveCodeBench
models=(ctfcoder)

for model in "${models[@]}"
do
    echo $model
    model_path=/path/to/model/${model}
    checkpoints=($(ls -d ${model_path}/*/ | grep -v 'runs'))
    for checkpoint in "${checkpoints[@]}"
    do
        checkpoint_name=$(basename "${checkpoint}")
        echo $checkpoint_name
        python -m lcb_runner.runner.main \
            --model ${model}-${checkpoint_name} \
            --local_model_path ${checkpoint} \
            --use_cache --scenario codegeneration \
            --evaluate \
            --num_process_evaluate 100 \
            --continue_existing_with_eval \
            --release_version release_v3 \
            --stop "###,<|EOT|>" && \
        python -m lcb_runner.evaluation.compute_scores --eval_all_file output/${model}-${checkpoint_name}/Scenario.codegeneration_10_0.2_eval_all.json
    done
done