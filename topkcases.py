import os
import torch
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import matplotlib.pyplot as plt
from transformers import AutoTokenizer, AutoModel

# Load the tokenizer and model used for embedding
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# Load the pre-computed embeddings from the .pt file
embeddings = torch.load('./xml_embeddings.pt',weights_only=True)  
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
    # Reshape embeddings if necessary
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
    # ... (rest of your function)

    # Get the top K indices
    top_k_indices = similarities[0].argsort()[-top_k:][::-1]
    
    # Retrieve the corresponding file names and similarity scores
    similar_cases = [(file_names[i], similarities[0][i]) for i in top_k_indices]
    return similar_cases

# Function to construct a graph based on similarity between cases
def construct_case_graph(case_embeddings, threshold=0.75):
    G = nx.Graph()
    
    # Add nodes (case files)
    for i, case_name in enumerate(file_names):
        G.add_node(i, label=case_name)

    # Add edges based on cosine similarity between embeddings
    for i in range(len(case_embeddings)):
        for j in range(i+1, len(case_embeddings)):
            similarity = cosine_similarity(case_embeddings[i].reshape(1, -1), case_embeddings[j].reshape(1, -1))[0][0]
            if similarity > threshold:  # Only add edges above the similarity threshold
                G.add_edge(i, j, weight=similarity)

    return G

# Function to visualize the graph
def visualize_case_graph(G):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 7))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', font_size=10, node_size=500)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Graph of Legal Cases Based on Similarity")
    plt.show()

# Main code to find similar cases and construct the graph
if __name__ == "__main__":
    # Input case summary to be embedded
    input_summary = "This case involves the interpretation of land rights and responsibilities of the Native Title Registrar."

    # Embed the input summary
    input_embedding = embed_summary(input_summary)
    input_embedding = input_embedding.reshape(1, -1)

    # Find top-5 similar cases
    similar_cases = find_similar_cases(input_embedding, case_embeddings, file_names, top_k=5)
    
    # Print the similar cases
    print("Top 5 similar cases:")
    for case_name, similarity in similar_cases:
        print(f"Case: {case_name}, Similarity: {similarity:.4f}")
    
    # Construct the graph based on embeddings similarity
    case_graph = construct_case_graph(case_embeddings, threshold=0.75)
    
    # Visualize the graph
    visualize_case_graph(case_graph)
