visebuy
=======

1) The Shoes_DB has been uploaded to local/shoes_db
address: localhost:3306
username: root
password: root
using command

mysql> use DATABASE_NAME;
mysql> source path/to/file.sql;

but the text search needs to be deloyed online -> the database also needs to be deployed online


Login database:
mysql -u dat -p
password: 123456

ip address:  100.80.138.113
http://www.cyberciti.biz/tips/how-do-i-enable-remote-access-to-mysql-database-server.html

2) Next:
Install mysql on unix server
Deploy .sql file
Set up text search server

https://www.digitalocean.com/community/articles/how-to-install-linux-apache-mysql-php-lamp-stack-on-debian

visebuy project

Things to do next:
1) Deploy to the server provided by Tim
2) Finish other search functions:
    a) Text search (doesn't work)
    b) Search by uploading image
        - Insert a browse and upload function (refer to old code)
        - THen return result
    c) Search by category
        - Add in category (refer to old code)
3) Indexing and searching using a new API


II) Text Search
To start text search server
Goto: opt/solr/apache-solr
Execute: java -jar start.jar
http://msm3.cais.ntu.edu.sg/documentation/zixiang/index.html
change bind address at etc/mysql/my.cnf to 0.0.0.0
III) Inspectdb

* Rearrange model order
* Make sure each model has one field with primary key = true
* remove managed = false lines for those models you wish to give write access to
Can rename the models but dont rename bb_table values or field balues
You will have to insert output of 'django-admin.py sqlcustom [appname] to your database'

IV) Image Search
APIkey: 6cDgWkHEfqnFFgw13oqq6XBiKXxrqC0ZtPbaIChP4uc


V) Test the Params Filter, by taking the URL from the old visebuy website:
Text search with filter
- http://localhost:8000/dmserver/debugparamsfilter/?text=2010&filter=color:11,-1,-1,-1;&page=1&
Category search with filter
http://localhost:8000/dmserver/debugparamsfilter/?category=%E8%BF%90%E5%8A%A8%E9%9E%8B&filter=style:%E7%94%9F%E6%B4%BB%E9%9E%8B;&page=1&


VI) Transfer big file from window to remote unix server using scp


VII) Future plan
-Receive the returned result from Kyle
-Create a new table in database to support testing of the new image server (for both local and product enviroment)

=========
To start project
-tmux
-run process
-Ctrl B then D for detach
