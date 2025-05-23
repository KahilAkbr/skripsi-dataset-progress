const fs = require('fs');

function extractExactWordMatches(filePath, keyword, outputPath) {
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      console.error('Gagal membaca file:', err);
      return;
    }

    const lines = data.split('\n');
    const keywordRegex = new RegExp(`\\b${keyword}\\b`, 'i'); // mencocokkan kata utuh, tidak case-sensitive
    const matchingLines = lines.filter(line => keywordRegex.test(line));

    const outputText = matchingLines.map((line, i) => `${line.trim()}`).join('\n');

    fs.writeFile(outputPath, outputText, 'utf8', err => {
      if (err) {
        console.error('Gagal menulis ke file:', err);
      } else {
        console.log(`Berhasil menyimpan ${matchingLines.length} kalimat ke file: ${outputPath}`);
      }
    });
  });
}

// Ganti nama file input, kata kunci, dan file output sesuai kebutuhan
const filePath = '../3_clean_data/comment.for';
const keyword = 'pilih';
const outputPath = 'result/extracted_word.txt';

extractExactWordMatches(filePath, keyword, outputPath);
