# Clean data 2 are 
#     removing duplicate sentences (case sensitive)
#     deleting unmeaningful data like only mention, tags, or emoticon

import os
import re

def normalized_text(line):
    # Hapus placeholder xmentionx, xtagarx, xemoticonx, xnumberx
    return re.sub(r'x(mention|tagar|emoticon|number)x', '', line).strip()

def is_meaningful(line):
    line = re.sub(r'\s+', ' ', line).strip()
    if not line:
        return False
    # Hapus semua placeholder x...x
    cleaned = re.sub(r'x(mention|tagar|emoticon|number)x', '', line)
    # Jika tidak ada huruf alfabet setelah dibersihkan → tidak meaningful
    return bool(re.search(r'[a-zA-Z]', cleaned))


def remove_duplicates_with_logging(input_path, source_label):
    seen = set()
    unique_lines = []
    removed_lines = []

    with open(input_path, 'r', encoding='utf-8') as infile:
        for i, line in enumerate(infile, start=1):
            line = line.rstrip('\n')
            if not is_meaningful(line):
                removed_lines.append((source_label, i, line))
                continue

            normalized = normalized_text(line)

            if normalized not in seen:
                seen.add(normalized)
                unique_lines.append(line)
            else:
                removed_lines.append((source_label, i, line))

    return unique_lines, removed_lines

# ======= SETTING =========
input_files = [
    '1_clean_data/emil1.csv',
    '1_clean_data/emil2.csv',
    '1_clean_data/khofifah.csv',
    '1_clean_data/lukman.csv',
    '1_clean_data/luluk.csv',
    '1_clean_data/pdip.csv',
]

output_files = [
    '2_clean_data/emil1.csv',
    '2_clean_data/emil2.csv',
    '2_clean_data/khofifah.csv',
    '2_clean_data/lukman.csv',
    '2_clean_data/luluk.csv',
    '2_clean_data/pdip.csv',
]

combine_output = True
combined_output_file = '2_clean_data/comment_all.csv'
log_file = '2_clean_data/duplicates_log.txt'
# ==========================

if len(input_files) != len(output_files):
    raise ValueError("Jumlah input_files dan output_files harus sama.")

all_unique_lines = []
all_removed_log = []

# Proses masing-masing file
for idx in range(len(input_files)):
    input_path = input_files[idx]
    output_path = output_files[idx]
    source_label = os.path.basename(input_path)

    unique_lines, removed_lines = remove_duplicates_with_logging(input_path, source_label)

    # Tulis hasil bersih
    with open(output_path, 'w', encoding='utf-8') as out:
        for line in unique_lines:
            out.write(line + '\n')

    print(f"✔ {input_path} → {output_path} ({len(unique_lines)} unique lines, {len(removed_lines)} removed)")

    # Simpan untuk penggabungan & log
    if combine_output:
        all_unique_lines.extend(unique_lines)
    all_removed_log.extend(removed_lines)

# Gabungkan semua jika perlu
if combine_output:
    seen_all = set()
    combined_result = []

    for line in all_unique_lines:
        if line not in seen_all:
            seen_all.add(line)
            combined_result.append(line)

    with open(combined_output_file, 'w', encoding='utf-8') as out:
        for line in combined_result:
            out.write(line + '\n')

    print(f"\n🗂 Semua komentar unik digabung ke: {combined_output_file} ({len(combined_result)} total unik)")

# Tulis file log untuk semua komentar yang dibuang (duplikat & meaningless)
if all_removed_log:
    with open(log_file, 'w', encoding='utf-8') as log:
        for source_file, line_number, line_content in all_removed_log:
            log.write(f"{source_file}, Line {line_number}: {line_content}\n")
    print(f"\n📄 Log komentar dibuang disimpan di: {log_file} ({len(all_removed_log)} total baris)")
else:
    print("\n✅ Tidak ada komentar yang dibuang.")
