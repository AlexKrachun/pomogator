import pytest
from db.main import WorkWithDB
import time

@pytest.fixture
def test_db():
    db = WorkWithDB(db_path='sqlite:///:memory:')
    return db


def test_add_user(test_db):
    test_db.add_user(name='test_name', sub_status='free', token_has=500, tg_id=12345, site_id=67890, last_used_model='test_model')
    user = test_db.get_user_by_tg_id(12345)
    assert user is not None
    assert user.name == 'test_name'
    assert user.sub_status == 'free'
    assert user.token_has == 500
    assert user.site_id == 67890
    assert user.last_used_model == 'test_model'


def test_get_user_by_tg_id(test_db):
    test_db.add_user(last_used_model='test_model', name='test_name', tg_id=54321)
    user = test_db.get_user_by_tg_id(54321)
    assert user is not None
    assert user.name == 'test_name'


def test_update_site_id_by_tg_id(test_db):
    test_db.add_user(last_used_model='test_model', name='test_name', tg_id=44444, site_id=0)
    test_db.update_site_id_by_tg_id(44444, 55555)
    user = test_db.get_user_by_tg_id(44444)
    assert user.site_id == 55555



def test_update_sub_status_by_tg_id(test_db):
    test_db.add_user(last_used_model='test_model', name='test_name', sub_status='free', tg_id=33333)
    test_db.update_sub_status_by_tg_id(33333, 'premium')
    user = test_db.get_user_by_tg_id(33333)
    assert user.sub_status == 'premium'



def test_update_token_has_by_tg_id(test_db):
    test_db.add_user(last_used_model='test_model', name='test_name', token_has=100, tg_id=66666)
    test_db.update_token_has_by_tg_id(66666, 9999)
    user = test_db.get_user_by_tg_id(66666)
    assert user.token_has == 9999



def test_get_sub_status_by_tg_id(test_db):
    test_db.add_user(last_used_model='test_model', name='test_name', sub_status='free', tg_id=12345)
    sub_status = test_db.get_sub_status_by_tg_id(12345)
    assert sub_status == 'free'



def test_get_token_has_by_tg_id(test_db):
    test_db.add_user(last_used_model='test_model', name='test_name', token_has=1500, tg_id=11111)
    token_has = test_db.get_token_has_by_tg_id(11111)
    assert token_has == 1500



def test_user_is_new_by_tg_id(test_db):
    assert test_db.user_is_new_by_tg_id(9999) is True
    test_db.add_user(last_used_model='test_model', name='someone', tg_id=9999)
    assert test_db.user_is_new_by_tg_id(9999) is False


def test_create_new_context_by_tg_id(test_db):
    test_db.add_user(last_used_model='test_model', name='user_for_context', tg_id=1111)
    new_chat_id = test_db.create_new_context_by_tg_id(1111)
    assert new_chat_id is not None


def test_set_current_context_by_tg_id(test_db):
    test_db.add_user(last_used_model='test_model', name='context_user', tg_id=2222)
    new_chat_id = test_db.create_new_context_by_tg_id(2222)
    test_db.set_current_context_by_tg_id(2222, new_chat_id)
    user = test_db.get_user_by_tg_id(2222)
    assert user.current_chat_id == new_chat_id


def test_get_current_context_by_tg_id(test_db):
    test_db.add_user(last_used_model='test_model', name='context_user2', tg_id=3333)
    new_chat_id = test_db.create_new_context_by_tg_id(3333)
    test_db.set_current_context_by_tg_id(3333, new_chat_id)
    chat = test_db.get_current_context_by_tg_id(3333)
    assert chat is not None
    assert chat.id == new_chat_id


def test_user_has_empty_curr_context_by_tg_id(test_db):
    test_db.add_user(last_used_model='test_model', name='empty_context_user', tg_id=4444)
    chat_id = test_db.create_new_context_by_tg_id(4444)
    test_db.set_current_context_by_tg_id(4444, chat_id)
    assert test_db.user_has_empty_curr_context_by_tg_id(4444) is True

    test_db.add_message(chat_id, 'user', 'Hello', author_name='test_name')
    assert test_db.user_has_empty_curr_context_by_tg_id(4444) is False


