from flask import Flask, request
import json
import requests

'''
This script is meant to simulate an SFC (Shop Floor Control) Server
running at Chinese factories.

This SFC server will serve 3 purpose:
1. To relay information from the Mac Mini to the Vendor Credential Server
2. To relay information from the Vendor Credential Server to the Mac Mini
'''
sfc = Flask(__name__) # Define flask instance

# Define default url route which will handle all requests from Bali and the Vendor credential server
@sfc.route('/', methods = ['GET', 'POST'])
def relay():
    if request.method == 'POST':
        r = requests.post('http://localhost:4568', json = json.loads(request.data), stream=True)
        return r.text
    else:
        return json.dumps('{"message":"Invalid Request"}')