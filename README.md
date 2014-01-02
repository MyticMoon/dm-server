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
http://msm3.cais.ntu.edu.sg/documentation/zixiang/index.html

=========
1) Provide a fake API for Shu Qi
2) Deploy text search server on Azure
3) Deploy vise buy and SQL database to another Azure server