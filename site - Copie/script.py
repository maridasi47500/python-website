from http.server import HTTPServer, BaseHTTPRequestHandler
import sqlite3

from sqlite3 import Error
from urllib.parse import unquote
from urllib.parse import urlparse, parse_qs
from urllib import parse
def cleanup(url):
    try:
        return unquote(url, errors='strict')
    except UnicodeDecodeError:
        return unquote(url, encoding='latin-1')
from urllib.parse import urlparse
def force_to_unicode(unicode_or_str):
	if isinstance(unicode_or_str, str):
		text = unicode_or_str
		decoded = False
	else:
		text = unicode_or_str.decode(encoding)
		decoded = True
	return text

def create_connection(db_file):
	""" create a database connection to a SQLite database """
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		print(sqlite3.version)
	except Error as e:
		print(e)
	return conn
def create_post(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO posts(title,content)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    #return cur.lastrowid
def delete_post(conn, project):

    sql = ''' DELETE from posts where id = ? '''
    cur = conn.cursor()
    cur.execute(sql, (project,))
    conn.commit()
    #return 
def update_post(conn, project):

    sql = ''' update posts 
set title=?,content=?
where id = ? '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    #return
def all_posts(page=0):

	sql = ''' select * from posts order by id desc limit 10 offset '''
	sql=sql + str(page)
	cur = conn.cursor()
	cur.execute(sql)
	return cur.fetchall()
def get_post(conn,id):

	sql = ''' select * from posts where id = ? '''
	cur = conn.cursor()
	cur.execute(sql,(id,))
	return cur.fetchall()[0]
def create_table(conn, create_table_sql):

	try:
		c = conn.cursor()
		c.execute(create_table_sql)
	except Error as e:
		print(e)
class web_server(BaseHTTPRequestHandler):
	def _set_response(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
	def do_GET(self):
		try:
			query = self.path.split("?")[1]
		except:
			query=""
		print(query)
		if query == "":
			query_components = params = {}
		else:
			query_components = params = dict(qc.split("=") for qc in query.split("&"))
		mesposts=""
		try:
			mypath1=mypath= self.path.split("?")[0].replace('/','')
			if self.path.split("?")[0] == '/':

				if conn is not None:
					# create projects table
					sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS posts (
                                        id integer PRIMARY KEY,
                                        title text,
                                        content text,
					image varchar(300)	
                                    ); """
					create_table(conn, sql_create_projects_table)

		
				else:
					print("Error! cannot create the database connection.")

				self.path = "D:\Profils\goudon.marie\Bureau\site\index.html"
				try:
					page=query_components["page"]
				except:
					page="0"
				if len(all_posts(page)) > 0:
					for post in all_posts(page):
						mesposts+="<div class=\"card\"><h1>%s</h1><p>%s</p><p><a href=\"/editerunpost?id=%s\">editer</a><form onsubmit=\"return confirm('êtes vous sûre de vouloir supprimer?');\" method=\"post\" action=\"/supprimerunpost\"><input type=\"hidden\" name=\"id\" value=\"%s\" \/><input type=\"submit\" name=\"envoyer\" value=\"supprimer\" \/></form></p></div>" % (post[1], post[2],post[0],post[0])
					mesposts+="<a href=\"/?page=%s\">page suivante</a>" % str(int(page) + 10)
				elif page=="0":
					mesposts+="aucun post pour l'instant"
				else:
					mesposts+="aucun post"
				if int(page) > 0:
					mesposts+="<a href=\"/?page=%s\">page précédente</a>" % str(int(page) - 10)
				file_to_open = open(self.path).read().replace("mespostsici",mesposts)
			elif self.path.split("?")[0] == '/editerunpost':
				print("editer un post")
				self.path = "D:\Profils\goudon.marie\Bureau\site\editpost.html"
				print(self.path,params)
				post=get_post(conn,params["id"])
				print(post)
				post_params=(post[0],str(post[1]),str(post[2]))
				print(post_params)
				file_to_open = open(self.path).read() % post_params
		
			elif mypath1.split(".")[-1] in ['css']:
				print(mypath1)
				self.path = "D:\Profils\goudon.marie\Bureau\site\%s" % mypath1 
				file_to_open = open(self.path).read()		
			self.send_response(200)
		except:
			file_to_open = "File not found"
			self.send_response(404)
		self.end_headers()
		self.wfile.write(bytes(file_to_open, 'utf-8'))
	def do_POST(self):
		content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
		post_data = self.rfile.read(content_length) # <--- Gets the data itself
		print("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
			str(self.path), str(self.headers), post_data.decode('utf-8'))
		#self._set_response()

		params = fields = parse.parse_qs(post_data.decode('utf-8'))
		#print(post_data, "query components")

		if self.path == "/ajouterunpost":
			print("gkfor")
			post=(cleanup(force_to_unicode(params["title"][0])),cleanup(force_to_unicode(params["content"][0])))
			create_post(conn,post)
		elif self.path == "/supprimerunpost":
			delete_post(conn,params["id"][0])
		elif self.path == "/modifierunpost":
			filename=""
			post=(cleanup(force_to_unicode(params["title"][0])),cleanup(force_to_unicode(params["content"][0])),params["id"][0])
			update_post(conn,post)
		#self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
		self.send_response(301)
		self.send_header('Location','/')
		self.end_headers()

conn=create_connection(r"D:\Profils\goudon.marie\Bureau\site\pythonsqlite.db")
httpd = HTTPServer(('localhost', 8080), web_server)
print("http://localhost:8080")
httpd.serve_forever()
