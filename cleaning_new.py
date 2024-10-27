import os
import xml.etree.ElementTree as ET
import re

def clean_xml_file(file_path):
    # Read the XML file
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()

    # Clean the content (for example, fix malformed tags)
    content = re.sub(r'<catchphrase\s+"id=[^>]*>', lambda m: m.group(0).replace('"', '='), content)
    
    # Write the cleaned content back to a new file
    cleaned_file_path = file_path.replace('cleaned', 'cleaned_new')  # Save to a new directory
    with open(cleaned_file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def clean_xml_directory(input_directory):
    for filename in os.listdir(input_directory):
        if filename.endswith('.xml'):
            file_path = os.path.join(input_directory, filename)
            clean_xml_file(file_path)

# Usage
cleaned_xml_directory = r"D:\activities\legal_IR\data\cleaned"
clean_xml_directory(cleaned_xml_directory)
print("Cleaning complete.")
