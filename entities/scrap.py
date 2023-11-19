import numpy as np

from colour import Color
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Scrap:
    id: str
    color: Color
    fabric_class: str  # synthetic, natural or blend
    dimensions: List[np.array]
    owner: str
    geolocation: Tuple[float] = None
    fabric_type: str = None
    note: str = None
