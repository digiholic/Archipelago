import json
import logging
import os
from typing import *

from BaseClasses import Item, Tutorial, ItemClassification, Region, Entrance, CollectionState, MultiWorld
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_rule
from .Items import ONIItem, items_by_name, all_items, display_name_to_internal_name
from .Locations import ONILocation, all_locations, location_to_tech_name
from .ModJson import ModJson
from .Names import LocationNames, ItemNames, RegionNames
from .Options import ONIOptions
from .Regions import all_regions
from .Rules import *


class ONIWeb(WebWorld):
    theme = "ice"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Oxygen Not Included Randomizer connected to an Archipelago Multiworld",
        "English",
        "docs/setup_en.md",
        "setup/en",
        ["digiholic"]
    )
    tutorials = [setup_en]


class ONIWorld(World):
    game = "Oxygen Not Included"
    options_dataclass = ONIOptions
    options: ONIOptions
    topology_present = False
    web = ONIWeb()
    base_id = 0x257514000  # 0xYGEN___, clever! Thanks, Medic
    data_version = 0

    item_name_to_id = {data.itemName: 0x257514000 + index for index, data in enumerate(all_items)}
    location_name_to_id = {loc_name: 0x257514000 + index for index, loc_name in enumerate(all_locations)}

    def generate_early(self) -> None:
        """
        Run before any general steps of the MultiWorld other than options. Useful for getting and adjusting option
        results and determining layouts for entrance rando etc. start inventory gets pushed after this step.
        """
        pass

    def create_regions(self) -> None:
        """Method for creating and connecting regions for the World."""
        regions_by_name = {}

        for region_info in all_regions:
            region = Region(region_info.name, self.player, self.multiworld)
            regions_by_name[region_info.name] = region
            for location_name in region_info.locations:
                location = ONILocation(self.player, location_name, self.location_name_to_id.get(location_name, None),
                                       region)
                region.locations.append(location)
            self.multiworld.regions.append(region)

        regions_by_name["Menu"].connect(
            regions_by_name[RegionNames.Basic], None, None)
        regions_by_name[RegionNames.Basic].connect(
            regions_by_name[RegionNames.Advanced], None, lambda state: can_advanced_research(self.player, state))
        regions_by_name[RegionNames.Advanced].connect(
            regions_by_name[RegionNames.Nuclear], None, lambda state: can_nuclear_research(self.player, state))
        regions_by_name[RegionNames.Nuclear].connect(
            regions_by_name[RegionNames.Space_DLC], None, lambda state: can_space_research(self.player, state))

    def create_items(self) -> None:
        """
        Method for creating and submitting items to the itempool. Items and Regions must *not* be created and submitted
        to the MultiWorld after this step. If items need to be placed during pre_fill use `get_prefill_items`.
        """
        for item in all_items:
            self.multiworld.itempool.append(self.create_item(item.itemName))

    def set_rules(self) -> None:
        """Method for setting the rules on the World's regions and locations."""
        pass

    def generate_basic(self) -> None:
        """
        Useful for randomizing things that don't affect logic but are better to be determined before the output stage.
        i.e. checking what the player has marked as priority or randomizing enemies
        """
        pass

    def pre_fill(self) -> None:
        """Optional method that is supposed to be used for special fill stages. This is run *after* plando."""
        pass

    def fill_hook(self,
                  progitempool: List["Item"],
                  usefulitempool: List["Item"],
                  filleritempool: List["Item"],
                  fill_locations: List["Location"]) -> None:
        """Special method that gets called as part of distribute_items_restrictive (main fill)."""
        pass

    def post_fill(self) -> None:
        """Optional Method that is called after regular fill. Can be used to do adjustments before output generation.
        This happens before progression balancing, so the items may not be in their final locations yet."""

    def generate_output(self, output_directory: str) -> None:
        """This method gets called from a threadpool, do not use multiworld.random here.
        If you need any last-second randomization, use self.random instead."""
        # TODO generate mod json
        science_dicts = {}
        item_names = [data.itemName for data in all_items]
        for location_name in all_locations:
            tech_name = location_to_tech_name[location_name]
            if tech_name not in science_dicts:
                science_dicts[tech_name] = []

            location = self.multiworld.get_location(location_name, self.player)
            ap_item = location.item
            if ap_item is not None and ap_item.name in item_names:
                science_dicts[tech_name].append(display_name_to_internal_name[ap_item.name])

        mod_json = ModJson(self.multiworld.seed, self.multiworld.player_name[self.player], science_dicts)
        json_string = json.dumps(mod_json, indent=4)
        output_file_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.json")
        with open(output_file_path, "w") as file:
            file.write(json_string)


    def fill_slot_data(self) -> Dict[str, Any]:  # json of WebHostLib.models.Slot
        """Fill in the `slot_data` field in the `Connected` network package.
        This is a way the generator can give custom data to the client.
        The client will receive this as JSON in the `Connected` response.

        The generation does not wait for `generate_output` to complete before calling this.
        `threading.Event` can be used if you need to wait for something from `generate_output`."""
        return {}

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        """Fill in additional entrance information text into locations, which is displayed when hinted.
        structure is {player_id: {location_id: text}} You will need to insert your own player_id."""
        pass

    def modify_multidata(self, multidata: Dict[str, Any]) -> None:  # TODO: TypedDict for multidata?
        """For deeper modification of server multidata."""
        pass

    def create_item(self, name: str) -> "Item":
        """Create an item for this world type and player.
        Warning: this may be called with self.world = None, for example by MultiServer"""
        item = items_by_name[name]
        return ONIItem(item.itemName, item.progression, self.item_name_to_id[name], self.player)
