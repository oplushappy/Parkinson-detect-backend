import json
from fastapi import HTTPException, status
from jose import JWTError, jwt
from constant import SECRET_KEY, ALGORITHM
    # print(await get_current_user(jwt_token))

def decode_jwt(information):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # information = json.loads(information)
        jwt_token = information["access_token"]
        payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    return username

def form_change_to_json(information: str):
    information = json.loads(information)
    return information
