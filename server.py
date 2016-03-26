from flask import Flask, jsonify, request, abort
import twilio.twiml
from logic import Logic

app = Flask(__name__)

state = Logic()

@app.route('/api/onText', methods = ['POST'])
def onText():
	#state.updateLog({'data': request.data, 'form': request.form, 'json': request.json})
	state.openDoor(request.form['From'], request.form['Body'])
	return str(twilio.twiml.Response()), 200

@app.route('/api/addDoor', methods = ['POST'])
def addDoor():
	if not request.json:
		return jsonify({'error':'Body must be in JSON format. '}), 500
	elif not 'doorName' in request.json:
		return jsonify({'error':'No element doorName. '}), 500
	else:
		doorName = request.json['doorName']
		location = request.json['location'] if 'location' in request.json else ''
		people = request.json['people'] if 'people' in request.json else []
		response = state.addDoor(doorName = doorName, location = location, people = people)
		return jsonify({'response': response}), 200

@app.route('/api/getDoors', methods = ['POST'])
def getDoors():
	response = state.getDoors()
	return jsonify({'response': response}), 200

@app.route('/api/getDoor', methods = ['POST'])
def getDoor():
	if not request.json:
		return jsonify({'error':'Body must be in JSON format. '}), 500
	elif not 'doorName' in request.json:
		return jsonify({'error':'No element doorName. '}), 500
	else:
		doorName = request.json['doorName']
		response = state.getDoor(doorName = doorName)
		return jsonify({'response': response}), 200

@app.route('/api/removeDoor', methods = ['DELETE'])
def removeDoor():
	if not request.json:
		return jsonify({'error':'Body must be in JSON format. '}), 500
	elif not 'doorName' in request.json:
		return jsonify({'error':'No element doorName. '}), 500
	else:
		doorName = request.json['doorName']
		response = state.removeDoor(doorName = doorName)
		return jsonify({'response': response}), 200

@app.route('/api/addPerson', methods = ['POST'])
def addPerson():
	if not request.json:
		return jsonify({'error':'Body must be in JSON format. '}), 500
	elif not 'phoneNumber' in request.json:
		return jsonify({'error':'No element phoneNumber. '}), 500
	else:
		phoneNumber = request.json['phoneNumber']
		name = request.json['name']
		clearance = request.json['clearance']
		response = state.addPerson(phoneNumber = phoneNumber, name = name, clearance = clearance)
		return jsonify({'response': response}), 200

@app.route('/api/removePerson', methods = ['DELETE'])
def removePerson():
	if not request.json:
		return jsonify({'error':'Body must be in JSON format. '}), 500
	elif not 'phoneNumber' in request.json:
		return jsonify({'error':'No element phoneNumber. '}), 500
	else:
		phoneNumber = request.json['phoneNumber']
		response = state.removePerson(phoneNumber = phoneNumber)
		return jsonify({'response': response}), 200

@app.route('/api/getPerson', methods = ['POST'])
def getPerson():
	if not request.json:
		return jsonify({'error':'Body must be in JSON format. '}), 500
	elif not 'phoneNumber' in request.json:
		return jsonify({'error':'No element phoneNumber. '}), 500
	else:
		phoneNumber = request.json['phoneNumber']
		response = state.getPerson(phoneNumber = phoneNumber)
		return jsonify({'response': response}), 200

@app.route('/api/doorsByPerson', methods = ['POST'])
def doorsByPerson():
	if not request.json:
		return jsonify({'error':'Body must be in JSON format. '}), 500
	elif not 'phoneNumber' in request.json:
		return jsonify({'error':'No element phoneNumber. '}), 500
	else:
		phoneNumber = request.json['phoneNumber']
		response = state.doorsByPerson(phoneNumber = phoneNumber)
		return jsonify({'response': response}), 200

@app.route('/api/addPermission', methods = ['POST'])
def addPermission():
	if not request.json:
		return jsonify({'error':'Body must be in JSON format. '}), 500
	elif not 'phoneNumber' in request.json or not 'doorName' in request.json:
		return jsonify({'error':'No element phoneNumber or doorName. '}), 500
	else:
		phoneNumber = request.json['phoneNumber']
		doorName = request.json['doorName']
		response = state.addPermission(phoneNumber = phoneNumber, doorName = doorName)
		return jsonify({'response': response}), 200

@app.route('/api/removePermission', methods = ['POST'])
def removePermission():
	if not request.json:
		return jsonify({'error':'Body must be in JSON format. '}), 500
	elif not 'phoneNumber' in request.json or not 'doorName' in request.json:
		return jsonify({'error':'No element phoneNumber or doorName. '}), 500
	else:
		phoneNumber = request.json['phoneNumber']
		doorName = request.json['doorName']
		response = state.removePermission(phoneNumber = phoneNumber, doorName = doorName)
		return jsonify({'response': response}), 200

@app.route('/api/getPeople', methods = ['POST'])
def getPeople():
	response = state.getPeople()
	return jsonify({'response': response}), 200

@app.route('/api/getLog', methods = ['POST'])
def getLog():
	response = state.getLog()
	return jsonify({'response':response}), 200

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')


