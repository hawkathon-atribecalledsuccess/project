#import boto3
from twilio.rest import TwilioRestClient
class Logic:
	def __init__(self):
		self.log = []
		exec(open('./twilio.auth').read())
		sid = twilio['account_sid']
		sec = twilio['secret']
		self.twilio = TwilioRestClient(sid, sec)

	def openDoor(self, phone_number, doorName):
		# add door logic here. 
		msg = 'Opened door %s. ' % (doorName)
		self.twilio.messages.create(to=phone_number, from_="+16262437676", body=msg)
		print msg

	def updateLog(self, log_entry):
		self.log.append(log_entry)

	def getLog(self):
		return log
'''
s = logic()
s.open('+13476337300', 'a')
'''