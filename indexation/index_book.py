#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path, chdir, mkdir
from datetime import datetime
import json
import string
from pathlib import Path
from indexation.schema import BookSchema, SchemaClass
from whoosh.index import create_in, open_dir
from whoosh.filedb.filestore import FileStorage
from settings.config_default import (BASE_DIR, JSON_BOOK_FR_DIR,
                                     INDEXED_CHAP_PATHS)


class IndexBook:
    """ Class for indexing a book by whoosh """
    #  Thought to allow me work with class method independatly
    #  storage = None
    #  writer = None
    
    def __init__(self):
        """Docstring for __init__ in Class IndexBook

        :TODO: Create Instance and fill jsonBook and jsonData
        :returns: TODO

        """
        #  self.jsonBook = jsonBook
        #  self.jsonData = None

    @classmethod
    def get_index(cls, bookSchema: BookSchema, clean=False):
        """ 
        :TODO: Funtion to Create/Return Index 
        """
        chdir(BASE_DIR)
        # Create Index directory if not exist
        if not path.exists(path.join(BASE_DIR, 'INDEX_DIR')): 
            mkdir('INDEX_DIR')

        storage = FileStorage('INDEX_DIR')
        if not storage.index_exists('INDEX_DIR'):
            return storage.create_index(bookSchema, 'INDEX_DIR')
        else:
            if clean:
                return storage.create_index(bookSchema, 'INDEX_DIR')
            else:
                return storage.open_index('INDEX_DIR', bookSchema)

    @classmethod
    def add_to_index(cls, json_data, writer, path:string):
        """ Docstring for add_to_index.
            TODO: add to index each chapter from json_data
            :json_data: TODO
            :returns: TODO
        """
        data = json_data # Json data to write un index
        #  if json_data is DICT and has variable 'Content', get Content value
        #  else it's a list==part in book that containt chapters
        if isinstance(json_data, dict) and json_data['Content']:
            data = json_data['Content']

        for dic in data:
            if dic['is_part']: # dic['is_part'] == True if dic isn't chapter
                IndexBook.add_to_index(json_data=dic['chapters'],
                                       writer=writer, path=path)
            else: # If dic is chapter then add chapter to index
                writer.add_document(
                    path=u''+path+'#'+dic['chapter_title'],
                    chapter_title=u''+dic['chapter_title'],
                    content=u''+dic['content'],
                    book_id=u''+dic['book_id'],
                    book_title=u''+dic['book_title'],
                    creator=u''+dic['creator'],
                    contributor=u''+dic['contributor'],
                    context=u''+dic['context'],
                    tags=u''+dic['subject'],
                    published_date=datetime.strptime(dic['published_date'][:19],
                                                         "%Y-%m-%dT%H:%M:%S")
                )


if __name__== '__main__':
    index = IndexBook.get_index(BookSchema, clean=True)
    book_jsonFromat =  "/home/alassane/Code/JimBot/chatbotapp/books/jsonFrench/POUVOIR ILLIMITE by Anthony Robbins (z-lib.org).pdf.epub.json"
    writer = index.writer()
    with open(book_jsonFromat) as json_file:
        json_data = json.load(json_file)
        IndexBook.add_to_index(json_data=json_data, writer=writer,
                               path=str(book_jsonFromat))
    writer.commit() # Save index and close writer
    print('DONE !!! '+str(book_jsonFromat))
