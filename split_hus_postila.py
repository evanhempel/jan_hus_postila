import re
import os

def is_all_caps_header(line):
    """Check if a line is an ALL CAPS heading"""
    line = line.strip()
    # Skip empty lines, very short lines, and lines that are just numbers
    if not line or len(line) < 3 or line.isdigit():
        return False
    
    # Count uppercase letters and total letters
    uppercase_count = sum(1 for c in line if c.isupper())
    total_letters = sum(1 for c in line if c.isalpha())
    
    # Consider it a header if >70% of letters are uppercase
    return total_letters > 0 and uppercase_count / total_letters > 0.7

def split_text_file(input_file, output_dir="chunks"):
    """Split text file into chunks based on ALL CAPS headings"""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    sections = []
    current_section = []
    in_header_block = False
    consecutive_non_headers = 0
    
    for line in lines:
        if is_all_caps_header(line):
            # If we encounter a new header and we're already in a header block,
            # finish the current section first
            if in_header_block and current_section:
                sections.append(current_section)
                current_section = []
                consecutive_non_headers = 0
            
            in_header_block = True
            consecutive_non_headers = 0
            current_section.append(line)
        else:
            if in_header_block:
                consecutive_non_headers += 1
                current_section.append(line)
                
                # If we have too many non-header lines, end the header block
                if consecutive_non_headers > 10:
                    in_header_block = False
                    sections.append(current_section)
                    current_section = []
                    consecutive_non_headers = 0
            else:
                current_section.append(line)
    
    # Add the last section
    if current_section:
        sections.append(current_section)
    
    # Write sections to files
    for i, section in enumerate(sections):
        output_file = os.path.join(output_dir, f"{i:02d}.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(section)
    
    print(f"Created {len(sections)} sections in {output_dir}/ directory")

if __name__ == "__main__":
    split_text_file("hus_postila.txt")
