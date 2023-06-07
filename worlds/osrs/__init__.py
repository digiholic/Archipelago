from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification, Region, Entrance, \
    LocationProgressType
from worlds.AutoWorld import WebWorld, World

from .Regions import RegionNames, all_regions
from .Items import OSRSItem, ItemNames, all_items, item_table
from .Locations import LocationNames
from .Options import OSRSOptions


class OSRSWeb(WebWorld):
    theme = "stone"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Oldschool Runescape Randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["digiholic"]
    )
    tutorials = [setup_en]


class OSRSWorld(World):
    game = "Old School Runescape"
    option_definitions = OSRSOptions
    topology_present = False

    data_version = 1

    item_name_to_id = {}
    location_name_to_id = {}

    def generate_early(self) -> None:
        # Set Starting Chunk
        self.multiworld.push_precollected(self.create_item(ItemNames.Lumbridge))

    def create_regions(self) -> None:
        """
        called to place player's regions into the MultiWorld's regions list. If it's hard to separate, this can be done
        during generate_early or basic as well.
        """
        name_to_region = {}
        # Gotta loop through once and make all the region objects
        for region_info in all_regions:
            region = Region(region_info.name, self.player, self.multiworld)
            name_to_region[region_info.name] = region
            self.multiworld.regions.append(region)

        # Now set up the entrances and exits
        for region_info in all_regions:
            region = name_to_region[region_info.name]
            for connection in region_info.connections:
                connection_region = name_to_region[connection]
                entrance = Entrance(self.player, connection, region)
                entrance.connect(connection_region)

                # And now, the special rules

                # Karamja is adjacent to Mudskipper point but needs Port Sarim to sail there
                if connection == RegionNames.Karamja:
                    entrance.access_rule = lambda state: state.has(region_info.unlock, self.player) and \
                                                         state.can_reach(RegionNames.Port_Sarim, self.player)
                # You can only reach Crandor if you can reach all the places that are needed for the quest
                elif connection == RegionNames.Crandor:
                    entrance.access_rule = lambda state: state.has(region_info.unlock, self.player) and \
                                                         state.can_reach(RegionNames.South_Of_Varrock, self.player) and \
                                                         state.can_reach(RegionNames.Edgeville, self.player) and \
                                                         state.can_reach(RegionNames.Lumbridge, self.player) and \
                                                         state.can_reach(RegionNames.Rimmington, self.player) and \
                                                         state.can_reach(RegionNames.Monastery, self.player) and \
                                                         (state.can_reach(RegionNames.Dwarven_Mines,
                                                                          self.player) or state.can_reach(
                                                             RegionNames.Falador, self.player)) and \
                                                         state.can_reach(RegionNames.Port_Sarim, self.player) and \
                                                         state.can_reach(RegionNames.Draynor_Village, self.player)
                elif connection == RegionNames.Crafting_Guild:
                    entrance.access_rule = lambda state: state.has(region_info.unlock, self.player) and \
                                                         (state.can_reach(RegionNames.Central_Varrock, self.player) or \
                                                          (state.can_reach(RegionNames.East_Of_Varrock, self.player)))
                else:
                    entrance.access_rule = lambda state: state.has(region_info.unlock, self.player)

                # Thankfully, everything's bi-directional
                region.exits.append(entrance)

    def create_items(self) -> None:
        for item in all_items:
            for i in range(item.count):
                # One of these progressive armors needs to be progression due to Black Knight's Fortress
                if i == 0 and item.itemName == ItemNames.Progressive_Armor:
                    self.multiworld.itempool.append(self.create_item(item.itemName, ItemClassification.progression))
                else:
                    self.multiworld.itempool.append(self.create_item(item.itemName))

    def set_rules(self) -> None:
        """
        called to set access and item rules on locations and entrances.
        """

        # Quest locations
        self.multiworld.get_location(LocationNames.Q_Cooks_Assistant, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Lumbridge, self.player) and
                # Eggs
                (state.can_reach(RegionNames.Lumbridge_Farms, self.player) or state.can_reach(RegionNames.Falador_Farm,
                                                                                              self.player)) and
                # Wheat
                (state.can_reach(RegionNames.Lumbridge_Farms, self.player) or
                 (state.can_reach(RegionNames.West_Varrock, self.player) and state.can_reach(
                     RegionNames.East_Of_Varrock, self.player)))
        )
        self.multiworld.get_location(LocationNames.Q_Demon_Slayer, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Central_Varrock, self.player) and
                state.can_reach(RegionNames.Varrock_Palace, self.player) and
                state.can_reach(RegionNames.Wizards_Tower, self.player) and
                state.can_reach(RegionNames.South_Of_Varrock, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_Restless_Ghost, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Lumbridge, self.player) and
                state.can_reach(RegionNames.Lumbridge_Swamp, self.player) and
                state.can_reach(RegionNames.Wizards_Tower, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_Romeo_Juliet, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Central_Varrock, self.player) and
                state.can_reach(RegionNames.Varrock_Palace, self.player) and
                state.can_reach(RegionNames.South_Of_Varrock, self.player) and
                state.can_reach(RegionNames.West_Varrock, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_Sheep_Shearer, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Lumbridge_Farms, self.player) and
                # f2p Spinning Wheels
                (state.can_reach(RegionNames.Lumbridge, self.player) or
                 state.can_reach(RegionNames.Falador,self.player) or
                 state.can_reach(RegionNames.Crafting_Guild, self.player) or
                 state.can_reach(RegionNames.Barbarian_Village, self.player))
        )
        self.multiworld.get_location(LocationNames.Q_Shield_of_Arrav, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Central_Varrock, self.player) and
                state.can_reach(RegionNames.Varrock_Palace, self.player) and
                state.can_reach(RegionNames.South_Of_Varrock, self.player) and
                state.can_reach(RegionNames.West_Varrock, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_Ernest_the_Chicken, self.player).access_rule = lambda state: (
            state.can_reach(RegionNames.Draynor_Manor, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_Vampyre_Slayer, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Draynor_Village, self.player) and
                state.can_reach(RegionNames.Central_Varrock, self.player) and
                state.can_reach(RegionNames.Draynor_Manor, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_Imp_Catcher, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Wizards_Tower, self.player) and
                # imp spawns
                (state.can_reach(RegionNames.Draynor_Village, self.player) or
                 state.can_reach(RegionNames.Rimmington, self.player) or
                 state.can_reach(RegionNames.Central_Varrock, self.player) or
                 state.can_reach(RegionNames.Edgeville, self.player) or
                 state.can_reach(RegionNames.Lumbridge, self.player) or
                 state.can_reach(RegionNames.Lumbridge_Farms, self.player) or
                 state.can_reach(RegionNames.Falador, self.player) or
                 state.can_reach(RegionNames.Al_Kharid, self.player) or
                 state.can_reach(RegionNames.Falador_Farm, self.player) or
                 state.can_reach(RegionNames.Karamja, self.player)
                 )
        )
        self.multiworld.get_location(LocationNames.Q_Prince_Ali_Rescue, self.player).access_rule = lambda state: (
            state.can_reach(RegionNames.Al_Kharid, self.player) and
            state.can_reach(RegionNames.Central_Varrock, self.player) and
            # Bronze and clay
            (state.can_reach(RegionNames.South_Of_Varrock, self.player) or
             state.can_reach(RegionNames.Rimmington) or
             state.can_reach(RegionNames.Dwarven_Mines) or
             state.can_reach(RegionNames.Falador)
             ) and
            state.can_reach(RegionNames.Lumbridge_Farms, self.player) and
            # Spinning Wheels
            (state.can_reach(RegionNames.Lumbridge, self.player) or
             state.can_reach(RegionNames.Falador, self.player) or
             state.can_reach(RegionNames.Crafting_Guild, self.player) or
             state.can_reach(RegionNames.Barbarian_Village, self.player)) and
            state.can_reach(RegionNames.Draynor_Village, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_Dorics_Quest, self.player).access_rule = lambda state: (
            # All mineables can be found in the Dwarven Mines, where this quest is. No fancy checks needed
            state.can_reach(RegionNames.Dwarven_Mines, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_Black_Knights_Fortress, self.player).access_rule = lambda state: (
            # Non-Draynor Cabbage
            (state.can_reach(RegionNames.Edgeville, self.player) or
             state.can_reach(RegionNames.Falador_Farm, self.player)) and
            state.has(ItemNames.Progressive_Armor, self.player) and
            state.can_reach(RegionNames.Falador, self.player) and
            state.can_reach(RegionNames.Monastery, self.player) and
            state.can_reach(RegionNames.Ice_Mountain, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_Witchs_Potion, self.player).access_rule = lambda state: (
            state.can_reach(RegionNames.Rimmington, self.player) and
            state.can_reach(RegionNames.Port_Sarim, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_Knights_Sword, self.player).access_rule = lambda state: (
            state.can_reach(RegionNames.Falador, self.player) and
            state.can_reach(RegionNames.Varrock_Palace, self.player) and
            state.can_reach(RegionNames.Mudskipper_Point, self.player) and
            state.can_reach(RegionNames.South_Of_Varrock, self.player) and
            (state.can_reach(RegionNames.Lumbridge_Farms) or state.can_reach(RegionNames.West_Varrock))
        )
        self.multiworld.get_location(LocationNames.Q_Goblin_Diplomacy, self.player).access_rule = lambda state: (
            state.can_reach(RegionNames.Ice_Mountain, self.player) and
            state.can_reach(RegionNames.Draynor_Village, self.player) and
            state.can_reach(RegionNames.Falador, self.player) and
            state.can_reach(RegionNames.South_Of_Varrock, self.player) and
            (state.can_reach(RegionNames.Lumbridge_Farms) or state.can_reach(RegionNames.Rimmington))
        )
        self.multiworld.get_location(LocationNames.Q_Pirates_Treasure, self.player).access_rule = lambda state: (
            state.can_reach(RegionNames.Port_Sarim, self.player) and
            state.can_reach(RegionNames.Karamja, self.player) and
            state.can_reach(RegionNames.Falador, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_Rune_Mysteries, self.player).access_rule = lambda state: (
            state.can_reach(RegionNames.Lumbridge, self.player) and
            state.can_reach(RegionNames.Wizards_Tower, self.player) and
            state.can_reach(RegionNames.Central_Varrock, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_Misthalin_Mystery, self.player).access_rule = lambda state: (
            state.can_reach(RegionNames.Lumbridge_Swamp, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_Corsair_Curse, self.player).access_rule = lambda state: (
            state.can_reach(RegionNames.Falador_Farm, self.player) and
            state.can_reach(RegionNames.Corsair_Cove, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_X_Marks_the_Spot, self.player).access_rule = lambda state: (
            state.can_reach(RegionNames.Lumbridge, self.player) and
            state.can_reach(RegionNames.Draynor_Village, self.player) and
            state.can_reach(RegionNames.Port_Sarim, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_Below_Ice_Mountain, self.player).access_rule = lambda state: (
            state.can_reach(RegionNames.Dwarven_Mines, self.player) and
            state.can_reach(RegionNames.Ice_Mountain, self.player) and
            state.can_reach(RegionNames.Barbarian_Village, self.player) and
            state.can_reach(RegionNames.Falador, self.player) and
            state.can_reach(RegionNames.Central_Varrock, self.player) and
            state.can_reach(RegionNames.Edgeville, self.player)
        )
        
        # self.multiworld.get_location(, self.player).access_rule = lambda state:

    def create_item(self, name: str, progression: ItemClassification = None) -> "Item":
        item = item_table[name]
        if progression is None:
            progression = item.progression
        return OSRSItem(item.itemName, progression, item.id, self.player)

    def create_event(self, event: str):
        # while we are at it, we can also add a helper to create events
        return OSRSItem(event, ItemClassification.progression, None, self.player)
