from typing import Tuple
from dataclasses import dataclass

@dataclass
class Entity:
    name: str
    x: int
    y: int
    sprite: Tuple[int, int, int, int, int, int]
