from dataclasses import dataclass


@dataclass
class User:
    user_id: str
    username: str
    email: str
    instagram: str
    password: str = None
    description: str = None
