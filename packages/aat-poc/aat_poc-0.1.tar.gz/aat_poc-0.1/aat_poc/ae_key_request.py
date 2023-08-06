import json
import requests
import sys
from ipaddress import ip_address

def main():
    # Check that station id and bali Ip address was provided
    if len(sys.argv) != 3:
        sys.exit("Usage: python3 ae_key_init.py StationId MacMiniIPAddress")

    # Validate and Test Bali Connection
    try:
        ip_address(sys.argv[2])
    except ValueError:
        sys.exit("Invalid IP address entered. Usage: python3 StationId BaliIPAddress")

    stationId = sys.argv[1]
    requestKeys = requests.post("http://{}:5000/requestKeyPair/{}".format(sys.argv[2],stationId), stream=True)
    keyResponse = json.loads(requestKeys.text)

    # Store Private and Public Keys in folder
    with open("{}_private.pem".format(stationId), "w+") as privKeyFile:
        privKeyFile.write(keyResponse['privatekey'])
    with open("{}_public.pem".format(stationId), "w+") as pubKeyFile:
        pubKeyFile.write(keyResponse['publickey'])
    if keyResponse['CServer_pubkey'] == 'None' or stationId == 'CredentialServer': # Check if no Credential Server Public Key returned
        print("Private and Public Keys for {} stored".format(stationId))
        return

    # Store Credential Server Public Key if exists
    with open("CredentialServer_public.pem", "w+") as pubKeyFile:
        pubKeyFile.write(keyResponse['CServer_pubkey'])
    
    print("Private and Public Keys for {} stored as well as Credential Server Public Key".format(stationId))

if __name__ == "__main__":
    main()