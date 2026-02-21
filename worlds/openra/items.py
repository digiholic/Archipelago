from typing import NamedTuple

from BaseClasses import Item, ItemClassification


class ItemInfo(NamedTuple):
    name: str
    classification: ItemClassification
    id: int

structure_items = [
    # Structures
    ItemInfo("Structure: Power Plant", ItemClassification.progression, 0),
    ItemInfo("Structure: Allied Barracks", ItemClassification.progression, 1),
    ItemInfo("Structure: Ore Refinery", ItemClassification.progression, 2),
    ItemInfo("Structure: Soviet Barracks", ItemClassification.progression, 3),
    ItemInfo("Structure: Naval Yard", ItemClassification.progression, 4),
    ItemInfo("Structure: Sub Pen", ItemClassification.progression, 5),
    ItemInfo("Structure: War Factory", ItemClassification.progression, 6),
    ItemInfo("Structure: Radar Dome", ItemClassification.progression, 7),
    ItemInfo("Structure: Service Depot", ItemClassification.progression, 8),
    ItemInfo("Structure: Advanced Power Plant", ItemClassification.useful, 9),
    ItemInfo("Structure: Helipad", ItemClassification.progression, 10),
    ItemInfo("Structure: Allied Airfield", ItemClassification.progression, 11),
    ItemInfo("Structure: Soviet Airfield", ItemClassification.progression, 12),
    ItemInfo("Structure: Allied Tech Center", ItemClassification.progression, 13),
    ItemInfo("Structure: Soviet Tech Center", ItemClassification.progression, 14),
    ItemInfo("Structure: Kennel", ItemClassification.progression, 15),
    ItemInfo("Structure: Construction Yard", ItemClassification.progression, 16),
]

defensive_structure_items = [
# Defensive Structures
    ItemInfo("Defensive Structure: Sandbags", ItemClassification.useful, 17),
    ItemInfo("Defensive Structure: Silo", ItemClassification.useful, 18),
    ItemInfo("Defensive Structure: Pillbox", ItemClassification.progression, 19),
    ItemInfo("Defensive Structure: Barbed Wire", ItemClassification.useful, 20),
    ItemInfo("Defensive Structure: Concrete Wall", ItemClassification.useful, 21),
    ItemInfo("Defensive Structure: Camo Pillbox", ItemClassification.progression, 22),
    ItemInfo("Defensive Structure: Flame Tower", ItemClassification.progression, 23),
    ItemInfo("Defensive Structure: Turret", ItemClassification.progression, 24),
    ItemInfo("Defensive Structure: Tesla Coil", ItemClassification.progression, 25),
    ItemInfo("Defensive Structure: AA Gun", ItemClassification.progression, 26),
    ItemInfo("Defensive Structure: SAM Site", ItemClassification.progression, 27),
    ItemInfo("Defensive Structure: Gap Generator", ItemClassification.useful, 28),
    ItemInfo("Defensive Structure: Chronosphere", ItemClassification.useful, 29),
    ItemInfo("Defensive Structure: Iron Curtain", ItemClassification.useful, 30),
    ItemInfo("Defensive Structure: Missile Silo", ItemClassification.useful, 31),
]

fake_structure_items = [
    # Fake Structures
    ItemInfo("Defensive Structure: Fake Power Plant", ItemClassification.filler, 32),
    ItemInfo("Defensive Structure: Fake Barracks", ItemClassification.filler, 33),
    ItemInfo("Defensive Structure: Fake Naval Yard", ItemClassification.filler, 34),
    ItemInfo("Defensive Structure: Fake Sub Pen", ItemClassification.filler, 35),
    ItemInfo("Defensive Structure: Fake War Factory", ItemClassification.filler, 36),
    ItemInfo("Defensive Structure: Fake Radar Dome", ItemClassification.filler, 37),
    ItemInfo("Defensive Structure: Fake Service Depot", ItemClassification.filler, 38),
    ItemInfo("Defensive Structure: Fake Advanced Power Plant", ItemClassification.filler, 39),
    ItemInfo("Defensive Structure: Fake Tech Center", ItemClassification.filler, 40),
    ItemInfo("Defensive Structure: Fake Chronosphere", ItemClassification.filler, 41),
    ItemInfo("Defensive Structure: Fake Missile Silo", ItemClassification.filler, 42),
    ItemInfo("Defensive Structure: Fake Construction Yard", ItemClassification.filler, 43),
]

