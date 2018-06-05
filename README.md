# Book API Setup and Installation

## Requirements
1. MySQL
2. Python3
3. pip
4. pipenv

## Setup
1. Install MySQL
2. Login to mysql with root and create a new database and a user with permissions:
   
   `CREATE DATABASE bookdb;`  
   `INSERT INTO mysql.user (User,Host,authentication_string,ssl_cipher,x509_issuer,x509_subject)  
   VALUES('bookuser','localhost',PASSWORD('book'),'','','');`  
   `GRANT ALL PRIVILEGES ON bookdb.* to bookuser@localhost;`  
   `FLUSH PRIVILEGES;`
3. Install pip using whatever method you prefer. More [here](https://packaging.python.org/guides/installing-using-linux-tools/#installing-pip-setuptools-wheel-with-linux-package-managers).
4. Install pipenv: `pip install pipenv`
5. Clone this repository.
6. Change to the cloned directory.
7. Run `pipenv install`
