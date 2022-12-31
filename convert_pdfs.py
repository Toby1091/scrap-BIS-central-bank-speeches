import os
import subprocess
import glob

from config import CACHE_DIR, TXT_DIR

errors = []
for filepath in glob.glob(os.path.join(CACHE_DIR, 'review/*.pdf')):
    text_filepath = os.path.join(TXT_DIR, os.path.basename(filepath).replace('.pdf', '.txt'))

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
