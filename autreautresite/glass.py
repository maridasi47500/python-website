from directory import directory
import os
import sqlite3
db_file=r"D:\Profils\goudon.marie\Bureau\site\pythonsqlite1.db"
conn = sqlite3.connect(db_file)
global crsr
crsr=conn.cursor()
class glasspage(directory):
	def __init__(self,title):
		self.title=title
		self.css=""
		self.js=""
		self.path=".\\"
		create_table_sql = """ CREATE TABLE IF NOT EXISTS glasses(
                                        id integer PRIMARY KEY,
                                        name text,
					image varchar(300)
                                    ); """
		c = conn.cursor()
		c.execute(create_table_sql)
		conn.commit()
		
		if len(self.getglasses()) == 0:
			sql = " INSERT  OR IGNORE INTO glasses (name,image) VALUES(?,?)"
			cur = conn.cursor()
			list=[("verre d'eau","image"), ("verre 25cl","image")]
			for values in list:
				cur.execute(sql, values)
				conn.commit()
		mystr=""
		j=open(os.getcwd()+"\_glass.html","rb").read()
		for glass in self.getglasses():
			print(glass[1])
			mystr+=j.decode('utf-8') % (glass[0],glass[1])
		self.body=mystr
		print(self.body)
	def __init__(self,path,title):
		self.path=path
		self.title=title
		self.css=""
		self.js=""
		
		create_table_sql = """ CREATE TABLE IF NOT EXISTS glasses(
                                        id integer PRIMARY KEY,
                                        name text,
					image varchar(300)
                                    ); """
		c = conn.cursor()
		c.execute(create_table_sql)
		conn.commit()
		
		if len(self.getglasses()) == 0:
			sql = " INSERT  OR IGNORE INTO glasses (name,image) VALUES(?,?)"
			cur = conn.cursor()
			list=[("verre d'eau","image"), ("verre 25cl","image")]
			for values in list:
				cur.execute(sql, values)
				conn.commit()
		mystr=""
		j=open(os.getcwd()+"\_glass.html","rb").read()
		for glass in self.getglasses():
			print(glass[1])
			mystr+=j.decode('utf-8') % (glass[0],glass[1])
		self.body=mystr
		print(self.body)
	def getglasses(self):
		crsr.execute("select * from glasses")
		listglasses=crsr.fetchall()
		return listglasses
	def getmytitle(self):
		return this.title