from directory import directory
import sqlite3
con = sqlite3.connect('../sqlite.db')
global cur
cur = con.cursor()

class inscriptionpage(directory):
	def __init__(self,title):
		self.title=title
		pass
	def inscriptionform(self,path,title):
		#inscription form
		print("inscription form")
		self.url=""
		self.code=""
		self.htmlcode=""
		self.path=path
		self.create_table_users()
		self.title=title
		self.username=None
		f=open(self.get_file_from_directory()+"\inscriptionform.html", "rb")
		fcontent=f.read()
		self.css=""
		self.js=""
		self.body=fcontent.decode('utf-8') % ("","","")
		print("inscription form ok")
	def inscription(self,path,title,params):
		print("inscription form")
		#inscription
		self.path=path
		self.code=""
		self.htmlcode=""
		self.url=""
		username=params['username'][0]
		password=params['password'][0]
		print((username,password))
		self.create_table_users()
		users=self.search_user_email((username,))
		self.title=title
		print(title)
		f=open(self.get_file_from_directory()+"\inscriptionform.html", "rb")
		fcontent=f.read()
		if len(users) == 0:
			self.create_user((username,password))
			self.username=params["username"][0]
			self.redirect("/")
			self.file(301)
		else:
			self.username=False

			self.body=fcontent.decode('utf-8') % ("cet email ou pseudo existe déjà","","")
		self.title=""
		self.css=""
		self.js=""
		print("inscription form ok")
	def create_user(self,values):
		sql=""" INSERT INTO users(username,password) VALUES(?,?);"""
		cur.execute(sql,values)
		con.commit()
	def search_user(self,values):
		sql=""" select * from users where username = ? and password = ?"""
		cur.execute(sql,values)
		con.commit()
		return cur.fetchall()
	def search_user_email(self,values):
		sql=""" select * from users where username = ?"""
		cur.execute(sql,values)
		con.commit()
		return cur.fetchall()
	def create_table_users(self):
		sql=""" create table if not exists users (
		id integer PRIMARY KEY,
		username varchar(300) NOT NULL,
		password varchar(300) NOT NULL
		)"""
		cur.execute(sql)
		con.commit()
	def getusername(self):
		return self.username 