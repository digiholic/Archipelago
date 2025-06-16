import typing

from BaseClasses import Item, Tutorial, ItemClassification, Region, MultiWorld, CollectionState,Entrance
from rule_builder import *
from Fill import fill_restrictive, FillError
from worlds.AutoWorld import WebWorld, World
from .Items import OSRSItem, starting_area_dict, chunksanity_starting_chunks, QP_Items, ItemRow, \
    chunksanity_special_region_names
from .Locations import OSRSLocation
from .Rules import *
from .Options import OSRSOptions, StartingArea
from .Names import LocationNames, ItemNames, RegionNames
from Utils import visualize_regions

from .LogicCSV.LogicCSVToPython import data_csv_tag
#from .LogicCSV.items_generated import item_rows
#from .LogicCSV.locations_generated import location_rows
#from .LogicCSV.regions_generated import region_rows
#from .LogicCSV.resources_generated import resource_rows
from .LogicCSV.regions_generated2 import region_rows,item_rows,location_rows,resource_rows,rr_entrances,re_entrances,ee_entrances,rm_entrances,me_entrances,sub_quests,quests,non_quests,training_methods,non_monster_drops,monster_drops,mm_entrances
from .Regions import RegionRow, ResourceRow, DropElement, MonsterRow, RuleElement, RewardElement, LocationRow, EntranceRow, TrainingRow

from typing import Callable

class OSRSWeb(WebWorld):
    theme = "stone"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Old School Runescape Randomizer connected to an Archipelago Multiworld",
        "English",
        "docs/setup_en.md",
        "setup/en",
        ["digiholic"]
    )
    tutorials = [setup_en]

base_id = 0x070000

