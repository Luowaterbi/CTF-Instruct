import json
import random
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, default="oss_instruct.json")
    parser.add_argument("--input_file2", type=str, default="ctf_oss_all_kcenter_72957.json")
    parser.add_argument("--output_file", type=str, default="merged.json")
    parser.add_argument("--shuffle", type=bool, default=False)
    parser.add_argument("--k", type=int, default=0)
    args = parser.parse_args()
    ds1 = json.load(open(args.input_file, "r"))
    ds2 = json.load(open(args.input_file2, "r"))
    for d in ds2:
        if "ori" in d:
            del d["ori"]
        if "loss" in d:
            del d["loss"]
    if args.shuffle:
        random.shuffle(ds2)
    if args.k == 0:
        args.k = len(ds2)
    merge = ds1 + ds2[:args.k]
    print("Merged: ", len(merge))
    json.dump(merge, open(args.output_file, "w"), indent=4)