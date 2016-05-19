#!/usr/bin/env python

import urllib, requests
from bottle import route, run, template, request, static_file
from triggers_json import dic
from elasticsearch import Elasticsearch
import stopwords
stopwords = stopwords.getStopWords()
trigger_list = dic.keys()
print trigger_list

es = Elasticsearch()


@route('/', method = "GET")
def home(name = None):
	return template('template/index.html',name=request.environ.get('REMOTE_ADDR'))

@route('/<query>', method="GET")
def index(query=""):
	
	filtered_query = [i for i in query.split() if i not in stopwords]	##filtering out stopwpords
	
	print query

	template = [dic[x] for x in query if x in dic.keys()]
	print template

	query={
   "size":1,
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



# Static Routes
@route('/assets/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='assets/js')

@route('/assets/<filename:re:.*\.css>')
def stylesheets(filename):
	return static_file(filename, root='assets/css')

@route('/assets/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='assets/img')

@route('/assets/<filename:re:.*\.(eot|ttf|woff|woff2|svg)>')
def fonts(filename):
	return static_file(filename, root='assets/fonts')

@route('/assets/<filename:re:.*\.(json)>')
def json_assets(filename):
	return static_file(filename, root='assets/json')

@route('/fonts/<filename:re:.*\.(eot|ttf|woff|woff2|svg)>')
def fonts(filename):
	return static_file(filename, root='assets/fonts')

run(host='localhost', port=8080,debug=True)