class OSRSWorld(RuleWorldMixin, World):
    """
    The best retro fantasy MMORPG on the planet. Old School is RuneScape but… older! This is the open world you know and love, but as it was in 2007.
    The Randomizer takes the form of a Chunk-Restricted f2p Ironman that takes a brand new account up through defeating
    the Green Dragon of Crandor and earning a spot in the fabled Champion's Guild!
    """

    game = "Old School Runescape"
    options_dataclass = OSRSOptions
    options: OSRSOptions
    topology_present = True
    web = OSRSWeb()
    base_id = base_id
    data_version = 1
    explicit_indirect_conditions = False

    item_name_to_id = {item_rows[i].name: base_id + i for i in range(len(item_rows))}
    location_name_to_id = {location_rows[i].name: base_id + i for i in range(len(location_rows))}

    region_name_to_data: typing.Dict[str, Region]
    location_name_to_data: typing.Dict[str, OSRSLocation]

    location_rows_by_name: typing.Dict[str, LocationRow]
    region_rows_by_name: typing.Dict[str, RegionRow]
    resource_rows_by_name: typing.Dict[str, ResourceRow]
    monster_rows_by_name: typing.Dict[str, MonsterRow]
    item_rows_by_name: typing.Dict[str, ItemRow]

    starting_area_item: str

    locations_by_category: typing.Dict[str, typing.List[LocationRow]]
    available_QP_locations: typing.List[str]

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.region_name_to_data = {}
        self.location_name_to_data = {}

        self.location_rows_by_name = {}
        self.region_rows_by_name = {}
        self.resource_rows_by_name = {}
        self.item_rows_by_name = {}

        self.starting_area_item = ""

        self.locations_by_category = {}
        self.available_QP_locations = []

    def generate_early(self) -> None:
        location_categories = [location_row.category for location_row in location_rows]
        self.locations_by_category = {category:
                                          [location_row for location_row in location_rows if
                                           location_row.category == category]
                                      for category in location_categories}

        self.location_rows_by_name = {loc_row.name: loc_row for loc_row in location_rows}
        self.region_rows_by_name = {reg_row.name: reg_row for reg_row in region_rows}
        self.resource_rows_by_name = {rec_row.name: rec_row for rec_row in resource_rows}
        self.item_rows_by_name = {it_row.name: it_row for it_row in item_rows}
        self.monster_rows_by_name = {it_row.name: it_row for it_row in monster_drops}

        self.starting_area_item = "Area: Lumbridge Castle"

        self.multiworld.push_precollected(self.create_item(self.starting_area_item))

    """
    This function pulls from LogicCSVToPython so that it sends the correct tag of the repository to the client.
    _Make sure to update that value whenever the CSVs change!_
    """

    def fill_slot_data(self):
        data = self.options.as_dict("brutal_grinds")
        data["data_csv_tag"] = data_csv_tag
        data["starting_area"] = str(self.starting_area_item) #these aren't actually strings, they just play them on tv
        return data

    def interpret_slot_data(self, slot_data: typing.Dict[str, typing.Any]) -> None:
        if "starting_area" in slot_data:
            self.starting_area_item = slot_data["starting_area"]
            menu_region = self.multiworld.get_region("Menu",self.player)
            menu_region.exits.clear() #prevent making extra exits if players just reconnect to a differnet slot
            if self.starting_area_item in chunksanity_special_region_names:
                starting_area_region = chunksanity_special_region_names[self.starting_area_item]
            else:
                starting_area_region = self.starting_area_item[6:]  # len("Area: ")
            starting_entrance = menu_region.create_exit(f"Start->{starting_area_region}")
            starting_entrance.access_rule = lambda state: state.has(self.starting_area_item, self.player)
            starting_entrance.connect(self.region_name_to_data[starting_area_region])

    def parse_rule(self, rule_element: RuleElement):
        if rule_element.type == "has": #literal ap item has
            return Has(rule_element.value)
        elif rule_element.type == "task":
            return Has(rule_element.value)
        elif rule_element.type == "chunk":
            return CanReachRegion(rule_element.value)
        elif rule_element.type == "can_reach":
            return CanReachRegion(rule_element.value)
        elif rule_element.type == "kill":
            return CanReachRegion(rule_element.value)
        else:
            return None


    def generate_lambda(self, rule_list:list[RuleElement]):
        output_list = []
        if not rule_list:
            return None #if it's empty then let AP handle the default
        for rule in rule_list:
            temp_rule = self.parse_rule(rule)
            if temp_rule is not None: output_list.append(temp_rule)
        if len(output_list) > 1:
            return And(*output_list)
        elif len(output_list) == 1:
            return output_list[0]
        else:
            return None #if there's no valid rules, just let the default rule take over


    def create_regions(self) -> None:
        """
        called to place player's regions into the MultiWorld's regions list. If it's hard to separate, this can be done
        during generate_early or basic as well.
        """

        # First, create the "Menu" region to start
        menu_region = self.create_region("Menu")

        for region_row in region_rows:
            self.create_region(region_row.id) #id is the name of the region, name is the name of the item that unlocks it

        for resource_row in resource_rows:
            self.create_region(resource_row.name)
        
        for monster_row in monster_drops:
            self.create_region(monster_row.name)

        # Removes the word "Area: " from the item name to get the region it applies to.
        # I figured tacking "Area: " at the beginning would make it _easier_ to tell apart. Turns out it made it worse
        # if area hasn't been set, then we shouldn't connect it
        if self.starting_area_item != "":
            starting_area_region = self.item_rows_by_name[self.starting_area_item].cannonical_chunk
            assert starting_area_region is not None
            starting_entrance = menu_region.create_exit(f"Start->{starting_area_region}")
            starting_entrance.access_rule = lambda state: state.has(self.starting_area_item, self.player)
            starting_entrance.connect(self.region_name_to_data[starting_area_region])


        for location in location_rows:
            self.create_location(location)
        for sub_location in sub_quests:
            self.create_location(sub_location)

        #visualize_regions(self.region_name_to_data["chunk_11937"],"osrs_regions.puml",show_locations=False,show_entrance_names=False,show_other_regions=False)
    
    def set_rules(self):
        rr_entrances_cache:dict[str,tuple[Entrance,list]] = {}
        rr_entrances_cache_miss: list[str] = []

        for entrance in rr_entrances: #Region to Region connections
            sourceRegion = self.region_name_to_data[entrance.source]
            destRegion = self.region_name_to_data[entrance.dest]
            entrance_name = f"{sourceRegion.name} -> {destRegion.name}"
            if entrance_name in rr_entrances_cache:
                if entrance.rule:
                    temp_rule = self.generate_lambda(entrance.rule)
                    if temp_rule is not None: rr_entrances_cache[entrance_name][1].append(temp_rule)
                if entrance_name not in rr_entrances_cache_miss:
                    rr_entrances_cache_miss.append(entrance_name)
            else:
                temp_rule = self.generate_lambda(entrance.rule)
                if temp_rule is not None:
                    rr_entrances_cache[entrance_name] = (sourceRegion.connect(destRegion,entrance_name),[temp_rule])
                else:
                    rr_entrances_cache[entrance_name] = (sourceRegion.connect(destRegion,entrance_name),[])
        for entrance,rules in rr_entrances_cache.values():
            if len(rules) > 1:
                self.set_rule(entrance,Or(*rules))
            elif len(rules) == 1:
                self.set_rule(entrance,rules[0])
        
        re_entrances_cache:dict[str,tuple[Entrance,list]] = {}
        re_entrances_cache_miss: list[str] = []

        for entrance in re_entrances: #Region to rEsource connections
            sourceRegion = self.region_name_to_data[entrance.source]
            destRegion = self.region_name_to_data[entrance.dest]
            entrance_name = f"{sourceRegion.name} -> {destRegion.name}"
            if entrance_name in re_entrances_cache:
                if entrance.rule:
                    temp_rule = self.generate_lambda(entrance.rule)
                    if temp_rule is not None: re_entrances_cache[entrance_name][1].append(temp_rule)
                if entrance_name not in re_entrances_cache_miss:
                    re_entrances_cache_miss.append(entrance_name)
            else:
                temp_rule = self.generate_lambda(entrance.rule)
                if temp_rule is not None:
                    re_entrances_cache[entrance_name] = (sourceRegion.connect(destRegion,entrance_name),[temp_rule])
                else:
                    re_entrances_cache[entrance_name] = (sourceRegion.connect(destRegion,entrance_name),[])
        for entrance,rules in re_entrances_cache.values():
            if len(rules) > 1:
                self.set_rule(entrance,Or(*rules))
            elif len(rules) == 1:
                self.set_rule(entrance,rules[0])

        ee_entrances_cache:dict[str,tuple[Entrance,list]] = {}
        ee_entrances_cache_miss:list[str] = []

        for entrance in ee_entrances: #rEsource to rEsource connections
            sourceRegion = self.region_name_to_data[entrance.source]
            destRegion = self.region_name_to_data[entrance.dest]
            entrance_name = f"{sourceRegion.name} -> {destRegion.name}"
            if entrance_name in ee_entrances_cache:
                if entrance.rule:
                    temp_rule = self.generate_lambda(entrance.rule)
                    if temp_rule is not None: ee_entrances_cache[entrance_name][1].append(temp_rule)
                if entrance_name not in ee_entrances_cache_miss:
                    ee_entrances_cache_miss.append(entrance_name)
            else:
                temp_rule = self.generate_lambda(entrance.rule)
                if temp_rule is not None:
                    ee_entrances_cache[entrance_name] = (sourceRegion.connect(destRegion,entrance_name),[temp_rule])
                else:
                    ee_entrances_cache[entrance_name] = (sourceRegion.connect(destRegion,entrance_name),[])
        for entrance,rules in ee_entrances_cache.values():
            if len(rules) > 1:
                self.set_rule(entrance,Or(*rules))
            elif len(rules) == 1:
                self.set_rule(entrance,rules[0])

        me_entrances_cache:dict[str,tuple[Entrance,list]] = {}
        me_entrances_cache_miss:list[str] = []

        for entrance in me_entrances: #rEsource to rEsource connections
            sourceRegion = self.region_name_to_data[entrance.source]
            destRegion = self.region_name_to_data[entrance.dest]
            entrance_name = f"{sourceRegion.name} -> {destRegion.name}"
            if entrance_name in me_entrances_cache:
                if entrance.rule:
                    temp_rule = self.generate_lambda(entrance.rule)
                    if temp_rule is not None: me_entrances_cache[entrance_name][1].append(temp_rule)
                if entrance_name not in me_entrances_cache_miss:
                    me_entrances_cache_miss.append(entrance_name)
            else:
                temp_rule = self.generate_lambda(entrance.rule)
                if temp_rule is not None:
                    me_entrances_cache[entrance_name] = (sourceRegion.connect(destRegion,entrance_name),[temp_rule])
                else:
                    me_entrances_cache[entrance_name] = (sourceRegion.connect(destRegion,entrance_name),[])
        for entrance,rules in me_entrances_cache.values():
            if len(rules) > 1:
                self.set_rule(entrance,Or(*rules))
            elif len(rules) == 1:
                self.set_rule(entrance,rules[0])

        for entrance in rm_entrances: #Region to Monster connections
            sourceRegion = self.region_name_to_data[entrance.source]
            destRegion = self.region_name_to_data[entrance.dest]
            entrance_obj = sourceRegion.connect(destRegion,None)
            rule = self.generate_lambda(entrance.rule)
            if rule is not None: self.set_rule(entrance_obj,rule)

        for entrance in mm_entrances: #Monster to Monster connections
            sourceRegion = self.region_name_to_data[entrance.source]
            destRegion = self.region_name_to_data[entrance.dest]
            entrance_obj = sourceRegion.connect(destRegion,None)
            rule = self.generate_lambda(entrance.rule)
            if rule is not None: self.set_rule(entrance_obj,rule)
        
        for monster in monster_drops:
            assert isinstance(monster, MonsterRow)
            for drop in monster.drops:
                sourceRegion = self.region_name_to_data[monster.name]
                dest_name = drop.dest
                if "(noted)" in dest_name:
                    destRegion = self.region_name_to_data[drop.dest[:-8]]
                else:
                    destRegion = self.region_name_to_data[drop.dest]
                entrance_name = f"{sourceRegion.name} -> {dest_name}"
                sourceRegion.connect(destRegion,entrance_name,None) #todo: make drop rates matter

        for non_monster in non_monster_drops:
            assert isinstance(non_monster, MonsterRow)
            for drop in non_monster.drops:
                sourceRegion = self.region_name_to_data[non_monster.name]
                dest_name = drop.dest
                if "(noted)" in dest_name:
                    destRegion = self.region_name_to_data[drop.dest[:-8]]
                else:
                    destRegion = self.region_name_to_data[drop.dest]
                entrance_name = f"{sourceRegion.name} -> {dest_name}"
                sourceRegion.connect(destRegion,entrance_name,None) #todo: make drop rates matter

        for location_row in location_rows:
            if location_row.rule:
                location = self.multiworld.get_location(location_row.name,self.player)
                rule = self.generate_lambda(location_row.rule)
                if rule is not None:
                    self.set_rule(location,rule)
                    fake_location = self.multiworld.get_location(location_row.name+" event",self.player)
                    fake_location.access_rule = location.access_rule
                    if location_row.category == "quest" and location_row.quest_point_reward > 0:
                        qp_loc = self.multiworld.get_location("Points: " + location_row.name,self.player)
                        qp_loc.access_rule = location.access_rule
        for location_row in sub_quests:
            if location_row.rule:
                location = self.multiworld.get_location(location_row.name,self.player)
                rule = self.generate_lambda(location_row.rule)
                if rule is not None:
                    self.set_rule(location,rule)

        # place "Victory" at "Dragon Slayer" and set collection as win condition
        self.multiworld.get_location("~|Dragon Slayer I|~ Complete the quest", self.player) \
            .place_locked_item(self.create_item("Area: Victory"))
        self.multiworld.completion_condition[self.player] = lambda state: (state.has("~|Combat Achievements#Elite|~ Vardorvis Adept", self.player))

    def create_items(self) -> None:
        itempool = []
        for item_row in item_rows:
            if item_row.name not in [self.starting_area_item]:
                for c in range(item_row.amount):
                    item = self.create_item(item_row.name)
                    itempool.append(item)

        while len(itempool) < len(self.multiworld.get_unfilled_locations(self.player)):
            itempool.append(self.create_filler())

        self.multiworld.itempool += itempool

    def get_filler_item_name(self) -> str:
        return "Area: Nothing :("

    def create_location(self, location_row:LocationRow):
        if location_row.category == "goal" or location_row.category == "subquest":
            location_id = None
        elif location_row.name not in self.location_name_to_id:
            print(location_row.name)
            breakpoint()
            exit()
        else:
            location_id = self.location_name_to_id[location_row.name]
        location = OSRSLocation(self.player,location_row.name,location_id)
        self.location_name_to_data[location_row.name] = location

        region = self.region_name_to_data["Menu"]
        if location_row.parent_region:
            region = self.region_name_to_data[location_row.parent_region]
        location.parent_region = region
        region.locations.append(location)

        if location_row.category == "subquest":
            location.place_locked_item(self.create_event(location_row.name))
        else:
            fake_location = OSRSLocation(self.player,location_row.name+" event",location_id)
            fake_location.parent_region = region
            region.locations.append(fake_location)
        if location_row.category == "quest" and location_row.quest_point_reward > 0:
            qp_name = "Points: " + location_row.name
            qp_loc = OSRSLocation(self.player,qp_name,None)
            self.location_name_to_data[qp_name] = qp_loc
            qp_loc.parent_region = region
            qp_loc.place_locked_item(self.create_event(f"{location_row.quest_point_reward} QP ({location_row.name})"))
            region.locations.append(qp_loc)

    def create_region(self, name: str) -> "Region":
        region = Region(name, self.player, self.multiworld)
        self.region_name_to_data[name] = region
        self.multiworld.regions.append(region)
        return region

    def create_item(self, name: str) -> "Item":
        if name in self.item_rows_by_name:
            item = self.item_rows_by_name[name]
            item_id = None
            if name in self.item_name_to_id:
                item_id = self.item_name_to_id[name]
            return OSRSItem(item.name, item.progression, item_id, self.player)
        raise Exception("Not able to find item "+name)

    def create_event(self, event: str):
        # while we are at it, we can also add a helper to create events
        return OSRSItem(event, ItemClassification.progression, None, self.player)

