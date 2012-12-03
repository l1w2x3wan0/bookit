#coding=utf-8
'''
Created on 2012-10-11

@author: fengclient
'''
db = DAL('sqlite://storage.sqlite')
db.define_table('book',
                Field('douban_bookid','id'),
                Field('douban_title','string'),
                Field('douban_image','string'),
                Field('douban_bookurl','string'),
                Field('douban_apiurl','string'),
                Field('douban_apidata','text'),
                Field('totalcount','integer'),
                Field('availablecount','integer'))

db.define_table('borrowlog',
                Field('douban_bookid','integer'),
                Field('status','integer'),
                Field('user','string'))
db.define_table('doulist',
                Field('douban_doulistid','string'),
                Field('douban_bookid','string'),
                Field('douban_title','string'),
                Field('douban_image','string'),
                Field('douban_api','string'))

from gluon import current
current.db=db