import typing

from enum import StrEnum
from BaseClasses import Location

class LocationNames(StrEnum):
    Q_Cooks_Assistant = "Quest: Cook's Assistant"
    Q_Demon_Slayer = "Quest: Demon Slayer"
    Q_Restless_Ghost = "Quest: The Restless Ghost"
    Q_Romeo_Juliet = "Quest: Romeo & Juliet"
    Q_Sheep_Shearer = "Quest: Sheep Shearer"
    Q_Shield_of_Arrav = "Quest: Shield of Arrav"
    Q_Ernest_the_Chicken = "Quest: Ernest the Chicken"
    Q_Vampyre_Slayer = "Quest: Vampyre Slayer"
    Q_Imp_Catcher = "Quest: Imp Catcher"
    Q_Prince_Ali_Rescue = "Quest: Prince Ali Rescue"
    Q_Dorics_Quest = "Quest: Doric's Quest"
    Q_Black_Knights_Fortress = "Quest: Black Knights' Fortress"
    Q_Witchs_Potion = "Quest: Witch's Potion"
    Q_Knights_Sword = "Quest: The Knight's Sword"
    Q_Goblin_Diplomacy = "Quest: Goblin Diplomacy"
    Q_Pirates_Treasure = "Quest: Pirate's Treasure"
    Q_Rune_Mysteries = "Quest: Rune Mysteries"
    Q_Misthalin_Mystery = "Quest: Misthalin Mystery"
    Q_Corsair_Curse = "Quest: The Corsair Curse"
    Q_X_Marks_the_Spot = "Quest: X Marks the Spot"
    Q_Below_Ice_Mountain = "Quest: Below Ice Mountain"
    Stronghold_Of_Security = "Stronghold of Security"
    Simple_Lockbox = "Open a Simple Lockbox"
    Elaborate_Lockbox = "Open an Elaborate Lockbox"
    Ornate_Lockbox = "Open an Ornate Lockbox"
    Guppy = "Prepare a Guppy"
    Cavefish = "Prepare a Cavefish"
    Tetra = "Prepare a Tetra"
    Mind_Core = "Craft runes with a Mind Core"
    Body_Core = "Craft runes with a Body Core"
    Barronite_Deposit = "Crush a Barronite Deposit"
    Beginner_Clue = "Beginner Clue Completion"
    Edgeville_Altar = "Pray at the Edgeville Monastery"
    Oak_Log = "Cut an Oak Log"
    Willow_Log = "Cut a Willow Log"
    Catch_Lobster = "Catch a Lobster"
    Catch_Swordfish = "Catch a Swordfish"
    Holy_Symbol = "Make a Holy Symbol"
    Mine_Silver = "Mine Silver"
    Mine_Coal = "Mine Coal"
    Mine_Gold = "Mine Gold"
    Smelt_Silver = "Smelt a Silver Bar"
    Smelt_Steel = "Smelt a Steel Bar"
    Smelt_Gold = "Smelt a Gold Bar"
    Cut_Sapphire = "Cut a Sapphire"
    Cut_Emerald = "Cut an Emerald"
    Cut_Ruby = "Cut a Ruby"
    Cut_Diamond = "Cut a Diamond"
    K_Lesser_Demon = "Kill a Lesser Demon"
    K_Ogress_Shaman = "Kill an Ogress Shaman"
    K_Green_Dragon = "Kill a Green Dragon"
    K_Obor = "Kill Obor"
    K_Bryo = "Kill Bryophyta"
    Teleport_Varrock = "Teleport to Varrock"
    Teleport_Lumbridge = "Teleport to Lumbridge"
    Teleport_Falador = "Teleport to Falador"
    Bake_Apple_Pie = "Bake an Apple Pie"
    Bake_Cake = "Bake a Cake"
    Bake_Meat_Pizza = "Bake a Meat Pizza"
    Prospect_Rune = "Prospect a Rune Rock"
    Q_Dragon_Slayer = "Quest: Dragon Slayer"

class OSRSLocation(Location):
    game: str = "Old School Runescape"


class LocationData(typing.NamedTuple):
    id: int
    name: str
    qp: int = 0


