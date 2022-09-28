import os
import typing
import math
import threading


from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification, Region, RegionType, Entrance
from ..AutoWorld import WebWorld, World
from .Items import MMBN3Item, ItemData, item_table, all_items
from .Locations import MMBN3Location, all_locations, setup_locations, location_table
from .Options import MMBN3Options
from .Regions import regions
from .Names import ItemName, LocationName
from worlds.generic.Rules import add_rule, set_rule


class MMBN3Web(WebWorld):
    theme = "ice"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the MegaMan Battle Network 3 Randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["digiholic"]
    )
    tutorials = [setup_en]


class MMBN3World(World):
    """
    Play as Lan and MegaMan to stop the evil organization WWW led by the nefarious
    Dr. Wily in their plans to take over the Net! Collect BattleChips, Customize your Navi,
    and utilize powerful Style Changes to grow strong enough to take on the greatest
    threat the Internet has ever faced!
    """
    game: str = "MegaMan Battle Network 3"
    option_definitions = MMBN3Options
    topology_present = False
    remote_items = False
    remote_start_inventory = False

    data_version = 0

    base_id = 0xB31000
    item_name_to_id: typing.Dict[str, int] = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {locData.name: locData.id for locData in all_locations}

    web = MMBN3Web()

    def __init__(self, world: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(world, player)

    def create_item(self, name: str) -> "Item":
        item = Items.item_table[name]
        return MMBN3Item(item.itemName, item.progression, item.code, self.player)

    def generate_output(self, output_directory: str) -> None:
        pass

    def generate_early(self) -> None:
        """
        called per player before any items or locations are created. You can set properties on your world here.
        Already has access to player options and RNG.
        """
        pass

    def create_regions(self) -> None:
        """
        called to place player's regions into the MultiWorld's regions list. If it's hard to separate, this can be done
        during generate_early or basic as well.
        """
        name_to_region = {}
        for region_info in regions:
            region = Region(region_info.name, RegionType.Generic, region_info.name, self.player, self.world)
            name_to_region[region_info.name] = region
            for location in region_info.locations:
                region.locations.append(MMBN3Location(self.player, location,
                                                      self.location_name_to_id[location], region))
            self.world.regions.append(region)
        for region_info in regions:
            region = name_to_region[region_info.name]
            for connection in region_info.connections:
                connection_region = name_to_region[connection]
                entrance = Entrance(self.player, connection, region)
                entrance.connect(connection_region)
                if connection == "Undernet":
                    entrance.access_rule = lambda state: state.has(ItemName.HPMemory, self.player, 5)
                if connection == "Secret Area":
                    entrance.access_rule = lambda state: state.has(ItemName.HPMemory, self.player, 15)
                if connection == "WWW Island":
                    entrance.access_rule = lambda state:\
                        state.has(ItemName.Progressive_Undernet_Rank, self.player, 8) and\
                        state.has(ItemName.HPMemory, self.player, 10)
                region.exits.append(entrance)

    def create_items(self) -> None:
        # First add in all progression and useful items
        required_items = [item.itemName for item in all_items if item.progression != ItemClassification.filler]
        self.world.itempool += required_items

        # Then, get a random amount of fillers until we have as many items as we have locations
        filler_items = [item.itemName for item in all_items if item.progression == ItemClassification.filler]
        remaining = len(all_locations) - len(required_items)

        for i in range(remaining):
            self.world.itempool.append(self.world.random.choice(filler_items))

    def set_rules(self) -> None:
        """
        called to set access and item rules on locations and entrances.
        """
        # Set WWW ID requirements
        has_www_id = lambda state: state.has(ItemName.WWW_ID, self.player)
        set_rule(self.world.get_location(LocationName.ACDC_1_PMD, self.player),
                 has_www_id)
        set_rule(self.world.get_location(LocationName.SciLab_1_WWW_BMD),
                 has_www_id)
        set_rule(self.world.get_location(LocationName.Yoka_1_WWW_BMD),
                 has_www_id)
        set_rule(self.world.get_location(LocationName.Undernet_1_WWW_BMD),
                 has_www_id)

        # Set Job additional area access
        # TODO: Once we find a way to restrict overworld access

        # Set Trade quests
        set_rule(self.world.get_location(LocationName.Hades_GrabBack_K_Trade, self.player),
                 lambda state: state.has(ItemName.GrabBack_K, self.player))
        set_rule(self.world.get_location(LocationName.DNN_WideSwrd_C_Trade, self.player),
                 lambda state: state.has(ItemName.WideSwrd_C, self.player))
        set_rule(self.world.get_location(LocationName.Hospital_DynaWav_V_Trade, self.player),
                 lambda state: state.has(ItemName.DynaWave_V, self.player))
        set_rule(self.world.get_location(LocationName.ACDC_Recov120_S_Trade, self.player),
                 lambda state: state.has(ItemName.Recov120_S, self.player))

    def generate_basic(self) -> None:
        """
        called after the previous steps. Some placement and player specific randomizations can be done here. After this
        step all regions and items have to be in the MultiWorld's regions and itempool.
        """
        pass

    """
    pre_fill, fill_hook and post_fill are called to modify item placement before, during and after the regular fill 
    process, before generate_output.
    """
    def pre_fill(self) -> None:
        pass

    def fill_hook(cls,
                  progitempool: typing.List["Item"],
                  usefulitempool: typing.List["Item"],
                  filleritempool: typing.List["Item"],
                  fill_locations: typing.List["Location"]) -> None:
        pass

    def post_fill(self) -> None:
        pass

    """
    fill_slot_data and modify_multidata can be used to modify the data that will be used by the server to host 
    the MultiWorld.
    """
    def fill_slot_data(self) -> typing.Dict[str, typing.Any]:
        pass

    def modify_multidata(self, multidata: typing.Dict[str, typing.Any]) -> None:
        pass

    def assert_generate(cls) -> None:
        """
        is a class method called at the start of generation to check the existence of prerequisite files, usually a ROM
        for games which require one.
        """
        pass
