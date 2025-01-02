from sqlalchemy import Column, Integer, String, ForeignKey, asc, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import logging
import time


logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


Base = declarative_base()

class User(Base):
    __tablename__ = 'table_users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer, nullable=True)
    site_id = Column(Integer, nullable=True)
    name = Column(String(250), nullable=True)
    sub_status = Column(String(50), default='not subscribed', nullable=False)
    token_has = Column(Integer, default=1000, nullable=False)
    last_used_model = Column(String(500), nullable=False)
    

    current_chat_id = Column(Integer, nullable=True)

    chats = relationship(
        'Chat',
        back_populates='user',
        cascade='all',
        foreign_keys='Chat.user_id'
    )

    def __repr__(self):
        return f'<User: id = {self.id}, name = {self.name}, sub_status = {self.sub_status}, token_has = {self.token_has}>'
    
    
    
    
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
    
    chat_id = Column(Integer, ForeignKey('table_chats.id', ondelete='CASCADE'), nullable=False)
    chat = relationship('Chat', back_populates='messages')
    
    
    def to_dict(self):
        return {'role': self.author, 'content': self.text}
    
    def __repr__(self):
        return f'<Message: id = {self.id}, author = {self.author}, chat_id = {self.chat_id}, text = {self.text[:min(30, len(self.text))]}>'
    
    


# from functools import wraps

# def auto_session(func):
#     @wraps(func)
#     def wrapper(self, *args, **kwargs):
#         with self._get_session() as session:
#             return func(self, session, *args, **kwargs)
#     return wrapper


