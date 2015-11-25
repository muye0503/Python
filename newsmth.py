#!/usr/bin/env python3
# coding: utf-8

import requests
from bs4 import BeautifulSoup

url = "http://www.newsmth.net/nForum/board/PieLove"
header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'}
r = requests.get(url, headers= header)
bsObj = BeautifulSoup(r.text, 'html.parser')

for item in bsObj.find('table', class_='board-list tiz').find_all('td', class_='title_9'):
	print(item.string)
	print(item.a['href'])
	#print(type(item))
	#print(item.attrs)

