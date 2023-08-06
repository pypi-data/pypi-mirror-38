# -*- coding: utf-8 -*-
__author__ = 'lihe <imanux@sina.com>'
__date__ = '11/20 10:25'
__description__ = '''
mutagen
'''
import os
import sys

app_root = '/'.join(os.path.abspath(__file__).split('/')[:-2])
sys.path.append(app_root)

from izen import helper

md_file = os.path.join(app_root, 'README.md')

res = helper.md_rst_convert(md_file)
print(res)
helper.write_file(res, os.path.join(app_root, 'README.rst'))
