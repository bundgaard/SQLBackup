#!/bin/env python
from __future__ import print_function
from fabric.api import run, env, local
from fabric.utils import fastprint
import os, sys
import re
#env.hosts = ['produtil01.eu.ams1.ipcenter.com', 'produtil01.ipsoft.ny1.ip-soft.net']
commaPattern = re.compile(r'\,')

def backup05(host,username, password, databases, newnames="x"):
    if 'x' in newnames:
        for dbEntry in databases.split(','):
            local("mysqldump --databases --no-create-db --single-transaction --hex-blob -h%s -u%s -p%s %s > %s.sql" % (host, username, password, dbEntry, dbEntry) )
    else:
        for dbEntry in databases.split(','):
            local("mysqldump --no-create-db --single-transaction --hex-blob -h%s -u%s -p%s %s > %s.sql" % (host, username, password, dbEntry, dbEntry) )
    
    
def importSQL(host, username, password, databases, newnames="x"):
    if "x" not in newnames:
        fastprint("running with new names!!!!")
        entries = zip(databases.split(','),newnames.split(','))
        for (old, new) in entries:
            local("mysqladmin -h%s -u%s -p%s create %s" % (host, username, password, new))
        for (old, new) in entries:
            local("mysql -h%s -u%s -p%s %s < %s.sql" % (host, username, password, new, old) )
    else:
        for dbEntry in databases.split(','):
            local("cat %s.sql | mysql -h%s -u%s -p%s %s" % (dbEntry,host, username, password, dbEntry))
    
    
def migrate():
    if not os.path.exists('127005.conf'):
        sys.stdout.write('No config file found, create a file called 127005.conf. Aborting')
        sys.exit(1)
    with open('127005.conf', 'r') as f:
        lines = f.read()
    options = {}

    for number, line in enumerate(lines.split('\n')):
        if str(line).startswith('#') == True:
            continue
        if line == '':
            continue
        words = line.split('=')
        if words[0] not in options:
            options[words[0]] = words[1]


    if 'tousername' in options and 'topassword' in options:
        username = options['tousername']
        password = options['topassword']
    else:
        username = options['fromusername']
        password = options['frompassword']

    if 'newdatabases' in options:
        databases = options['newdatabases']
    else:
        databases = "x"

    backup05(options['fromhost'], options['fromusername'], options['frompassword'], options['databases'], databases )

    importSQL(options['tohost'], username, password, options['databases'], newnames=databases)

