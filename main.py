
from http.server import HTTPServer, BaseHTTPRequestHandler

from io import BytesIO


import login
from point import Point


# ==================================================
# Class: HTTPRequestHandler
# OPTIONS - Everything is allowed
# 
# GET - 
#	{"Username": username} - returns all the coordinates of the location history of people who have got corona who were at one point within 20 miles of username
#	{"Purpose": "heatMap"} - returns all the coordinates of locations people with corona have been to
# 
# POST -
#	{"Purpose": "sendCoords", "Username": username, "Coords": "latitude longitude"} - updates the system with the new coordinates of username
#	{"Purpose": "login", "Username": username} - updates the system with the username, sends back "Created new user" or "User exists"
#	{"Purpose": "gotCorona", "Username": username} - tells the system that the user got corona
# ====================================================
class HTTPRequestHandler(BaseHTTPRequestHandler):

	def do_OPTIONS(self):           
		self.send_response(200, "ok")       
		self.send_header('Access-Control-Allow-Origin', '*')
		self.send_header('Access-Control-Allow-Methods', '*')
		self.send_header("Access-Control-Allow-Headers", '*')  
		self.end_headers()

	def do_GET(self):
		self.send_response(200)
		# self.end_headers()
		if "Username" in self.headers:
			# Send all the points of close people with corona
			closePoints = login.getAllCorona(
				self.headers["Username"],
				login.clients
			)
			body = login.pointSet2Str(closePoints)
			print(body)
		elif "Purpose" in self.headers and \
		self.headers["Purpose"] == "heatMap":
			allPoints = login.heatMapCorona(login.clients)
			body = login.pointSet2Str(allPoints)
		else:
			# Just send index.html to anything else
			print(self.headers)
			with open("index.html", 'r') as fin:
				body = '\n'.join(fin.readlines())
		self.send_header("Access-Control-Allow-Origin", "*")
		self.send_header('Access-Control-Allow-Methods', '*')
		self.send_header("Access-Control-Allow-Headers", '*')  
		self.end_headers()
		self.wfile.write(body.encode())

	def do_POST(self):
		response = BytesIO()
		content_length = int(self.headers['Content-Length'])
		body = self.rfile.read(content_length)
		print(body, type(body))
		purpose = self.headers["Purpose"]
		if purpose == "sendCoords":
			try:
				coords = tuple(float(i) for i in self.headers["Coords"].split(' '))
				p = Point(*coords)
				login.clients[self.headers["Username"]].addLocation(p)
				login.updatePickle(login.clients)
			except ValueError:
				print("Go away with your bad formatting")
		elif purpose == "login":
			# Create username or say that username exists
			uname = self.headers["Username"]
			try:
				login.addUser(uname, login.clients)
				login.updatePickle(login.clients)
				response.write(b"Created new user")
			except AssertionError:
				response.write(b"User exists")
		elif purpose == "gotCorona":
			# Updates the Username to have had corona in the system
			login.clients[self.headers["Username"]].gotCorona()
			login.updatePickle(login.clients)
		print("Headers:", self.headers)
		self.send_response(200)
		self.send_header("Access-Control-Allow-Origin", "*")
		self.end_headers()
		self.wfile.write(response.getvalue())


# TODO Switch to socketserver.TCPServer, it should be more secure
print("Declaring HTTPServer", flush=True)
httpd = HTTPServer(('0.0.0.0', 3000), HTTPRequestHandler)
print("Starting")
httpd.serve_forever()
