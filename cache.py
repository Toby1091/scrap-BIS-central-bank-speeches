import requests
import os

import config

def get_cache_path(path):
    return os.path.join(config.CACHE_DIR, path.lstrip('/'))


def fetch_page_or_pdf(path, force_refetch=False):
    print(f'Fetch page {path} (force refetch={force_refetch})')
    cache_path = get_cache_path(path)

    if not force_refetch and os.path.exists(cache_path):
        return

    response = requests.get('https://www.bis.org/' + path)

    if(response.status_code != 200):
        raise Exception('HTTP request failed with status code', response.status_code)

    os.makedirs(os.path.dirname(cache_path), exist_ok=True)

    is_pdf = response.headers['content-type'].lower().startswith('application/pdf')
    mode = 'wb' if is_pdf else 'w'
    content = response.content if is_pdf else response.text

    file_handle = open(cache_path, mode)
    file_handle.write(content)
    file_handle.close()


def read_file_from_cache(path):
    cache_path = get_cache_path(path)
    return open(cache_path).read()