Quest_Locations = [
    LocationData(0x070000, LocationNames.Q_Cooks_Assistant, 1),
    LocationData(0x070001, LocationNames.Q_Demon_Slayer, 3),
    LocationData(0x070002, LocationNames.Q_Restless_Ghost, 1),
    LocationData(0x070003, LocationNames.Q_Romeo_Juliet, 5),
    LocationData(0x070004, LocationNames.Q_Sheep_Shearer, 1),
    LocationData(0x070005, LocationNames.Q_Shield_of_Arrav, 1),
    LocationData(0x070006, LocationNames.Q_Ernest_the_Chicken, 4),
    LocationData(0x070007, LocationNames.Q_Vampyre_Slayer, 3),
    LocationData(0x070008, LocationNames.Q_Imp_Catcher, 1),
    LocationData(0x070009, LocationNames.Q_Prince_Ali_Rescue, 3),
    LocationData(0x07000A, LocationNames.Q_Dorics_Quest, 1),
    LocationData(0x07000B, LocationNames.Q_Black_Knights_Fortress, 3),
    LocationData(0x07000C, LocationNames.Q_Witchs_Potion, 1),
    LocationData(0x07000D, LocationNames.Q_Knights_Sword, 1),
    LocationData(0x07000E, LocationNames.Q_Goblin_Diplomacy, 5),
    LocationData(0x07000F, LocationNames.Q_Pirates_Treasure, 2),
    LocationData(0x070010, LocationNames.Q_Rune_Mysteries, 1),
    LocationData(0x070011, LocationNames.Q_Misthalin_Mystery, 1),
    LocationData(0x070012, LocationNames.Q_Corsair_Curse, 2),
    LocationData(0x070013, LocationNames.Q_X_Marks_the_Spot, 1),
    LocationData(0x070014, LocationNames.Q_Below_Ice_Mountain, 1),
]

Skill_Locations = [
    LocationData(0x070015, LocationNames.Simple_Lockbox),
    LocationData(0x070016, LocationNames.Elaborate_Lockbox),
    LocationData(0x070017, LocationNames.Ornate_Lockbox),
    LocationData(0x070018, LocationNames.Guppy),
    LocationData(0x070019, LocationNames.Cavefish),
    LocationData(0x07001A, LocationNames.Tetra),
    LocationData(0x07001B, LocationNames.Mind_Core),
    LocationData(0x07001C, LocationNames.Body_Core),
    LocationData(0x07001D, LocationNames.Barronite_Deposit),
    LocationData(0x07001E, LocationNames.Oak_Log),
    LocationData(0x07001F, LocationNames.Willow_Log),
    LocationData(0x070020, LocationNames.Catch_Lobster),
    LocationData(0x070021, LocationNames.Catch_Swordfish),
    LocationData(0x070022, LocationNames.Holy_Symbol),
    LocationData(0x070023, LocationNames.Mine_Silver),
    LocationData(0x070024, LocationNames.Mine_Coal),
    LocationData(0x070025, LocationNames.Mine_Gold),
    LocationData(0x070026, LocationNames.Smelt_Silver),
    LocationData(0x070027, LocationNames.Smelt_Steel),
    LocationData(0x070028, LocationNames.Smelt_Gold),
    LocationData(0x070029, LocationNames.Cut_Sapphire),
    LocationData(0x07002A, LocationNames.Cut_Emerald),
    LocationData(0x07002B, LocationNames.Cut_Ruby),
    LocationData(0x07002C, LocationNames.Cut_Diamond),
    LocationData(0x07002D, LocationNames.Teleport_Falador),
    LocationData(0x07002E, LocationNames.Teleport_Varrock),
    LocationData(0x07002F, LocationNames.Teleport_Lumbridge),
    LocationData(0x070030, LocationNames.Bake_Apple_Pie),
    LocationData(0x070031, LocationNames.Bake_Cake),
    LocationData(0x070032, LocationNames.Bake_Meat_Pizza)
]

Misc_Locations = [
    LocationData(0x070033, LocationNames.Stronghold_Of_Security),
    LocationData(0x070034, LocationNames.Beginner_Clue),
    LocationData(0x070035, LocationNames.Edgeville_Altar),
    LocationData(0x070036, LocationNames.K_Lesser_Demon),
    LocationData(0x070037, LocationNames.K_Ogress_Shaman),
    LocationData(0x070039, LocationNames.K_Obor),
    LocationData(0x07003A, LocationNames.K_Bryo),
    LocationData(0x07003B, LocationNames.Prospect_Rune)
]

Resource_Locations = [
    # Sheep
    # Spinning Wheel
    # Wheat
    # Mill
    # Furnace
    # Anvil
    # Tin Rocks
    # Copper Rocks
    # Clay Rocks
    # Iron Rocks
    # Coal Rocks
]

all_locations: typing.List[LocationData] = Quest_Locations + Skill_Locations + Misc_Locations
location_table: typing.Dict[str, int] = {locData.name: locData.id for locData in all_locations}
location_data_table: typing.Dict[str, LocationData] = {locData.name: locData for locData in all_locations}