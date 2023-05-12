from directory import directory
import os
import html
import sqlite3
db_file=r"D:\Profils\goudon.marie\Bureau\site\pythonsqlite1.db"
global conn
conn = sqlite3.connect(db_file)
global crsr
crsr=conn.cursor()
class infouserpage(directory):
	def __init__(self,path,title,query_components):
		self.path=path
		print("mes infos")
		id=query_components["username"][0]
		self.code=""
		self.title=title
		self.css=""
		self.js=""
		create_table_sql = """ select * from users where username = ? """
		c = conn.cursor()
		c.execute(create_table_sql,(id,))
		conn.commit()
		user=c.fetchall()[0]
		form=open(os.getwd()+"\user\form.html","rb")
		if user:
			
		mystr="<p>dans le verre il y  a des sodas :</p>"

		escapes=["\\","\'","\n","\r","\t","\b","\f"]
		for escape in escapes:
			mystr = mystr.replace(escape,"\\"+escape)
		self.body=(mystr.strip())
		print(self.body)
		
