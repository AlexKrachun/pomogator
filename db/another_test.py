import pytest
from main import Base, User, Chat, Message, WorkWithDB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time

@pytest.fixture
def test_db():
    db = WorkWithDB(db_path='sqlite:///:memory:')
    return db


def test_user_is_new(test_db):
    is_new = test_db.user_is_new_by_tg_id(54321)
    assert not is_new

    test_db.add_user(name="existing_user", tg_id=54321)
    is_new = test_db.user_is_new_by_tg_id(54321)
    assert is_new

def test_user_has_no_contexts(test_db):
    test_db.add_user(name="no_context_user", tg_id=11111)
    has_no_contexts = test_db.user_has_no_contexts_by_tg_id(11111)
    assert has_no_contexts

    test_db.create_new_context_by_tg_id(11111, "First Chat")
    has_no_contexts = test_db.user_has_no_contexts_by_tg_id(11111)
    assert not has_no_contexts

def test_add_message(test_db):
    test_db.add_user(name="messaging_user", tg_id=22222)
    test_db.create_new_context_by_tg_id(22222, "Chat for Messages")
    chat = test_db.get_users_contexts_by_tg_id(22222)[0]

    test_db.add_message(chat_id=chat.id, role="user", text="Hello, World!")
    messages = (test_db._get_session()
                      .query(Message)
                      .filter(Message.chat_id == chat.id)
                      .all())
    print('m' * 100, messages)
    assert len(messages) == 1
    assert messages[0].text == "Hello, World!"
    assert messages[0].author == "user"

def test_set_and_get_current_context(test_db):
    test_db.add_user(name="context_user", tg_id=33333)
    test_db.create_new_context_by_tg_id(33333, "Chat One")
    test_db.create_new_context_by_tg_id(33333, "Chat Two")
    chats = test_db.get_users_contexts_by_tg_id(33333)
    chat_one, chat_two = chats

    test_db.set_current_context_by_tg_id(33333, chat_one.id)
    current_chat = test_db.get_current_context_by_tg_id(33333)
    assert current_chat.id == chat_one.id

    test_db.set_current_context_by_tg_id(33333, chat_two.id)
    current_chat = test_db.get_current_context_by_tg_id(33333)
    assert current_chat.id == chat_two.id

def test_switch_user_model(test_db):
    test_db.add_user(name="model_user", tg_id=44444, last_used_model="gpt-3")
    model = test_db.get_user_model_by_tg_id(44444)
    assert model == "gpt-3"

    test_db.switch_user_model_by_tg_id(44444, "gpt-4")
    model = test_db.get_user_model_by_tg_id(44444)
    assert model == "gpt-4"

def test_make_context_history(test_db):
    test_db.add_user(name="history_user", tg_id=55555)
    test_db.create_new_context_by_tg_id(55555, "History Chat")
    chat = test_db.get_users_contexts_by_tg_id(55555)[0]

    test_db.add_message(chat_id=chat.id, role="user", text="Hi!")
    test_db.add_message(chat_id=chat.id, role="assistant", text="Hello!")

    history = test_db.make_context_history(chat_id=chat.id)
    expected_history = "😍 you:\nHi!\n\n🤖ChatGPT:\nHello!\n\nКонтекст переключен"
    assert history == expected_history

def test_from_context_id_get_topic(test_db):
    test_db.add_user(name="topic_user", tg_id=66666)
    test_db.create_new_context_by_tg_id(66666, "Topic Chat")
    chat = test_db.get_users_contexts_by_tg_id(66666)[0]

    topic = test_db.from_context_id_get_topic(chat.id)
    assert topic == "Topic Chat"

def test_get_users_contexts_by_tg_id(test_db):
    test_db.add_user(name="multi_chat_user", tg_id=77777)
    test_db.create_new_context_by_tg_id(77777, "Chat A")
    time.sleep(1)
    test_db.create_new_context_by_tg_id(77777, "Chat B")
    chats = test_db.get_users_contexts_by_tg_id(77777)
    
    assert len(chats) == 2
    assert chats[0].name == "Chat A"
    assert chats[1].name == "Chat B"


def test_delete_user_cascade(test_db):
    test_db.add_user(name="delete_user", tg_id=101010)
    test_db.create_new_context_by_tg_id(101010, "Delete Chat")
    chat = test_db.get_users_contexts_by_tg_id(101010)[0]

    test_db.add_message(chat_id=chat.id, role="user", text="To be deleted")

    with test_db._get_session() as session:
        user = session.query(User).filter_by(tg_id=101010).first()
        session.delete(user)
        session.commit()

    user = test_db.get_user_by_tg_id(101010)
    assert user is None

    with test_db._get_session() as session:
        dead_chat = session.query(Chat).filter_by(id=chat.id).first()
        assert dead_chat is None
        messages = session.query(Message).filter_by(chat_id=chat.id).all()
        assert len(messages) == 0
