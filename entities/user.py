from dataclasses import dataclass
from scrap import Scrap
from typing import Set, Dict


@dataclass
class User:
    id: str
    username: str
    name: str
    email: str
    password: str
    description: str
    preferences: Dict[str:str]
    scraps: Set[Scrap]
