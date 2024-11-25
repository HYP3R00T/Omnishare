import os
import re

import frontmatter


def process_file(file_path):
    # Now it begins
    if not os.path.exists(file_path):
        return f"Error: The file '{file_path}' does not exist."

    if not os.path.isfile(file_path):
        return f"Error: The path '{file_path}' is not a file."

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            post = frontmatter.load(file)
            return post
    except Exception as e:
        return f"Error reading the file: {e}"


def markdown_to_plain(markdown_text):
    """
    Convert markdown text to plain text with emojis for headers and unicode bullets.
    Preserves links (without square brackets) and code blocks.

    Args:
        markdown_text (str): Input markdown text

    Returns:
        str: Converted plain text
    """
    # Store the converted lines
    converted_lines = []

    # Process the text line by line
    lines = markdown_text.split("\n")

    in_code_block = False
    code_block_lines = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Handle code blocks
        if line.startswith("```"):
            if not in_code_block:
                # Start of code block - skip the opening line
                in_code_block = True
                i += 1
                continue
            else:
                # End of code block - add collected lines
                in_code_block = False
                converted_lines.extend(code_block_lines)
                code_block_lines = []
                i += 1
                continue

        if in_code_block:
            code_block_lines.append(line)
            i += 1
            continue

        if not line:
            converted_lines.append("")
            i += 1
            continue

        # Handle headers
        if line.startswith("# "):
            converted_lines.append(f"📌 {line[2:].strip()}")
        elif line.startswith("## "):
            converted_lines.append(f"🔹 {line[3:].strip()}")
        # Handle bullet points
        elif line.startswith("* ") or line.startswith("- "):
            converted_lines.append(f"• {line[2:].strip()}")
        elif re.match(r"^\d+\. ", line):
            number_end = line.find(". ")
            converted_lines.append(f"• {line[number_end + 2:].strip()}")
        else:
            # Regular text - remove bold and italic markers
            clean_line = re.sub(r"\*\*|__|\*|_", "", line)
            # Remove inline code
            clean_line = re.sub(r"`([^`]+)`", r"\1", clean_line)
            # Convert links: [text](url) to text (url)
            clean_line = re.sub(r"\[([^\]]+)\]\(([^\)]+)\)", r"\1(\2)", clean_line)
            converted_lines.append(clean_line)

        i += 1

    # Join the lines and remove multiple consecutive empty lines
    result = "\n".join(converted_lines)
    result = re.sub(r"\n\s*\n", "\n\n", result)

    return result.strip()
