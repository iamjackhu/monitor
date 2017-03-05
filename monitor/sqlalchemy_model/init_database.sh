#!/usr/bin/env bash

export mysql_username=root
export mysql_password=root

mysql -u$mysql_username -p$mysql_password -e "CREATE DATABASE model";
mysql -u$mysql_username -p$mysql_password -e "CREATE USER 'model'@'%' IDENTIFIED BY 'model123'";
mysql -u$mysql_username -p$mysql_password -e "GRANT ALL PRIVILEGES ON model.* TO 'model'@'%' IDENTIFIED BY 'model123' WITH GRANT OPTION;"
