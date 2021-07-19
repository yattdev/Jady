#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from os import chdir, mkdir, path
from pathlib import Path

from dateutil import parser
from whoosh.filedb.filestore import FileStorage
from whoosh.index import create_in, open_dir

from indexation.schema import BookSchema, SchemaClass
from settings.config_default import (BASE_DIR, INDEXED_CHAP_PATHS,
                                     JSON_BOOK_FR_DIR)


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

        if clean:
            return storage.create_index(bookSchema, 'INDEX_DIR')

        return storage.open_index('INDEX_DIR', bookSchema)

    @classmethod
    def add_to_index(cls, json_data, writer, path: str):
        """ Docstring for add_to_index.
            TODO: add to index each chapter from json_data
            :json_data: Dict or List to content list of book chapters's
            :returns: None
        """
        data = json_data  # Json data to write un index
        #  if json_data is DICT and has variable 'Content', get Content value
        #  else it's a list==part in book that containt chapters
        if isinstance(json_data, dict) and json_data['Content']:
            data = json_data['Content']

        for dic in data:
            if dic['is_part']:  # dic['is_part'] == True if dic isn't chapter
                IndexBook.add_to_index(json_data=dic['chapters'],
                                       writer=writer, path=path)
            else:  # If dic is chapter then add chapter to index
                writer.add_document(
                    path=u''+path+'#'+dic['chapter_title'],
                    chapter_title=u''+dic['chapter_title'],
                    content=u''+dic['content'],
                    book_id=u''+dic['book_id'],
                    cover_img_path=u''+dic['cover_img_path'],
                    book_title=u''+dic['book_title'],
                    creator=u''+dic['creator'],
                    contributor=u''+dic['contributor'],
                    context=u''+dic['context'],
                    tags=u''+dic['subject'],
                    published_date=datetime.strptime(
                        dic['published_date'][:19],
                        "%Y-%m-%dT%H:%M:%S")
                )

    @classmethod
    def add_to_index_by_chapter(cls, chap_json_data, writer, file_path: str):
        """ Docstring for add_to_index_by_chapter.
            TODO: add to index each chapter from chap_json_data
            params:
                chap_json_data: Dict or List to content list of book chapters's
            :returns: None
        """
        chapter = chap_json_data  # Json data to write un index
        try:
            date = parser.parse(chapter['published_date'][:19])
        except parser.ParserError as e:
            date = datetime.now()

        try:
            writer.add_document(
                path=u''+file_path+'#'+chapter['chapter_title'],
                intent=IndexBook.dir_name(file_path),
                chapter_title=u''+chapter['chapter_title'],
                content=u''+chapter['content'],
                book_id=u''+chapter['book_id'],
                cover_img_path=u''+chapter['cover_img_path'],
                book_title=u''+chapter['book_title'],
                creator=u''+chapter['creator'],
                contributor=u''+chapter['contributor'],
                context=u''+chapter['context'],
                tags=u''+chapter['subject'],
                published_date=date
                                                 #  "%Y-%m-%dT%H:%M:%S")
            )
        except KeyError as e:
            print(file_path)
            raise e

    @classmethod
    def dir_name(cls, file_absolue_path):
        dir_absolue_path = path.dirname(file_absolue_path)
        return dir_absolue_path.split("/")[-1]

#  if __name__ == '__main__':
    #  index = IndexBook.get_index(BookSchema, clean=True)
    #  book_jsonFromat =  "/home/alassane/Code/JimBot/chatbotapp/books/jsonFrench/POUVOIR ILLIMITE by Anthony Robbins (z-lib.org).pdf.epub.json"
    #  writer = index.writer()
    #  with open(book_jsonFromat) as json_file:
        #  json_data = json.load(json_file)
        #  IndexBook.add_to_index(json_data=json_data, writer=writer,
                               #  path=str(book_jsonFromat))
    #  writer.commit() # Save index and close writer
    #  print('DONE !!! '+str(book_jsonFromat))
