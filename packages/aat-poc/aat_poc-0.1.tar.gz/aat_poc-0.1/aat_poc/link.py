import base64
import json
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from datetime import datetime
from flask import Flask, request

'''
This script is meant to serve a new light server running on the mac Mini's which will
serve the following purposes:
1. To validate, log and  relay requests from the AE to SFC
2. To validate, log and relay responses from the SFC to the AE
3. To assist with inital Public and private key assigning to station id's
'''

link = Flask(__name__) # Define flask instance

# Define authentication procedure
@link.route('/authenticate', methods = ['GET', 'POST'])
def relay():
    if request.method == 'POST':
        jsonRequest = request.get_json()
        logTransaction(json.dumps(jsonRequest), "incoming")

        with open("keystore.json","r") as keyFile:
            readJson = json.loads(keyFile.read())
            CS_pubKey = readJson['CredentialServer']['publickey']

        if verifyJson(jsonRequest, jsonRequest['message']['AEpublickey']): # Validate json
            r = requests.post('http://localhost:4567', json = json.loads(request.data), stream=True) # send to SFC
            if verifyJson(json.loads(r.text), CS_pubKey):
                return r.text
            else:
                return json.dumps({ "message" : None })
        else:
            return json.dumps({ "message" : None })
    else:
        return json.dumps({ "message" : None })

@link.route('/requestKeyPair/<stationid>', methods = ['GET', 'POST'])
def setup(stationid):
    if request.method == 'POST':
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # Generate public key
        public_key = private_key.public_key()
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # Try to retrieve Credential Server Public Key
        try:
            with open("keystore.json","r") as keyFile:
                readJson = json.loads(keyFile.read())
                CS_pubKey = readJson['CredentialServer']['publickey']
        except:
            CS_pubKey = None

        keyJson = {
            "stationid" : "{}".format(stationid),
            "privatekey" : "{}".format(bytes.decode(private_pem)),
            "publickey" : "{}".format(bytes.decode(public_pem)),
            "CServer_pubkey" : "{}".format(CS_pubKey)
        }

        # Store Json on Mac Mini
        try:
            with open("keystore.json","r") as keyFile:
                readJson = json.loads(keyFile.read())
        except:
            readJson = {}
        with open("keystore.json", "w") as keyFile:
            readJson[stationid] = {
                                    "privatekey" : keyJson["privatekey"],
                                    "publickey"  : keyJson["publickey"]
            }
            json.dump(readJson, keyFile, sort_keys=True, indent=4)
        
        return json.dumps(keyJson)
    else:
        return None

def logTransaction(text, type):
    with open("link.log", "a+") as link_log:
        if type == "outgoing":
            link_log.write("Outgoing message at {}\n".format(datetime.now()))
            link_log.write(text + "\n")
        elif type == "incoming":
            link_log.write("Incoming message at {}\n".format(datetime.now()))
            link_log.write(text + "\n")

def verifyJson(signedJson, publicKey):
    public_key = serialization.load_pem_public_key(
        str.encode(publicKey),
        backend=default_backend()) # Load Public Key

    encodedSign = str.encode(signedJson['signature']) # Convert string to bytes
    signature = base64.b64decode(encodedSign) # Convert signature from readable format to binary
    try:
        public_key.verify(
            signature,
            str.encode(json.dumps(signedJson['message'])),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        ) # Verify signature, if signature is invalid, exception will be raised and function will return False
        return True
    except:
        return False