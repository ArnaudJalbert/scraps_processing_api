from dataclasses import dataclass
from entities.scrap import Scrap
from typing import Set, Dict


@dataclass
class User:
    user_id: str
    username: str
    email: str
    instagram: str
    password: str = None
    description: str = None
    scraps: Set[str] = None
