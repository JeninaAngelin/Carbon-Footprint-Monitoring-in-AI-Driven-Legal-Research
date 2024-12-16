import os
import xml.etree.ElementTree as ET
from datetime import datetime
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

# Load the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# Function to extract legal case data from XML files
def extract_case_data(xml_folder):
    cases = []
    for filename in os.listdir(xml_folder):
        if filename.endswith('.xml'):
            tree = ET.parse(os.path.join(xml_folder, filename))
            root = tree.getroot()
            case_name = root.find('name').text
            date_str = root.find('date').text  # Adjust this according to your XML structure
            date = datetime.strptime(date_str, '%Y-%m-%d')  # Adjust format as needed
            related_cases = [related.text for related in root.findall('related_cases/case')]
            cases.append({'case_name': case_name, 'date': date, 'related_cases': related_cases})
    return cases

# Function to embed the input summary
def embed_summary(summary):
    inputs = tokenizer(summary, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)  # Average pooling
    return embeddings

# Function to find similar cases based on cosine similarity
def find_similar_cases(input_embedding, case_embeddings, cases, top_k=5):
    similarities = cosine_similarity(input_embedding.numpy(), case_embeddings.numpy())
    similar_indices = similarities.argsort()[0][-top_k:][::-1]  # Get indices of top_k similar cases
    similar_cases = [(cases[i]['case_name'], cases[i]['date']) for i in similar_indices]
    return similar_cases

# Load case data and embeddings
xml_folder = 'data\cleaned_new_new'
legal_cases = extract_case_data(xml_folder)

# Load the embeddings from the file
embeddings = torch.load('./xml_embeddings.pt')

# Example input summary
input_summary = "This case involves the interpretation of land rights and the responsibilities of the Native Title Registrar."
input_embedding = embed_summary(input_summary)

# Find and print similar cases
similar_cases = find_similar_cases(input_embedding, embeddings, legal_cases)
for case_name, date in similar_cases:
    print(f"Case: {case_name}, Date: {date.strftime('%Y-%m-%d')}")