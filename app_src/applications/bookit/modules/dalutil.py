#coding=utf-8
'''
Created on 2012-10-11

@author: fengclient
'''
from gluon.dal import DAL,Field,Row
from gluon import current
import json

class ActionType(object):
    Borrow=1
    Return=2
    Checkin=3
    Checkout=4

def insert_book_raw(douban_bookid,douban_title,douban_image,douban_bookurl,douban_apiurl,douban_apidata,totalcount,availablecount):
    return current.db.book.insert(douban_bookid=douban_bookid,douban_title=douban_title,douban_image=douban_image,
                                  douban_bookurl=douban_bookurl,douban_apiurl=douban_apiurl,douban_apidata=douban_apidata,
                                  totalcount=totalcount,availablecount=availablecount)
    
def insert_book_json(douban_bookid,jsondata):
    book=json.loads(jsondata)
    douban_apiurl=(i for i in book['link'] if i['@rel']=='self').next()['@href']
    douban_bookurl=(i for i in book['link'] if i['@rel']=='alternate').next()['@href']
    douban_image=(i for i in book['link'] if i['@rel']=='image').next()['@href']
    return insert_book_raw(douban_bookid,book['title']['$t'],douban_image,douban_bookurl,douban_apiurl,jsondata,1,1)

def borrow_book(douban_bookid,borrower):
    bookmodel=current.db.book
    logmodel=current.db.borrowlog
    row=bookmodel[douban_bookid]
    if row and row.availablecount>0:
        row.update_record(availablecount=row.availablecount-1)
        logmodel.insert(douban_bookid=douban_bookid,status=ActionType.Borrow,user=borrower)
        return row.availablecount

def return_book(douban_bookid,borrower):
    bookmodel=current.db.book
    logmodel=current.db.borrowlog
    row=bookmodel[douban_bookid]
    row.update_record(availablecount=row.availablecount+1)
    logmodel.insert(douban_bookid=douban_bookid,status=ActionType.Return,user=borrower)
    return row.availablecount

def checkin_book(douban_bookid,count,user):
    bookmodel=current.db.book
    logmodel=current.db.borrowlog
    row=bookmodel[douban_bookid]
    row.update_record(totalcount=row.totalcount+1,availablecount=row.availablecount+1)
    logmodel.insert(douban_bookid=douban_bookid,status=ActionType.Checkin,user=user)
    return (row.totalcount,row.availablecount)

def checkout_book(douban_bookid,count,user):
    bookmodel=current.db.book
    logmodel=current.db.borrowlog
    row=bookmodel[douban_bookid]
    if row and row.totalcount>0 and row.availablecount>0:
        row.update_record(totalcount=row.totalcount-1,availablecount=row.availablecount-1)
        logmodel.insert(douban_bookid=douban_bookid,status=ActionType.Checkin,user=user)
        return (row.totalcount,row.availablecount)

def get_book(bookid):
    bookmodel=current.db.book
    return bookmodel[bookid]

def get_books_by_name(name):
    bookmodel=current.db.book
    rows=current.db(bookmodel.douban_title==name).select()
    if rows and len(rows)>0:
        return rows
    