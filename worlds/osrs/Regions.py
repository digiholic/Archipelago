import typing

from enum import StrEnum
from .Locations import LocationNames
from .Items import ItemNames


class RegionNames(StrEnum):
    Lumbridge = "Lumbridge"
    Lumbridge_Swamp = "Lumbridge Swamp"
    Lumbridge_Farms = "Lumbridge Farms"
    HAM_Hideout = "HAM Hideout"
    Draynor_Village = "Draynor Village"
    Draynor_Manor = "Draynor Manor"
    Wizards_Tower = "Wizard's Tower"
    Al_Kharid = "Al Kharid"
    Citharede_Abbey = "Citharede Abbey"
    South_Of_Varrock = "South of Varrock"
    Central_Varrock = "Central Varrock"
    Varrock_Palace = "Varrock Palace"
    East_Of_Varrock = "East of Varrock"
    West_Varrock = "West Varrock"
    Edgeville = "Edgeville"
    Barbarian_Village = "Barbarian Village"
    Monastery = "Monastery"
    Ice_Mountain = "Ice Mountain"
    Dwarven_Mines = "Dwarven Mines"
    Falador = "Falador"
    Falador_Farm = "Falador Farm"
    Crafting_Guild = "Crafting Guild"
    Rimmington = "Rimmington"
    Port_Sarim = "Port Sarim"
    Mudskipper_Point = "Mudskipper Point"
    Karamja = "Karamja"
    Corsair_Cove = "Corsair Cove"
    Wilderness = "The Wilderness"
    Crandor = "Crandor"


class RegionInfo(typing.NamedTuple):
    name: str
    unlock: str
    connections: typing.List[str]
    locations: typing.List[str]


