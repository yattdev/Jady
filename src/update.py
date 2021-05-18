#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import string
from os.path import exists, join
from pathlib import Path


from indexation.index_book import IndexBook
from indexation.schema import BookSchema
from processing_book.processEpub import ProcessBook
from settings.config_default import EPUB_BOOK_FR_DIR, JSON_BOOK_FR_DIR


class UpdateJsonBook(object):

    """ Class to update books/JsonFrench if
    books/EpubFrench is upadate with new books """

    def __init__(self):
        """ Create Instance UpdateJsonBook """

    @classmethod
    def split_book(cls, book: string):
        """
        SPLIT BOOK TO CHAPTERS THEN SAVE IT TO JSON FORMAT

        :book: name of epub book
        :returns:

        """
        try:
            processBook = ProcessBook(book) # Process Book: Work on Book
            #  split epub-book to chapters and save it to book-name.json
            processBook.book_to_jsonFile() # value == True if all rigth
        except Exception as e:
            print("Can't split book to json")
            raise e
        return True

    @classmethod
    def update_jsonBook(cls):
        """ Update books/JsonFrench dir from books/EpubFrench
            by use split_book function """
        epub_books = Path(EPUB_BOOK_FR_DIR).glob('*.epub')
        for book in epub_books:
            # if: To skip the book already exist in books/JsonFrench dir
            if not exists(join(JSON_BOOK_FR_DIR,
                               str(book).split('/')[-1])+'.json'):
                UpdateJsonBook.split_book(str(book))
                #  if make: print('DONE !!!')

        print('SUCCESSFULL ! All Epub-books splited into CHAPTERS in Json Format !!!')
        print()
        print('JsonFrench dir Updated !')


class UpdateIndex(object):

    """ UpdateIndex: For update index if JsonFrench dir is updated """

    def __init__(self):
        """ Create Instance from UpdateIndex """

    @classmethod
    def add_to_index(cls, bookSchema: BookSchema, book_name:string, index=None):
        """ Add JSON FORMAT FILE in index, by use 'IndexBook' Class """
        # TODO: Add possibility to create index or open exist index from
        # index_dir:Insert in function arg: add_to_index(..., index_dir:string)
        if index:
            storage = index
        else:
            storage = IndexBook.get_index(bookSchema)

        writer = storage.writer()
        with open(book_name) as json_file:
            json_data = json.load(json_file)
            IndexBook.add_to_index(json_data=json_data, writer=writer,
                                   path=str(jsonBookName))

        writer.commit() # Save index and close writer
        print('SUCCESSFULL ! All Json-books indexed !!!')
        print()
        print('Index_dir Updated !')

    @classmethod
    def clean_index(cls, bookSchema: BookSchema):
        """ clean_index is call to re-write index """
        index = IndexBook.get_index(bookSchema, clean=True)
        json_books = Path(JSON_BOOK_FR_DIR).glob('*.json')
        writer = index.writer()
        for book in json_books:
            #  Write jsonBook to index
            with open(book) as json_file:
                json_data = json.load(json_file)
                IndexBook.add_to_index(json_data=json_data, writer=writer,
                                       path=str(book))
            print('DONE !!! '+str(book))

        writer.commit() # Save index and close writer
        print('INDEX CLEANED SUCCESSFULL !')
        print()
        print('All Json-books are indexed !!!')