infantry_items = [
# Infantry
    ItemInfo("Infantry: Allied Rifle Infantry", ItemClassification.progression, 44),
    ItemInfo("Infantry: Soviet Rifle Infantry", ItemClassification.progression, 45),
    ItemInfo("Infantry: Rocket Soldier", ItemClassification.progression, 46),
    ItemInfo("Infantry: Medic", ItemClassification.useful, 47),
    ItemInfo("Infantry: Allied Grenadier", ItemClassification.progression, 48),
    ItemInfo("Infantry: Soviet Grenadier", ItemClassification.progression, 49),
    ItemInfo("Infantry: Attack Dog", ItemClassification.progression, 50),
    ItemInfo("Infantry: Engineer", ItemClassification.progression, 51),
    ItemInfo("Infantary: Flamethrower", ItemClassification.progression, 52),
    ItemInfo("Infantry: Spy", ItemClassification.progression, 53),
    ItemInfo("Infantry: British Spy", ItemClassification.useful, 54),
    ItemInfo("Infantry: Mechanic", ItemClassification.useful, 55),
    ItemInfo("Infantry: Thief", ItemClassification.useful, 56),
    ItemInfo("Infantry: Allied Tanya", ItemClassification.progression, 57),
    ItemInfo("Infantry: Soviet Tanya", ItemClassification.progression, 58),
    ItemInfo("Infantry: Shock Trooper", ItemClassification.progression, 59),
    ItemInfo("Infantry: Zombie", ItemClassification.filler, 60),
    ItemInfo("Infantry: Gaint Ant", ItemClassification.filler, 61),
    ItemInfo("Infantry: Fire Ant", ItemClassification.filler, 62),
    ItemInfo("Infantry: Scout Ant", ItemClassification.filler, 63),
    ItemInfo("Infantry: Warrior Ant", ItemClassification.filler, 64),
]

vehicle_items = [
# Vehicle
    ItemInfo("Vehicle: Ore Truck", ItemClassification.progression, 65),
    ItemInfo("Vehicle: Light Tank", ItemClassification.progression, 66),
    ItemInfo("Vehicle: APC", ItemClassification.progression, 67),
    ItemInfo("Vehicle: Ranger", ItemClassification.progression, 68),
    ItemInfo("Vehicle: Mobile Flak", ItemClassification.progression, 69),
    ItemInfo("Vehicle: MCV", ItemClassification.progression, 70),
    ItemInfo("Vehicle: Medium Tank", ItemClassification.progression, 71),
    ItemInfo("Vehicle: Heavy Tank", ItemClassification.progression, 72),
    ItemInfo("Vehicle: V2 Rocket", ItemClassification.progression, 73),
    ItemInfo("Vehicle: Artillery", ItemClassification.progression, 74),
    ItemInfo("Vehicle: Mine Layer", ItemClassification.progression, 75),
    ItemInfo("Vehicle: Mammoth Tank", ItemClassification.progression, 76),
    ItemInfo("Vehicle: Radar Jammer", ItemClassification.useful, 77),
    ItemInfo("Vehicle: Mobile Gap Generator", ItemClassification.useful, 78),
    ItemInfo("Vehicle: Tesla Tank", ItemClassification.progression, 79),
    ItemInfo("Vehicle: Demolition Truck", ItemClassification.progression, 80),
    ItemInfo("Vehicle: Chrono Tank", ItemClassification.progression, 81),
    ItemInfo("Vehicle: Phase Transport", ItemClassification.progression, 82),
    ItemInfo("Vehicle: Supply Truck", ItemClassification.filler, 83),
    ItemInfo("Vehicle: M.A.D. Tank", ItemClassification.progression, 84),
]

