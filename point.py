from location import distance

class Point:
	def __init__(self, lat: float, lon: float):
		self.latitude = lat
		self.longitude = lon
		self.corona = False

	def gotCorona(self):
		self.corona = True

	# Equality is defined as both points being within 20 miles of each other
	def __eq__(self, other):
		return distance(
			self.latitude, self.longitude,
			other.latitude, other.longitude
		) <= 20

	def __str__(self):
		return f"({self.latitude}, {self.longitude})"

	def __repr__(self):
		return self.__str__()

	def __hash__(self):
		return hash((self.latitude, self.longitude, self.corona))
		