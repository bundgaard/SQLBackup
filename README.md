Hi

usage is create a conf file 1270005.conf, with a key-value for each entry, as for now the script understand 

This script is dependent on fabric from fabfile.org.

The script will create files for each database entry and can handle import to a new database, by creating databases before, all this require the user to log into the database to have proper grants.


The conf file 127005.conf can handle '#' as comments.

So to deactivate a line just put a # in front.

if you want to rename databases please make sure you have equal items.

databases=database1,database3 
fromusername=myusername
frompassword=mypassword
fromhost=mysqlhost1
tohost=mysqlhost2
tousername=username-host2
topassword=password-host2
#newdatabases=newdatabase2,newdatabase3

USAGE:

* Add two SSH tunnels or change from local to run and add SSH keys on the servers.

TODO:


* Add compression

* Make sure to not show passwords in output


* I have to actually verify this will work with more data like 20GB and more.

* This is a very crude example. 
