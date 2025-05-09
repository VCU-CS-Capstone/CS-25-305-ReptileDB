#!/usr/bin/env python3
import argparse
import unicodedata

def remove_control_characters(s):
    # Remove Unicode control characters (category "Cc") except newline (\n) and tab (\t)
    return ''.join(ch for ch in s if not (unicodedata.category(ch) == 'Cc' and ch not in ('\n', '\t')))

def clean_text(content):
    # Normalize newlines to Unix-style (\n)
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    # Remove extraneous control characters but keep \n and \t
    content = remove_control_characters(content)
    
    # Remove leading and trailing whitespace from each line
    lines = content.split('\n')
    cleaned_lines = [line.strip() for line in lines]
    return '\n'.join(cleaned_lines)

def read_file_with_fallback(file_path):
    # Try different encodings until one succeeds
    encodings = ["utf-8", "utf-16", "latin-1"]
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                return f.read(), enc
        except UnicodeDecodeError:
            continue
    raise ValueError("Unable to decode file with available encodings.")

def main():
    parser = argparse.ArgumentParser(
        description='Clean a .txt database file for easier SQLite conversion.'
    )
    parser.add_argument('input_file', help='Path to the input .txt file')
    parser.add_argument('output_file', help='Path where the cleaned output will be saved')
    args = parser.parse_args()

    # Read file with fallback encoding detection
    content, encoding_used = read_file_with_fallback(args.input_file)
    print(f"File read successfully using encoding: {encoding_used}")

    cleaned_content = clean_text(content)
    
    # Write cleaned content in UTF-8
    with open(args.output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(cleaned_content)
    
    print(f"Cleaned file written to: {args.output_file}")

if __name__ == '__main__':
    main()
