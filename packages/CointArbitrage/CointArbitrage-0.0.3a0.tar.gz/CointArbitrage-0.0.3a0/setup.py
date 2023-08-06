# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 10:54:40 2018

@author: yili.peng
"""

from setuptools import setup
from pypandoc import convert_file

setup(name='CointArbitrage'
      ,version='0.0.3a'
      ,description='Conintegration method'
      ,long_description=convert_file('README.md', 'rst', format='markdown_github').replace("\r","")
      ,keywords='quant statistical arbitrage'
      ,lisence='MIT'
      ,author='Yili Peng'
      ,packages=['CointArbitrage',
                'CointArbitrage.pairing_period',
                'CointArbitrage.trading_period',
                'CointArbitrage.instant_with_wind'
                 ]
      ,install_requires=[
          'RNWS',
          'mini_exchange'
      ]
      ,author_email='yili_peng@outlook.com'
      ,zip_safe=False)