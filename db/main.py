import logging
import time
from datetime import datetime

from sqlalchemy import asc, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import Column

from db.tables import User, Chat, Message, Base



logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

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

    def get_dalle_quality_by_tg_id(self, tg_id) -> Column[str]:
        with self._get_session() as session:
            return session.query(User).filter_by(tg_id=tg_id).first().dalle_quality

    def get_dalle_shape_by_tg_id(self, tg_id) -> str:
        with self._get_session() as session:
            return session.query(User).filter_by(tg_id=tg_id).first().dalle_shape


    def set_dalle_quality_by_tg_id(self, tg_id, dalle_quality: str):
        with self._get_session() as session:
            user = session.query(User).filter(User.tg_id == tg_id).first()

            try:
                user.dalle_quality = dalle_quality
                session.commit()
                logging.info(f'User dalle_quality changed successfully to {dalle_quality}')
            except Exception as e:
                session.rollback()
                logging.error(f'Error User dalle_quality changin to {dalle_quality}, {e}')

    def set_dalle_shape_by_tg_id(self, tg_id, dalle_shape: str):
        with self._get_session() as session:
            user = session.query(User).filter(User.tg_id == tg_id).first()

            try:
                user.dalle_shape = dalle_shape
                session.commit()
                logging.info(f'User dalle_shape changed successfully to {dalle_shape}')
            except Exception as e:
                session.rollback()
                logging.error(f'Error User dalle_shape changin to {dalle_shape}, {e}')


    def user_is_new_by_tg_id(self, tg_id):
        '''нет пользователя с таким tg_id'''
        with self._get_session() as session:
            user = session.query(User).filter(User.tg_id == tg_id).first()
            return not bool(user)




    def user_has_empty_curr_context_by_tg_id(self, us_id):
        with self._get_session() as session:
            curr_context_id = session.query(User).filter(User.tg_id == us_id).first().current_chat_id
            user_curr_context_messages = session.query(Chat).filter(Chat.id == curr_context_id).first().messages
            return len(user_curr_context_messages) == 0

    def add_message(self, chat_id, role, text, author_name):
        with self._get_session() as session:
            try:
                msg = Message(
                    text=text,
                    author=role,
                    time=int(time.time()),
                    chat_id=chat_id,
                    author_name=author_name,
                )
                session.add(msg)
                session.commit()
                logging.info(f'Message {msg} added successfully.')
            except Exception as e:
                session.rollback()
                logging.error(f'Error adding message: {e}')

    def get_user_by_tg_id(self, tg_id) -> User:
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


    def make_context_history(self, chat_id) -> list[str]:
        '''
        по чату, вернуть его содержимое
        '''
        with self._get_session() as session:
            messages = (session.query(Message)
                               .filter(Message.chat_id == chat_id)
                               .order_by(asc(Message.time))).all()
        context_history = ['']
        for m in messages:
            saying = ''
            if m.author == 'user':
                saying += f'😍 @{m.author_name.replace('_', '\\_')}:'
            elif m.author == 'assistant':
                saying += f'🤖 {m.author_name.replace('_', '\\_')}:'

            saying += '\n'
            saying += m.text
            saying += '\n\n'

            if len(context_history[-1]) + len(saying) < 4096:
                context_history[-1] += saying
            else:
                if len(saying) < 4096:
                    context_history.append(saying)
                else:
                    # print(f'went to while: |{saying}|')

                    while saying != '':
                        # print(f'I am in while: |{saying}|')
                        # if saying == '``` ':
                        #     break
                        st = saying[:min(4090, len(saying))]

                        if st.count('```') % 2 == 0:
                            context_history.append(st)
                            saying = saying[len(st):]
                        else:
                            context_history.append(st + '```')
                            saying = saying[len(st):]
                            if saying.count('```') % 2 != 0:
                                saying = '``` ' + saying



        if context_history[-1] == '':
            context_history.pop()
        # context_history.append('Контекст переключен')
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


    def get_user_model_by_tg_id(self, tg_id):
        with self._get_session() as session:
            return session.query(User).filter(User.tg_id == tg_id).first().last_used_model


    def add_user(self, name, tg_id, last_used_model):
        '''
        Добавляет пользователя с переданными параметрами.
        '''
        with self._get_session() as session:
            try:
                user = User(tg_id=tg_id, last_used_model=last_used_model)
                session.add(user)
                session.commit()
                logging.info(f'User {name} added successfully.')
            except Exception as e:
                session.rollback()
                logging.error(f'Error adding user: {e}')

    def get_user_by_tg_id(self, tg_id):
        with self._get_session() as session:
            return session.query(User).filter_by(tg_id=tg_id).first()


    # def update_sub_status_by_tg_id(self, tg_id, new_status):
    #     with self._get_session() as session:
    #         try:
    #             user = session.query(User).filter_by(tg_id=tg_id).first()
    #             if user:
    #                 user.sub_status = new_status
    #                 session.commit()
    #                 logging.info(f'Updated sub_status to {new_status} for tg_id {tg_id}.')
    #             else:
    #                 logging.warning(f'User with tg_id {tg_id} not found.')
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


    def update_sub_by_tg_id(self, tg_id):
        with self._get_session() as session:
            try:
                user = session.query(User).filter_by(tg_id=tg_id).first()
                if user:
                    # если подписка была, но кончилась
                    if user.sub_end and user.sub_end.date() < datetime.now().date():
                        # default = User.__table__.c.weekly_candy_from_sub.default.arg
                        user.weekly_candy_from_sub = 0
                        user.sub_end = None
                        user.has_sub = False
                        session.commit()
                        logging.info(f'Updated weekly_candy_from_sub to {0} for tg_id {tg_id}.')
            except Exception as e:
                session.rollback()
                logging.error(f'Error updating sub: {e}')


    def update_candy_by_tg_id(self, tg_id):
        with self._get_session() as session:
            try:
                user = session.query(User).filter_by(tg_id=tg_id).first()
                if user:
                    # если еженедельные фантики еще не приходили или приходили больше недели назад 
                    if (not user.last_fantiks_update_date) or ((datetime.now().date() - user.last_fantiks_update_date.date()).days >= 7):
                        user.candy_left = user.weekly_candy_from_sub  # либо 0, либо как в подписке
                        user.last_request = datetime.now()
                        if user.has_sub:
                            user.deposits_amount -= 1
                        session.commit()
                    print(f'Updated candy_left to {user.weekly_candy_from_sub} for tg_id {tg_id}.')

            except Exception as e:
                session.rollback()
                logging.error(f'Error updating candy: {e}')

    def get_candy_left_by_tg_id(self, tg_id):
        with self._get_session() as session:
            try:
                user = session.query(User).filter_by(tg_id=tg_id).first()
                if user:
                    logging.info(f'User with tg_id {tg_id} has {user.candy_left} candies.')
                    return user.candy_left

            except Exception as e:
                session.rollback()
                logging.error(f'Error getting candy: {e}')
            return 0

    def get_weekly_candy_by_tg_id(self, tg_id):
        with self._get_session() as session:
            try:
                user = session.query(User).filter_by(tg_id=tg_id).first()
                if user:
                    return user.weekly_candy_from_sub

            except Exception as e:
                session.rollback()
                logging.error(f'Error getting candy: {e}')
                # return 0
            return 0

    def decrease_candy_by_tg_id(self, tg_id, amount):
        with self._get_session() as session:
            try:
                user = session.query(User).filter_by(tg_id=tg_id).first()
                if user:
                    candy_left = user.candy_left
                    user.candy_left = max(0, candy_left - amount)
                    session.commit()
            except Exception as e:
                session.rollback()
                logging.error(f'Error getting candy: {e}')
            




db_client = WorkWithDB()


# db_client = WorkWithDB(db_path='sqlite:///:memory:')
