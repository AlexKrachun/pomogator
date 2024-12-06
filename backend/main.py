from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Annotated
from backend.auth import get_current_user, router
from backend.db_work import db_dependency




# fastapi
app = FastAPI()
app.include_router(router)


## Аутентификация


user_dependency = Annotated[dict, Depends(get_current_user)]

# auth testing begin
@app.get('/test_auth/')
async def get_my_id(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return {"answer": "great, db done", 'User': user.items()}


# auth testing end


@app.post('/logout')
async def post_logout():
    '''
    Фукнция для выхода из системы

    args: None
    

    return-values:
        - code = 200, answer = {'message': 'Успешный выход из системы'}
    '''
    pass



## Чаты
@app.get('/chats')
async def get_chats():
    '''
    Функция для получения списка чатов пользователя


    args: None
    

    return-values:
        - code = 200, answer =  [
                                    {
                                        'id': 'abc123',
                                        'title': 'Мой чат',
                                        'last_message': 'Последнее сообщение в чате',
                                        'updated_at': '2023-10-15T14:30:00Z'
                                    }
                                ]
        - code = 401, text = 'Необходима авторизация'

    '''
    pass


@app.post('/chats/')
async def post_chats():
    '''
    Функция для создания нового чата

    args:   {
                title': 'Новый чат'
            }
    

    return-values:
        - code = 201, answer =  {
                                    'id': 'abc123',
                                    'user_id': 'user123',
                                    'title': 'Мой чат',
                                    'created_at': '2023-10-15T14:00:00Z',
                                    'updated_at': '2023-10-15T14:30:00Z'
                                }
        - code = 401, text = 'Необходима авторизация'
    '''
    pass

@app.get('/chats/{chat_id}')
async def get_chat_details(chat_id: str):
    '''
    Фукния для получения данных чата - сообщения и технические данные

    args: chat_id: str
    

    return-values:
        - code = 200, answer =  {
                                    'id': 'abc123',
                                    'user_id': 'user123',
                                    'title': 'Мой чат',
                                    'created_at': '2023-10-15T14:00:00Z',
                                    'updated_at': '2023-10-15T14:30:00Z',
                                    'messages': [
                                        {
                                        'id': 'msg123',
                                        'chat_id': 'abc123',
                                        'sender': 'user',
                                        'content': 'Привет! Как дела?',
                                        'created_at': '2023-10-15T14:15:00Z'
                                        }
                                    ]
                                }
        - code = 401, text = 'Необходима авторизация'
        - code = 404, text = 'Чат не найден'
    '''
    pass

@app.delete('/chat/{chat_id}')
async def delete_chat_by_id(chat_id: str):
    '''
    Функция для удаления чата


    args: chat_id: str
    

    return-values:
        - code = 200, answer = 'Чат удален'
        - code = 401, text = 'Необходима авторизация'
        - code = 404, text = 'Чат не найден'
    '''
    pass


## Сообщения
@app.post('/chats/{chat_id}/messages')
async def post_message(chat_id: str):
    '''
    Фукнция для отправки сообщений в чат


    args: 
        - chat_id: str
        -   {
                'content': 'Привет! Как дела?'
            }
    

    return-values:
        - code = 202, answer = 'Сообщение принято для обработки'
        - code = 401, text = 'Необходима авторизация'
        - code = 404, text = 'Чат не найден'


    '''
    pass









'''
обсудить
 - зачем в @app.get('/chats') возвращаем last_message? - просто интересно

'''