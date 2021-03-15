#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path, chdir, mkdir
from pathlib import Path
import subprocess
from settings.config_default import NLU_DATA_PATH


def update_data_from_booksUtterance(booksUtters_dir_path):
    """TODO: Docstring for update_data_from_booksUtterance.
    Update data NLU by:
        1 : Generate Utterances JSON-FORMAT from books=(chap1.txt, ch2.txt,... 
        in chatette format)
        2 : Update data NLU by copying Utterances generated into the data/ dir

    :booksUtters_Dir: TODO
    :returns: TODO

    """
    # Get current dir path contained this script
    current_dir_path = path.dirname(path.realpath(__file__))
    chdir(current_dir_path) # Change the current working directory

    try:
        book_chaps_txt = Path(booksUtters_dir_path).glob('*.txt')
        for chap_txt in book_chaps_txt:
            #  Generat Utterance in JSON-FORMAT
            chap_txt = str(chap_txt)
            print(subprocess.Popen("python -m chatette "+chap_txt, shell=True,
                                   stdout=subprocess.PIPE).stdout.read())

            # Update nlu data dir by cp output.json generate 
            chap_name = str(chap_txt.split('/')[-1])
            book_name = str(chap_txt.split('/')[-2])
            # copy_dir_path = NLU_DATA_PATH + generated_data copy name
            copy_dir_path = path.join(NLU_DATA_PATH +'/data_books/')
            copy_dir_path = str(path.join(copy_dir_path,
                                          book_name +'/'+ chap_name +'.json'))
            if path.exists('output/train/output.json'):
                print(
                subprocess.Popen("cp output/train/output.json "+copy_dir_path,
                                shell=True,
                                stdout=subprocess.PIPE).stdout.read()
                )
    except Exception as e:
        print('\n######################################\n')
        print('Heho, Ya probleme :) ERROR !!!')
        print('\n######################################\n')
        raise e

    print('\n######################################\n')
    print('DATA NUL UPDATED SUCCESSFULLY')
    print('\n######################################\n')


if __name__ == '__main__':
    utter_path = "/home/alassane/Code/JimBot/chatbotapp/book_utterances/"
    utter_path += "Pouvoir_Illimité_BY_[Anthony_Robbins]"
    update_data_from_booksUtterance(utter_path)