def test_add_message(test_db):
    test_db.add_user(last_used_model='test_model', name='msg_user', tg_id=5555)
    chat_id = test_db.create_new_context_by_tg_id(5555)
    test_db.add_message(chat_id, 'assistant', 'Hello from the assistant', author_name='test_name')
    messages = test_db.get_full_dialog(chat_id)
    assert len(messages) == 1
    assert messages[0]['role'] == 'assistant'
    assert messages[0]['content'] == 'Hello from the assistant'


def test_update_dialog_neame(test_db):
    test_db.add_user(last_used_model='test_model', name='rename_dialog_user', tg_id=6666)
    chat_id = test_db.create_new_context_by_tg_id(6666)
    test_db.set_current_context_by_tg_id(tg_id=6666, context_id=chat_id)
    test_db.update_dialog_neame(chat_id, 'New Chat Name')
    chat = test_db.get_current_context_by_tg_id(6666)
    assert chat.name == 'New Chat Name'


def test_switch_user_model_by_tg_id(test_db):
    test_db.add_user(name='model_user', tg_id=7777, last_used_model='gpt-3')
    test_db.switch_user_model_by_tg_id(7777, 'gpt-4')
    user = test_db.get_user_by_tg_id(7777)
    assert user.last_used_model == 'gpt-4'


def test_get_user_by_tg_id_again(test_db):
    test_db.add_user(last_used_model='test_model', name='get_user_test', tg_id=8888)
    user = test_db.get_user_by_tg_id(8888)
    assert user is not None
    assert user.name == 'get_user_test'


def test_get_full_dialog(test_db):
    test_db.add_user(last_used_model='test_model', name='dialog_user', tg_id=1010)
    chat_id = test_db.create_new_context_by_tg_id(1010)
    test_db.add_message(chat_id, 'user', 'Hello', author_name='test_name')
    test_db.add_message(chat_id, 'assistant', 'Hi, how can I help?', author_name='test_name')
    dialog = test_db.get_full_dialog(chat_id)
    assert len(dialog) == 2
    assert dialog[0]['role'] == 'user'
    assert dialog[1]['role'] == 'assistant'


# def test_make_context_history(test_db):
#     test_db.add_user(last_used_model='test_model', name='history_user', tg_id=2020)
#     chat_id = test_db.create_new_context_by_tg_id(2020)
#     test_db.add_message(chat_id, 'user', 'User message', author_name='test_name')
#     test_db.add_message(chat_id, 'assistant', 'Assistant reply', author_name='test_name')
#     history = test_db.make_context_history(chat_id)
#     assert '😍 you:\nUser message' in history
#     assert '🤖ChatGPT:\nAssistant reply' in history
#     assert 'Контекст переключен' in history


def test_from_context_id_get_topic(test_db):
    test_db.add_user(last_used_model='test_model', name='topic_user', tg_id=3030)
    chat_id = test_db.create_new_context_by_tg_id(3030)
    test_db.update_dialog_neame(chat_id, 'Some Topic')
    topic = test_db.from_context_id_get_topic(chat_id)
    assert topic == 'Some Topic'


def test_get_users_contexts_by_tg_id(test_db):
    test_db.add_user(last_used_model='test_model', name='multi_chat_user', tg_id=4040)
    c1 = test_db.create_new_context_by_tg_id(4040)
    time.sleep(1)  
    c2 = test_db.create_new_context_by_tg_id(4040)
    chats = test_db.get_users_contexts_by_tg_id(4040)
    assert len(chats) == 2
    assert chats[0]['id'] == c1
    assert chats[1]['id'] == c2


def test_get_user_model_by_tg_id(test_db):
    test_db.add_user(name='model_check_user', tg_id=5050, last_used_model='gpt-4-mini')
    model = test_db.get_user_model_by_tg_id(5050)
    assert model == 'gpt-4-mini'
