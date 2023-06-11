from typing import Tuple
from dataclasses import dataclass

@dataclass
class Entity:
    name: str
    x: int
    y: int
    sprite: Tuple[int, int, int, int, int, int]
    speed: int = 0
    atk: int = 0
    strength: int = 0
    dexterity: int = 0
    intelligence: int = 0
    repeat: int = 0
    direct: int = 0
    is_alive: bool = True


    def verifyCollision(objeto1, objeto2):
            if (objeto1.x < objeto2.x + objeto2.sprite[3] and
                    objeto1.x + objeto1.sprite[3] > objeto2.x and
                    objeto1.y < objeto2.y + objeto2.sprite[4] and
                    objeto1.y + objeto1.sprite[4] > objeto2.y):
                return True
            else:
                return False
    
    def changeSprite(character):
         if character.name == "Attack":
              if character.sprite != "SPRITEATTACK4":
                   print(character.sprite)

    def die(character):
        character.is_alive = False
        character.x = -100 
        character.y = -100