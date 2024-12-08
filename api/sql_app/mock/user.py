import json
import os
from re import U

from api.routes.security.schema import UserDB

def load_users_from_json(file_path):
    abs_path = os.path.join(os.path.dirname(__file__), file_path)
    with open(abs_path, "r", encoding="utf-8") as file:
        return json.load(file)

fake_users_db = load_users_from_json("./user.json")

def get_user_form_db_by_username(username: str)-> UserDB|None:
    for user in fake_users_db:
        if user["username"] == username:
            return user
    return None

def get_user_form_db_by_id(id: int)-> UserDB|None:
    for user in fake_users_db:
        if user["id"] == id:
            return user
    return None