#!/usr/bin/env python
# -*- coding: utf-8 -*-

from whoosh.fields import (SchemaClass, TEXT, KEYWORD, ID, STORED,
                           DATETIME, NUMERIC)
from whoosh.analysis import LanguageAnalyzer


class BookSchema(SchemaClass):
    """
        BookSchema is a custom schema From SchemaClass for index
        and search Ebook
    """
    path = ID(unique=True, stored=True)
    intent = TEXT(analyzer=LanguageAnalyzer(lang='fr'), stored=True)
    book_id = TEXT(analyzer=LanguageAnalyzer(lang='fr'), stored=True)
    book_title = TEXT(analyzer=LanguageAnalyzer(lang='fr'), stored=True)
    creator = TEXT(analyzer=LanguageAnalyzer(lang='fr'), stored=True)
    contributor = TEXT(analyzer=LanguageAnalyzer(lang='fr'), stored=True)
    published_date = DATETIME(stored=True, sortable=True)
    chapter_title = TEXT(analyzer=LanguageAnalyzer(lang='fr'), stored=True,
                         field_boost=2.0)
    content = TEXT(analyzer=LanguageAnalyzer(lang='fr'), stored=True,
                   spelling=True)
    # Le context est une courte resumer de quoi ont par dans le chapitre
    context = TEXT(analyzer=LanguageAnalyzer(lang='fr'), phrase=True,
                   stored=True, field_boost=1.0, spelling=True)
    #  Ce sont des tags comme les categories: Vente, Marketing, Dev-personnel,
    #  Entrepreneuriat, Comedie etc.
    tags = KEYWORD(stored=True, lowercase=True, commas=True,
                   analyzer=LanguageAnalyzer(lang='fr'), sortable=True)
