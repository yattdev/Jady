#!/usr/bin/env python
# -*- coding: utf-8 -*-



from whoosh.qparser import QueryParser

from indexation.index_book import IndexBook
from indexation.schema import BookSchema
from src.update import UpdateIndex, UpdateJsonBook
from pathlib import Path
from settings.config_default import (EPUB_BOOK_FR_DIR,
                                     JSON_BOOK_FR_DIR,
                                     THEMES_DIR,
                                     )
from os import path


def test():
    chapters = Path(JSON_BOOK_FR_DIR).rglob('*.json')
    for chap in chapters:
        print(chap)


if __name__ == '__main__':
    """ Main function to test code """
    #  qp = QueryParser('chapter_title', schema=BookSchema())
    #  query = qp.parse(u""+"La marchandise des rois")
    index = IndexBook.get_index(bookSchema=BookSchema)
    qp = QueryParser('intent', schema=index.schema)
    query = qp.parse(u"procrastination")
    with index.searcher() as searcher:
        result = searcher.search(query)
        print('###RESULTAT###')
        for i, hit in enumerate(result):
            print('#########'+str(i)+'########')
            print(hit)

    """ Update books/JsonFRench directory """
    #  UpdateJsonBook.update_json_book()

    """ Update Index """
    #  UpdateIndex.add_to_index_by_chapter(book_schema=BookSchema)
