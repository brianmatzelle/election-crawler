# About

This directory is responsible for the fun part of this project.
First, in this directory we take care of **[raw data](#defining-raw-data) parsing + cleaning**.

## Quickstart for WSL

1. install cuda 12.1 [inst.](https://developer.nvidia.com/cuda-12-1-0-download-archive?target_os=Linux&target_arch=x86_64&Distribution=WSL-Ubuntu&target_version=2.0&target_type=deb_network)
2. install anaconda on wsl [inst.](https://gist.github.com/kauffmanes/5e74916617f9993bc3479f401dfec7da)
3. cd to this directory (`finetune/`)
4. run `conda env create -f wsl-environment.yml`

Notebook run order:
`process-raw-data.ipynb` -> `dataset.ipynb` -> `finetune.ipynb`

DEPRECATED:
archive/*

## TODO

- [X] make sure no posts or comments are skipped when parsing
- [X] build dataset
- [ ] refactor datasets into two types
  - [ ] main datset with all threads, with attributes describing the threads
  - [ ] refined datasets that are subsets of this main dataset

### Notes

Using these resources to help me build datasets and finetune llama3.1 in conversational style:

- [youtube tutorial](https://www.youtube.com/watch?v=pxhkDaKzBaY)
- [colab notebook from unsloth](https://colab.research.google.com/drive/15OyFkGoCImV9dSsewU1wa2JuKB4-mDE_?usp=sharing)

### Defining "raw data"

Raw data is the collection of posts scraped from Reddit. They were not preprocessed at all, just stored in a MongoDB data lake.
