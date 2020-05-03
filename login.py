import pickle
import shutil
import os
from typing import Dict, Set

from location_history import LocationHistory
from point import Point


USER_FILE = "users.pickle"

def getUsers() -> Dict[str, LocationHistory]:
	try:
		with open(USER_FILE, 'rb') as fin:
			users = pickle.load(fin)
	except FileNotFoundError:
		users = dict()
	return users

def updatePickle(users: Dict[str, LocationHistory]):
	try:
		shutil.copy(USER_FILE, '.' + USER_FILE)
		os.remove(USER_FILE)
	except FileNotFoundError:
		pass
	with open(USER_FILE, 'wb+') as fout:
		pickle.dump(users, fout)

def addUser(username: str, users: Dict[str, LocationHistory]) -> None:
	assert username not in users
	users.update({username: LocationHistory()})

def addLocation(username: str, 
		users: Dict[str, LocationHistory], 
		location: Point) -> None:
	assert username in users
	users[username].addLocation(location)

def markCorona(username: str, users: Dict[str, LocationHistory]) -> None:
	assert username in users
	users[username].gotCorona()

def getAllCorona(username: str, users: Dict[str, LocationHistory]) -> Set[Point]:
	points = set()
	userhist = users[username]
	for user, hist in users.items():
		if hist.hasCorona():
			points = points.union(hist.intersection(userhist))
	return points

def heatMapCorona(users: Dict[str, LocationHistory]) -> Set[Point]:
	points = set()
	for _, hist in users.items():
		if hist.hasCorona():
			points = points.union(hist.getLocations())
	return points

def pointSet2Str(points: Set[Point]) -> str:
	points = [str(p) for p in points]
	return '\n'.join(points)

clients = getUsers()
