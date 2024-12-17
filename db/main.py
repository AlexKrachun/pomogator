from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import logging
import json

# Настройка логирования
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Базовый класс
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    pk = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer, nullable=True)
    site_id = Column(Integer, nullable=True)
    name = Column(String(250), nullable=False)
    sub_status = Column(String(50), nullable=False)
    token_has = Column(Integer, nullable=False)
    
    

'''
{
    'user_id_1': [
        'dialog_di_1':[
            {"role": "user", "content": "Hello, how are you?"},
            {"role": "bot", "content": "I'm fine, thank you!"},
            {"role": "user", "content": "What's the weather like today?"}, 
            ...
            ],
        'dialog_di_2':[
            {"role": "user", "content": "Hello, how are you?"},
            {"role": "bot", "content": "I'm fine, thank you!"},
            {"role": "user", "content": "What's the weather like today?"}, 
            ...
            ],
        ]
    'user_id_2': [...],
    ...
}
'''




class WorkWithDB:
    def __init__(self, db_path='sqlite:///db/orm.db'):
        self.engine = create_engine(db_path)
        self.Session = sessionmaker(bind=self.engine)
        # Создание таблиц
        Base.metadata.create_all(self.engine)
    
    def _get_session(self):
        """Получение новой сессии."""
        return self.Session()
    
    def add_user(self, **kwargs):
        """Добавляет пользователя с переданными параметрами."""
        with self._get_session() as session:
            try:
                user = User(**kwargs)
                session.add(user)
                session.commit()
                logging.info(f"User {user.name} added successfully.")
            except Exception as e:
                session.rollback()
                logging.error(f"Error adding user: {e}")
    
    def get_user_by_tg_id(self, tg_id):
        with self._get_session() as session:
            return session.query(User).filter_by(tg_id=tg_id).first()
    
    def get_user_by_site_id(self, site_id):
        with self._get_session() as session:
            return session.query(User).filter_by(site_id=site_id).first()
    
    
        
    def get_sub_status_by_tg_id(self, tg_id):
        with self._get_session() as session:
            return session.query(User).filter_by(tg_id=tg_id).first().sub_status
    
    def get_sub_status_by_site_id(self, site_id):
        with self._get_session() as session:
            return session.query(User).filter_by(site_id=site_id).first().sub_status
    
        
        
    def get_token_has_by_tg_id(self, tg_id):
        with self._get_session() as session:
            return session.query(User).filter_by(tg_id=tg_id).first().token_has
    
    def get_token_has_by_site_id(self, site_id):
        with self._get_session() as session:
            return session.query(User).filter_by(site_id=site_id).first().token_has



    def update_sub_status_by_tg_id(self, tg_id, new_status):
        with self._get_session() as session:
            try:
                user = session.query(User).filter_by(tg_id=tg_id).first()
                if user:
                    user.sub_status = new_status
                    session.commit()
                    logging.info(f"Updated sub_status to {new_status} for tg_id {tg_id}.")
                else:
                    logging.warning(f"User with tg_id {tg_id} not found.")
            except Exception as e:
                session.rollback()
                logging.error(f"Error updating sub_status: {e}")
                
    def update_sub_status_by_site_id(self, site_id, new_status):
        with self._get_session() as session:
            try:
                user = session.query(User).filter_by(site_id=site_id).first()
                if user:
                    user.sub_status = new_status
                    session.commit()
                    logging.info(f"Updated sub_status to {new_status} for site_id {site_id}.")
            except Exception as e:
                session.rollback()
                logging.error(f"Error updating sub_status: {e}")



    def update_site_id_by_tg_id(self, tg_id, new_site_id):
        with self._get_session() as session:
            try:
                user = session.query(User).filter_by(tg_id=tg_id).first()
                if user:
                    user.site_id = new_site_id
                    session.commit()
                    logging.info(f"Updated site_id to {new_site_id} for tg_id {tg_id}.")
            except Exception as e:
                session.rollback()
                logging.error(f"Error updating site_id: {e}")
                
    def update_tg_id_by_site_id(self, site_id, new_tg_id):
        with self._get_session() as session:
            try:
                user = session.query(User).filter_by(site_id=site_id).first()
                if user:
                    user.tg_id = new_tg_id
                    session.commit()
                    logging.info(f"Updated tg_id to {new_tg_id} for site_id {site_id}.")
            except Exception as e:
                session.rollback()
                logging.error(f"Error updating tg_id: {e}")



    def update_token_has_by_tg_id(self, tg_id, token_amount):
        with self._get_session() as session:
            try:
                user = session.query(User).filter_by(tg_id=tg_id).first()
                if user:
                    user.token_has = token_amount
                    session.commit()
                    logging.info(f"Updated token_has to {token_amount} for tg_id {tg_id}.")
            except Exception as e:
                session.rollback()
                logging.error(f"Error updating token_has: {e}")

    def update_token_has_by_site_id(self, site_id, token_amount):
        with self._get_session() as session:
            try:
                user = session.query(User).filter_by(site_id=site_id).first()
                if user:
                    user.token_has = token_amount
                    session.commit()
                    logging.info(f"Updated token_has to {token_amount} for site_id {site_id}.")
            except Exception as e:
                session.rollback()
                logging.error(f"Error updating token_has: {e}")
