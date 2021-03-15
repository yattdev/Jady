#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import string
from errno import ENOENT
from os import strerror
from typing import Dict, List

from textwrap3 import wrap
from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub
from ebooklib.utils import get_pages

from settings import config_default as cfg


class  ProcessBook():
    """ Class to splite Epubbook by chapter to jsonFormat """

    def __init__(self, bookname: string):
        """ Initialize create instance and variables """
        self.book_to_chaps = []
        self.blacklist = ['[document]', 'noscript', 'header', 'html', 'meta', 'head','input', 'script']
        self.book = None
        self.book_name = bookname.split('/')[-1]
        self.book_data = {}
        try:
            self.book = epub.read_epub(bookname)
        except FileNotFoundError as e:
            raise e(ENOENT, strerror(ENOENT), bookname)

        self.book_data = self.get_book_info() # Get book info
        # Get chapter and it's page number [(chapter, page), ...]
        # Delete duplicate chapter by set() function
        self.pages = ProcessBook.get_chapters_and_pages(self.book.toc, [], set())
        # sorted chapter par page number
        #  self.pages = sorted(self.pages, key=lambda tup: int(tup[0]))
        # Split book to chapters
        self.book_to_chaps = self.splitbook_to_chapters(self.book.toc,
                                                        self.book_to_chaps)

    def get_pages(self):
        """ Return book chapter and it's page.

        :returns: TODO

        """
        return self.pages

    def get_book(self):
        """ Get Epubook in processing """
        return self.book

    def get_book_name(self):
        """ Get book name """
        return self.book_name

    def get_book_to_chaps(self):
        """
        :returns: chapters list
        """
        return self.book_to_chaps

    @staticmethod
    def get_chapters_and_pages(toc, pages: List, duplicat: set):
        """ Return list of chapters """
        for chap in toc:
            if isinstance(chap, epub.Link):
                if "#" in chap.href:
                    if str(chap.href).split('#')[1] not in duplicat:
                        pages.append((str(chap.href).split('#')[1], chap.title))
                        duplicat.add(str(chap.href).split('#')[1])
            elif isinstance(chap, tuple):
                pages += ProcessBook.get_chapters_and_pages(chap[1], [], duplicat)
        return pages

    def book_to_jsonFile(self):
        """
            Save book splited to json format
            dictionary = {
                'Book Name': 'Art de se lancer',
                'Others details': ...
                'Content':  [
                    {
                        'title': 'title',
                        'content': 'txt txt txt...',
                    },

                    {
                        'title': 'title',
                        'content': 'txt txt txt...',
                    }
                 ]
            }
        """
        dictionary = {
            'Book Name': self.book_name,
            'Content': self.get_book_to_chaps()
        }
        #  json_obj = json.dumps(dictionary, indent=4)
        outputFile = cfg.JSON_BOOK_FR_DIR + '/' + self.book_name + '.json'
        with open(outputFile, 'w') as jsonFile:
            json.dump(dictionary, jsonFile)

    def get_content(self, chapter) -> str:
        """Return chapter content in string format"""
        output = ''
        soup = BeautifulSoup(chapter, 'html.parser')
        text = soup.find_all(text=True)
        for t in text:
            if t.parent.name not in self.blacklist:
                output += '{} '.format(t)
        return output.strip().replace("  ", " ")

    def get_next_chap_page(self, page_num: str):
        """ Return next chapter page number with current page_num given in para

        :page_num: TODO
        :returns: TODO

        """
        try:
            index = [chap[0] for chap in self.pages].index(page_num)
            next_page_index = index + 1 
            # If next_page_index out of range, below-line throw indexError
            # exception, we catch it and : return False, because next_page_num
            # no exist.
            next_page_num = self.pages[next_page_index][0] 
            return next_page_num
        except ValueError as e:
            return False
        except IndexError as e:
            return False

    def get_chapter_content(self, item, page_num: str) -> str:
        """ Return content of a chapter that's between pages like:
            FROM index_01#pX TO index_01#pY

        :page_num: String: Page number where chapter start.
        :returns chap_output: String 

        """
        chap_output = '' # Fill from chapter Content from page-x to page-y
        # Get next page number
        next_page_num = self.get_next_chap_page(page_num) 
        # call beautiful funtion to get chapter contains
        soup = BeautifulSoup(item.get_content(), 'html.parser')
        # find where chapter start = <p>..</p>  
        if soup.find(id=page_num).parent.name not in 'body div':
            chapter_start = soup.find(id=page_num).parent
        else: 
            chapter_start = soup.find(id=page_num)
        chap_output += '{}:\n'.format((self.get_text(chapter_start)).capitalize())
        # Get all paragraphe after title
        chapter_siblings = chapter_start.find_next_siblings('p')
        # find where chapter end/next chapter start = <p><a id='next_page_num'></a>..</p>  
        for paragraph in chapter_siblings:
            if paragraph.a:
                a_tag = paragraph.a
                if a_tag.get('id') and a_tag.get('id') == next_page_num:
                    break
            if paragraph.get('id') and paragraph.get('id') == next_page_num:
                break
            chap_output += '{} '.format(self.get_text(paragraph))
            
        return chap_output.strip().replace("  ", " ")

    def get_text(self, tag):
        """ Return all text containt from a 'tag' given in parameter 

        :tag:
        :returns output: String

        """
        output = ''
        for string in tag.stripped_strings:
            output += '{} '.format(string)
        return output.strip().replace("  ", " ") + "\n"

    def splitbook_to_chapters(self, toc, chapters: List) -> List:
        """
        1: Fill self.book_to_chaps[] from 'book table content'
        2: Fill in string the key 'content' of self.book_to_chaps
           from content of each chapter

        :return chapters[] # List of 'chapter and its contents'
        """
        #  'content': '\n'.join(wrap(self.get_content(
            #  item.get_content()), 40))
        #  'content': self.get_content(item.get_content())
        for chap in toc:
            if isinstance(chap, epub.Link):
                #  continue
                item = self.book.get_item_with_href(str(chap.href).split('#')[0])
                if "#" in chap.href:
                    page_num = str(chap.href).split('#')[1]
                    #  with open('content.html', 'w') as fil:
                        #  soup = BeautifulSoup(item.get_content(), 'html.parser')
                        # find where chapter start = <p>..</p>  
                        #  if soup.find(id=page_num).parent.name not in 'body div':
                            #  chapter_start = soup.find(id=page_num).parent
                        #  else:
                            #  chapter_start = soup.find(id=page_num)
                        #  print(chapter_start, file=fil)
                    chapters.append(
                        {
                            'is_part': False,
                            'book_title': self.book_data['title'],
                            'book_id': self.book_data['identifier'],
                            'creator': self.book_data['creator'],
                            'contributor': self.book_data['contributor'],
                            'published_date': self.book_data['date'],
                            'href': str(item),
                            'chapter_title': chap.title,
                            'subject': self.book_data['subject'],
                            'context': self.book_data['description'],
                            'content': self.get_chapter_content(item, page_num),
                        }
                    )
                else:
                    chapters.append(
                        {
                            'is_part': False,
                            'book_title': self.book_data['title'],
                            'book_id': self.book_data['identifier'],
                            'creator': self.book_data['creator'],
                            'contributor': self.book_data['contributor'],
                            'published_date': self.book_data['date'],
                            'href': str(item),
                            'chapter_title': chap.title,
                            'subject': self.book_data['subject'],
                            'context': self.book_data['description'],
                            'content': self.get_content(item.get_content()),
                        }
                    )
            elif isinstance(chap, tuple):
                #  continue
                chapters.append(
                    {
                        'is_part': True,
                        'title': chap[0].title,
                        'chapters': self.splitbook_to_chapters(chap[1], [])
                    }
                )
        return chapters

    def get_book_info(self):
        """ Return a list: data=[(id1,value1), (id2, value2)] or None=[] """
        list_ids = ['title', 'creator', 'identifier', 'description',
                    'subject', 'language', 'contributor', 'publisher', 'date',
                    'rigths', 'coverage']
        for info in  list_ids:
            data = list(self.book.get_metadata('DC', info))
            if data:  # if data not empty 
                self.book_data[info] = []
                for x in data:  # Extract each tuple
                    dataTuple = x
                    self.book_data[info].append(str(dataTuple[0]))
                #  Join [] to str by ,
                self.book_data[info] = ", ".join(self.book_data[info])
            else: self.book_data[info] = ""
        return self.book_data


if __name__ == '__main__':
    print('Je suis YATTARA')
    pbook = ProcessBook("/home/alassane/Code/JimBot/chatbotapp/books/epubFrench/POUVOIR ILLIMITE by Anthony Robbins (z-lib.org).pdf.epub")
    pbook.book_to_jsonFile()
    #  print(pbook.get_pages())

