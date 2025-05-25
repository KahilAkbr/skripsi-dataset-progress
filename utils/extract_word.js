const fs = require('fs');

function extractExactWordMatches(filePath, keyword, outputPath) {
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      console.error('Gagal membaca file:', err);
      return;
    }

    const lines = data.split('\n');
    const keywordRegex = new RegExp(`\\b${keyword}\\b`, 'i');
    const matchingLinesWithNumbers = [];

    lines.forEach((line, index) => {
      if (keywordRegex.test(line)) {
        matchingLinesWithNumbers.push({
          lineNumber: index + 1,
          content: line.trim()
        });
      }
    });

    const outputText = matchingLinesWithNumbers
      .map(item => `Line ${item.lineNumber}: ${item.content}`)
      .join('\n');

    fs.writeFile(outputPath, outputText, 'utf8', err => {
      if (err) {
        console.error('Gagal menulis ke file:', err);
      } else {
        console.log(`Berhasil menyimpan ${matchingLinesWithNumbers.length} kalimat ke file: ${outputPath}`);
      }
    });
  });
}

// Ganti nama file input, kata kunci, dan file output sesuai kebutuhan
const filePath = '../3_clean_data/comment.for';
const keyword = 'sama';
const outputPath = 'result/extracted_word.txt';

extractExactWordMatches(filePath, keyword, outputPath);