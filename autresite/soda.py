from directory import directory
import os
import html
import sqlite3
db_file=r"D:\Profils\goudon.marie\Bureau\site\pythonsqlite1.db"
global conn
conn = sqlite3.connect(db_file)
global crsr
crsr=conn.cursor()
class deletesodaaction(directory):
	def __init__(self,title,query_components):
		id=query_components["id"][0]
		create_table_sql = """ select * from glasses where id = ?"""
		print(create_table_sql,id)
		crsr.execute(create_table_sql, (id,))
		print(crsr.fetchall())
		create_table_sql = """ delete from glasses where id = ?"""
		print(create_table_sql,id)
		crsr.execute(create_table_sql, (id,))
		conn.commit()
		self.htmlcode=""
		self.code=301
		self.url="/glass"
class sodapage(directory):
	def __init__(self,title,query_components):
		print(query_components,"query components")
		id=query_components["id"][0]
		self.title=title
		self.css=""
		self.code=200
		self.js=""

		create_table_sql = """ CREATE TABLE IF NOT EXISTS sodas(
                                        id integer PRIMARY KEY,
                                        name text,
					image varchar(300)
                                    ); """
		c = conn.cursor()
		c.execute(create_table_sql)
		conn.commit()
		sql = " INSERT  OR IGNORE INTO sodas (name,image) VALUES(?,?)"
		cur = conn.cursor()
		list=[("fanta","image"), ("floup","image")]
		if len(self.getglasses()) == 0:
			for values in list:
				cur.execute(sql, values)
				conn.commit()
		mystr=""
		j=open(os.getcwd()+"_glass.html").read()
		for glass in self.getglasses():
			print(glass[1])
			mystr+=j % (glass[1],)
		sql = " select * from glasses where id = ? "
		self.body=mystr
		print(self.body)
	def __init__(self,path,title,query_components):
		self.path=path
		print("mes sodas")
		id=query_components["id"][0]
		self.code=""
		self.title=title
		self.css=""
		self.js=""
		create_table_sql = """ CREATE TABLE IF NOT EXISTS sodas(
                                        id integer PRIMARY KEY,
                                        name text,
					image varchar(300)
                                    ); """
		c = conn.cursor()
		c.execute(create_table_sql)
		conn.commit()
		sql = " INSERT  OR IGNORE INTO sodas (name,image) VALUES(?,?)"
		cur = conn.cursor()
		list=[("fanta","image"), ("floup","image")]
		if len(self.getsodas()) == 0:
			for values in list:
				cur.execute(sql, values)
				conn.commit()
		mystr="<p>dans le verre il y  a des sodas :</p>"
		print(mystr)
		mypath=os.getcwd()+self.get_path().replace(".","")+"\_soda.html"
		print(mypath)
		j=open(mypath,"rb").read()
		for soda in self.getsodas():
			print(soda,j.decode('utf-8'))
			print(j.decode('utf-8') % (str(soda[0]),str(soda[1]),str(soda[0]),str(soda[1])))
			mystr += j.decode('utf-8') % (str(soda[0]),str(soda[1]),str(soda[0]),str(soda[1]))
			
		print(mystr)
		glass=self.getglass(id)[0]
		print(glass)
		myglasspath=self.get_file_from_directory()+"\_myglass.html"
		print(myglasspath)
		k=open(myglasspath,"rb").read().decode('utf-8')
		mystr+=k % (glass[1])
		escapes=["\\","\'","\n","\r","\t","\b","\f"]
		for escape in escapes:
			mystr = mystr.replace(escape,"\\"+escape)
		self.body=(mystr.strip())
		print(self.body)
		
	def getglass(self,id):
		crsr.execute("select * from glasses where id = ?",(id,))
		listglasses=crsr.fetchall()
		return listglasses
	def getglasses(self):
		crsr.execute("select * from glasses")
		listglasses=crsr.fetchall()
		return listglasses
	def getsodas(self):
		crsr.execute("select * from sodas")
		listglasses=crsr.fetchall()
		return listglasses
	def getmytitle(self):
		return this.title