all_regions = [
    RegionInfo(RegionNames.Lumbridge,
               ItemNames.Lumbridge,
               [
                   RegionNames.Lumbridge_Swamp,
                   RegionNames.Lumbridge_Farms,
                   RegionNames.HAM_Hideout,
                   RegionNames.Al_Kharid
               ],
               [
                   LocationNames.Q_Cooks_Assistant,
                   LocationNames.Q_Rune_Mysteries,
                   LocationNames.Q_Restless_Ghost,
                   LocationNames.Q_X_Marks_the_Spot
               ]),
    RegionInfo(RegionNames.Lumbridge_Swamp,
               ItemNames.Lumbridge_Swamp,
               [
                  RegionNames.Lumbridge,
                  RegionNames.HAM_Hideout
               ],
               [
                   LocationNames.Q_Misthalin_Mystery
               ]),
    RegionInfo(RegionNames.Lumbridge_Farms,
               ItemNames.Lumbridge_Farms,
               [
                   RegionNames.Lumbridge,
                   RegionNames.HAM_Hideout,
                   RegionNames.Draynor_Village,
                   RegionNames.South_Of_Varrock
               ],
               [
                   LocationNames.Q_Sheep_Shearer
               ]),
    RegionInfo(RegionNames.HAM_Hideout,
               ItemNames.Ham_Hideout,
               [
                   RegionNames.Lumbridge,
                   RegionNames.Lumbridge_Swamp,
                   RegionNames.Lumbridge_Farms,
                   RegionNames.Draynor_Village
               ],
               []),
    RegionInfo(RegionNames.Draynor_Village,
               ItemNames.Draynor_Village,
               [
                   RegionNames.Lumbridge_Farms,
                   RegionNames.HAM_Hideout,
                   RegionNames.Wizards_Tower,
                   RegionNames.Draynor_Manor,
                   RegionNames.Falador_Farm
               ],
               [
                   LocationNames.Q_Vampyre_Slayer
               ]),
    RegionInfo(RegionNames.Draynor_Manor,
               ItemNames.Draynor_Manor,
               [
                   RegionNames.Draynor_Village,
                   RegionNames.Barbarian_Village
               ],
               [
                   LocationNames.Q_Ernest_the_Chicken
               ]),
    RegionInfo(RegionNames.Wizards_Tower,
               ItemNames.Wizards_Tower,
               [
                   RegionNames.Draynor_Village
               ],
               [
                   LocationNames.Q_Imp_Catcher
               ]),
    RegionInfo(RegionNames.Al_Kharid,
               ItemNames.Al_Kharid,
               [
                   RegionNames.Lumbridge,
                   RegionNames.South_Of_Varrock,
                   RegionNames.Citharede_Abbey
               ],
               [
                   LocationNames.Q_Prince_Ali_Rescue
               ]),
    RegionInfo(RegionNames.Citharede_Abbey,
               ItemNames.Cathraede_Abbey,
               [
                   RegionNames.Al_Kharid
               ],
               []),
    RegionInfo(RegionNames.South_Of_Varrock,
               ItemNames.South_Varrock,
               [
                   RegionNames.Al_Kharid,
                   RegionNames.Central_Varrock,
                   RegionNames.East_Of_Varrock,
                   RegionNames.West_Varrock
               ],
               [
                   LocationNames.Q_Dragon_Slayer
               ]),
    RegionInfo(RegionNames.Central_Varrock,
               ItemNames.Central_Varrock,
               [
                   RegionNames.South_Of_Varrock,
                   RegionNames.East_Of_Varrock,
                   RegionNames.West_Varrock,
                   RegionNames.Varrock_Palace
               ],
               [
                   LocationNames.Q_Demon_Slayer,
                   LocationNames.Q_Romeo_Juliet
               ]),
    RegionInfo(RegionNames.Varrock_Palace,
               ItemNames.Varrock_Palace,
               [
                   RegionNames.East_Of_Varrock,
                   RegionNames.Wilderness
               ],
               [
                   LocationNames.Q_Shield_of_Arrav
               ]),
    RegionInfo(RegionNames.East_Of_Varrock,
               ItemNames.East_Varrock,
               [
                   RegionNames.Central_Varrock,
                   RegionNames.Varrock_Palace,
                   RegionNames.South_Of_Varrock,
                   RegionNames.Wilderness
               ],
               []),
    RegionInfo(RegionNames.West_Varrock,
               ItemNames.West_Varrock,
               [
                   RegionNames.Central_Varrock,
                   RegionNames.Varrock_Palace,
                   RegionNames.Edgeville,
                   RegionNames.Barbarian_Village,
                   RegionNames.Wilderness,
                   RegionNames.South_Of_Varrock
               ],
               []),
    RegionInfo(RegionNames.Edgeville,
               ItemNames.Edgeville,
               [
                   RegionNames.Wilderness,
                   RegionNames.West_Varrock,
                   RegionNames.Monastery,
                   RegionNames.Barbarian_Village
               ],
               []),
    RegionInfo(RegionNames.Barbarian_Village,
               ItemNames.Barbarian_Village,
               [
                   RegionNames.Edgeville,
                   RegionNames.West_Varrock,
                   RegionNames.Draynor_Manor,
                   RegionNames.Dwarven_Mines
               ],
               [
                   LocationNames.Stronghold_Of_Security
               ]),
    RegionInfo(RegionNames.Monastery,
               ItemNames.Monastery,
               [
                   RegionNames.Edgeville,
                   RegionNames.Dwarven_Mines,
                   RegionNames.Ice_Mountain,
                   RegionNames.Wilderness
               ],
               []),
    RegionInfo(RegionNames.Ice_Mountain,
               ItemNames.Ice_Mountain,
               [
                   RegionNames.Wilderness,
                   RegionNames.Monastery,
                   RegionNames.Dwarven_Mines
               ],
               []),
    RegionInfo(RegionNames.Dwarven_Mines,
               ItemNames.Dwarven_Mines,
               [
                   RegionNames.Barbarian_Village,
                   RegionNames.Monastery,
                   RegionNames.Ice_Mountain,
                   RegionNames.Falador
               ],
               [
                   LocationNames.Q_Below_Ice_Mountain,
                   LocationNames.Q_Dorics_Quest
               ]),
    RegionInfo(RegionNames.Falador,
               ItemNames.Falador,
               [
                   RegionNames.Dwarven_Mines,
                   RegionNames.Falador_Farm
               ],
               [
                   LocationNames.Q_Knights_Sword,
                   LocationNames.Q_Black_Knights_Fortress
               ]),
    RegionInfo(RegionNames.Falador_Farm,
               ItemNames.Falador_Farm,
               [
                   RegionNames.Crafting_Guild,
                   RegionNames.Draynor_Village,
                   RegionNames.Rimmington,
                   RegionNames.Port_Sarim
               ],
               [
                   LocationNames.Q_Corsair_Curse
               ]),
    RegionInfo(RegionNames.Crafting_Guild,
               ItemNames.Crafting_Guild,
               [
                   RegionNames.Falador_Farm,
                   RegionNames.Rimmington
               ],
               []),
    RegionInfo(RegionNames.Rimmington,
               ItemNames.Rimmington,
               [
                   RegionNames.Crafting_Guild,
                   RegionNames.Falador_Farm,
                   RegionNames.Port_Sarim,
                   RegionNames.Mudskipper_Point,
                   RegionNames.Corsair_Cove
               ],
               [
                   LocationNames.Q_Witchs_Potion
               ]),
    RegionInfo(RegionNames.Port_Sarim,
               ItemNames.Port_Sarim,
               [
                   RegionNames.Falador_Farm,
                   RegionNames.Rimmington,
                   RegionNames.Mudskipper_Point
               ],
               [
                   LocationNames.Q_Pirates_Treasure
               ]),
    RegionInfo(RegionNames.Mudskipper_Point,
               ItemNames.Mudskipper_Point,
               [
                   RegionNames.Port_Sarim,
                   RegionNames.Rimmington,
                   RegionNames.Karamja
               ],
               []),
    RegionInfo(RegionNames.Karamja,
               ItemNames.Karamja,
               [
                   RegionNames.Mudskipper_Point
               ],
               []),
    RegionInfo(RegionNames.Corsair_Cove,
               ItemNames.Corsair_Cove,
               [
                   RegionNames.Port_Sarim
               ],
               []),
    RegionInfo(RegionNames.Wilderness,
               ItemNames.Wilderness,
               [
                   RegionNames.Ice_Mountain,
                   RegionNames.Monastery,
                   RegionNames.Edgeville,
                   RegionNames.West_Varrock,
                   RegionNames.Varrock_Palace,
                   RegionNames.East_Of_Varrock
               ],
               []),
    RegionInfo(RegionNames.Crandor,
               ItemNames.Crandor,
               [
                   RegionNames.Karamja,
                   RegionNames.Port_Sarim
               ],
               [])
]