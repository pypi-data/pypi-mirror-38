import base64
import json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from datetime import datetime
from flask import Flask, request

'''
This script is meant to simulate an SFC (Shop Floor Control) Server
running at Chinese factories.

This Credential server will serve 3 purposes:
1. Accept setup requests to request public/private key pair from mac mini as well as all available station id's and public keys.
2. The credential database will keep a tally of employee badges, their names, companies, Access levels per station id. The access level should be per Floor and Station Type
3. Accept requests from sfc for badge access requests
4. Accept request for user access changes
5. Access requests for group user access changes
'''

credServer = Flask(__name__) # Define flask instance


# Define default url route which will handle all requests from Bali and the Vendor credential server
@credServer.route('/', methods = ['GET', 'POST'])
def relay():
    if request.method == 'POST':
        with open('CredentialServer_private.pem','r') as keyFile: # Load Server Private Key
            CS_privKey = keyFile.read()

        AE_request = json.loads(request.data)
        AE_publicKey = AE_request["message"]["AEpublickey"]
        logTransaction(json.dumps(AE_request), "incoming") # Log incoming request

        if verifyJson(AE_request, AE_publicKey): # Validate Signature
            decryptedNum = decryptString(AE_request["message"]["randomnumber"], CS_privKey) # Decrypt random number
            reEncryptedNum = encryptString(decryptedNum, AE_publicKey) # Re-Encrypt random number

            # Create Test Credential Server response
            CS_response = {
                "fingerprinthash" : "{}".format(AE_request["message"]["fingerprinthash"]),
                "employeename" : "John Doe",
                "stationid" : "{}".format(AE_request["message"]["stationid"]),
                "accesslevel" : 2,
                "randomnumber" : "{}".format(reEncryptedNum),
                "requesttimestamp" : "{}".format(AE_request["message"]["requesttimestamp"])
            }

            signedCS_response = signJson(CS_response, CS_privKey) # Generate signed Json
            logTransaction(json.dumps(signedCS_response), "outgoing") # Log outgoing response

            return json.dumps(signedCS_response)
        else:
            return json.dumps({"message": "Signature cannot be verififed"})
    else:
        return json.dumps('{"message":"Invalid Request"}')

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


def signJson(unsignedJson, privateKey):
    private_key = serialization.load_pem_private_key(
        str.encode(privateKey),
        password=None,
        backend=default_backend()) # Load Private Key

    sign = private_key.sign(
        str.encode(json.dumps(unsignedJson)),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    ) # Generate Signature

    encodedRawSign = base64.b64encode(sign) # Encode signature in readable format
    signature = bytes.decode(encodedRawSign) # Convert bytes to string

    signedJson = {
        "message" : unsignedJson,
        "signature" : signature
    }
    return signedJson
    

def encryptString(text, publicKey):
    public_key = serialization.load_pem_public_key(
        str.encode(publicKey),
        backend=default_backend()) # Load Public Key

    ciphertext = public_key.encrypt(
        str.encode(text),
        padding.OAEP(
           mgf=padding.MGF1(algorithm=hashes.SHA256()),
           algorithm=hashes.SHA256(),
           label=None
        )
    ) # Generate Encrpytion

    encodedString = base64.b64encode(ciphertext) # Encode encryption in readable format
    ciphertext = bytes.decode(encodedString) # Convert bytes to string
    return ciphertext


def decryptString(text, privateKey):
    private_key = serialization.load_pem_private_key(
        str.encode(privateKey),
        password=None,
        backend=default_backend()) # Load Private Key

    rawCipherText = base64.b64decode(str.encode(text)) # Decode from readable format
    
    decryption = private_key.decrypt(
            rawCipherText,
            padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    ) # Decrypt Text

    plaintext = bytes.decode(decryption) # Convert bytes to string
    return plaintext

def logTransaction(text, type):
    with open("CS.log", "a+") as CS_log:
        if type == "outgoing":
            CS_log.write("Outgoing message at {}\n".format(datetime.now()))
            CS_log.write(text + "\n")
        elif type == "incoming":
            CS_log.write("Incoming message at {}\n".format(datetime.now()))
            CS_log.write(text + "\n")