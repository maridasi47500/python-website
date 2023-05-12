import directory
import os
class premierepage(directory.directory):
	def __init__(self,path,params,title,username):
		self.title=title
		self.path=path
		filename="index.html"
		j=open((os.getcwd()+"\\"+filename),"rb")
		filename="navconnexion.html"
		k=open((os.getcwd()+"\\connexion\\"+filename),"rb")
		kcontent=k.read()
		self.path=""
		self.css=""
		self.js=""
		connected=""
		print(username, "username")
		if username:
			print(kcontent.decode("utf-8"),str(username))
			print(kcontent.decode("utf-8") % str(username))
			l=open((os.getcwd()+"\\connexion\\liensdeconnexion.html"),"rb")
			connected += kcontent.decode("utf-8") % str(username)
			connected+=l.read().decode('utf-8')
		else:
			print(kcontent.decode("utf-8"),str("étranger(ère)"),len(("étranger(ère)",)))
			print(kcontent.decode("utf-8") % "étranger(ère)")
			l=open((os.getcwd()+"\\connexion\\liensconnexion.html"),"rb")
			connected += kcontent.decode("utf-8") % str("étranger(ère)")
			connected+=l.read().decode('utf-8')
		self.body=connected
		self.code=""
		self.htmlcode=""
		self.url=""
		self.htmlcode=""
		print("page  1 ok")
	def getmytitle(self):
		return this.title