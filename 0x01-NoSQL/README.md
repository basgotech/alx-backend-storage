0x01. NoSQL
===========

Back-end NoSQLMongoDB



Resources
---------

**Read or watch**:

-   [NoSQL Databases Explained](https://alx-intranet.hbtn.io/rltoken/wweK7dOY4pf8haCqv9Iv6Q "NoSQL Databases Explained")
-   [What is NoSQL ?](https://alx-intranet.hbtn.io/rltoken/QqqNmgzgwopHBv305ki6bg "What is NoSQL ?")
-   [MongoDB with Python Crash Course - Tutorial for Beginners](https://alx-intranet.hbtn.io/rltoken/RyyP9OH1EMBWWYpTs4TqoA "MongoDB with Python Crash Course - Tutorial for Beginners")
-   [MongoDB Tutorial 2 : Insert, Update, Remove, Query](https://alx-intranet.hbtn.io/rltoken/9__3tR-NimgXlmjPQwTF-Q "MongoDB Tutorial 2 : Insert, Update, Remove, Query")
-   [Aggregation](https://alx-intranet.hbtn.io/rltoken/ziEDeniRobC6owPE1_avAQ "Aggregation")
-   [Introduction to MongoDB and Python](https://alx-intranet.hbtn.io/rltoken/axwwF4CjO7FnK8Ecochqnw "Introduction to MongoDB and Python")
-   [mongo Shell Methods](https://alx-intranet.hbtn.io/rltoken/lUqnLwOHbbp9FK39ijNmDQ "mongo Shell Methods")
-   [The mongo Shell](https://alx-intranet.hbtn.io/rltoken/bffQMLcTB4cg1bKqgBW3jw "The mongo Shell")

Learning Objectives
-------------------

At the end of this project, you are expected to be able to [explain to anyone](https://alx-intranet.hbtn.io/rltoken/9u20uNESC1dnTNowO5waNQ "explain to anyone"), **without the help of Google**:

### General

-   What NoSQL means
-   What is difference between SQL and NoSQL
-   What is ACID
-   What is a document storage
-   What are NoSQL types
-   What are benefits of a NoSQL database
-   How to query information from a NoSQL database
-   How to insert/update/delete information from a NoSQL database
-   How to use MongoDB

More Info
---------

### Install MongoDB 4.2 in Ubuntu 18.04

[Official installation guide](https://alx-intranet.hbtn.io/rltoken/8p4x14Ddn1UxKXZ5nPt3zA "Official installation guide")

```
$ wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | apt-key add -
$ echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" > /etc/apt/sources.list.d/mongodb-org-4.2.list
$ sudo apt-get update
$ sudo apt-get install -y mongodb-org
...
$  sudo service mongod status
mongod start/running, process 3627
$ mongo --version
MongoDB shell version v4.2.8
git version: 43d25964249164d76d5e04dd6cf38f6111e21f5f
OpenSSL version: OpenSSL 1.1.1  11 Sep 2018
allocator: tcmalloc
modules: none
build environment:
    distmod: ubuntu1804
    distarch: x86_64
    target_arch: x86_64
$
$ pip3 install pymongo
$ python3
>>> import pymongo
>>> pymongo.__version__
'3.10.1'

```

Potential issue if documents creation doesn't work or this error: `Data directory /data/db not found., terminating` ([source](https://alx-intranet.hbtn.io/rltoken/as8vd5VBnj4VDz5EINszMg "source") and [source](https://alx-intranet.hbtn.io/rltoken/9Df5v1NcWFFCn_sRNgsJUg "source"))

```
$ sudo mkdir -p /data/db

```

Or if `/etc/init.d/mongod` is missing, please find here an example of the file:

Click to expand/hide file contents

### Use "container-on-demand" to run MongoDB

-   Ask for container `Ubuntu 18.04 - MongoDB`
-   Connect via SSH
-   Or via the WebTerminal
-   In the container, you should start MongoDB before playing with it:

```
$ service mongod start
* Starting database mongod                                              [ OK ]
$
$ cat 0-list_databases | mongo
MongoDB shell version v4.2.8
connecting to: mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb
Implicit session: session { "id" : UUID("70f14b38-6d0b-48e1-a9a4-0534bcf15301") }
MongoDB server version: 4.2.8
admin   0.000GB
config  0.000GB
local   0.000GB
bye
$

```


## Authors

- [@Basliel Tegegn](https://www.github.com/basgotech)

