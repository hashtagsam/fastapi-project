from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = 'd834701e4c741a20a6320dccc676ece945c7a3ec995dd6e2c6f1e3b0f2b033a1' # SECRET_KEY
ALGORITHM = 'HS256' # Algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Expiration time
oath2_scheme = OAuth2PasswordBearer('tokenUrl'='/login')

def create_access_token(data:dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_token

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM)
    
        id: str = payload.get('user_id')

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    
    except JWTError:
        raise credentials_exception

def get_current_user(token: str = Depends())

