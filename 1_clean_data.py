# Clean data 1 are 
#     cleaning space in beginning and in the end of sentences
#     removing tag
#     removing hastag
#     removing emoji
#     removing number

import csv
import re
import os

def clean_comment(comment):
    comment = comment.replace('\n', ' ').replace('\r', ' ')

    # Ganti @mention → xmentionx
    comment = re.sub(r'@[\w._]+', ' xmentionx ', comment)
    
    # Ganti #hashtag → xhashtagx
    comment = re.sub(r'#[\w._]+', ' xhashtagx ', comment)
    
    # Ganti simbol non-standar/emoji kecuali tanda petik satu → xemoticonx
    comment = re.sub(r"[^\w\s,.!?'\[\]-]", ' xemoticonx ', comment)

    # Hilangkan spasi berlebih
    comment = re.sub(r'\s+', ' ', comment)

    return comment.strip()


# ======= SETTING =========
input_files = [
    'raw_data/emil1.csv',
    'raw_data/emil2.csv',
    'raw_data/khofifah.csv',
    'raw_data/lukman.csv',
    'raw_data/luluk.csv',
    'raw_data/pdip.csv',
]
output_files = [
    '1_clean_data/emil1.csv',
    '1_clean_data/emil2.csv',
    '1_clean_data/khofifah.csv',
    '1_clean_data/lukman.csv',
    '1_clean_data/luluk.csv',
    '1_clean_data/pdip.csv',
]  # Sama jumlahnya dengan input_files

combine_output = True  # True untuk gabungkan semua output
combined_output_file = '1_clean_data/comment_all.csv'
# =========================

def process_file(input_file):
    cleaned_comments = []
    with open(input_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cleaned = clean_comment(row['comment'])
            if cleaned:
                cleaned_comments.append(cleaned)
    return cleaned_comments

if combine_output:
    with open(combined_output_file, 'w', encoding='utf-8') as outfile:
        for f in input_files:
            comments = process_file(f)
            for c in comments:
                outfile.write(c + '\n')
    print(f"Gabungan komentar disimpan ke: {combined_output_file}")
else:
    if len(output_files) != len(input_files):
        raise ValueError("Jumlah output_files harus sama dengan jumlah input_files.")
    for i in range(len(input_files)):
        comments = process_file(input_files[i])
        with open(output_files[i], 'w', encoding='utf-8') as out:
            for c in comments:
                out.write(c + '\n')
        print(f"Komentar dari {input_files[i]} disimpan ke {output_files[i]}")
