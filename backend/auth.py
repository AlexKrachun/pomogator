import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from backend.models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
import os
from dotenv import load_dotenv
import uuid
from backend.db_work import db_dependency

load_dotenv()


router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)

JWT_HASHING_KEY = os.environ.get('JWT_HASHING_KEY')
JWT_HASHING_ALGORITHM = os.environ.get('JWT_HASHING_ALGORITHM')

JWT_TIMEDELTA = datetime.timedelta(minutes=120)


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')




class CreateUserRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str



# @router.post('/', status_code=status.HTTP_201_CREATED)
# async def create_user(db: db_dependency, 
#                       create_user_request: CreateUserRequest):
#     '''
#     в этой функции происходит обработка добавления нового пользователя в бд
#     '''
#     create_user_model = User(id=str(uuid.uuid4()),
#                             username=create_user_request.username,
#                             hashed_password=bcrypt_context.hash(create_user_request.password),
#                             )
    
#     db['users'] = db.get('users', []) + [create_user_model.model_dump()]
    
    
@router.post('/register', status_code=status.HTTP_201_CREATED)
async def post_register(db: db_dependency, create_user_request: CreateUserRequest):
    '''
    Функция для регистрации нового пользователя

    args: 
        `{
            'username': 'user123',
            'password': 'password123',
        }`
    

    return-values: \n
        - code = 201, answer = {'message': 'Успешная авторизация'} \n
        - code = 400, text = 'Некорректные данные'

    '''
    create_user_model = User(id=str(uuid.uuid4()),
                            username=create_user_request.username,
                            hashed_password=bcrypt_context.hash(create_user_request.password),
                            )
    
    db['users'] = db.get('users', []) + [create_user_model.model_dump()]
    
    token = await create_access_token(create_user_model.username,
                                      create_user_model.id,
                                      JWT_TIMEDELTA)
    

    print("зарегестрирован новый челик", {'access_token': token, 'token_type': 'bearer'})
    return {'access_token': token, 'token_type': 'bearer'}



@router.post('/login')
async def post_login():
    '''
    Функция для автроризации пользователя (предоставление прав на действия)

    args: 
        {
            'username': 'user123',
            'password': 'password123',
        }
    

    return-values:
        - code = 200, answer = {'message': 'Успешная авторизация'}
        - code = 401, text = 'Неверное имя пользователя или пароль'
    '''
    pass
    

@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
                                 db: db_dependency):
    print('great I am in the /token page')
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        print('The error came from here1')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='не верный логин или пароль 1')

    token = await create_access_token(user.username, user.id, JWT_TIMEDELTA)
    
    print("tttttttttttt", token)

    print({'access_token': token, 'token_type': 'bearer'})
    return {'access_token': token, 'token_type': 'bearer'}


async def authenticate_user(username: str, password: str, db):
    print('authenticating now')
    user_list = list(filter(lambda u: u['username'] == username, db['users']))
    if len(user_list) == 0:
        print('you False is returning1')
        return False
    
    user = User(**user_list[0])
    if not bcrypt_context.verify(password, user.hashed_password):
        print('you False is returning2')
        return False
    return user


async def create_access_token(username: str, user_id: str, expires_delta: datetime.timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.datetime.now() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, key=JWT_HASHING_KEY, algorithm=JWT_HASHING_ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    '''
    в этой функции я проверяю существует ли пользователь в бд
    и если все хорошо, возвращаю его днанные
    если он импостер, то ловит ошибку
    '''
    try:
        payload = jwt.decode(token, key=JWT_HASHING_KEY, algorithms=[JWT_HASHING_ALGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('id')
        
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='не верный логин или пароль2')
        return {'username': username, 'id': user_id}
    except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='не верный логин или пароль3')    



'''
К Федору
1. я сделал так, чтобы /register возвращал jwt, чтобы после регистрации не надо было логиниться
'''