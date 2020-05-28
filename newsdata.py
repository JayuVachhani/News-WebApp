import sqlite3

mydb = sqlite3.connect("news.db")
print("database created successfully")

mydb.execute("create table users(id INTEGER PRIMARY KEY AUTOINCREMENT, username varchar(25), email varchar(45), password varchar(15))")
mydb.execute("create table news(id INTEGER PRIMARY KEY AUTOINCREMENT,headlines varchar(150), description varchar(300), author varchar(50), category varchar(30))")
mydb.execute("create table contact(id INTEGER PRIMARY KEY AUTOINCREMENT,name varchar(30), email varchar(30), heading varchar(30), subject varchar(100) )")
print("Table created successfully")
