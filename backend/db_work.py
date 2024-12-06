from fastapi import Depends
from typing import Annotated
import json

def get_db():
    '''
    db = {
        users: list[User]
    }
    '''
    db_file_path = 'backend/textted_db.json'

    with open(db_file_path, 'r', encoding='utf-8') as f:
        db = json.load(f)
    try:
        yield db
    finally:
        with open(db_file_path, 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=4)
    

db_dependency = Annotated[dict, Depends(get_db)]

