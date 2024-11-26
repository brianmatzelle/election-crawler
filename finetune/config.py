# Description: Configuration file for the finetune module, could eventually be used as flags

# feel free to change these to make new datasets
SUBREDDITS = [
  'destiny', 
  'hasan_piker'
]

HUGGINGFACE_USERNAME = 'brianmatzelle'


# change if you know what you're doing
RAW_DATA_FILE_NAME = 'posts-11-13-2024'

# DONT CHANGE
RAW_DATA_FILE = f'data/raw/{RAW_DATA_FILE_NAME}.json'
PROCESSED_DATA_FILE = f'data/processed/{RAW_DATA_FILE_NAME}-processed.json'