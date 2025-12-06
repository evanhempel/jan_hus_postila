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
    header_block_lines = 0
    non_header_lines_in_block = 0
    
    for line in lines:
        if is_all_caps_header(line):
            in_header_block = True
            header_block_lines += 1
            current_section.append(line)
        else:
            if in_header_block:
                # We're in a header block, check if this is a short non-header line
                if non_header_lines_in_block < 10:
                    # Still consider this part of the header block
                    non_header_lines_in_block += 1
                    current_section.append(line)
                else:
                    # Too many non-header lines, end the header block
                    in_header_block = False
                    sections.append(current_section)
                    current_section = [line]
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
