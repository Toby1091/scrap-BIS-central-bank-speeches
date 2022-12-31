# Page size when fetching speech lists from bis.org. Allowed values: 5, 10, 15, 20, 25
PAGE_SIZE = 25

# Directory in which to store / cache downloaded files (will be written in)
CACHE_DIR = 'output/cache'

# Directory in which to store text files containing the content extracted from PDFs
TXT_DIR = 'output/textified_pdfs'

# JSON file with metadata about speeches extracted from HTML (will be created / overwritten)
RESULT_FILE = 'output/result.json'

# Text file that will be read with additional bank names and mapped bank names (will only be read)
BANK_NAMES_FILE = 'input/list_of_missing_bank_names.txt'

# Text file that will be read with keywords to search (will only be read)
KEYWORDS_FILE = 'input/list_of_keywords.txt'