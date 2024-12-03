import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from torch.utils.data.distributed import DistributedSampler
import torch.distributed as dist
from transformers import AutoModelForCausalLM, AutoTokenizer
import argparse
import os
import json
from tqdm import tqdm


prompt_no_input = (
    "Below is an instruction that describes a task. "
    "Write a response that appropriately completes the request.\n\n"
    "### Instruction:\n{instruction}\n\n### Response:"
)

def parse_args():
    parser = argparse.ArgumentParser(description="Compute embeddings for data using a decoder model")
    parser.add_argument('--model_name_or_path', type=str, default='gpt2', help='Model name or path')
    parser.add_argument('--data_file', type=str, required=True, help='Path to data file (JSON lines format)')
    parser.add_argument('--output_dir', type=str, required=True, help='Directory to save embeddings')
    parser.add_argument('--batch_size', type=int, default=8, help='Batch size per GPU')
    parser.add_argument('--local-rank', type=int, default=-1, help='Local rank for distributed training')
    parser.add_argument('--max_seq_length', type=int, default=2048, help='Maximum sequence length')
    parser.add_argument('--debug', action='store_true', help='Debug mode')
    args = parser.parse_args()
    return args


class MyDataset(Dataset):
    def __init__(self, ds, tokenizer, max_seq_length):
        self.data = ds
        self.tokenizer = tokenizer
        self.max_seq_length = max_seq_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        instruction = item['instruction']
        output = item['output']
        # Prepare instruction input
        instruction_encoding = self.tokenizer(instruction, truncation=True, max_length=self.max_seq_length, return_tensors='pt')
        # Prepare combined input
        combined_text = prompt_no_input.format(instruction=self.data[idx]['instruction']) + self.data[idx]['output']
        combined_encoding = self.tokenizer(combined_text, truncation=True, max_length=self.max_seq_length, return_tensors='pt')
        return {
            'instruction_input_ids': instruction_encoding['input_ids'].squeeze(0),
            'instruction_attention_mask': instruction_encoding['attention_mask'].squeeze(0),
            'combined_input_ids': combined_encoding['input_ids'].squeeze(0),
            'combined_attention_mask': combined_encoding['attention_mask'].squeeze(0),
            'index': idx
        }

def collate_fn(batch, tokenizer):
    # Collate function to pad sequences
    instruction_input_ids = [item['instruction_input_ids'] for item in batch]
    instruction_attention_mask = [item['instruction_attention_mask'] for item in batch]
    combined_input_ids = [item['combined_input_ids'] for item in batch]
    combined_attention_mask = [item['combined_attention_mask'] for item in batch]
    indices = [item['index'] for item in batch]
    instruction_input_ids = nn.utils.rnn.pad_sequence(instruction_input_ids, batch_first=True, padding_value=tokenizer.pad_token_id)
    instruction_attention_mask = nn.utils.rnn.pad_sequence(instruction_attention_mask, batch_first=True, padding_value=0)
    combined_input_ids = nn.utils.rnn.pad_sequence(combined_input_ids, batch_first=True, padding_value=tokenizer.pad_token_id)
    combined_attention_mask = nn.utils.rnn.pad_sequence(combined_attention_mask, batch_first=True, padding_value=0)
    return {
        'instruction_input_ids': instruction_input_ids,
        'instruction_attention_mask': instruction_attention_mask,
        'combined_input_ids': combined_input_ids,
        'combined_attention_mask': combined_attention_mask,
        'indices': indices
    }

def setup_distributed():
    dist.init_process_group(backend='nccl')

def cleanup():
    dist.destroy_process_group()

