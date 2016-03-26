from flask import Flask, jsonify, request, abort
import twilio.twiml
from logic import Logic

app = Flask(__name__)

state = Logic()

@app.route('/', methods=['GET'])
def index():
	return jsonify(state.getLog()), 200

@app.route('/onText', methods = ['POST'])
def onText():
	state.updateLog({'data': request.data, 'form': request.form, 'json': request.json})
	state.openDoor(request.form['From'], request.form['Body'])
	return str(twilio.twiml.Response()), 200

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')


