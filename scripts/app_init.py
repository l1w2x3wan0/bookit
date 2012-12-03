#coding=utf-8
'''
Created on 2012-11-30

@author: fengclient
'''
import sys
sys.path.append('/data/web2py')

from gluon.dal import DAL
from gluon.tools import Auth

if __name__ == '__main__':
    db = DAL('sqlite://../app_src/applications/bookit/databases/storage.sqlite')
    auth=Auth(db)
    
    g_manager_id=auth.add_group('Manager','can access the manage action/page')
    g_user_id=auth.add_group('User','can view and borrow')
    g_admin_id=auth.add_group('Admin','everything')
    
    auth.add_permission(g_manager_id,'access to manage')
    auth.add_permission(g_manager_id,'access to borrow')
    
    auth.add_permission(g_user_id,'access to borrow')
    
    auth.add_permission(g_admin_id,'access to manage')
    auth.add_permission(g_admin_id,'access to borrow')
    auth.add_permission(g_admin_id,'access to admin')
    
    
    
    pass