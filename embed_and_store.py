import json
import pandas as pd
from sentence_transformers import SentenceTransformer, util

# Step 1: Load and parse JSON file
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Step 2: Load legal texts from JSON file
json_file_path = "D:/activities/legal_IR/2019-02-19_oldp_cases.json"
legal_data = load_json(json_file_path)

# Convert loaded data to a list of texts (adjust according to the JSON structure)
if isinstance(legal_data, dict):
    legal_texts = [entry['text'] for entry in legal_data.values() if 'text' in entry]
elif isinstance(legal_data, list):
    legal_texts = [entry['text'] for entry in legal_data if 'text' in entry]
else:
    legal_texts = []

print(f"Loaded {len(legal_texts)} legal texts.")

# Step 3: Initialize the SentenceTransformer model
model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

# Step 4: Create embeddings for legal texts
embeddings = model.encode(legal_texts, convert_to_tensor=True)

# Step 5: Function to perform similarity search
def search(query, top_k=5):
    # Encode the query
    query_embedding = model.encode(query, convert_to_tensor=True)
    
    # Compute cosine similarities
    cos_scores = util.pytorch_cos_sim(query_embedding, embeddings)[0]
    
    # Get the top_k results
    top_results = torch.topk(cos_scores, k=top_k)
    
    # Return the results
    return [(legal_texts[idx], cos_scores[idx].item()) for idx in top_results.indices]

# Step 6: Example of searching for similar legal texts
query = "Die Klägerin fordert die Rückzahlung."
results = search(query)

# Display the results
for text, score in results:
    print(f"Text: {text}\nScore: {score}\n")
