import random
from flask import Flask, jsonify, make_response

app = Flask(__name__)

def return_zuzu():
	zuzus = random.randint(1,10)
	times = random.randint(1,10)
	zuzu = "zu"*times
	for i in range(zuzus-1):
		times = random.randint(1,10)
		zuzu += " "+("zu"*times)
	return zuzu


@app.route("/")
def hello():
	rtrned = return_zuzu()
	return rtrned

@app.route("/api")
def api():
	api_return = {"zuzu_text":return_zuzu()}
	api_ret = make_response(jsonify(api_return), 200)
	return api_ret

def get_zuzus():
	app.run()

if __name__ == '__main__':
	get_zuzus()
