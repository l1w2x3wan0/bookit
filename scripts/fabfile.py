#!/usr/bin/python
from fabric.api import *
import os

env.hosts=['xiaoftang@192.168.111.128']

user='xiaoftang'
package_name='bookit.tar.gz'

def routes():
    deploy('routes.py')
    
def app():
    '''
    exclude databases
    '''
    deploy('applications/bookit','applications/bookit/databases')

def deploy(path='*',exclude=''):
    parent=os.path.dirname(os.path.dirname(env.real_fabfile))
    local_path=os.path.join(parent,'app_src')
    remote_path='/data/web2py/'
    with lcd(local_path):
        local('rm %s -f'%(package_name))
        cmd='tar -czf %s %s'%(package_name,path)
        if exclude:
            cmd='%s --exclude %s'%(cmd,exclude)
        local(cmd)
        put(package_name,'/tmp/%s'%(package_name))
    with cd(remote_path):
        sudo('tar -xzf /tmp/%s'%(package_name))
        sudo('chown apache:apache %s -R -f'%(remote_path))
        sudo('chmod 777 %s -R -f'%(remote_path))

def restart_httpd():
    sudo('service httpd restart')

if __name__ == "__main__":
    deploy()