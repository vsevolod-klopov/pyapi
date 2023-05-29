# This file is responsible for signing , encoding , decoding and returning JWTS
import time
from typing import Dict
from sql_connector import connect
import jwt
import settings



def token_response(token: str, id: int):
    return {
        "access_token": token,
        "user_id":id
    }

# function used for signing the JWT string
def signJWT(user_id: str) -> Dict[str, str]:
    wowtoDB = connect()
    mycursor = wowtoDB.cursor()
    mycursor.execute(f"SELECT id FROM User WHERE Phone ={int(user_id)}")
    id = mycursor.fetchall()[0][0]
    payload = {
        "user_id": id,
        "expires": time.time() + settings.ACCESS_TOKEN_EXPIRE_SECONDS
    }
    token = jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)

    return token_response(token,id)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}


def GetIdJWT(token:str) -> int:
    return decodeJWT(token)["user_id"]
