import re
import os
import subprocess

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

def extract_all_caps_lines(chunk_lines):
    """Extract ALL CAPS lines from a chunk"""
    all_caps_lines = []
    for line in chunk_lines:
        if is_all_caps_header(line):
            all_caps_lines.append(line.strip())
    return all_caps_lines

def generate_descriptive_title(all_caps_lines):
    """Generate a descriptive title from ALL CAPS lines using LLM"""
    if not all_caps_lines:
        return "unknown"
    
    # Combine all caps lines with newlines
    input_text = "\n".join(all_caps_lines)
    
    try:
        # Run the llm command
        result = subprocess.run(
            ['llm', '-m', 'openrouter/amazon/nova-2-lite-v1:free', 
             '-s', f'translate the title (TEXT IN ALL CAPS) to english and return only the translated title:\n{input_text}'],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Get the output and clean it up
        title = result.stdout.strip()
        
        # Replace consecutive spaces with underscores
        title = re.sub(r'\s+', '_', title)
        
        # Remove non-alphanumeric characters (except underscores)
        title = re.sub(r'[^a-zA-Z0-9_]', '', title)
        
        return title.lower()
    
    except subprocess.CalledProcessError as e:
        print(f"Error calling llm: {e}")
        return "unknown"
    except Exception as e:
        print(f"Error generating title: {e}")
        return "unknown"

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
            # If we encounter a new header and we're not in a header block,
            # finish the current section first
            if not in_header_block and current_section:
                sections.append(current_section)
                current_section = []
            
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
            else:
                current_section.append(line)
    
    # Add the last section
    if current_section:
        sections.append(current_section)
    
    # Write sections to files with descriptive names
    for i, section in enumerate(sections):
        # Extract ALL CAPS lines for title generation
        all_caps_lines = extract_all_caps_lines(section)
        descriptive_title = generate_descriptive_title(all_caps_lines)
        
        # Create filename with number and descriptive title
        filename = f"{i:02d}_{descriptive_title}.txt"
        output_file = os.path.join(output_dir, filename)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(section)
        
        print(f"Created {output_file}")
    
    print(f"Created {len(sections)} sections in {output_dir}/ directory")

if __name__ == "__main__":
    split_text_file("hus_postila.txt")
