data=$1
python -m torch.distributed.launch --nproc_per_node=8 calcu_embedding.py \
    --model_name_or_path /mnt/afs/xzluo/ctf/dc-1.3b-cf/checkpoint-306 \
    --data_file ../datasets/new_ctf/main/${1}_exps.json \
    --output_dir /mnt/afs/xzluo/data/${1}_exps \
    --batch_size 8 \
    --max_seq_length 2048 

python -m torch.distributed.launch --nproc_per_node=8 calcu_embedding.py \
    --model_name_or_path /mnt/afs/xzluo/ctf/dc-1.3b-cf/checkpoint-306 \
    --data_file ../datasets/new_ctf/main/${1}_oris.json \
    --output_dir /mnt/afs/xzluo/data/${1}_oris \
    --batch_size 8 \
    --max_seq_length 2048 

python -m torch.distributed.launch --nproc_per_node=8 calcu_embedding.py \
    --model_name_or_path /mnt/afs/xzluo/ctf/dc-1.3b-cf/checkpoint-306 \
    --data_file ../datasets/new_ctf/main/${1}_ctfs.json \
    --output_dir /mnt/afs/xzluo/data/${1}_ctfs \
    --batch_size 8 \
    --max_seq_length 2048 