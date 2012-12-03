# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
import dalutil

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

def index():
    '''
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    '''
    response.flash = T('Welcome to library!')
    response.title=T('Bookit - your personal library')
    return dict()

def show():
    '''
    show info and stock
    '''
    response.files.append(URL('static','js/show.js'))
    book=dalutil.get_book(request.vars['bookid'])
    return dict(title=book.douban_title,imgsrc=book.douban_image,total=book.totalcount,
                available=book.availablecount,doubanurl=book.douban_bookurl,bookid=book.douban_bookid) if book else 'Not found'

def search():
    '''
    search by id, name and other keys.TODO
    '''
    response.files.append(URL('static','js/search.js'))
    if 'key' in request.vars:
        return dict(books=dalutil.get_books_by_name(request.vars['key']),key=request.vars['key'])
    else:
        return dict(books=[],key='')
    