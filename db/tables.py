from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, func
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column


Base = declarative_base()

class User(Base):
    __tablename__ = 'table_users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer, nullable=True)
    
    # site_id = Column(Integer, nullable=True)
    # name = Column(String(250), nullable=True)
    # sub_status = Column(String(50), default='not subscribed', nullable=False)
    # token_has = Column(Integer, default=1000, nullable=False)
    
    last_used_model = Column(String(500), nullable=False)
    
    dalle_shape = Column(String(100), default='1024x1024', nullable=False)
    dalle_quality = Column(String(100), default='standard', nullable=False)  # 'standard'/'hd'    

    current_chat_id = Column(Integer, nullable=True)

    # Конец подписки
    sub_end: Mapped[DateTime] = mapped_column(DateTime)
    
    # Последний запрос
    last_request: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), nullable=False)


    chats = relationship(
        'Chat',
        back_populates='user',
        cascade='all',
        foreign_keys='Chat.user_id'
    )

    def __repr__(self):
        return f'<User: id = {self.id}>'
    
    
    
class Chat(Base):
    __tablename__ = 'table_chats'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), default='Пустой чат', nullable=False)
    time = Column(Integer, nullable=False)  # время в секундах для сортировки 

    user_id = Column(Integer, ForeignKey('table_users.id', ondelete='CASCADE'), nullable=False)
    user = relationship(
        'User',
        back_populates='chats',
        foreign_keys=[user_id]
    )
    
    messages = relationship('Message', back_populates='chat', cascade='all')


    def to_list_of_roled_messages(self):
        mes = sorted(self.messages.copy(), key=lambda x: x.time)
        return [m.to_dict() for m in mes]
            
    
    def __repr__(self):
        return f'<Chat: id = {self.id}, user_id = {self.user_id}>'
    
    
    
class Message(Base):
    __tablename__ = 'table_messages'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    author = Column(String(100), nullable=False)  # user или assistant
    time = Column(Integer, nullable=False)  # время в секундах для сортировки 
    
    author_name = Column(String(100), nullable=False)
    
    chat_id = Column(Integer, ForeignKey('table_chats.id', ondelete='CASCADE'), nullable=False)
    chat = relationship('Chat', back_populates='messages')
    
    
    def to_dict(self):
        return {'role': self.author, 'content': self.text}
    
    def __repr__(self):
        return f'<Message: id = {self.id}, author = {self.author}, chat_id = {self.chat_id}, text = {self.text[:min(30, len(self.text))]}>'
    
    

class Candy(Base):
    __tablename__ = 'table_candy'

    # tg_id
    id = Column(Integer, primary_key=True)

    # Сколько фантиков пользователь получает каждый день
    daily_candy: Mapped[int] = mapped_column(default=0, nullable=False)

    # Сколько ежедневных фантиков осталось
    daily_candy_left: Mapped[int] = mapped_column(default=0, nullable=False)
    
    # Кол-во платных фантиков
    paid_candy_left: Mapped[int] = mapped_column(default=0, nullable=False)
