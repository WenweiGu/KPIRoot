# [ISSRE'24] KPIRoot: Efficient Monitoring Metric-based Root Cause Localization in Large-scale Cloud Systems

This is the public repository for our paper **"KPIRoot: Efficient Monitoring Metric-based Root Cause Localization in Large-scale Cloud Systems"** accepted by ISSRE 2024, Research Track. 
In this paper, we propose an efficient and effective approach to localize the root causes of VM instances.

![overview](https://github.com/user-attachments/assets/8e85580c-7d6b-4e93-aff7-6ef2ecc42fad)


## Quick Start
- Install Requirements

```
conda create -n kpiroot python=3.9
conda activate kpiroot
pip install -r requirements.txt
```

- Run the script
```
python3 kpiroot.py
```

### Dataset

The dataset is available at `./data/`.
In this repository, we provide an anonymized data sample with confidential information removed.

### Citation
If you find this repo helpful, please cite our paper:

```
@inproceedings{gu2024kpiroot,
  title={KPIRoot: Efficient Monitoring Metric-based Root Cause Localization in Large-scale Cloud Systems},
  author={Gu, Wenwei and Sun, Xinying and Liu, Jinyang and Huo, Yintong and Chen, Zhuangbin and Zhang, Jianping and Gu, Jiazhen and Yang, Yongqiang and Lyu, Michael R},
  booktitle={2024 IEEE 35th International Symposium on Software Reliability Engineering (ISSRE)},
  pages={403--414},
  year={2024},
  organization={IEEE}
}
```
