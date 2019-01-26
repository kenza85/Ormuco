"""
By Jacob Shnaidman
shnaidmanj@gmail.com

This code requires:
- python 3.6.5
- pytz library (http://pytz.sourceforge.net/)

To run test cases: ./jacob_shnaidman_test.py
"""

# 
## Question A
#

"""This function accepts two tuples that represent line segments on the x axis and returns whether or not they intersect"""
def isIntersecting(line1, line2):
	x1, x2 = line1
	x3, x4 = line2

	# If smaller (left) end of line1 is after line2's left end, then the left end of line1
	# also has to come before the larger (right) end of line2
	if (x1 >= x3 and x1 <= x4):
		return True

	# Vice Versa
	if (x3 >= x1 and x3 <= x2):
		return True

	return False

# Test cases
print("## True ##")
print(isIntersecting((1,5),(2,6)))
print(isIntersecting((2,6),(1,5)))

print(isIntersecting((1,5),(3,4)))
print(isIntersecting((3,4),(1,5)))

print(isIntersecting((1,5),(2,6)))
print(isIntersecting((2,6),(1,5)))

print(isIntersecting((1,5),(0,7)))
print(isIntersecting((0,7),(1,5)))

print("## False ##")
print(isIntersecting((1,5),(6,7)))
print(isIntersecting((6,7),(1,5)))


print('---------------------------------------------------')

# 
## Question B
#

"""Compares version string and outputs which one is greater or if they are equal. Assumes 1.2 is of smaller version than 1.2.0"""
def compareVersions(str1,str2):
	if type(str1) != str or type(str2) != str:
		print("Inputs must both be strings")
		return

	# We split the string by periods into a list and iterate through each section
	ver1 = str1.split(".")
	ver2 = str2.split(".")

	# To reduce code duplication and to give code greater clarity, assign these variables
	if len(ver1) > len(ver2):
		shorter_ver = ver2
		shorter_ver_str = str2
		longer_ver = ver1
		longer_ver_str = str1
	else:
		# If they are equal, this is the default case and these assignments don't really matter.
		shorter_ver = ver1
		shorter_ver_str = str1
		longer_ver = ver2
		longer_ver_str = str2

	shorter_ver_len = len(shorter_ver)
	longer_ver_len = len(longer_ver)

	# Go through each index and if one is greater than the other, then we are done. 
	for idx in range(len(shorter_ver)):
		try:
			num1 = float(ver1[idx])
		except ValueError:
			print("Invalid version string given. \"%s\" must be a period delimited string of floats." %str1)
			return
		try:
			num2 = float(ver2[idx])
		except ValueError:
			print("Invalid version string given. \"%s\" must be a period delimited string of floats." %str2)
			return
		if (num1 > num2):
			print ("%s > %s" %(str1,str2))
			return
		if (num1 < num2):
			print ("%s > %s" %(str2,str1))
			return

	# Since we have iterated through the whole list and verified the input and they are all equal, it is safe to output that they are equal
	if longer_ver_len == shorter_ver_len:
		print("%s = %s" %(str1,str2))
	else:
		# We must verify the rest of the input before we output which is greater
		for num in longer_ver[shorter_ver_len:]:
			try:
				float(num)
			except ValueError:
				print("Invalid version string given. \"%s\" must be a period delimited string of floats." %longer_ver_str)
				return
		print("%s > %s" %(longer_ver_str,shorter_ver_str))


print("Test Cases:")
compareVersions("1.2.0", "1.2")
print("#####")
compareVersions("1.2.f", "1.2")
print("#####")
compareVersions("1.2", "1.2.")
print("#####")
compareVersions("1.2", "1.2.f")
print("#####")
compareVersions("1.2", "1.2")
print("#####")
compareVersions("1/0", "1.2f")
print("#####")
compareVersions("1.2", "DROP TABLE")
print("#####")
compareVersions(123, 5321)
print("#####")
compareVersions(None, "1.0")
print("#####")
compareVersions("0x123", "0x123")
print("#####")
compareVersions("1.1", "1.0.99999999")
print("#####")
compareVersions("1.000000000000001", "1")
print("#####")
compareVersions("1.0000000000000000000000000000000000000000000000000000001", "1.0.1")
print("#####")
compareVersions("2.3.4", "2.3.4")
print("#####")
compareVersions("2.3.4", "2.3")
print("#####")
compareVersions("2.3.0", "2.3")
print("#####")
compareVersions("0.3", "0")


# 
## Question C
#

import datetime
import pytz
"""
This class is a node in a doubly linked list. 
It stores a key, value pair and an expiry date in the form of a datetime object
"""
class Node:
	def __init__(self, key, value, expiryDate=None):
		self.key = key
		self.value = value
		self.expiryDate = expiryDate
		self.prev = None
		self.next = None

