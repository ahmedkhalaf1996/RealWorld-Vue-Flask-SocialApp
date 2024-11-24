import time 
from typing import Dict
import jwt 

JWT_SECRET = "BfFd7XxkMHVo5M59JB7K2kzwP4JoGeeMHqh93uznTRQ="
JWT_ALGORIITHM = "HS256"

def token_response(token: str):
    return {
        "access_token": token
    }

def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 86400
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORIITHM)
    return token_response(token)

def decodeJWT(token: str) -> dict:
    try:
      decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORIITHM])
      return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}