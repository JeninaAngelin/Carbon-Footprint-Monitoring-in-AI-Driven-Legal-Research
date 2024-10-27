import os
import re

def fix_xml_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Regex pattern to find malformed catchphrase tags
        pattern = r'<catchphrase\s+"id=(\w+)">'
        # Correct the malformed catchphrase attributes
        corrected_content = re.sub(pattern, r'<catchphrase id="\1">', content)

        return corrected_content
    except UnicodeDecodeError as e:
        print(f"Cannot decode file {file_path}: {e}")
        return None  # Indicate that the file couldn't be processed

def clean_xml_directory(input_directory, output_directory):
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    unparsed_count = 0  # Counter for files that can't be parsed
    cleaned_count = 0   # Counter for successfully cleaned files

    for filename in os.listdir(input_directory):
        if filename.endswith('.xml'):
            input_file_path = os.path.join(input_directory, filename)
            output_file_path = os.path.join(output_directory, filename)

            print(f"Processing file: {input_file_path}")
            corrected_content = fix_xml_file(input_file_path)

            if corrected_content is not None:
                # Write the corrected content to the new cleaned directory
                with open(output_file_path, 'w', encoding='utf-8') as file:
                    file.write(corrected_content)
                cleaned_count += 1  # Increment the counter for cleaned files
            else:
                unparsed_count += 1  # Increment the counter for unparsed files

    print(f"Total files that couldn't be parsed: {unparsed_count}")
    print(f"Total files successfully cleaned: {cleaned_count}")

# Specify the input and output directories
input_xml_directory = r"D:\activities\legal_IR\data\raw"
output_xml_directory = r"D:\activities\legal_IR\data\cleaned"

clean_xml_directory(input_xml_directory, output_xml_directory)