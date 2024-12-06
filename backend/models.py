from pydantic import BaseModel



class User(BaseModel):
    id: str
    username: str
    hashed_password: str


class Message(BaseModel):
    id: str  # id сообщения в базе данных
    chat_id: str  # id чата в базе данных
    sender: str  # 'user' или 'gpt'
    content: str  # текст сообщения
    created_at: str  # '2023-10-15T14:15:00Z'


class Chat(BaseModel):
    id: str  # id чата в базе данных
    user_id: str  # id пользователя в базе данных
    title: str  # название чата - для списка чатов
    created_at: str  # '2023-10-15T14:00:00Z'
    updated_at: str  # '2023-10-15T14:30:00Z'
    messages: list[Message]
