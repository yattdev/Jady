#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" DocString: Load configuration from .yaml file."""


from pathlib import Path
from os import path
import confuse


# get path of the projet !
BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
#  BASE_DIR = '/home/alassane/Code/JimBot/chatbotapp'

# Load config.yaml
config = confuse.Configuration('chatbotapp', __name__)
config.set_file(path.join(BASE_DIR, 'settings/config.yaml'))

# Create Variable for book json path
JSON_BOOK_FR_DIR = path.join(BASE_DIR, config['books']['json']['french'].get())
JSON_BOOK_EN_DIR = path.join(BASE_DIR, config['books']['json']['english'].get())

INDEXED_CHAP_PATHS = path.join(BASE_DIR, config['books']['paths']['french'].get())

# Create Variable for book epub path
EPUB_BOOK_FR_DIR = path.join(BASE_DIR, config['books']['epub']['french'].get())
EPUB_BOOK_EN_DIR = path.join(BASE_DIR, config['books']['epub']['english'].get())
THEMES_DIR = path.join(BASE_DIR, config['books']['themes']['french'].get())

NLU_DATA_PATH = path.join(BASE_DIR, config['nlu_data_path'].get())

VERIFY = config['VERIFY'].as_str_expanded()
SECRET = config['SECRET'].as_str_expanded()
PAGE_ACCESS_TOKEN = config['PAGE_ACCESS_TOKEN'].as_str_expanded()

# Dir path for images of books coverage
COVER_IMG_PATH = path.join(BASE_DIR, config['books']['cover_img_path'].get())
