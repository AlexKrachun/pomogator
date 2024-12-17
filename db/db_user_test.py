import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Base, User, WorkWithDB

@pytest.fixture
def test_db():
    db = WorkWithDB(db_path='sqlite:///:memory:')
    yield db


def test_add_user(test_db):
    test_db.add_user(name="test_name", sub_status="free", token_has=500, tg_id=12345, site_id=67890)
    user = test_db.get_user_by_tg_id(12345)
    assert user is not None
    assert user.name == "test_name"
    assert user.sub_status == "free"
    assert user.token_has == 500
    assert user.site_id == 67890



def test_get_user_by_tg_id(test_db):
    test_db.add_user(name="test_name", sub_status="premium", token_has=1000, tg_id=54321, site_id=12345)
    user = test_db.get_user_by_tg_id(54321)
    assert user is not None
    assert user.name == "test_name"

def test_get_user_by_site_id(test_db):
    test_db.add_user(name="test_name", sub_status="normal", token_has=1500, tg_id=11111, site_id=22222)
    user = test_db.get_user_by_site_id(22222)
    assert user is not None
    assert user.tg_id == 11111
    assert user.name == "test_name"
    



def test_update_site_id_by_tg_id(test_db):
    test_db.add_user(name="test_name", sub_status="normal", token_has=300, tg_id=44444, site_id=0)
    test_db.update_site_id_by_tg_id(44444, 55555)
    user = test_db.get_user_by_tg_id(44444)
    assert user.site_id == 55555
    
def test_update_tg_id_by_site_id(test_db):
    test_db.add_user(name="test_name", sub_status="free", token_has=500, site_id=88888, tg_id=0)
    test_db.update_tg_id_by_site_id(88888, 123456)
    user = test_db.get_user_by_site_id(88888)
    assert user.tg_id == 123456
    
    
    
def test_update_sub_status_by_tg_id(test_db):
    test_db.add_user(name="test_name", sub_status="free", token_has=200, tg_id=33333)
    test_db.update_sub_status_by_tg_id(33333, "premium")
    user = test_db.get_user_by_tg_id(33333)
    assert user.sub_status == "premium"
    
def test_update_sub_status_by_site_id(test_db):
    test_db.add_user(name="test_name", sub_status="normal", token_has=400, site_id=77777)
    test_db.update_sub_status_by_site_id(77777, "god")
    user = test_db.get_user_by_site_id(77777)
    assert user.sub_status == "god"



def test_update_token_has_by_tg_id(test_db):
    test_db.add_user(name="test_name", sub_status="free", token_has=100, tg_id=66666)
    test_db.update_token_has_by_tg_id(66666, 9999)
    user = test_db.get_user_by_tg_id(66666)
    assert user.token_has == 9999
    
def test_update_token_has_by_site_id(test_db):
    test_db.add_user(name="test_name", sub_status="premium", token_has=700, site_id=99999)
    test_db.update_token_has_by_site_id(99999, 5555)
    user = test_db.get_user_by_site_id(99999)
    assert user.token_has == 5555
    
    

def test_get_sub_status_by_tg_id(test_db):
    test_db.add_user(name="test_name", sub_status="free", token_has=500, tg_id=12345)
    sub_status = test_db.get_sub_status_by_tg_id(12345)
    assert sub_status == "free"

def test_get_sub_status_by_site_id(test_db):
    test_db.add_user(name="test_name", sub_status="premium", token_has=1000, site_id=67890)
    sub_status = test_db.get_sub_status_by_site_id(67890)
    assert sub_status == "premium"
    
    

def test_get_token_has_by_tg_id(test_db):
    test_db.add_user(name="test_name", sub_status="normal", token_has=1500, tg_id=11111)
    token_has = test_db.get_token_has_by_tg_id(11111)
    assert token_has == 1500

def test_get_token_has_by_site_id(test_db):
    test_db.add_user(name="test_name", sub_status="god", token_has=9999, site_id=22222)
    token_has = test_db.get_token_has_by_site_id(22222)
    assert token_has == 9999
    
    
    