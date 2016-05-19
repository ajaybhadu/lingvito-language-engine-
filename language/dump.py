#!/usr/bin/env python

from elasticsearch import Elasticsearch
es = Elasticsearch()
import json
import os

x= os.listdir("/home/ajay/zeroclickinfo-goodies/share/goodie/cheat_sheets/json/language")
li=[]
for xx in x:
	try:
		if ".json" in xx:
			js = json.loads(open("/home/ajay/zeroclickinfo-goodies/share/goodie/cheat_sheets/json/language/"+xx,"r").read())
			print xx
			res = es.index(index="ddg", doc_type='cheatsheet', id=xx, body=js)
			print(res['created'])
	except Exception as e:
		li.append(xx+str(e))
print li
