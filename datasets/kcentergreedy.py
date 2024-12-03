from scipy.spatial import distance
import numpy as np
import multiprocessing as mp
from tqdm import tqdm
import argparse
import torch
import json


def compute_distances(chunk, centers):
    dist_matrix = distance.cdist(centers, chunk, 'euclidean')
    min_dists = np.min(dist_matrix, axis=0)
    return min_dists


def k_center_greedy_parallel(old, new, new_data, k, n_processors, emb_type):
    n_samples = len(new)
    new_ds = []
    new_dist = []
    new_embeddings = []
    pool = mp.Pool(processes=n_processors)

    # 初始化距离矩阵
    dists = np.full(n_samples, np.inf)
    remaining_indices = np.arange(n_samples)
    
    for _ in tqdm(range(k)):
        # Divide data into chunks for each processor
        chunk_size = int(np.ceil(len(remaining_indices) / n_processors))
        chunks = [remaining_indices[i * chunk_size:min((i + 1) * chunk_size, len(remaining_indices))] for i in range(n_processors)]
        
        # 使用Pool的map方法并行计算距离并更新最小距离
        results = pool.starmap(compute_distances, [(new[chunk], old) for chunk in chunks])
        results = np.concatenate(results)
        dists[remaining_indices] = np.minimum(dists[remaining_indices], results)
        # print(results)
        # print(dists[remaining_indices])

        # 找到距离最大的点作为下一个中心
        cur_dist = np.max(dists[remaining_indices])
        if cur_dist == 0.0:
            print("now dist is 0")
            break 
        next_index_local = np.argmax(dists[remaining_indices])
        next_index = remaining_indices[next_index_local]
        old = new[next_index].reshape(1, -1)
        new_ds.append(new_data[next_index])
        new_dist.append(dists[next_index])
        new_embeddings.append(new[next_index].unsqueeze(0))
        
        # 更新remaining_indices
        remaining_indices = np.delete(remaining_indices, next_index_local)

        # if len(new_ds) % 30000 == 0:
        #     json.dump(new_ds, open(f"evol_{emb_type}_kcenter_middle_{len(new_ds)}.json", "w"), indent=4)

    return new_ds, new_dist, new_embeddings


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--old', type=str, default="evol_ori_final_filter")
    parser.add_argument('--new', type=str, default="evol_ctf_final_filter")
    parser.add_argument('--emb_type', type=str, default="avg")
    parser.add_argument('--k', type=int, default=0)
    args = parser.parse_args()
    sources_embeddings = {}

    new_data = json.load(open(f"{args.new}.json", "r"))
    sources_embeddings["ori"] = torch.load(f"evol_ori_final_combined_embeddings_{args.emb_type}.pt")
    sources_embeddings["ctf"] = torch.load(f"evol_ctf_final_combined_embeddings_{args.emb_type}.pt")
    old = [torch.tensor(v) for v in sources_embeddings["ori"].values()]
    old = torch.stack(old)
    new = [torch.tensor(sources_embeddings["ctf"][str(d["idx"])]) for d in new_data]
    new = torch.stack(new)
    n_processors = mp.cpu_count()
    if args.k == 0:
        args.k = len(new_data)
    print("old size:", old.size(), "new size:", new.size(), "new data size:", len(new_data), "emb_type", args.emb_type, "k:", args.k)
    new_ds, new_dist, _ = k_center_greedy_parallel(old, new, new_data, min(args.k, len(new_data)), n_processors, args.emb_type)
    json.dump(new_ds, open(f"evol_{args.emb_type}_kcenter_{args.k}.json", "w"))
    json.dump(new_dist, open(f"evol_{args.emb_type}_kcenter_{args.k}_dist.json", "w"))