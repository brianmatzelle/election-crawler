# About
This directory is responsible for the fun part of this project.
First, in this directory we take care of **[raw data](#defining-raw-data) parsing + cleaning**.
Then, we move to the `models/` directory to transform the cleaned dataset into a further refined dataset, specifically prepared for finetuning a large language model.
For example, the `hasan_piker/` directory is where we will build a dataset containing comments, prepared for finetuning llama3.1.

## Quickstart for WSL:
1. install cuda 12.1 [inst.](https://developer.nvidia.com/cuda-12-1-0-download-archive?target_os=Linux&target_arch=x86_64&Distribution=WSL-Ubuntu&target_version=2.0&target_type=deb_network)
2. install anaconda on wsl [inst.](https://gist.github.com/kauffmanes/5e74916617f9993bc3479f401dfec7da)
3. cd here (`finetune/`)
4. run `conda env create -f wsl-environment.yml`

Notebook run order:
`prepare-dev.ipynb` -> `clean.ipynb` ->

DEPRECATED:
archive/*

## TODO:
- [ ] refactor `clean.ipynb`
- [ ] make sure no posts or comments are skipped when parsing
- [ ] build dataset

### Notes:
Using [this](https://www.youtube.com/watch?v=pxhkDaKzBaY) tutorial to help me finetune llama3.1.

### Defining "raw data":
Raw data is the collection of posts scraped from Reddit. They were not preprocessed at all, just stored in a MongoDB data lake.