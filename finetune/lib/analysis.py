# helper analysis functions for all notebooks

def normalize_controversiality_rating(sum: int, thread_length: int, decimals=5):
    """
    Important: This function should be called on the thread, not the conversation that includes the system message

    Normalize controversiality rating by dividing the sum of controversiality ratings by the conversation length
    - sum: sum of controversiality ratings in a thread
    Note: since the post itself does not have a rating, we remove it from the conversation length to prevent dilution
          - this is why we have the is_post_included parameter
          - is_post_included is true when the post hasn't been removed or deleted
          - see how we build conversations in dataset.ipynb to understand why we need this parameter
    """
    normalized_rating = sum / thread_length
    return round(normalized_rating, decimals)


if __name__ == "__main__":
  print("Running analysis.py development tests:")

  # normalized_controversiality_rating() test params
  sum, thread_len, decimals = 4, 10, 5 
  print(f"normalized_controversiality_rating({sum}, {thread_len}, {decimals}): {normalize_controversiality_rating(sum, thread_len, decimals)}")

  sum, thread_len, decimals = 8, 10, 2 
  print(f"normalized_controversiality_rating({sum}, {thread_len}, {decimals}): {normalize_controversiality_rating(sum, thread_len, decimals)}")
  
  sum, thread_len, decimals = 2, 4, 4 
  print(f"normalized_controversiality_rating({sum}, {thread_len}, {decimals}): {normalize_controversiality_rating(sum, thread_len, decimals)}")