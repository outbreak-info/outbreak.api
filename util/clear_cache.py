#!/usr/bin/env python

import sys
import requests
import logging
import os
logging.basicConfig(filename='/var/log/nginx/cache_clear.log', encoding='utf-8', level=logging.DEBUG)

sys.path.append('/home/ubuntu/outbreak.api')
import config

from shutil     import rmtree
from subprocess import run
from time       import sleep

CURRENT_INDEX_FILE = '/home/ubuntu/.current_index_name.txt'
CACHE_DIRECTORY    = '/var/lib/nginx/cache/'

def did_genomics_update(live_index):
    if os.path.exists(CURRENT_INDEX_FILE):
        with open(CURRENT_INDEX_FILE) as index_file:
            index_name = index_file.read().strip()

    else:
        logging.warning(f'creating file {live_index}')
        with open(CURRENT_INDEX_FILE, 'w') as index_file:
            index_file.write(live_index)
        return False

    return live_index == index_name

def clear_nginx_cache():
    DELAY = 120
    
    subdirs = os.listdir(CACHE_DIRECTORY)
    for subdir in subdirs:
        cache_directory = os.path.join(CACHE_DIRECTORY, subdir)
        rmtree(cache_directory)
        sleep(DELAY)

def main():
    es_host = config.ES_HOST
    live_index = requests.get(f'http://{es_host}/_cat/indices/genomics*?h=idx').text.strip()

    if did_genomics_update():
        logging.info('genomics updated, clearing cache')
        clear_nginx_cache()

        with open(CURRENT_INDEX_FILE, 'w') as index_file:
            logging.info(f'updating file {live_index}')
            index_file.write(live_index)

if __name__ == '__main__':
    try:
        main()

    except Exception as e:
        logging.error(str(e))
