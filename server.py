from flask import Flask, jsonify, request, abort
app = Flask(__name__)

@app.route('/onText', methods='GET'):
def default():
	return 'Hello World', 200

@app.route('/onText', methods='POST')
def onText():
	if not request.json:
		return abort(500)
	else:
		print request.json
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