"""
This class implements an LRU cache by using a doubly linked list as a queue to keep track of the order of least recently used nodes.
The *put* operation adds a key value pair to the back of the queue as the most recently used item
The *get* operation removes the key value pair and inserts it at the back of the queue as the most recently used item, and returns the value
If the get operation does not find a key, it returns -1
The doubly linked list is wrapped in a dictionary to reduce the time complexity of the put and get operations to O(1) time complexity.

This isn't a distributed LRU, so work needs to be done to have this project.
    1 - Simplicity. Integration needs to be dead simple.  # The current implementation seems simple enough 1/1
    2 - Resilient to network failures or crashes. # It's not network aware at the moment and work needs to be done to meet this requirement. 0/1
    3 - Near real time replication of data across Geolocation. Writes need to be in real time. # The application doesn't yet implement file i/o 0/1
    4 - Data consistency across regions # The application is consistent in terms of expiry dates, but work needs to be done to do file replication 0/1
    5 - Locality of reference, data should almost always be available from the closest region # This isn't running as a service, so this is 0/1
    6 - Flexible Schema # The implementation doesn't use a database yet, but this can easily be integrated in later. 0/1
    7 - Cache can expire # The cache does expire 1/1

The purpose of this attempt was to write something scalable that can be worked on later to meet the requirements in the future. 


The nodes expire after a certain expiry date given as a string formatted as: "%Y-%m-%d %H:%M:%S"
A cron task should call removeExpiredNodes() on the cache every so often depending on the requirements of the cache. 

The LRU cache stores nodes up to a capacity (integer)
The timezone must be a string indicating the local timezone of where the cache is located. See http://pytz.sourceforge.net/
													Can use print(' '.join(pytz.country_timezones['ca'])) to find timezones for canada
is_dst specifies if there is day light savings.
"""
class GeoLRUCache:
	def __init__(self,capacity, localTimezone, is_dst):
		self.capacity = capacity
		self.dictionary = dict()
		self.localTimezone = pytz.timezone(localTimezone)
		self.is_dst = is_dst

		# The head of the queue is the front
		self.head = Node(0, 0)
		self.tail = Node(0,0)

		# The head of the queue is the front of the queue
		# The tail of the queue is the back of the queue
		# prev points towards tail
		# next points towards head
		self.head.prev = self.tail
		self.tail.next = self.head

	"""
	Returns a node given a key in O(1). If key is not found, it returns -1
	This puts the node with this key at the back of the queue
	"""
	def get(self,key):
		if key in self.dictionary:
			node = self.dictionary[key]

			# Remove before adding it back to the queue
			self._remove(node)

			# If it's past the expiry date, don't readd it, just return -1
			if (node.expiryDate):
				# always work in UTC to keep expiry dates consistent
				if (pytz.utc.localize(datetime.datetime.utcnow()) >= node.expiryDate):
					del self.dictionary[node.key] # remove it from the dictionary
					return -1

			# add to back of the queue
			self._add(node)
			return node.value
		return -1

	"""
	Adds a key value pair to the cache as a node at the back of the queue
	The expiryDateString is the expiry date in the format of "YYYY-m-D H:M:S" 
	"""
	def put(self, key, value, expiryDateString):
		# If it's in there already, remove it first so put operation will "refresh" the node and put it at the back of the queue
		if key in self.dictionary:
			self._remove(self.dictionary[key])

		naive = datetime.datetime.strptime(expiryDateString, "%Y-%m-%d %H:%M:%S") # Strip datetime without timezone info (naive)
		localTime = self.localTimezone.localize(naive, is_dst=self.is_dst) # convert to local timezone with specified daylight savings option
		expiryDate = localTime.astimezone(pytz.utc) # convert to UTC since all times are kept internally as UTC
		node = Node(key,value,expiryDate)
		self._add(node)
		self.dictionary[key] = node

		# if the dictionary is beyond capacity after adding a new node, remove the node at the top of the queue from the queue and dictionary
		if len(self.dictionary) > self.capacity:
			node = self.head.prev
			self._remove(node)
			del self.dictionary[node.key]

	"""
	This is a function that can run as a cron task to remove expired nodes in the cache
	"""
	def removeExpiredNodes(self):
		for key in self.dictionary:
			node = self.dictionary[key]

			# if past expiry date, remove it from queue and dictionary
			if (node.expiryDate):
				# Always work in UTC to keep times consistent. 
				if (pytz.utc.localize(datetime.datetime.utcnow()) >= node.expiryDate):
					self._remove(node)
					del self.dictionary[node.key] 

	"""
	remove a node from the doubly linked list
	"""
	def _remove(self, node):
		node.prev.next = node.next
		node.next.prev = node.prev

	"""
	add a node to the back of the doubly linked list
	"""
	def _add(self,node):
		node.prev = self.tail
		node.next = self.tail.next
		self.tail.next = node
		node.next.prev = node


cache = GeoLRUCache(3, "America/Toronto", True)

cache.put(1,1, "2019-01-26 11:43:59")
cache.put(2,2, "2019-01-26 11:38:00")
cache.put(3,3, "2019-01-26 11:38:00")
# cache.put(0,0, "2019-01-26 10:38:00")

node = cache.tail

for i in range(3):
	# node = node.next
	# print(node.value)
	print(cache.get(1))