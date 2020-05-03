from math import radians, cos, sin, asin, sqrt 

# Basically taken from Geeks4Geeks, I don't know the formula
def distance(lat1, lon1, lat2, lon2): 
    lon1 = radians(lon1) 
    lon2 = radians(lon2) 
    lat1 = radians(lat1) 
    lat2 = radians(lat2) 
       
    # Haversine formula  
    dlon = lon2 - lon1  
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  
    c = 2 * asin(sqrt(a))  
     
    # Radius of earth in kilometers. Use 3956 for miles 
    r = 6371
       
    # calculate the result 
    return c * r 

def getAllPoints():
	with open("coords.txt", 'r') as fin:
		contents = (s[:-1] for s in fin.readlines())
	points = (tuple(float(i) for i in j.split(' ')) for j in contents)
	return points

def getPointsWithin(lat1, lon1, radius=10):
	points = getAllPoints()
	return list(filter(
		lambda p: distance(lat1, lon1, *p) <= radius, 
		points
	))
