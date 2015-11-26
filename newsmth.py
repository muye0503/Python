#!/usr/bin/env python3
# coding: utf-8

import requests
from bs4 import BeautifulSoup

url = "http://www.newsmth.net/nForum/board/PieLove"
header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'}
r = requests.get(url, headers= header)
bsObj = BeautifulSoup(r.text, 'lxml')

content = bsObj.select(".title_9")
for item in content[9:]:
	#print(item)
	print(item.a['href'])
	print(item.a.get_text())
	#print(type(item))
	#print(item.attrs)

