import os
import torch
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM, pipeline

# Load the tokenizer and model used for embedding
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# Load a text generation model (like GPT)
text_gen_model = AutoModelForCausalLM.from_pretrained("gpt2")
text_gen_tokenizer = AutoTokenizer.from_pretrained("gpt2")
text_generator = pipeline("text-generation", model=text_gen_model, tokenizer=text_gen_tokenizer)

# Load the pre-computed embeddings from the .pt file
embeddings = torch.load('./xml_embeddings.pt', weights_only=True)  # Assuming this contains a dict of file embeddings
file_names = list(embeddings.keys())  # List of file names (cases)

# Convert embeddings from torch tensors to numpy for cosine similarity computation
case_embeddings = torch.stack(list(embeddings.values())).numpy()

# Function to embed the input case summary
def embed_summary(summary):
    inputs = tokenizer(summary, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)  # Average pooling
    return embeddings

def find_similar_cases(input_embedding, case_embeddings, file_names, top_k=5):
    # Reshape input embedding
    
    if len(input_embedding.shape) == 3:
        input_embedding = input_embedding.reshape(input_embedding.shape[0], -1)
    if len(case_embeddings.shape) == 3:
        case_embeddings = case_embeddings.reshape(case_embeddings.shape[0], -1)
   
    print("Input embedding shape:", input_embedding.shape)  # Should be [1, 384]
    print("Case embeddings shape:", case_embeddings.shape)  # Should be [n_cases, 768]

    # Adjust case_embeddings to match input_embedding size
    if case_embeddings.shape[1] > input_embedding.shape[1]:
        case_embeddings = case_embeddings[:, :input_embedding.shape[1]]  # Truncate to 384

    # Calculate cosine similarities
    similarities = cosine_similarity(input_embedding, case_embeddings)

    # Get the top K indices
    top_k_indices = similarities[0].argsort()[-top_k:][::-1]
    
    # Retrieve the corresponding file names and similarity scores
    similar_cases = [(file_names[i], similarities[0][i]) for i in top_k_indices]
    return similar_cases

# Function to generate explanations for the similar cases
def generate_explanation(input_summary, similar_cases):
    explanations = []
    for case_name, _ in similar_cases:
        prompt = f"Explain how the case '{case_name}' relates to the following case summary: {input_summary}"
        explanation = text_generator(prompt, max_length=100, num_return_sequences=1)[0]['generated_text']
        explanations.append((case_name, explanation))
    return explanations

# Main code to find similar cases and generate explanations
if __name__ == "__main__":
    # Input case summary to be embedded
    input_summary = input("Enter the case summary: ")

    # Input number of similar cases to find
    top_k = int(input("Enter the number of similar cases to find (e.g., 5): "))

    # Embed the input summary
    input_embedding = embed_summary(input_summary)

    # Find top-k similar cases
    similar_cases = find_similar_cases(input_embedding, case_embeddings, file_names, top_k=top_k)
    
    # Print the similar cases
    print(f"Top {top_k} similar cases:")
    for case_name, similarity in similar_cases:
        print(f"Case: {case_name}, Similarity: {similarity:.4f}")
    
    # Generate explanations for the similar cases
    explanations = generate_explanation(input_summary, similar_cases)
    
    # Print explanations
    print("\nExplanations for similar cases:")
    for case_name, explanation in explanations:
        print(f"Case: {case_name}\nExplanation: {explanation}\n")

