#!/usr/bin/env python
# -*- coding: utf-8 -*-



from whoosh.qparser import QueryParser

from indexation.index_book import IndexBook
from indexation.schema import BookSchema
from src.update import UpdateIndex, UpdateJsonBook

if __name__ == '__main__':
    """ Main function to test code """
    #  index = IndexBook.get_index(bookSchema=BookSchema)
    #  qp = QueryParser('chapter_title', schema=BookSchema())
    #  query = qp.parse(u""+"La marchandise des rois")
    #  qp = QueryParser('title', schema=index.schema)
    #  query = qp.parse(u"Préface : de 0 à 1")
    #  with index.searcher() as searcher:
        #  result = searcher.search(query)
        #  print('###RESULTAT###')
        #  for i, hit in enumerate(result):
            #  print('#########'+str(i)+'########')
            #  print(hit)

    """ Update books/JsonFRench directory """
    #  UpdateJsonBook.update_jsonBook()

    """ Update Index """
    UpdateIndex.clean_index(BookSchema)
    