aircraft_items = [
    # Aircraft
    ItemInfo("Aircraft: Chinook", ItemClassification.useful, 85),
    ItemInfo("Aircraft: Hind", ItemClassification.progression, 86),
    ItemInfo("Aircraft: Blackhawk", ItemClassification.progression, 87),
    ItemInfo("Aircraft: Yak", ItemClassification.progression, 88),
    ItemInfo("Aircraft: Longbow", ItemClassification.progression, 89),
    ItemInfo("Aircraft: Mig", ItemClassification.progression, 90),
]

naval_items = [
    # Naval
    ItemInfo("Naval: Transport", ItemClassification.progression, 91),
    ItemInfo("Naval: Gunboat", ItemClassification.progression, 92),
    ItemInfo("Naval: Submarine", ItemClassification.progression, 93),
    ItemInfo("Naval: Destroyer", ItemClassification.progression, 94),
    ItemInfo("Naval: Cruiser", ItemClassification.progression, 95),
    ItemInfo("Naval: Missile Sub", ItemClassification.progression, 96),
]

mission_unlocks = {
    "Allied Campaign": [
        ItemInfo("Mission Unlock: In the Thick of It (Allied Campaign)", ItemClassification.progression, 97),
        ItemInfo("Mission Unlock: Five to One (Allied Campaign)", ItemClassification.progression, 98),
        ItemInfo("Mission Unlock: Ten to One (Allied Campaign)", ItemClassification.progression, 102),
        ItemInfo("Mission Unlock: Sunken Treasure (Allied Campaign)", ItemClassification.progression, 110),
        ItemInfo("Mission Unlock: Evacuate Kosygin (Allied Campaign)", ItemClassification.progression, 114),
        ItemInfo("Mission Unlock: Suspicion (Allied Campaign)", ItemClassification.progression, 115),
        ItemInfo("Mission Unlock: Evidence (Allied Campaign)", ItemClassification.progression, 116),
        ItemInfo("Mission Unlock: Focused Blast (Allied Campaign)", ItemClassification.progression, 117),
    ],
    "Soviet Campaign": [
        ItemInfo("Mission Unlock: Lesson in Blood (Soviet Campaign)", ItemClassification.progression, 118),
        ItemInfo("Mission Unlock: Covert cleanup (Soviet Campaign)", ItemClassification.progression, 122),
        ItemInfo("Mission Unlock: Distant Thunder (Soviet Campaign)", ItemClassification.progression, 126),
        ItemInfo("Mission Unlock: Core of the Matter (Soviet Campaign)", ItemClassification.progression, 130),
        ItemInfo("Mission Unlock: Liability Elimination (Soviet Campaign)", ItemClassification.progression, 134),
        ItemInfo("Mission Unlock: Overseer (Soviet Campaign)", ItemClassification.progression, 135),
    ],
    "Counterstrike Allied Missions": [
        ItemInfo("Mission Unlock: Sarin Gas 1: Crackdown (Counterstrike Allied Missions)", ItemClassification.progression, 142),
        ItemInfo("Mission Unlock: Sarin Gas 2: Down Under (Counterstrike Allied Missions)", ItemClassification.progression, 143),
        ItemInfo("Mission Unlock: Sarin Gas 3: Controlled Burn (Counterstrike Allied Missions)", ItemClassification.progression, 144),
        ItemInfo("Mission Unlock: Fall of Greece 1: Personal War(Counterstrike Allied Missions)", ItemClassification.progression, 145),
        ItemInfo("Mission Unlock: Fall of Greece 2: Evacuation (Counterstrike Allied Missions)", ItemClassification.progression, 146),
        ItemInfo("Mission Unlock: Siberian Conflict 1: Fresh Tracks (Counterstrike Allied Missions)", ItemClassification.progression, 147),
        ItemInfo("Mission Unlock: Siberian Conflict 3: Wasteland (Counterstrike Allied Missions)", ItemClassification.progression, 148),
    ],
    "Counterstrike Soviet Missions": [
        ItemInfo("Mission Unlock: Mousetrap (Counterstrike Soviet Missions)", ItemClassification.progression, 149),
        ItemInfo("Mission Unlock: Soviet Soldier Volkov & Chitzkoi (Counterstrike Soviet Missions)", ItemClassification.progression, 150),
        ItemInfo("Mission Unlock: Top o' the World (Counterstrike Soviet Missions)", ItemClassification.progression, 151),
    ],
    "Aftermath Allied Missions": [
        ItemInfo("Mission Unlock: In the Nick of Time (Aftermath Allied Missions)", ItemClassification.progression, 152),
        ItemInfo("Mission Unlock: Production Disruption (Aftermath Allied Missions)", ItemClassification.progression, 153),
        ItemInfo("Mission Unlock: Monster Tank Madness (Aftermath Allied Missions)", ItemClassification.progression, 154),
        ItemInfo("Mission Unlock: Negotiations (Aftermath Allied Missions)", ItemClassification.progression, 155),
    ],
    "Aftermath Soviet Missions": [
        ItemInfo("Mission Unlock: Shock Therapy (Aftermath Soviet Missions)", ItemClassification.progression, 156),
        ItemInfo("Mission Unlock: Situation Critical (Aftermath Soviet Missions)", ItemClassification.progression, 157),
    ],
    "OpenRA Originals": [
        ItemInfo("Mission Unlock: Evacuation (OpenRA Originals)", ItemClassification.progression, 158),
        ItemInfo("Mission Unlock: Exodus (OpenRA Originals)", ItemClassification.progression, 159),
        ItemInfo("Mission Unlock: Infiltration (OpenRA Originals)", ItemClassification.progression, 160),
        ItemInfo("Mission Unlock: Intervention (OpenRA Originals)", ItemClassification.progression, 161),
        ItemInfo("Mission Unlock: Survival 01 (OpenRA Originals)", ItemClassification.progression, 162),
        ItemInfo("Mission Unlock: Survival 02 (OpenRA Originals)", ItemClassification.progression, 163),
    ],
    "Ant Missions": [
        ItemInfo("Mission Unlock: 01: Discovery (Ant Missions)", ItemClassification.progression, 164),
        ItemInfo("Mission Unlock: 03: Hunt! (Ant Missions)", ItemClassification.progression, 165),
    ]
}

