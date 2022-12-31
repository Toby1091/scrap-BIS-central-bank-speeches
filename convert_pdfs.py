import os
import subprocess
import glob

errors = []
for filepath in glob.glob('cache/review/*.pdf'):
    text_filepath = 'textified_pdfs/' + os.path.basename(filepath).replace('.pdf', '.txt')

    if os.path.exists(text_filepath):
        print('Skip', filepath)
        continue

    cmd = f'qpdf --decrypt {filepath} - | pdftotext - {text_filepath}'
    print('cmd:', cmd)
    try:
        proc = subprocess.run([cmd], check=True, shell=True)
    except Exception as e:
        errors.append((filepath, e))


print(errors)