class WorkWithDB:
    def __init__(self, db_path='sqlite:///db/orm.db'):
        self.engine = create_engine(db_path)
        self.Session = sessionmaker(bind=self.engine)
        
        # Создание таблиц
        Base.metadata.create_all(self.engine)
    
    def _get_session(self):
        return self.Session()
    
    
    def user_is_new_by_tg_id(self, tg_id):
        '''нет пользователя с таким tg_id'''
        with self._get_session() as session:
            user = session.query(User).filter(User.tg_id == tg_id).first()
            return not bool(user)

    
    # def user_has_no_contexts_by_tg_id(self, tg_id):
    #     with self._get_session() as session:
    #         user = session.query(User).filter(User.tg_id == tg_id).first()
    #         print('u' * 100, user.chats)
    #         return len(user.chats) == 0
    
    
    def user_has_empty_curr_context_by_tg_id(self, us_id):
        with self._get_session() as session:
            curr_context_id = session.query(User).filter(User.tg_id == us_id).first().current_chat_id
            user_curr_context_messages = session.query(Chat).filter(Chat.id == curr_context_id).first().messages
            return len(user_curr_context_messages) == 0
    
    def add_message(self, chat_id, role, text):
        with self._get_session() as session:
            try:
                msg = Message(
                    text=text,
                    author=role,
                    time=int(time.time()),
                    chat_id=chat_id,
                )
                session.add(msg)
                session.commit()
                logging.info(f'Message {msg} added successfully.')
            except Exception as e:
                session.rollback()
                logging.error(f'Error adding message: {e}')
    
    def get_user_by_tg_id(self, tg_id):
        with self._get_session() as session:
            return session.query(User).filter_by(tg_id=tg_id).first()
    
    
    def set_current_context_by_tg_id(self, tg_id, context_id):
        with self._get_session() as session:
            user = session.query(User).filter(User.tg_id == tg_id).first()
            
            try:
                user.current_chat_id = context_id
                session.commit()
                logging.info(f'User current_chat_id changed successfully to {context_id}')
            except Exception as e:
                session.rollback()
                logging.error(f'Error User current_chat_id changin to {context_id}, {e}')
            
            

    def get_current_context_by_tg_id(self, tg_id) -> Chat:
        with self._get_session() as session:
            chat_id = session.query(User).filter(User.tg_id == tg_id).first().current_chat_id
            
            return session.query(Chat).filter(Chat.id == chat_id).first()
        
        
    def get_current_context_id_by_tg_id(self, tg_id) -> int:
        with self._get_session() as session:
            chat_id = session.query(User).filter(User.tg_id == tg_id).first().current_chat_id
            
            return session.query(Chat).filter(Chat.id == chat_id).first().id
            

    # def create_new_context_by_site_id(self, site_id, dialog_name):
    #     '''добавить новый диалог с названием'''
    #     with self._get_session() as session:
    #         try:
    #             user_id = session.query(User).filter_by(User.site_id == site_id).id
                
    #             if not user_id:
    #                 logging.error(f'Ппри попытки создания нового контекста, пользователь с site_id={site_id} не найден')
    #                 return
                
    #             new_chat = Chat(
    #                 name=dialog_name,
    #                 time=int(time.time()),
    #                 user_id=user_id,
    #             )
    #             session.add(new_chat)
    #             session.commit()
    #             logging.info(f'Chat {dialog_name} added successfully.')
    #         except Exception as e:
    #             session.rollback()
    #             logging.error(f'Error adding by site_id Chat {dialog_name}, {e}')

    def update_dialog_neame(self, chat_id, dialog_name):
        with self._get_session() as session:
            chat = session.query(Chat).filter(Chat.id == chat_id).first()
            try:
                chat.name = dialog_name
                session.commit()
                logging.info(f'Переименовали диалог успешно')
            except Exception as ex:
                logging.error(f'Ошибка при переименовании диалога на {chat_id=}, {dialog_name=}, error: {ex}')
    
    def create_new_context_by_tg_id(self, tg_id) -> int:
        '''добавить новый диалог'''
        with self._get_session() as session:
            try:
                user_id = session.query(User.id).filter(User.tg_id == tg_id).scalar()

                
                if not user_id:
                    logging.error(f'Ппри попытки создания нового контекста, пользователь с tg_id={tg_id} не найден')
                    return
                
                curr_time=int(time.time())
                new_chat = Chat(
                    time=curr_time,
                    user_id=user_id,
                )
                session.add(new_chat)
                session.commit()
                logging.info(f'Chat {new_chat.id} added successfully.')
                return new_chat.id
            except Exception as e:
                session.rollback()
                logging.error(f'Error adding by tg_id Chat by {tg_id}, {e}')
    
    # def switch_user_model_by_site_id(self, site_id, new_model_name):
    #     '''
    #     поменять в бд последнюю используемую нейронку на указанную
    #     '''
    #     with self._get_session() as session:
    #         user = session.query(User).filter_by(User.site_id == site_id).first()
    #         if user:
    #             try:
    #                 user.last_used_model = new_model_name
    #                 session.commit()
    #                 logging.info(f'У {user} успешно обновлена last_used_model на {new_model_name}')
    #             except Exception as e:
    #                 session.rollback()
    #                 logging.error(f'Ошибка {e} при обновлении last_used_model у {user} на {new_model_name}')



    def switch_user_model_by_tg_id(self, tg_id, new_model_name):
        '''
        поменять в бд последнюю используемую нейронку на указанную
        '''
        with self._get_session() as session:
            user = session.query(User).filter(User.tg_id == tg_id).first()
            if user:
                try:
                    user.last_used_model = new_model_name
                    session.commit()
                except Exception as e:
                    session.rollback()
                    logging.error(f'Ошибка {e} при обновлении last_used_model у {user} на {new_model_name}')

    
    def get_full_dialog(self, chat_id) -> list[Message]:
        '''
        [
            {'role': 'user', 'content': user_message}, 
            {'role': 'assistant', 'content': user_message}, 
            ...
        ]
        '''
        with self._get_session() as session:
            # messages = (session.query(Message)
            #                    .filter(Message.chat_id == chat_id)
            #                    .order_by(asc(Message.time))).all() 
            chat = session.query(Chat).filter(Chat.id == chat_id).first() 
            messages = chat.to_list_of_roled_messages()
            
        return messages
        
    
    def make_context_history(self, chat_id):
        '''
        по чату, вернуть его содержимое
        '''
        with self._get_session() as session:
            messages = (session.query(Message)
                               .filter(Message.chat_id == chat_id)
                               .order_by(asc(Message.time))).all()
        context_history = ''
        for m in messages:
            if m.author == 'user':
                context_history += f'😍 you:'
            elif m.author == 'assistant':
                context_history += '🤖ChatGPT:'
                
            context_history += '\n'
            context_history += m.text
            context_history += '\n\n'

        context_history += 'Контекст переключен'
        return context_history 


    def from_context_id_get_topic(self, context_id):
        '''
        По контексту, вернуть его название
        '''
        with self._get_session() as session:
            return session.query(Chat.name).filter(Chat.id == context_id).scalar()


    def get_users_contexts_by_tg_id(self, tg_id) -> list[dict[str: int, str: str]]:
        '''
        Cписок контекстов, посорченый по дате создания
        '''
        with self._get_session() as session:
            chats = (session.query(Chat)
                           .join(User)
                           .filter(User.tg_id == tg_id)
                           .order_by(Chat.time)
                           .all())
            contextst = [{'id': ch.id, 'name': ch.name} for ch in chats]
        return contextst
            
        
    # def get_users_contexts_by_site_id(self, site_id):
    #     '''
    #     Cписок контекстов, посорченый по дате создания
    #     '''
    #     with self._get_session() as session:
    #         return (session.query(Chat)
    #                        .join(User)
    #                        .filter_by(User.site_id == site_id)
    #                        .order_by(Chat.time)
    #                        .all())
    
    
    
    def get_user_model_by_tg_id(self, tg_id):
        with self._get_session() as session:
            return session.query(User).filter(User.tg_id == tg_id).first().last_used_model
        
    # def get_user_model_by_site_id(self, site_id):
    #     with self._get_session() as session:
    #         return session.query(User).filter_by(User.site_id == site_id).first().last_used_model

    
    def add_user(self, **kwargs):
        '''
        Добавляет пользователя с переданными параметрами.
        '''
        with self._get_session() as session:
            try:
                user = User(**kwargs)
                session.add(user)
                session.commit()
                logging.info(f'User {user.name} added successfully.')
            except Exception as e:
                session.rollback()
                logging.error(f'Error adding user: {e}')
    
    def get_user_by_tg_id(self, tg_id):
        with self._get_session() as session:
            return session.query(User).filter_by(tg_id=tg_id).first()
    
    # def get_user_by_site_id(self, site_id):
    #     with self._get_session() as session:
    #         return session.query(User).filter_by(site_id=site_id).first()
    
    
        
    def get_sub_status_by_tg_id(self, tg_id):
        with self._get_session() as session:
            return session.query(User).filter_by(tg_id=tg_id).first().sub_status
    
    # def get_sub_status_by_site_id(self, site_id):
    #     with self._get_session() as session:
    #         return session.query(User).filter_by(site_id=site_id).first().sub_status
    
        
        
    def get_token_has_by_tg_id(self, tg_id):
        with self._get_session() as session:
            return session.query(User).filter_by(tg_id=tg_id).first().token_has
    
    # def get_token_has_by_site_id(self, site_id):
    #     with self._get_session() as session:
    #         return session.query(User).filter_by(site_id=site_id).first().token_has



    def update_sub_status_by_tg_id(self, tg_id, new_status):
        with self._get_session() as session:
            try:
                user = session.query(User).filter_by(tg_id=tg_id).first()
                if user:
                    user.sub_status = new_status
                    session.commit()
                    logging.info(f'Updated sub_status to {new_status} for tg_id {tg_id}.')
                else:
                    logging.warning(f'User with tg_id {tg_id} not found.')
            except Exception as e:
                session.rollback()
                logging.error(f'Error updating sub_status: {e}')
                
    # def update_sub_status_by_site_id(self, site_id, new_status):
    #     with self._get_session() as session:
    #         try:
    #             user = session.query(User).filter_by(site_id=site_id).first()
    #             if user:
    #                 user.sub_status = new_status
    #                 session.commit()
    #                 logging.info(f'Updated sub_status to {new_status} for site_id {site_id}.')
    #         except Exception as e:
    #             session.rollback()
    #             logging.error(f'Error updating sub_status: {e}')



    def update_site_id_by_tg_id(self, tg_id, new_site_id):
        with self._get_session() as session:
            try:
                user = session.query(User).filter_by(tg_id=tg_id).first()
                if user:
                    user.site_id = new_site_id
                    session.commit()
                    logging.info(f'Updated site_id to {new_site_id} for tg_id {tg_id}.')
            except Exception as e:
                session.rollback()
                logging.error(f'Error updating site_id: {e}')
                
    # def update_tg_id_by_site_id(self, site_id, new_tg_id):
    #     with self._get_session() as session:
    #         try:
    #             user = session.query(User).filter_by(site_id=site_id).first()
    #             if user:
    #                 user.tg_id = new_tg_id
    #                 session.commit()
    #                 logging.info(f'Updated tg_id to {new_tg_id} for site_id {site_id}.')
    #         except Exception as e:
    #             session.rollback()
    #             logging.error(f'Error updating tg_id: {e}')



    def update_token_has_by_tg_id(self, tg_id, token_amount):
        with self._get_session() as session:
            try:
                user = session.query(User).filter_by(tg_id=tg_id).first()
                if user:
                    user.token_has = token_amount
                    session.commit()
                    logging.info(f'Updated token_has to {token_amount} for tg_id {tg_id}.')
            except Exception as e:
                session.rollback()
                logging.error(f'Error updating token_has: {e}')

    # def update_token_has_by_site_id(self, site_id, token_amount):
    #     with self._get_session() as session:
    #         try:
    #             user = session.query(User).filter_by(site_id=site_id).first()
    #             if user:
    #                 user.token_has = token_amount
    #                 session.commit()
    #                 logging.info(f'Updated token_has to {token_amount} for site_id {site_id}.')
    #         except Exception as e:
    #             session.rollback()
    #             logging.error(f'Error updating token_has: {e}')





db_client = WorkWithDB()


# db_client = WorkWithDB(db_path='sqlite:///:memory:')