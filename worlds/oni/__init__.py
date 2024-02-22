import logging
from typing import *

from BaseClasses import Item, Tutorial, ItemClassification, Region, Entrance, CollectionState, MultiWorld
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_rule
from .Names import LocationNames, ItemNames, RegionNames
from .Options import ONIOptions


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
    base_id = 0x820000
    data_version = 0

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)

    def generate_early(self) -> None:
        """
        Run before any general steps of the MultiWorld other than options. Useful for getting and adjusting option
        results and determining layouts for entrance rando etc. start inventory gets pushed after this step.
        """
        pass

    def create_regions(self) -> None:
        """Method for creating and connecting regions for the World."""
        pass

    def create_items(self) -> None:
        """
        Method for creating and submitting items to the itempool. Items and Regions must *not* be created and submitted
        to the MultiWorld after this step. If items need to be placed during pre_fill use `get_prefill_items`.
        """
        pass

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
        pass

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
        raise NotImplementedError

    def get_filler_item_name(self) -> str:
        """Called when the item pool needs to be filled with additional items to match location count."""
        logging.warning(f"World {self} is generating a filler item without custom filler pool.")
        return self.multiworld.random.choice(tuple(self.item_name_to_id.keys()))