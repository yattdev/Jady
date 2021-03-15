#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
from os import path, chdir, mkdir


dict_file = [{'sports' : ['soccer', 'football', 'basketball', 'cricket', 'hockey', 'table tennis']},
{'countries' : ['Pakistan', 'USA', 'India', 'China', 'Germany', 'France', 'Spain']}]


# Get current dir path contained this script
current_dir_path = str(path.dirname(path.realpath(__file__)))
chdir(current_dir_path) # Change the current working directory
file_name = current_dir_path + '/file.yml'

with open(r''+file_name, 'r') as yamlfile:
    current_yml_file = yaml.dump(yamlfile)
    intent = current_yml_file[0]
    intent.append('yattara est un sports aussi')
    ['sports'].update(dict_file[0])
    current_yml_file['countries'].update(dict_file[1])
    
