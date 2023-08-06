import collections
import requests
import urllib.parse
from scipy.interpolate import interp1d
import random

# Locations:
# [ ["pickup":pickup, "dropoff":dropoff, "time":time], ["pickup":pickup, "dropoff":dropoff, "time":time], ... ]

# Drivers:
# [ ["name":name, "loaciton":location], ["name":name, "loaciton":location], ... ]


key = ""
time_float = interp1d([0,60], [0,100])
float_time = interp1d([0, 100], [0,60])

class Driver(object):
	""" Stores info about a driver """
	def __init__(self, name: str, start_location: str):
		self.name = name
		self.location = start_location
		self.busy = False
		self.cooldown = 0 # up to 2
	
	def busy(self,value=None):
		if value == None:
			return self.busy
		self.busy = value

class Student(object):
	""" Stores data about a student """
	def __init__(self, pickup_location: str, dropoff_location: str, time_start: str):
		self.pickup = pickup_location
		self.dropoff = dropoff_location
		self.same_location = True if self.pickup == self.dropoff else False
		self.time = time_start
		self.uid = random.randint(0, 1000000) # Gives every student an id. Makes sure that students cant be equal

def parseLoactions(locations: list):
	for student in locations:
		yield Student(student["pickup"], student["dropoff"], student["time"])

def parseDrivers(drivers: list):
	for driver in drivers:
		yield Driver(driver["name"], driver["location"])

def getDistance(loc1, loc2):
	loc1 = urllib.parse.quote_plus(loc1.encode())
	loc2 = urllib.parse.quote_plus(loc2.encode())
	data = requests.get("https://maps.googleapis.com/maps/api/directions/json?origin="+ loc1 +"&destination="+ loc2 +"&key="+ str(key)).json()
	time = 0
	
	for leg in data["routes"][0]["legs"]:
		time += leg["duration"]["value"]
	
	return time

def timeToFloat(time:str) -> float:
	return float(str(time.split(":")[0]+ "." +str(float(time_float(time.split(":")[1]))).split(".")[0]))

def secondsToTime(seconds:int) -> str:
	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)
	return f"{h}:{m}"

def floatToTime(number:float) -> str:
	hours = str(number).split(".")[0]
	mins = str(float(float_time(str(number).split(".")[1]))).split(".")[0]
	raw_time =  f"{hours}:{mins}"
	if raw_time[len(raw_time) -  2] == ":":
		raw_time += "0"
	return raw_time
	
class Coordinator(object):
	""" Finds the best jobs for each driver """
	def __init__(self, locations: list, drivers: list):
		# Populate the arrays with objects
		self.students     = list(parseLoactions(locations))
		self.drivers      = list(parseDrivers(drivers))
		self.driver_count = len(drivers)
		
		# Convert "stringy" time to a number
		for student in self.students:
			student.time = timeToFloat(student.time)
		
	def assignDriver(self):
		job = self.students[0]
		
		closest_ticker, closest_name = 1000000, ""
		for driver in self.drivers:
			# Skip the driver if they are busy
			if driver.busy and driver.cooldown > 0.5: continue
			
			# Find the closest driver
			distance = getDistance(driver.location, job.pickup)
			
			# If a driver is in their "travel" period, and in range, allow them to do the job.
			if not driver.cooldown > timeToFloat(secondsToTime(distance)) and driver.busy: continue
			
			if distance < closest_ticker:
				closest_ticker = distance
				closest_name   = driver.name
		
		# Parse through drivers and set values
		for driver in self.drivers:
			if driver.name == closest_name:
				driver.busy = True
				driver.cooldown = 2.5 # Extra half-hour to allow travel times
				driver.location = job.dropoff
				driver.cooldown += 0.5 # Bugfix
				self.output[driver.name].append([job.pickup, floatToTime(job.time)])
				
				# Remove the student
				self.students.popleft()
				break

	
	def calculate(self) -> dict:
		self.output = {}
		# Fill output with drivers to schedule
		for driver in self.drivers:
			self.output[driver.name] = []
		
		# Sort students by priority
		self.students.sort(key=lambda x: x.time)
		self.students = collections.deque(self.students)
		
		hour = 0.0 # 0-24
		while hour <= 24.0:
			# Stop loop if we run out of students
			if len(self.students) == 0:
				break
			
			# Deal with students
			previous_student = None # Lock to prevent infinite loops
			while True: # Loop to allow multiple students to be picked up at once
				try:
					if self.students[0].time == float(hour) and self.students[0] != previous_student:
						previous_student = self.students[0]
						self.assignDriver()
					else:
						break
				except:
					break
			
			# Handle busy drivers
			for driver in self.drivers:
				if driver.busy:
					driver.cooldown -= 0.5
					driver.busy = False if driver.cooldown <= 0.0 else True
			
			print(hour)
			hour += 0.5
		
		# Add a list of appointments that can not be achived to the output
		self.output["failed"] = list(self.students)
		
		return self.output
	

if __name__ == "__main__":
	key = "AIzaSyCsISzpm12wluR-9Rj1VTIbGcr7HhPXtJM"
	locs = [{"pickup":"525 Dundas St, London, ON N6B 1W5", "dropoff":"450 Dundas St, London, ON N6B 3K3", "time":"12:00"},
	{"pickup":"525 Dundas St, London, ON N6B 1W5", "dropoff":"450 Dundas St, London, ON N6B 3K3", "time":"13:30"},
	{"pickup":"525 Dundas St, London, ON N6B 1W5", "dropoff":"450 Dundas St, London, ON N6B 3K3", "time":"12:00"},
	]
	driv = [{"name":"d1", "location":"600 Oxford St E, London, ON N5Y 3J1"},
	{"name":"d2", "location":"600 Oxford St E, London, ON N5Y 3J1"}]
	t = Coordinator(locs, driv)
	print(t.calculate())