 #!/bin/bash
 cd cache/review
 FILES=*.pdf
 for f in $FILES
 do
  echo "Processing $f file..."
  qpdf $f --decrypt ../../decrypted_pdfs/$f
  pdftotext -enc UTF-8 ../../decrypted_pdfs/$f "../../textified_pdfs/$f"
 done
