const fs = require('fs');

function insertModifiedLines(originalFilePath, modifiedFilePath, outputFilePath) {
  // Baca file asli
  fs.readFile(originalFilePath, 'utf8', (err, originalData) => {
    if (err) {
      console.error('Gagal membaca file asli:', err);
      return;
    }

    // Baca file yang sudah dimodifikasi
    fs.readFile(modifiedFilePath, 'utf8', (err, modifiedData) => {
      if (err) {
        console.error('Gagal membaca file modifikasi:', err);
        return;
      }

      const originalLines = originalData.split('\n');
      const modifiedLines = modifiedData.split('\n');

      // Parse baris yang sudah dimodifikasi
      const modifications = {};
      modifiedLines.forEach(line => {
        const match = line.match(/^Line (\d+): (.*)$/);
        if (match) {
          const lineNumber = parseInt(match[1]);
          const newContent = match[2];
          modifications[lineNumber] = newContent;
        }
      });

      // Terapkan modifikasi ke file asli
      const updatedLines = originalLines.map((line, index) => {
        const lineNumber = index + 1;
        if (modifications[lineNumber]) {
          return modifications[lineNumber];
        }
        return line;
      });

      // Tulis hasil ke file baru
      const outputText = updatedLines.join('\n');
      fs.writeFile(outputFilePath, outputText, 'utf8', err => {
        if (err) {
          console.error('Gagal menulis ke file output:', err);
        } else {
          console.log(`Berhasil menyimpan file yang sudah diupdate ke: ${outputFilePath}`);
          console.log(`Total ${Object.keys(modifications).length} baris telah diperbarui`);
        }
      });
    });
  });
}

// Konfigurasi file
const originalFilePath = '../3_clean_data/comment.for';          // File asli
const modifiedFilePath = 'result/extracted_word_modified.txt';   // File hasil modifikasi Anda
const outputFilePath = 'result/comment_updated.for';            // File output hasil akhir

insertModifiedLines(originalFilePath, modifiedFilePath, outputFilePath);