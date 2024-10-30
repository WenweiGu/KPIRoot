# KPIRoot: Efficient Monitoring Metric-based Root Cause Localization in Large-scale Cloud Systems

This is the public repository for our paper **"KPIRoot: Efficient Monitoring Metric-based Root Cause Localization in Large-scale Cloud Systems"** accepted by ISSRE 2024, Research Track. 
In this paper, we propose an automated approach to extract fault-indicating information from logs.

![Extracting Log Fault-indicting Information](./docs/diagnosis.png)

```

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
