def capitalize_first_letter_per_line(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    capitalized_lines = []
    for line in lines:
        if line.strip() == "":
            capitalized_lines.append(line)
        elif line.lstrip().startswith('x'):
            capitalized_lines.append(line)
        else:
            stripped = line.lstrip()
            leading_spaces = len(line) - len(stripped)
            modified = stripped[:1].upper() + stripped[1:]
            capitalized_lines.append(' ' * leading_spaces + modified)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(capitalized_lines)

# Contoh penggunaan
capitalize_first_letter_per_line('../3_clean_data/comment.for', 'output.txt')
