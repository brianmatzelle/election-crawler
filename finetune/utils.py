import os
import json

def get_unique_filename(file_path):
    """
    Appends a number to the file name if the file already exists.
    I always overwrite the file by accident so this is a safety measure lol
    """
    base, ext = os.path.splitext(file_path)
    counter = 1
    new_file_path = file_path

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    while os.path.exists(new_file_path):
        new_file_path = f"{base}({counter}){ext}"
        counter += 1
    return new_file_path

def dump_unique_json(data, file_path):
    """
    Dumps json to a file, appending a number to the file name if it already exists.
    """
    new_file_path = get_unique_filename(file_path)
    with open(new_file_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {new_file_path}")
    return new_file_path

def to_k(size: int, logger):
  if size < 1000:
    logger.error(f"{size} rows is too small to train a model with, exiting")
    exit(1)
  elif size < 1000000:
    logger.info(f"{size // 1000}k rows")
    return f"{size // 1000}k"
  else:
    logger.info(f"{size // 1000000}.{size // 100000 % 10}M rows")
    return f"{size // 1000000}.{size // 100000 % 10}M"
  

def is_comment_valid(comment) -> tuple[bool, str]:
  if (comment.startswith('!') and comment != "!") or 'http:' in comment or 'https:' in comment:
    return False, f"Comment is a bot call or contains a link: {comment}"
  match comment:
    case '[deleted]':
      return False, "Comment was deleted"
    case '[removed]':
      return False, "Comment was removed"
    case _:
      return True, ""
    
def is_post_valid(post_row) -> tuple[bool, str]:
  if post_row['selftext'].startswith('#'):
    return False, f"Post is a bot: {post_row['selftext']}"
  if post_row['num_comments'] == 0:
    return False, "Post has no comments"
  return True, ""

def get_conversations_file(cfg: str, size: str): 
  name = f"{cfg}-conversations-{size}"
  path = f'data/datasets/{name}.json'.lower()
  unique_path = get_unique_filename(path)
  return unique_path, name