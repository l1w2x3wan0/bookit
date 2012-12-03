#coding=utf-8
'''
Created on 2012-10-15

@author: fengclient
'''
import urllib2
import dalutil
import butil
from bs4 import BeautifulSoup

def get():
    '''
    get book info by id or name
    '''
    response.view='generic.jsonp' if 'callback' in request.vars else 'generic.json'
    if 'id' in request.vars:
        bookid=request.vars['id']
        book=dalutil.get_book(bookid)
        return book.as_dict() if book else 'wrong bookid'
    elif 'name' in request.vars:
        name=request.var['name']
        books=dalutil.get_books_by_name(name)
        booklist=[a.as_dict() for a in books]
        return booklist if book else 'book name not exist'
    else:
        return 'missing id or name argument'
    
def add():
    '''
    add a book
    '''
    response.view='generic.jsonp' if 'callback' in request.vars else 'generic.json'
    url=request.vars.url
    douban_id,douban_apiurl=butil.getid_from_url(url)
    try:
        jsondata=urllib2.urlopen(douban_apiurl).read()
    except urllib2.HTTPError as e:
        return dict(ret=-1,msg=str(e.code)+' '+e.msg)
    if dalutil.get_book(douban_id):
        return dict(ret=-2,msg='book exists',bookid=douban_id)
    if dalutil.insert_book_json(douban_id, jsondata):
        return dict(ret=0,msg='success',bookid=douban_id)
    else:
        return dict(ret=-1,msg='unknown error')

def borrow():
    '''
    borrow a book
    '''
    response.view='generic.jsonp' if 'callback' in request.vars else 'generic.json'
    bookid=request.vars.id
    borrower=request.vars.borrower
    count=dalutil.borrow_book(bookid,borrower,'admin')
    if count:
        return dict(ret=0,msg='success',data=count)
    else:
        return dict(ret=-1,msg='failed')

def returnb():
    '''
    return a book
    '''
    response.view='generic.jsonp' if 'callback' in request.vars else 'generic.json'
    bookid=request.vars.id
    borrower=request.vars.borrower
    if bookid.isdigit():
        return dict(ret=dalutil.return_book(bookid,borrower,'admin'))
    
def checkin():
    '''
    check in several copies for one book
    '''
    response.view='generic.jsonp' if 'callback' in request.vars else 'generic.json'
    bookid=request.vars.id
    count=request.vars.count
    if bookid.isdigit() and count.isdigit():
        total,available=dalutil.checkin_book(bookid,count,'admin')
        return dict(ret=0,total=total,available=available)

def checkout():
    '''
    check out server copies for one book
    '''
    response.view='generic.jsonp' if 'callback' in request.vars else 'generic.json'
    bookid=request.vars.id
    count=request.vars.count
    if bookid.isdigit() and count.isdigit():
        retdata=dalutil.checkout_book(bookid,count,'admin')
        if retdata:
            return dict(ret=0,total=retdata[0],available=retdata[1])
        return dict(ret=-1,msg='cannot check out anymore')
    return dict(ret=-2,msg='argument error')

def importdoulist():
    '''
    import from doulist
    '''
    response.view='generic.jsonp' if 'callback' in request.vars else 'generic.json'
    url=request.vars.url
    books=butil.parse_doulist(url)
    count_succeed=0
    count_failed=0
    count_existed=0
    
    for book in books:
        douban_id,douban_apiurl=butil.getid_from_url(book)
        if dalutil.get_book(douban_id):
            count_existed+=1
        else:
            try:
                jsondata=urllib2.urlopen(douban_apiurl).read()
            except urllib2.HTTPError as e:
                count_failed+=1
                continue
            if dalutil.insert_book_json(douban_id, jsondata):
                count_succeed+=1
            else:
                count_failed+=1
    return dict(ret=0 if count_failed==0 else -1,msg='succeed=%d,failed=%d,exist=%d'%(count_succeed,count_failed,count_existed))
    