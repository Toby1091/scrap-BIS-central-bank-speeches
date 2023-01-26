def read_keywords_file():
    with open('speech_analysis/list_of_keywords.txt') as file_handle:
        content = file_handle.read()

    return [s for s in content.split('\n') if s]
