from flask import Flask,request,jsonify
# import requests

app = Flask(__name__)
@app.route('/api/require_recommendation')
def output0():
    # print("hello world hahaha")
    return jsonify({'result': 'this is a recommendation'})

@app.route('/check')
def output1():
    return 'output1'

app.run()
