from BaseClasses import Tutorial, Region
from worlds.AutoWorld import WebWorld
from .items import OpenRAItem
from .locations import OpenRALocation

from .options import option_groups, option_presets
from collections.abc import Mapping
from typing import Any

# Imports of base Archipelago modules must be absolute.
from worlds.AutoWorld import World

# Imports of your world's files must be relative.
from . import items, locations, regions, rules
from . import options as openra_options  # rename due to a name conflict with World.options

# For our game to display correctly on the website, we need to define a WebWorld subclass.
class OpenRAWebWorld(WebWorld):
    # We need to override the "game" field of the WebWorld superclass.
    # This must be the same string as the regular World class.
    game = "OpenRA"

    # Your game pages will have a visual theme (affecting e.g. the background image).
    # You can choose between dirt, grass, grassFlowers, ice, jungle, ocean, partyTime, and stone.
    theme = "grass"

    # A WebWorld can have any number of tutorials, but should always have at least an English setup guide.
    # Many WebWorlds just have one setup guide, but some have multiple, e.g. for different languages.
    # We need to create a Tutorial object for every setup guide.
    # In order, we need to provide a title, a description, a language, a filepath, a link, and authors.
    # The filepath is relative to a "/docs/" directory in the root folder of your apworld.
    # The "link" parameter is unused, but we still need to provide it.
    setup_en = Tutorial("","","","","",[])

    # We add these tutorials to our WebWorld by overriding the "tutorials" field.
    tutorials = []

    # If we have option groups and/or option presets, we need to specify these here as well.
    option_groups = option_groups
    options_presets = option_presets




class OpenRAWorld(World):
    """
    OpenRA is an open source project that recreates and modernizes classic real time strategy games, like Red Alert, Command & Conquer, and Dune 2000.
    """

    game = "OpenRA"

    web = OpenRAWebWorld()
    options_dataclass = openra_options.OpenRAOptions
    options: openra_options.OpenRAOptions

    # Our world class must have a static location_name_to_id and item_name_to_id defined.
    # We define these in regions.py and items.py respectively, so we just set them here.
    location_name_to_id = { loc.name: loc.id for loc in locations.all_locations }
    item_name_to_id = { it.name: it.id for it in items.all_items }

    # These aren't used by the multiworld but make our lives easier:
    item_name_to_info = { it.name: it for it in items.all_items }
    location_name_to_info = { loc.name: loc for loc in locations.all_locations }


    # There is always one region that the generator starts from & assumes you can always go back to.
    # This defaults to "Menu", but you can change it by overriding origin_region_name.
    origin_region_name = "Menu"

    # Our world class must have certain functions ("steps") that get called during generation.
    # The main ones are: create_regions, set_rules, create_items.
    # For better structure and readability, we put each of these in their own file.
    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        for loc in locations.all_locations:
            if loc.campaign not in self.options.included_campaigns: continue
            # TODO more regions than one in the future
            location = OpenRALocation(self.player, loc.name, loc.id, menu_region)
            menu_region.locations.append(location)

    def set_rules(self) -> None:
        pass

    def create_items(self) -> None:
        for item in items.tech_items:
            self.multiworld.itempool.append(self.create_item(item.name))
        for campaign in self.options.included_campaigns:
            for item in items.mission_unlocks[campaign]:
                self.multiworld.itempool.append(self.create_item(item.name))
            if self.options.split_mission_type == openra_options.SplitMissionType.option_any:
                for item in items.combined_mission_unlocks[campaign]:
                    self.multiworld.itempool.append(self.create_item(item.name))
            else:
                for item in items.split_mission_unlocks[campaign]:
                    self.multiworld.itempool.append(self.create_item(item.name))


    # Our world class must also have a create_item function that can create any one of our items by name at any time.
    # We also put this in a different file, the same one that create_items is in.
    def create_item(self, name: str) -> items.OpenRAItem:
        item = self.item_name_to_info[name]
        return OpenRAItem(item.name, item.classification, item.id, self.player)

    # For features such as item links and panic-method start inventory, AP may ask your world to create extra filler.
    # The way it does this is by calling get_filler_item_name.
    # For this purpose, your world *must* have at least one infinitely repeatable item (usually filler).
    # You must override this function and return this infinitely repeatable item's name.
    # In our case, we defined a function called get_random_filler_item_name for this purpose in our items.py.
    def get_filler_item_name(self) -> str:
        return "+500 Starting Ore"

    # There may be data that the game client will need to modify the behavior of the game.
    # This is what slot_data exists for. Upon every client connection, the slot's slot_data is sent to the client.
    # slot_data is just a dictionary using basic types, that will be converted to json when sent to the client.
    def fill_slot_data(self) -> Mapping[str, Any]:
        # If you need access to the player's chosen options on the client side, there is a helper for that.
        return self.options.as_dict(
            "included_campaigns", "split_mission_type", "enable_cross_faction_tech", "enable_ant_tech", "number_of_campaigns", "campaign_clear_condition"
        )
