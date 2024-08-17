import bcrypt # type: ignore
import uuid
import jwt # type: ignore
from fastapi import HTTPException, APIRouter, Depends, Header # type: ignore
from models.user import User
from pydantic_schemas.user_create import UserCreate # type: ignore
from database import get_db
from sqlalchemy.orm import Session # type: ignore
from pydantic_schemas.user_login import UserLogin

router = APIRouter()

@router.post('/signup', status_code = 201)
def signup_user(user: UserCreate, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.email == user.email).first() 
    if user_db:
        raise HTTPException(400, 'User with the same email already exist!')
    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()) # type: ignore
    user_db = User(id = str(uuid.uuid4()), email = user.email, password = hashed_pw, name = user.name)
    db.add(user_db) 
    db.commit() 
    db.refresh(user_db) 
    return user_db

@router.post('/login')
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.email == user.email).first()
    if not user_db: 
        raise HTTPException(400, 'User with this email doesn\'t exist')
    is_match = bcrypt.checkpw(user.password.encode(), user_db.password)
    if not is_match:
        raise HTTPException(400, 'Incorrect password!')
    token = jwt.encode({'id': user_db.id}, 'password_key')
    return {'token': token, 'user': user_db}

@router.get('/')
def current_user_data(db: Session = Depends(get_db), x_auth_token = Header()):
    try:
        if not x_auth_token:
            raise HTTPException(401, 'No auth token, access denied!')
        verified_token = jwt.decode(x_auth_token, 'password_key', ['HS256'])
        if not verified_token:
            raise HTTPException(401, 'Token verification failed, authorization denied!')
        uid = verified_token.get('id')
        return uid
    except jwt.PyJWTError as e:
        raise HTTPException(401, 'Token isn\'t valid, authorization denied!') from e