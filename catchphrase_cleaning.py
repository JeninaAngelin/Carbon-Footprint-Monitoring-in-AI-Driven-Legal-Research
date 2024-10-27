import os  # Import the os module to interact with the operating system
import xml.etree.ElementTree as ET

def extract_catchphrases(directory):
    catchphrases = {}
    
    for filename in os.listdir(directory):
        if filename.endswith('.xml'):
            file_path = os.path.join(directory, filename)
            tree = ET.parse(file_path)
            root = tree.getroot()

            for catchphrase in root.findall('.//catchphrase'):
                text = catchphrase.text
                if text:
                    catchphrases[text] = filename  # Store catchphrase and associated file name

    return catchphrases

# Usage
cleaned_xml_directory_new = r"D:\activities\legal_IR\data\cleaned_new"
catchphrases_dict = extract_catchphrases(cleaned_xml_directory_new)
print("Catchphrases extracted.")