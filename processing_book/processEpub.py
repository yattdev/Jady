#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from errno import ENOENT
from os import strerror, path, chdir, mkdir
from settings.config_default import (BASE_DIR, JSON_BOOK_FR_DIR,
                                     INDEXED_CHAP_PATHS)

from typing import List
from bs4 import BeautifulSoup
from ebooklib import epub

from settings import config_default as cfg


class ProcessBook():
    """ Class to splite Epubbook by chapter to jsonFormat """

    def __init__(self, bookname: str):
        """ Initialize create instance and variables """
        self.book_to_chaps = []
        self.blacklist = ['[document]', 'noscript', 'header', 'html', 'meta',
                          'head', 'input', 'script']
        self.book = None
        self.book_name = bookname.split('/')[-1]
        self.book_data = {}
        try:
            self.book = epub.read_epub(bookname)
        except FileNotFoundError as e:
            raise e(ENOENT, strerror(ENOENT), bookname)

        self.book_data = self.get_book_info()  # Get book info
        # Get chapter and it's page number [(chapter, page), ...]
        # Delete duplicate chapter by set() function
        self.pages = ProcessBook.get_chapters_and_pages(self.book.toc, [],
                                                        set())
        # sorted chapter par page number
        #  self.pages = sorted(self.pages, key=lambda tup: int(tup[0]))
        # Split book to chapters
        self.book_to_chaps = self.splitbook_to_chapters(self.book.toc,
                                                        self.book_to_chaps)

    #  def get_pages(self):
        #  """ Return book chapter and it's page.

        #  :returns: TODO

        #  """
        #  return self.pages

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
    def get_chapters_and_pages(toc, pages, duplicat: set):
        """ Return list of chapters
        Params:
            pages: List -> It's list of pages to return
            duplicat: Set -> It's set
        Return:
            pages
        """
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

    def get_next_chap_page_num(self, page_num: str):
        """ Return next chapter page number with current page_num given in para

        :page_num: TODO
        :returns: TODO

        """
        try:
            index = [chap[0] for chap in self.pages].index(page_num)
            next_page_index = index + 1
            # If next_page_index out of range, below-line throw indexError
            # exception, we catch it and : return False, because next_chap_page_num
            # no exist.
            next_chap_page_num = self.pages[next_page_index][0]
            return next_chap_page_num
        except ValueError:
            return False
        except IndexError:
            return False

    def get_chapter_content(self, chap_title: str, item, page_num: str) -> str:
        """ Return content of a chapter that's between pages like:
            FROM index_01#pX TO index_01#pY

        :page_num: String: Page number where chapter start.
        :returns chap_output: String

        """
        chap_output = ''  # Fill with chapter content from page-x to page-y
        # Get next chapter start page number
        next_chap_page_num = self.get_next_chap_page_num(page_num)
        # call beautiful funtion to get chapter contains
        soup = BeautifulSoup(item.get_content(), 'html.parser')
        # find where chapter start = <p>..</p>
        if soup.find(id=page_num):
            try:
                if soup.find(id=page_num).parent.name not in 'body div':
                    chapter_start = soup.find(id=page_num).parent
                else:
                    chapter_start = soup.find(id=page_num)
            except AttributeError as e:
                print("Can't split book: {book_name}".format(
                    book_name=self.book_name))
                print("Error to get contents of chapter: {chap_title}".format(
                    chap_title=chap_title))
                print("Item: {item}".format(item=item))
                raise e

            # Get chapter title
            chap_output += '{}:\n'.format(
                (self.get_text(chapter_start)).capitalize())
            # Get all paragraphe after title
            chapter_siblings = chapter_start.find_next_siblings('p')
            # find where chapter end/next chapter start = <p><a id='next_chap_page_num'></a>..</p>
            for paragraph in chapter_siblings:
                if paragraph.a:
                    a_tag = paragraph.a
                    if a_tag.get('id') and a_tag.get('id') == next_chap_page_num:
                        break
                if paragraph.get('id') and paragraph.get('id') == next_chap_page_num:
                    break
                chap_output += '{} '.format(self.get_text(paragraph))

        return chap_output.strip().replace("  ", " ")

    def get_text(self, tag):
        """ Return all text containt from a 'tag' given in parameter

        :tag:
        :returns output: String

        """
        output = ''
        for _ in tag.stripped_strings:
            output += '{} '.format(_)
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
                            'content': self.get_chapter_content(chap.title,
                                                                item,
                                                                page_num)
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

    def save_chaps_to_file(self, file_path=None, chapters=None):
        """
            Save each book chapter's in separate file into json format !
        """
        if not path.exists(path.join(JSON_BOOK_FR_DIR, self.book_name)):
            # Change path
            chdir(JSON_BOOK_FR_DIR)
            mkdir(self.book_name)  # Create directorie with bookname

        if chapters is None:
            # If chapters is empty so its function first call and
            chapters = self.book_to_chaps
            # add book_name to path
            book_path = path.join(JSON_BOOK_FR_DIR, self.book_name)
            # Change path
            chdir(book_path)

        if file_path:  # if file_path is not None so:
            book_path = file_path
            chdir(book_path)

        for chap in chapters:
            if chap['is_part']:
                """ Create a directorie with par name if not exist
                    then call this function with List of chapter
                    of this part
                """
                if not path.exists(path.join(book_path, chap['title'])):
                    mkdir(chap['title'])  # Create directorie with part title

                part_path = path.join(book_path, chap['title'])
                chdir(part_path)
                self.save_chaps_to_file(part_path, chap['chapters'])
                chdir(book_path)  # cd.. to part dir after save its chapters
            else:
                title = chap['chapter_title'].replace('/', ' ou ')
                output = book_path + '/' + title + '.json'
                with open(output, 'w') as json_file:
                    json.dump(chap, json_file)

    @classmethod
    def save(cls, file_path, chapter):
        """ Save chapter to file in json format """
        output = file_path + '/' + chapter['chapter_title'] + '.json'
        with open(output, 'w') as json_file:
            json.dump(chapter, json_file)

    def get_book_info(self):
        """ Return a list: data=[(id1,value1), (id2, value2)] or None=[] """
        list_ids = ['title', 'creator', 'identifier', 'description',
                    'subject', 'language', 'contributor', 'publisher', 'date',
                    'rigths', 'coverage']
        for info in list_ids:
            data = list(self.book.get_metadata('DC', info))
            if data:  # if data not empty
                self.book_data[info] = []
                for _ in data:  # Extract each tuple
                    dataTuple = _
                    self.book_data[info].append(str(dataTuple[0]))
                #  Join [] to str by ,
                self.book_data[info] = ", ".join(self.book_data[info])
            else:
                self.book_data[info] = ""
        return self.book_data


if __name__ == '__main__':
    print('Je suis YATTARA')
    pbook = ProcessBook("/home/alassane/Code/JimBot/chatbotapp/books/epubFrench/startup_entreprise/L’autoroute du millionnaire by MJ De Marco [Marco, MJ De] (z-lib.org).epub")
    pbook.save_chaps_to_file()
    #  print(pbook.get_pages())
