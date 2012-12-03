#coding=utf-8
'''
Created on 2012-11-4

@author: fengclient
'''
import urllib2
import urlparse
from bs4 import BeautifulSoup

def parse_doulist(url):
    url=urlparse.urlunparse(urlparse.urlparse(url)[0:3]+(None,None,None))
    books=[]
    while(url):
        html_doc=urllib2.urlopen(url).read()
        soup=BeautifulSoup(html_doc)
        items=soup.find_all('tr',class_='doulist_item')
        for item in items:
            books.append(item.td.a['href'])
        nextdiv=soup.find('div',class_='paginator')
        url=None
        if nextdiv:
            link=nextdiv.find('span',class_='next').a
            if link:
                url=link['href']
    return books

def getid_from_url(url):
    urlobj=urlparse.urlparse(url)
    parts=urlobj.path.split('/')
    douban_id=(i for i in parts[::-1] if i).next()
    douban_apiurl='http://api.douban.com/book/subject/%s?alt=json'%(douban_id);
    return douban_id,douban_apiurl