combined_mission_unlocks = {
    "Allied Campaign": [
        ItemInfo("Mission Unlock: Dead End (Allied Campaign)", ItemClassification.progression, 99),
        ItemInfo("Mission Unlock: Tanya's Tale (Allied Campaign)", ItemClassification.progression, 103),
        ItemInfo("Mission Unlock: Cripple Iron Curtain Research (Allied Campaign)", ItemClassification.progression, 107),
        ItemInfo("Mission Unlock: Protect the Chronosphere (Allied Campaign)", ItemClassification.progression, 111),
    ],
    "Soviet Campaign": [
        ItemInfo("Mission Unlock: The Thin Red Line (Soviet Campaign)", ItemClassification.progression, 119),
        ItemInfo("Mission Unlock: Behind the Lines (Soviet Campaign)", ItemClassification.progression, 123),
        ItemInfo("Mission Unlock: Bridge over the River (Soviet Campaign)", ItemClassification.progression, 127),
        ItemInfo("Mission Unlock: Investigate Elba Island (Soviet Campaign)", ItemClassification.progression, 131),
        ItemInfo("Mission Unlock: Sunk Costs (Soviet Campaign)", ItemClassification.progression, 136),
        ItemInfo("Mission Unlock: Capture the Chronosphere (Soviet Campaign)", ItemClassification.progression, 139),
    ],
    "Counterstrike Allied Missions": [],
    "Counterstrike Soviet Missions": [],
    "Aftermath Allied Missions": [],
    "Aftermath Soviet Missions": [],
    "OpenRA Originals": [],
    "Ant Missions": [],
}

