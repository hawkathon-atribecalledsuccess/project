from flask import Flask, jsonify, request, abort
import twilio.twiml

app = Flask(__name__)

class logic:
	def __init__(self):
		self.lr = {}

	def update(self, n):
		self.lr = {'data':n}

	def get(self):
		return self.lr

state = logic()

@app.route('/', methods=['GET'])
def index():
	return jsonify(state.get()), 200

@app.route('/onText', methods = ['POST'])
def onText():
	state.update({'data': request.data, 'form': request.form, 'json': request.json})
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


