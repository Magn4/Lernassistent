import time
from datasets import load_dataset

print("Loading dataset...")

try:
    start_time = time.time()
    ds = load_dataset("open-spaced-repetition/anki-revlogs-10k", "cards")
    elapsed_time = time.time() - start_time

    print(f"Dataset loaded successfully in {elapsed_time:.2f} seconds.")
    print(ds)
except ValueError as e:
    print("Error: Invalid dataset format or arguments.")
    print(f"Details: {e}")
except FileNotFoundError as e:
    print("Error: Dataset not found. Please ensure the dataset name and arguments are correct.")
    print(f"Details: {e}")
except Exception as e:
    print("An unexpected error occurred while loading the dataset.")
    print(f"Details: {e}")
