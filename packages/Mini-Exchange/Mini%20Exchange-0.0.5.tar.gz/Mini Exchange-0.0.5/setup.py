# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 10:54:40 2018

@author: yili.peng
"""

from setuptools import setup

setup(name='Mini Exchange'
      ,version='0.0.5'
      ,description='Time based strategy back testing system'
      ,long_description=open('README.md').read()
      ,keywords='quant'
      ,lisence='MIT'
      ,author='Yili Peng'
      ,author_email='yili_peng@outlook.com'
      ,packages=['mini_exchange']
      ,install_requires=[
          'plotly'
      ]
      ,zip_safe=False)