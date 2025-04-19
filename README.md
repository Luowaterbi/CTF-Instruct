# Success is in the Details: Test Sensitivity to Details and Boost Performance of Code LLMs through Counterfactuals

<a href="https://huggingface.co/datasets/Luoberta/CTF-Instruct" target="_blank">🤗 Dataset(HuggingFace)</a> | <a href="https://www.modelscope.cn/datasets/Luoberta/CTF-Instruct" target="_blank">🤖 Dataset(ModelScope)</a> | <a href="https://huggingface.co/Luoberta/CTFCoder" target="_blank">🤗 Model(HuggingFace)</a> | <a href="https://www.modelscope.cn/models/Luoberta/CTFCoder" target="_blank">🤖 Model(ModelScope)</a> | <a href="" target="_blank">📑 Paper(Comming Soon) </a>

This repository contains the code to train and infer CTFCoder. 


<!-- ## Overview

![main](fig/main.png) -->

## Data
|  Dataset  | Download Link  |
|  ----  | ----  |
|CTF-Instruct  | [HuggingFace](https://huggingface.co/datasets/Luoberta/CTF-Instruct) |
|CTF-Instruct  | [ModelScope](https://www.modelscope.cn/datasets/Luoberta/CTF-Instruct)|
|CTF-Evol-Instruct  | [ModelScope](modelscope.cn/datasets/Luoberta/CTF-Evol-Instruct/)|
|CTF-Oss-Instruct  | [ModelScope](https://www.modelscope.cn/datasets/Luoberta/CTF-Oss-Instruct)|

<!-- ## Train
The whole training process consists of two stages. To train the ChartCoder, ```siglip-so400m-patch14-384``` and ```deepseek-coder-6.7b-instruct``` should be downloaded first.

For **Pre-training**, run
```
bash scripts/train/pretrain_siglip.sh
```
For **SFT**, run 
```
bash scripts/train/finetune_siglip_a4.sh
```
Please change the model path to your local path. See the corresponding ```.sh ``` file for details. 
We also provide other training scripts, such as using CLIP ```_clip``` and multiple machines ```_m```. See ``` scripts/train ``` for further information.

## Inference
Please see ```inference.py``` for details. -->

<!-- ## Results
Please refer to our paper for detailed performance on ChartMimic, Plot2Code and ChartX benchmarks. Thanks for these contributions to the chart-to-code field.
![results](fig/results.png) -->

## Contact

For any questions, you can contact [xzluo@ir.hit.edu.cn](mailto:xzluo@ir.hit.edu.cn).


## Citation
If you find this work useful, consider giving this repository a star ⭐️ and citing 📝 our paper as follows:
```
Comming Soon...
```

## Acknowledgement
The code is based on the [evalplus](https://github.com/evalplus/evalplus),[LiveCodebench](https://github.com/LiveCodeBench/LiveCodeBench), Thanks for these great works and open sourcing!
