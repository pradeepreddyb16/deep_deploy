
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
# from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode


cnx = mysql.connector.connect(user='root', password='',host='127.0.0.1')
cursor = cnx.cursor()


DB_NAME = 'deepfactsoriginal'


TABLES = {}
TABLES['category_collection'] = (
    "CREATE TABLE `category_collection` ("
    "  `id` int(11) NOT NULL,"
    "  `category_type` varchar(50) NOT NULL,"
    "  `category_id` varchar(10) NOT NULL"
    ") ENGINE=InnoDB")

TABLES['client'] = (
    "CREATE TABLE `client` ("
    "  `id` int(10) NOT NULL,"
    "  `name` varchar(50) NOT NULL,"
    "  `mobile` varchar(20) NOT NULL,"
    "   `email` varchar(50) NOT NULL,  "
    "   `password` varchar(20) NOT NULL,"
    "   `OTP` int(10) NOT NULL,"
    "   `category_id` int(10) NOT NULL,"
    "   `Status` varchar(10) NOT NULL DEFAULT 'True`',"
    "   `DF_Super_Admin_id` int(11) NOT NULL,"
    "   `DF_Admin` int(11) NOT NULL,"
    "   `DF_Customer_Success` int(11) NOT NULL,"
    "   `DF_Command_Center` int(11) NOT NULL,"
    "   `DF_Finance` int(11) NOT NULL"
    ") ENGINE=InnoDB")

TABLES['DF_Admin'] = (
    "CREATE TABLE `DF_Admin` ("
    "  `id` int(10) NOT NULL,"
    "  `name` varchar(50) NOT NULL,"
    "  `mobile` varchar(20) NOT NULL,"
    "   `email` varchar(50) NOT NULL,  "
    "   `password` varchar(50) NOT NULL,"
    "   `OTP` int(10) NOT NULL,"
    "   `category_id` int(10) NOT NULL,"
    "   `Status` varchar(10) NOT NULL DEFAULT 'True`',"
    "   `DF_Super_Admin_id` int(11) NOT NULL"
    ") ENGINE=InnoDB ")

TABLES['DF_Command_Center'] = (
    "CREATE TABLE `DF_Command_Center` ("
    "  `id` int(10) NOT NULL,"
    "  `name` varchar(50) NOT NULL,"
    "  `mobile` varchar(20) NOT NULL,"
    "   `email` varchar(50) NOT NULL,  "
    "   `password` varchar(20) NOT NULL,"
    "   `OTP` int(10) NOT NULL,"
    "   `category_id` int(10) NOT NULL,"
    "   `Status` varchar(10) NOT NULL DEFAULT 'True`',"
    "   `DF_Super_Admin_id` int(11) NOT NULL,"
    "   `DF_Admin` int(11) NOT NULL,"
    "   `DF_Customer_Success` int(11) NOT NULL"
    ") ENGINE=InnoDB")

TABLES['DF_Customer_Success_Team'] = (
    "CREATE TABLE `DF_Customer_Success_Team` ("
    "  `id` int(10) NOT NULL,"
    "  `name` varchar(50) NOT NULL,"
    "  `mobile` varchar(20) NOT NULL,"
    "   `email` varchar(50) NOT NULL,  "
    "   `password` varchar(20) NOT NULL,"
    "   `OTP` int(10) NOT NULL,"
    "   `category_id` int(10) NOT NULL,"
    "   `Status` varchar(10) NOT NULL DEFAULT 'True`',"
    "   `DF_Super_Admin_id` int(11) NOT NULL,"
    "   `DF_Admin` int(11) NOT NULL"
    ") ENGINE=InnoDB")

TABLES['DF_Finance'] = (
    "CREATE TABLE `DF_Finanace` ("
    "  `id` int(10) NOT NULL,"
    "  `name` varchar(50) NOT NULL,"
    "  `mobile` varchar(20) NOT NULL,"
    "   `email` varchar(50) NOT NULL,  "
    "   `password` varchar(20) NOT NULL,"
    "   `OTP` int(10) NOT NULL,"
    "   `category_id` int(10) NOT NULL,"
    "   `Status` varchar(10) NOT NULL DEFAULT 'True`',"
    "   `DF_Super_Admin_id` int(11) NOT NULL,"
    "   `DF_Admin` int(11) NOT NULL,"
    "   `DF_Customer_Success` int(11) NOT NULL,"
    "   `DF_Command_Center` int(11) NOT NULL,"
    "   `Client` int(10) NOT NULL"
    ") ENGINE=InnoDB")

TABLES['DF_Super_Admin'] = (
    "CREATE TABLE `DF_Super_Admin` ("
    "  `id` int(10) NOT NULL,"
    "  `name` varchar(50) NOT NULL,"
    "  `mobile` varchar(20) NOT NULL,"
    "   `email` varchar(50) NOT NULL,  "
    "   `password` varchar(20) NOT NULL,"
    "   `OTP` int(10) NOT NULL,"
    "   `category_id` int(10) NOT NULL,"
    "   `Status` varchar(10) NOT NULL DEFAULT 'True`'"
    ") ENGINE=InnoDB")





# cursor.execute(add_salary)

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print(err)
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:

        print(err)
        exit(1)

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
cnx.close()
