from directory import directory
import sqlite3
import os
con = sqlite3.connect('../sqlite.db')
global cur
cur = con.cursor()

class connexionpage(directory):
	def __init__(self,title):
		pass
	def connexionform(self,path,title):
		self.code=""
		self.htmlcode=""
		self.url=""
		print("xonnexion form",path)
		#connexion form
		self.path=path
		self.create_table_users()
		self.title=title
		self.username=None
		print(os.getcwd(),path.replace(".",""),"connexionform.html")
		f=open(os.getcwd()+self.get_path().replace(".","")+"\\connexionform.html", "rb")
		fcontent=f.read()
		print(fcontent)
		self.css=""
		self.js=""
		self.body=fcontent.decode('utf-8') % ("","","")
		print("xonnexion form ok")
	def connexion(self,path,title,params):
		#connexion
		self.path=path
		self.code=""
		self.htmlcode=""
		self.url=""
		username=params['username'][0]
		password=params['password'][0]
		self.create_table_users()
		users=self.search_users((username,password))
		print(users)
		f=open(os.getcwd()+self.get_path().replace(".","")+"\\connexionform.html", "rb")
		fcontent=f.read()
		self.title=title
		self.css=""
		self.js=""
		if len(users) > 0:
			self.username=username
			self.redirect("/")
			self.file(301)
		else:
			self.username=False
			self.body=fcontent.decode('utf-8') % ("le nom d'utilisateur ou le mot de passe est incorrect",username,"")
	def create_user(self,values):
		sql=""" INSERT INTO users(username,password) VALUES(?,?);"""
		cur.execute(sql,values)
		con.commit()
	def search_users(self,values):
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
		print(sql)
		cur.execute(sql)
		con.commit()
	def getusername(self):
		return self.username 