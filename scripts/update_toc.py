import re
import os

def generate_anchor(text):
    # Strip markdown links [text](url) -> text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Lowercase
    text = text.lower()
    # Remove non-alphanumeric (except space and hyphen)
    # We need to handle unicode characters if we want to be perfect, 
    # but for this specific case, the user's anchor "textby" implies stripping '（' and '）'.
    # So we strip everything that is not a-z, 0-9, space, hyphen.
    text = re.sub(r'[^a-z0-9\s_-]', '', text)
    # Replace spaces with -
    text = text.strip().replace(' ', '-')
    # Collapse dashes
    text = re.sub(r'-+', '-', text)
    return text

def main():
    readme_path = os.path.join(os.path.dirname(__file__), '..', 'README.md')
    with open(readme_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 1. Extract Cases
    cases = []
    case_pattern = re.compile(r'^###\s+(Case\s+\d+:\s+.*)$')
    
    for line in lines:
        m = case_pattern.match(line)
        if m:
            cases.append(m.group(1))

    # 2. Generate TOC lines
    new_toc_lines = ["- [✨ Cases list](#️-cases)\n"]
    for header_text in cases:
        # Display text: strip links
        display_text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', header_text)
        # Anchor
        anchor = generate_anchor(header_text)
        new_toc_lines.append(f"  - [{display_text}](#{anchor})\n")

    # 3. Replace in file
    # Find start of TOC
    start_idx = -1
    end_idx = -1
    
    for i, line in enumerate(lines):
        if line.strip().startswith("- [✨ Cases list]"):
            start_idx = i
            break
            
    if start_idx != -1:
        # Find end of TOC (first empty line or next header)
        for i in range(start_idx + 1, len(lines)):
            if not lines[i].strip() or lines[i].startswith("#"):
                end_idx = i
                break
        if end_idx == -1:
            end_idx = len(lines)
            
        # Replace
        print(f"Replacing lines {start_idx+1} to {end_idx}")
        new_content = lines[:start_idx] + new_toc_lines + lines[end_idx:]
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.writelines(new_content)
        print("README.md updated successfully.")
    else:
        print("Could not find TOC start location.")

if __name__ == '__main__':
    main()