def main():
    args = parse_args()

    # Initialize distributed process group
    torch.cuda.set_device(args.local_rank)
    dist.init_process_group(backend='nccl')
    world_size = dist.get_world_size()
    rank = dist.get_rank()

    # Create output directory (only once)
    # if rank == 0 and not os.path.exists(args.output_dir):
    #     os.makedirs(args.output_dir)
    dist.barrier()  # Ensure all processes wait until directory is created

    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path)
    # Ensure padding token is defined
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(args.model_name_or_path)
    model.eval()
    model.to(torch.device('cuda', args.local_rank))

    # Wrap model with DDP
    model = nn.parallel.DistributedDataParallel(model, device_ids=[args.local_rank], output_device=args.local_rank, find_unused_parameters=False)

    # Prepare dataset and dataloader
    ds = json.load(open(args.data_file, "r"))
    if args.debug:
        ds = ds[:400]
    dataset = MyDataset(ds, tokenizer, args.max_seq_length)
    sampler = DistributedSampler(dataset, shuffle=False)
    dataloader = DataLoader(dataset, batch_size=args.batch_size, sampler=sampler, collate_fn=lambda x: collate_fn(x, tokenizer))

    # For saving embeddings per process
    local_embeddings = []

    with torch.no_grad():
        for batch in tqdm(dataloader, desc=f"Rank {rank}", ncols=80):
            # Move tensors to device
            instruction_input_ids = batch['instruction_input_ids'].to(model.device)
            instruction_attention_mask = batch['instruction_attention_mask'].to(model.device)
            combined_input_ids = batch['combined_input_ids'].to(model.device)
            combined_attention_mask = batch['combined_attention_mask'].to(model.device)
            indices = batch['indices']

            # Get model outputs for instruction
            outputs_instruction = model(input_ids=instruction_input_ids, attention_mask=instruction_attention_mask, output_hidden_states=True)
            hidden_states_instruction = outputs_instruction.hidden_states[-1]  # Last hidden layer

            # Compute average pooling
            instruction_avg_pool = (hidden_states_instruction * instruction_attention_mask.unsqueeze(-1)).sum(dim=1) / instruction_attention_mask.sum(dim=1, keepdim=True)
            # Get last token hidden state
            instruction_last_token = hidden_states_instruction[torch.arange(hidden_states_instruction.size(0)), instruction_attention_mask.sum(dim=1) - 1]

            # Get model outputs for combined
            outputs_combined = model(input_ids=combined_input_ids, attention_mask=combined_attention_mask, output_hidden_states=True)
            hidden_states_combined = outputs_combined.hidden_states[-1]  # Last hidden layer

            # Compute average pooling
            combined_avg_pool = (hidden_states_combined * combined_attention_mask.unsqueeze(-1)).sum(dim=1) / combined_attention_mask.sum(dim=1, keepdim=True)
            # Get last token hidden state
            combined_last_token = hidden_states_combined[torch.arange(hidden_states_combined.size(0)), combined_attention_mask.sum(dim=1) - 1]

            # Store embeddings
            for idx in range(len(indices)):
                index = indices[idx]
                embedding = {
                    'index': index,
                    'instruction_avg': instruction_avg_pool[idx].cpu().numpy(),
                    'instruction_last': instruction_last_token[idx].cpu().numpy(),
                    'combined_avg': combined_avg_pool[idx].cpu().numpy(),
                    'combined_last': combined_last_token[idx].cpu().numpy()
                }
                local_embeddings.append(embedding)

    # Gather all embeddings from all processes
    all_embeddings = [None for _ in range(world_size)]
    dist.all_gather_object(all_embeddings, local_embeddings)

    # Only rank 0 process saves the combined embeddings
    if rank == 0:
        # Flatten the list of lists
        combined_embeddings = []
        for embeddings in all_embeddings:
            combined_embeddings.extend(embeddings)
        # Sort embeddings by index to maintain order
        combined_embeddings.sort(key=lambda x: x['index'])

        # Prepare final embeddings dictionaries
        instruction_embeddings_avg = {}
        instruction_embeddings_last = {}
        combined_embeddings_avg = {}
        combined_embeddings_last = {}

        for item in combined_embeddings:
            # str是一个失误，但是因为之后的都是str的，所以将错就错了
            index = str(ds[item['index']]["idx"])
            instruction_embeddings_avg[index] = item['instruction_avg']
            instruction_embeddings_last[index] = item['instruction_last']
            combined_embeddings_avg[index] = item['combined_avg']
            combined_embeddings_last[index] = item['combined_last']

        # Save embeddings
        torch.save(instruction_embeddings_avg, args.output_dir + '_instruction_embeddings_avg.pt')
        torch.save(instruction_embeddings_last, args.output_dir + '_instruction_embeddings_last.pt')
        torch.save(combined_embeddings_avg, args.output_dir + '_combined_embeddings_avg.pt')
        torch.save(combined_embeddings_last, args.output_dir + '_combined_embeddings_last.pt')

if __name__ == '__main__':
    main()