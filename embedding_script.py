import os
import xml.etree.ElementTree as ET
from transformers import AutoTokenizer, AutoModel
import torch

# Define the folder containing XML files
xml_folder = "./data/cleaned_new_new"  # Assuming your XML files are in the folder 'data'

# Load a pre-trained model and tokenizer
model_name = "sentence-transformers/all-mpnet-base-v2"  # Or another suitable model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Function to parse XML and extract text from each file
def extract_text_from_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Extract all text content from the XML file
    text = []
    for elem in root.iter():
        if elem.text:
            text.append(elem.text.strip())
    
    return " ".join(text)  # Combine all the text into a single string

# Function to get embeddings for a given text
def get_embeddings(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Mean pooling the last hidden state to get sentence-level embeddings
    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings

# Function to process XML files and generate embeddings
def process_xml_files(xml_folder):
    all_embeddings = {}
    
    for filename in os.listdir(xml_folder):
        if filename.endswith(".xml"):  # Process only XML files
            xml_path = os.path.join(xml_folder, filename)
            print(f"Processing: {xml_path}")
            
            # Extract text from the XML file
            text = extract_text_from_xml(xml_path)
            
            if text:
                # Get embeddings for the extracted text
                embeddings = get_embeddings(text)
                
                # Store the embeddings in a dictionary (filename as the key)
                all_embeddings[filename] = embeddings
            else:
                print(f"No text found in {filename}")
    
    return all_embeddings

# Function to save embeddings to a file
def save_embeddings(embeddings, output_file):
    torch.save(embeddings, output_file)
    print(f"Embeddings saved to {output_file}")

# Main function to run the process
def main():
    # Process the XML files and get embeddings
    embeddings = process_xml_files(xml_folder)
    
    # Define output file to store embeddings
    output_file = "./xml_embeddings.pt"  # You can choose any name and format
    
    # Save the embeddings to a file
    save_embeddings(embeddings, output_file)

if __name__ == "__main__":
    main()