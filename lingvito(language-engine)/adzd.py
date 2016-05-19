#!/usr/bin/env python

import urllib, requests
from bottle import route, run
#from triggers_json import dic
from elasticsearch import Elasticsearch

#trigger_list = dic.keys()
#print trigger_list

es = Elasticsearch()

@route('/<query>', method="GET")
def index(query=""):
	
	#filtered_query = [i for i in query.split() if i not in stopwords]	##filtering out stopwpords
	
	print query

	#template = [dic[x] for x in query if x in dic.keys()]
	#print template

	query={
   
   "query": {
     "filtered": {
       "query": {
             "multi_match": {
               "query": query,
               "fields": ["description^5", "name^10","val^2"],
               "type": "cross_fields"
             }
         
         
       }
     }
 
   }
 }
	query = es.search(index="ddg", doc_type="cheatsheet", body=query)
	return {"cheat":query}

run(host='localhost', port=8080,debug=True)
