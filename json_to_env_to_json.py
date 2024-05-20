import json
import base64
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

def encodeJSON(service_account_dict):
    #convert json to string
    service_account_string = json.dumps(service_account_dict)
    # print(service_account_string)

    #encode service account string
    encoded_service_account= base64.b64encode(service_account_string.encode("utf-8"))
    # print(encoded_service_account)




def decodeENV():
    #Now get the value of encoded service account that was copied and created in the .env, get it back and convert the encoded string back to JSON
    encoded_key= os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")

    # remove the first two chars and the last char in the key
    encoded_key_trimmed= str(encoded_key)[2:-1]

    #decode
    decode_encoded_key= base64.b64decode(encoded_key_trimmed).decode('utf-8')

    original_service_account= json.loads(decode_encoded_key)
    # print(original_service_account['private_key'])
    
    return original_service_account
