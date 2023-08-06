# -*- coding: utf-8 -*-
"""
Created on Thu May  3 16:50:29 2018

@author: yili.peng
"""

from setuptools import setup
from pypandoc import convert_file

setup(name='RNWS'
      ,version='0.1.2'
      ,description='read and write daily stock data'
      ,long_description=convert_file('README.md', 'rst', format='markdown_github').replace("\r","")
      ,keywords='i/o quant'
      ,author='Yili Peng'
      ,author_email='yili.peng@outlook.com'
      ,packages=['RNWS']
      ,package_data={
		'RNWS': ['data/trading_date.csv'],
		}
      ,lisence='MIT'
      ,zip_safe=False)