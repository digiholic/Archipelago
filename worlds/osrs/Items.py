from enum import Enum


class ItemSlot(Enum):
    INVENTORY = 0
    WEAPON = 1
    SHIELD = 2
    HEAD = 3
    BODY = 4
    LEGS = 5
    BOOTS = 6
    GLOVES = 7
    BACK = 8
    NECK = 9
    RING = 10
    AMMO = 11


class ItemDefinition:
    name: str
    ap_id: int
    rs_id: int
    slot: ItemSlot
    survival_score: int
    melee_score: int
    range_score: int
    magic_score: int