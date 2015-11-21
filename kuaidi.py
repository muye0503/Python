#!/usr/bin/env python3
# coding: utf-8

import requests
import sys

while True:
	yundan_id = input('请输入运单号:')
	
	if yundan_id:
		params = {}
		params.setdefault('text',yundan_id)

		# 查询该运单所属的快递公司
		r = requests.post('http://www.kuaidi100.com/autonumber/autoComNum', data=params)
		dict_r = r.json() # post 请求的response 为json 格式，调用r.json（）转换成json字典
		list_r_auto = dict_r['auto'] # dict_r中, key auto 的值是一个list
		dict_auto = list_r_auto[0] # list 的第一个元素包含了快递公司的信息，类型是字典
		com_code = dict_auto['comCode'] # dict_auto 中，key comCode 的值是快递公司名字
		print('快递公司：%s' %com_code)

		# 查询该运单详情
		val = {'type':com_code, 'postid':params['text']}
		content = requests.get('http://www.kuaidi100.com/query', params=val) 
		dict_content = content.json() # post 请求的response 为json 格式，调用r.json（）转换成json字典
		list_content_data = dict_content['data'] # dict_content中，key data 的值是一个list
		for item in list_content_data[::-1]: # 将 list_content_data 中的内容倒序输出，元素类型是字典
			print('时间：%s | 地点：%s' %(item['time'], item['context'])) # 字典中，key time的值是快件的到达时间，key context的值是快件中转信息

		sys.exit()
	else:
		print('请输入运单号!!!')

