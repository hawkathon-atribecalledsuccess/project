from flask import Flask, jsonify, request, abort
app = Flask(__name__)

latest_request = {}

@app.route('/', methods=['GET'])
def index():
	return jsonify(latest_request), 200

@app.route('/onText', methods = ['POST'])
def onText():
	if not request.json:
		return abort(500)
	else:
		latest_request = request.json
		return jsonify({'value':'success'}), 200



@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')


