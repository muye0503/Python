#!/usr/bin/env python3
# coding: utf-8

import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.request import urlretrieve
import os

url = "http://www.newsmth.net"
header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'}
downloadDir = "download"

def getDownloadPath(dirName, link, downloadDir):
	reg = re.compile(r"/(\d+)$")
	fileName = re.search(reg, link).group(1)
	fileName = fileName + ".jpg"
	path = os.path.join(os.path.join(downloadDir, dirName), fileName)
	print(path)
	directory = os.path.dirname(path)
	if not os.path.exists(directory):
		os.makedirs(directory)
	return path


def getImage(link):
	#url = "http://www.newsmth.net/nForum/article/PieLove/2344293"
	global url, downloadDir
	r = requests.get(url+link, headers=header)
	bsObj = BeautifulSoup(r.text, 'html.parser')

	dirName = bsObj.find("title").get_text()
	content = bsObj.find_all("a", href=re.compile(r"http://att.newsmth.net/.*"))
	for links in content:
		if 'href' in links.attrs:
			print(links.attrs['href'])
			#print("title:%s" %dirName)
			urlretrieve(links.attrs['href'], getDownloadPath(dirName, links.attrs['href'], downloadDir))

if __name__ == '__main__':
	r = requests.get(url+"/nForum/board/PieLove", headers=header)
	bsObj = BeautifulSoup(r.text, 'html.parser')

	content = bsObj.select(".title_9")
	for item in content[9:]:
		if 'href' in item.a.attrs:
			print(item.a.attrs['href']) #得到帖子的链接
			print(item.a.get_text())
			getImage(item.a.attrs['href'])
			time.sleep(3)




#getImage("http://www.newsmth.net/nForum/article/PieLove/2344293")