split_mission_unlocks = {
    "Allied Campaign": [
        ItemInfo("Mission Unlock: Dead End A (Allied Campaign)", ItemClassification.progression, 100),
        ItemInfo("Mission Unlock: Dead End B (Allied Campaign)", ItemClassification.progression, 101),
        ItemInfo("Mission Unlock: Tanya's Tale A (Allied Campaign)", ItemClassification.progression, 104),
        ItemInfo("Mission Unlock: Tanya's Tale B (Allied Campaign)", ItemClassification.progression, 105),
        ItemInfo("Mission Unlock: Tanya's Tale C (Allied Campaign)", ItemClassification.progression, 106),
        ItemInfo("Mission Unlock: Cripple Iron Curtain Research A (Allied Campaign)", ItemClassification.progression,
                 108),
        ItemInfo("Mission Unlock: Cripple Iron Curtain Research B (Allied Campaign)", ItemClassification.progression,
                 109),
        ItemInfo("Mission Unlock: Protect the Chronosphere A (Allied Campaign)", ItemClassification.progression, 112),
        ItemInfo("Mission Unlock: Protect the Chronosphere B (Allied Campaign)", ItemClassification.progression, 113),
    ],
    "Soviet Campaign": [
        ItemInfo("Mission Unlock: The Thin Red Line A (Soviet Campaign)", ItemClassification.progression, 120),
        ItemInfo("Mission Unlock: The Thin Red Line B (Soviet Campaign)", ItemClassification.progression, 121),
        ItemInfo("Mission Unlock: Behind the Lines A (Soviet Campaign)", ItemClassification.progression, 124),
        ItemInfo("Mission Unlock: Behind the Lines B (Soviet Campaign)", ItemClassification.progression, 125),
        ItemInfo("Mission Unlock: Bridge over the River A (Soviet Campaign)", ItemClassification.progression, 128),
        ItemInfo("Mission Unlock: Bridge over the River B (Soviet Campaign)", ItemClassification.progression, 129),
        ItemInfo("Mission Unlock: Investigate Elba Island A (Soviet Campaign)", ItemClassification.progression, 132),
        ItemInfo("Mission Unlock: Investigate Elba Island B (Soviet Campaign)", ItemClassification.progression, 133),
        ItemInfo("Mission Unlock: Sunk Costs A (Soviet Campaign)", ItemClassification.progression, 137),
        ItemInfo("Mission Unlock: Sunk Costs B (Soviet Campaign)", ItemClassification.progression, 138),
        ItemInfo("Mission Unlock: Capture the Chronosphere A (Soviet Campaign)", ItemClassification.progression, 140),
        ItemInfo("Mission Unlock: Capture the Chronosphere B (Soviet Campaign)", ItemClassification.progression, 141),
    ],
    "Counterstrike Allied Missions": [],
    "Counterstrike Soviet Missions": [],
    "Aftermath Allied Missions": [],
    "Aftermath Soviet Missions": [],
    "OpenRA Originals": [],
    "Ant Missions": [],
}

filler_items = [
    ItemInfo("+500 Starting Ore", ItemClassification.filler, 166)
]

tech_items = structure_items + defensive_structure_items + fake_structure_items + infantry_items + vehicle_items + aircraft_items + naval_items

all_items = ((structure_items + defensive_structure_items + fake_structure_items + infantry_items + vehicle_items
             + aircraft_items + naval_items) +
             [item for sublist in [camp for camp in mission_unlocks.values()] for item in sublist] +
             [item for sublist in [camp for camp in combined_mission_unlocks.values()] for item in sublist] +
             [item for sublist in [camp for camp in split_mission_unlocks.values()] for item in sublist])

class OpenRAItem(Item):
    game = "OpenRA"