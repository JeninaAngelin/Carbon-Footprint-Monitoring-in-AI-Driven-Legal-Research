import os
import xml.etree.ElementTree as ET

def clean_xml_content(content):
    """Clean XML content by removing leading/trailing whitespace and ensuring proper format."""
    # Remove BOM if present and strip leading/trailing whitespace
    if content.startswith('\ufeff'):
        content = content.encode('utf-8')[3:].decode('utf-8')  # Remove BOM

    content = content.strip()  # Remove leading/trailing whitespace
    # Replace any illegal characters (e.g., control characters)
    return ''.join(c for c in content if c.isprintable() or c in ['\n', '\t', '\r'])

def clean_xml_file(xml_file, output_directory):
    """Clean the XML file by ensuring valid format and handling parsing errors."""
    try:
        with open(xml_file, 'r', encoding='utf-8') as file:
            content = file.read()

            # Clean the XML content
            cleaned_content = clean_xml_content(content)

            # Attempt to parse the cleaned content
            root = ET.fromstring(cleaned_content)

            # Re-create the cleaned XML structure
            cleaned_tree = ET.ElementTree(root)
            cleaned_file_path = os.path.join(output_directory, os.path.basename(xml_file))
            cleaned_tree.write(cleaned_file_path, encoding='utf-8', xml_declaration=True)

            return True  # Indicate successful cleaning

    except ET.ParseError as e:
        print(f"ParseError for {xml_file}: {e}")
        return False  # Indicate failure to clean

    except Exception as e:
        print(f"Error processing {xml_file}: {e}")
        return False  # Indicate failure to clean

def check_parsable_xml(directory):
    """Check if XML files in the directory are parsable."""
    parsable_count = 0
    non_parsable_count = 0

    for filename in os.listdir(directory):
        if filename.endswith('.xml'):
            xml_path = os.path.join(directory, filename)
            try:
                ET.parse(xml_path)  # Try parsing the XML
                parsable_count += 1
            except ET.ParseError:
                non_parsable_count += 1

    return parsable_count, non_parsable_count

def clean_xml_directory(input_directory, output_directory):
    """Clean all XML files in the specified directory."""
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    total_files_cleaned = 0
    total_files_failed = 0

    for filename in os.listdir(input_directory):
        if filename.endswith('.xml'):
            xml_path = os.path.join(input_directory, filename)
            success = clean_xml_file(xml_path, output_directory)

            if success:
                total_files_cleaned += 1
            else:
                total_files_failed += 1

    print(f"Total files cleaned: {total_files_cleaned}")
    print(f"Total files failed to clean: {total_files_failed}")

    # Check the cleaned files for parsing
    parsable_count, non_parsable_count = check_parsable_xml(output_directory)
    print(f"Parsable cleaned files: {parsable_count}")
    print(f"Non-parsable cleaned files: {non_parsable_count}")

    return non_parsable_count  # Return the count of non-parsable files

# Main execution
if __name__ == "__main__":
    input_directory = r"D:\activities\legal_IR\data\cleaned"
    output_directory = r"D:\activities\legal_IR\data\cleaned_new_new"
    non_parsable_files_count = clean_xml_directory(input_directory, output_directory)
    
    # You can use the count of non-parsable files for further processing if needed
    print(f"Count of non-parsable files: {non_parsable_files_count}")
