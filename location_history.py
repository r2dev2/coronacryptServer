from point import Point

# ==================================================
# class LocationHistory
# 
# attributes:
# 	locations: set containing all of the location points
# 	corona: boolean containing whether the person got corona
#
# methods:
# 	getLocations - returns location set
#	hasCorona - returns whether the user got corona
#	addLocation - takes in a point and adds it
# 	gotCorona - marks the location history as having corona
# 	intersection - returns all points in the set which have been within 20 miles of each other
# ==================================================

class LocationHistory:
	def __init__(self):
		self.locations = set()
		self.corona = False

	def getLocations(self):
		return self.locations

	def gotCorona(self):
		self.corona = True
		for loc in self.locations:
			loc.gotCorona()

	def hasCorona(self):
		return self.corona

	def addLocation(self, location: Point):
		location.gotCorona()
		self.locations.add(location)

	def intersection(self, other):
		intersection = set()
		for point in self.locations:
			if any([point == p for p in other.getLocations()]):
				intersection.add(point)
		return intersection
