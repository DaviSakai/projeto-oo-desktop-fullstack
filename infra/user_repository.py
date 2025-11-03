from typing import List, Optional
from .json_store import read_json, write_json
from domain.user import User
from config import USERS_JSON

def _to_dict(user: User) -> dict:
    return user.model_dump() if hasattr(user, "model_dump") else user.dict()

class UserRepository:
    def __init__(self, path=USERS_JSON):
        self.path = path
        self._ensure()

    def _ensure(self):
        data = read_json(self.path)
        if data is None:
            write_json(self.path, {"seq": 0, "users": []})

    def _load(self):
        data = read_json(self.path)
        if not data:
            data = {"seq": 0, "users": []}
            write_json(self.path, data)
        data.setdefault("seq", 0)
        data.setdefault("users", [])
        return data

    def _save(self, data):
        write_json(self.path, data)

    def list_all(self) -> List[User]:
        data = self._load()
        return [User(**u) for u in data["users"]]

    def find_by_email(self, email: str) -> Optional[User]:
        data = self._load()
        for u in data["users"]:
            if u.get("email","").lower() == email.lower():
                return User(**u)
        return None

    def get_by_id(self, uid: int) -> Optional[User]:
        data = self._load()
        for u in data["users"]:
            if int(u.get("id",-1)) == int(uid):
                return User(**u)
        return None

    def create(self, user: User) -> User:
        data = self._load()
        data["seq"] += 1
        user_dict = _to_dict(user)
        user_dict["id"] = data["seq"]
        data["users"].append(user_dict)
        self._save(data)
        return User(**user_dict)

    def update(self, user: User) -> User:
        data = self._load()
        for i, u in enumerate(data["users"]):
            if int(u.get("id",-1)) == int(user.id):
                data["users"][i] = _to_dict(user)
                self._save(data)
                return user
        raise ValueError("Usuário não encontrado")
