import boto3
from boto3.dynamodb.conditions import Key, Attr
from twilio.rest import TwilioRestClient
from datetime import datetime
import md5

class Logic:
	def __init__(self):
		self.log = []
		'''
		Initialize DynamoDB connection. 
		'''
		db = boto3.resource('dynamodb')

		self.doors = db.Table('hawkathonDoors')
		print(self.doors.creation_date_time)
		self.people = db.Table('hawkathonDoorsUsers')
		print(self.people.creation_date_time)

		self.requests = db.Table('hawkathonDoorsUsageLog')
		print(self.requests.creation_date_time)

		self.mqtt = boto3.client('iot-data')

		exec(open('./twilio.auth').read())
		sid = twilio['account_sid']
		sec = twilio['secret']
		self.twilio = TwilioRestClient(sid, sec)

		self.md5 = md5.new()

		self.getDoors()

	'''
	DB Operations. 
	'''

	def getDoor(self, doorName):
		key = {'doorName':doorName}
		response = self.doors.get_item(Key = key)
		if 'Item' in response:
			return response
		else:
			return None

	def addDoor(self, doorName, location, people):
		item = {'doorName': doorName, 'location': location, 'people': people}
		response = self.doors.put_item(Item = item)
		return response

	def removeDoor(self, doorName):
		key = {'doorName':doorName}
		response = self.doors.delete_item(Key = key)
		return response

	def getDoors(self):
		doors = self.doors.scan()['Items']
		doors = [door['doorName'] for door in doors]
		self.doorNames = doors
		return doors

	def validDoor(self, doorName):
		return doorName in self.doors

	def getPerson(self, phoneNumber):
		key = {'phoneNumber':phoneNumber}
		response = self.people.get_item(Key = key)
		if 'Item' in response:
			return reponse
		else:
			return None

	def getPeople(self):
		people = self.people.scan()['Items']
		return people

	def addPerson(self, phoneNumber, name, clearance):
		item = {'phoneNumber':phoneNumber, 'name': name, 'clearance': clearance}
		response = self.people.put_item(Item = item)
		return response

	def _removePerson(self, phoneNumber):
		key = {'phoneNumber': phoneNumber}
		response = self.people.delete_item(Key = key)
		return response

	def getPerson(self, phoneNumber):
		key = {'phoneNumber': phoneNumber}
		response = self.people.get_item(Key = key)
		return response

	def addPermission(self, doorName, phoneNumber):
		key = {'doorName': doorName}
		uExp = 'SET people = list_append(people, :val1)'
		expAttrVals = {':val1':[phoneNumber]}
		response = self.doors.update_item(Key = key, UpdateExpression=uExp, ExpressionAttributeValues=expAttrVals)
		return response

	def removePermission(self, doorName, phoneNumber):
		key = {'doorName': doorName}
		people = self.getDoor(doorName)['Item']['people']
		uExp = 'SET people = :val1'
		removal = [person for person in people if person != phoneNumber]
		expAttrVals = {':val1':removal}
		response = self.doors.update_item(Key = key, UpdateExpression = uExp, ExpressionAttributeValues = expAttrVals)
		return response

	def doorsByPerson(self, phoneNumber):
		response = self.doors.scan(FilterExpression=Attr('people').contains(phoneNumber))
		doors = [door['doorName'] for door in response['Items']]
		return doors

	def removePerson(self, phoneNumber):
		for door in self.doorsByPerson(phoneNumber):
			self.removePermission(door, phoneNumber)
		self._removePerson(phoneNumber)
		return self.doorsByPerson(phoneNumber)

	def auth(self, phoneNumber, doorName):
		door = self.getDoor(doorName)
		if door == None:
			return False
		elif phoneNumber in door['Item']['people']:
			return True
		else:
			return False

	def addLogEntry(self, doorName, phoneNumber, auth):
		timestamp = str(datetime.now())
		self.md5.update(doorName + phoneNumber + timestamp + str(auth))
		item = {'hash':str(self.md5.hexdigest()), 'timestamp':timestamp, 'doorName':doorName, 'phoneNumber':phoneNumber, 'auth':str(auth)}
		response = self.requests.put_item(Item = item)
		return response

	def getLog(self):
		response = self.requests.scan()['Items']
		return response

	def openDoor(self, phoneNumber, doorName):
		# add door logic here. 
		auth = self.auth(phoneNumber, doorName)
		msg = ''
		if doorName not in self.doorNames:
			msg = 'Invalid door %s. ' % (doorName)
		elif auth:
			msg = 'Opened door %s. ' % (doorName)
		else:
			msg = 'Number not authorized for door %s. ' % (doorName)
		self.addLogEntry(doorName, phoneNumber, auth)
		self.twilio.messages.create(to=phoneNumber, from_="+16262437676", body=msg)

		response = self.mqtt.publish(topic = doorName, payload = 'Open')

		print msg
		return msg

if __name__ == "__main__":
	l = Logic()
	DBTEST = False
	TTEST = False
	if DBTEST:
		print 'Testing DB methods:'
		print 'Get Doors:' + str(l.getDoors())
		print 'Door 308: ' + str(l.getDoor('308'))
		print 'Add Doors:'
		print 'Adding Door 307:' + str(l.addDoor('307', 'Third Floor central corridor. ', ['+13476337300', '+15085175880']))
		print 'Doors' + str(l.getDoors())
		print 'Remove Doors:'
		print 'Removing Door 307:'  + str(l.removeDoor('307'))
		print 'Doors' + str(l.getDoors())
		print 'addPerson' + str(l.addPerson('+13476337300', 'Thomas Hsu', '0'))
		print 'People: ' + str(l.getPeople())
		print 'Adding Many Doors'
		myPeople = ['+1' + `i` for i in range(4)]
		myDoors = ['40' + `i` for i in range(8)]
		for door in myDoors:
			l.addDoor(door, '4th floor eastern corridor', myPeople)
		for person in myPeople:
			l.addPerson(person, 'T', '5')

		print 'Doors' + str(l.getDoors())
		print 'People' + str(l.getPeople())
		print 'Door 404:' + str(l.getDoor('404'))
		print '+11\'s doors' + str(l.doorsByPerson('+11'))
		print 'Remove +11'
		l.removePerson('+11')
		print '+11\'s doors' + str(l.doorsByPerson('+11'))
		print 'Door 404:' + str(l.getDoor('404'))
		print 'Doors' + str(l.getDoors())
		print 'People' + str(l.getPeople())
		for door in myDoors:
			l.removeDoor(door)
		for person in myPeople:
			l._removePerson(person)
		print 'Doors' + str(l.getDoors())
		print 'People' + str(l.getPeople())
		print 'Done'
	if TTEST:
		print 'Open Door:' + l.openDoor('+13476337300', '308')
		print 'Wrong Door:' + l.openDoor('+13476337300', '307')
		print 'Wrong Number:' + l.openDoor('+15085175880', '308')

#print 
