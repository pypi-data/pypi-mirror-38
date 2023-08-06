import base64
import json
import os.path
import requests
import sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from datetime import datetime
from secrets import token_urlsafe

'''
This script is meant to Simulate an AE machine exchanging information with a standalone bali application 
on the same machine. 
It's purpose is to:
1. Send out encryption key requests to bali to generate private and public key pairs and retrieve public key for credential server
2. Send sfc_post requests for authentication to bali
3. Receive responses from bali and log requests and responses to a local excel sheet
'''

def main():
    # Check that station id & fingerprint Hash file were provided
    if len(sys.argv) != 3:
        sys.exit("Usage: python3 AE_Sim.py StationId FingerprintFile")

    stationId = sys.argv[1]
    fingerPrintFile =  sys.argv[2]

    if not os.path.isfile(fingerPrintFile): # Check that files exist
        sys.exit("FingerprintFile provided is invalid")
    elif not os.path.isfile("{}_private.pem".format(stationId)):
        sys.exit("Private Key File for Station '{}' does not exist".format(stationId))
    elif not os.path.isfile("{}_public.pem".format(stationId)):
        sys.exit("Public Key File for Station '{}' does not exist".format(stationId))
    elif not os.path.isfile("CredentialServer_public.pem"):
        sys.exit("Public Key File for Credential Server does not exist")

    # Open Key & FingerprintFiles
    with open('{}_public.pem'.format(stationId),'r') as keyFile:
        AE_pubKey = keyFile.read()
    with open('{}_private.pem'.format(stationId),'r') as keyFile:
        AE_privKey = keyFile.read()
    with open('CredentialServer_public.pem','r') as keyFile:
        CS_pubKey = keyFile.read()
    with open(fingerPrintFile,'r') as fpFile:
        fingerPrintHash = fpFile.read()
    
    # Create Test AE JSON
    randNumber = token_urlsafe() # Generate random number
    encRandNumber = encryptString(randNumber, CS_pubKey) # Enrypt random number

    AE_json = {
        "fingerprinthash" : "{}".format(fingerPrintHash),
        "stationid" : "{}".format(stationId),
        "requesttimestamp" : "{}".format(datetime.now()),
        "randomnumber" : "{}".format(encRandNumber),
        "AEpublickey" : "{}".format(AE_pubKey)
    } # Replace parts of public key that cause json transfer to fail.
    signedJson = signJson(AE_json, AE_privKey)
    logTransaction(json.dumps(signedJson), "outgoing") # Log outgoing request

    r = requests.post('http://localhost:5000/authenticate', json= signedJson, stream=True)
    jsonResponse = json.loads(r.text)
    logTransaction(r.text, "incoming") # Log incoming response
    verification = verifyJson(jsonResponse, CS_pubKey)
    decRandNumber = decryptString(jsonResponse["message"]["randomnumber"], AE_privKey)

    station = jsonResponse['message']['stationid'],
    employee = jsonResponse['message']['employeename'],
    accessLevel = jsonResponse['message']['accesslevel']
    responseTimestamp = jsonResponse['message']['requesttimestamp']

    if randNumber == decRandNumber and verification and AE_json['requesttimestamp'] == responseTimestamp:
        print("Random Number and Signature verified")
        print("Acess level {} granted to '{}' for Station '{}'".format(accessLevel, employee[0], station[0]))
    else:
        print('Verification failed')

def logTransaction(text, type):
    with open("AE.log", "a+") as AE_log:
        if type == "outgoing":
            AE_log.write("Outgoing message at {}\n".format(datetime.now()))
            AE_log.write(text + "\n")
        elif type == "incoming":
            AE_log.write("Incoming message at {}\n".format(datetime.now()))
            AE_log.write(text + "\n")

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

if __name__ == "__main__":
    main()