import numpy as np

from colour import Color
from dataclasses import dataclass
from typing import List, Tuple
from user import User


@dataclass
class Scrap:
    id: str
    color: Color
    fabric_class: str  # synthetic, natural or blend
    dimensions: List[np.ndarray]
    geolocation: Tuple[float]
    owner: User
    fabric_type: str = None
    note: str = None