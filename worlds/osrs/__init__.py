import typing

from BaseClasses import CollectionState, Item, Tutorial, ItemClassification, Region, MultiWorld
from worlds.AutoWorld import WebWorld, World
from Options import OptionError
from .Items import OSRSItem, non_starting_area_dict, starting_area_dict, all_starting_area_dict, chunksanity_starting_chunks, QP_Items, ItemRow, \
    chunksanity_special_region_names
from .Locations import OSRSLocation, LocationRow, task_types
from .Rules import *
from rule_builder.rules import *
from .Options import OSRSOptions, StartingArea
from .Names import LocationNames, ItemNames, RegionNames

from .LogicCSV.LogicCSVToPython import data_csv_tag
from .LogicCSV.items_generated import item_rows
from .LogicCSV.locations_generated import location_rows
from .LogicCSV.regions_generated import region_rows
from .LogicCSV.resources_generated import resource_rows
from .Regions import RegionRow, ResourceRow


class OSRSWeb(WebWorld):
    theme = "stone"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Old School Runescape Randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["digiholic"]
    )
    tutorials = [setup_en]


class OSRSWorld(World):
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
    base_id = 0x070000
    data_version = 1
    explicit_indirect_conditions = False
    ut_can_gen_without_yaml = True

    item_name_to_id = {item_rows[i].name: 0x070000 + i for i in range(len(item_rows))}
    location_name_to_id = {location_rows[i].name: 0x070000 + i for i in range(len(location_rows))}

    region_name_to_data: typing.Dict[str, Region]
    location_name_to_data: typing.Dict[str, OSRSLocation]

    location_rows_by_name: typing.Dict[str, LocationRow]
    region_rows_by_name: typing.Dict[str, RegionRow]
    resource_rows_by_name: typing.Dict[str, ResourceRow]
    item_rows_by_name: typing.Dict[str, ItemRow]

    starting_area_item: str

    locations_by_category: typing.Dict[str, typing.List[LocationRow]]
    available_QP_locations: typing.List[str]

    tracker_world: typing.ClassVar = {
        "map_page_folder": "pack",
        "map_page_maps": "jsons/maps.json",
        "map_page_locations": "jsons/locations.json"
    }

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
        self.bingo_board:list[list[str]] = []

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

        rnd = self.random
        starting_area = self.options.starting_area

        #UT specific override, if we are in normal gen, resolve starting area, we will get it from slot_data in UT
        if not hasattr(self.multiworld, "generation_is_fake"):
            if starting_area.value == StartingArea.option_any_bank:
                self.starting_area_item = rnd.choice(list(starting_area_dict.values()))
            elif starting_area.value == StartingArea.option_no_bank:
                self.starting_area_item = rnd.choice(list(non_starting_area_dict.values()))
            elif starting_area.value == StartingArea.option_chunksanity:
                self.starting_area_item = rnd.choice(chunksanity_starting_chunks)
            else:
                self.starting_area_item = all_starting_area_dict[starting_area.value]

            # Set Starting Chunk
            self.multiworld.push_precollected(self.create_item(self.starting_area_item))

            #setup bingo board
            for _ in range(self.options.bingo_size.value):
                self.bingo_board.append([]) #make the blank rows, we'll put location names in them once we
        elif hasattr(self.multiworld,"re_gen_passthrough") and self.game in self.multiworld.re_gen_passthrough:
            re_gen_passthrough = self.multiworld.re_gen_passthrough[self.game] # UT passthrough
            if re_gen_passthrough["data_csv_tag"] != data_csv_tag:
                raise OptionError(f"Multiworld was generated with CSV tag {re_gen_passthrough['data_csv_tag']} please get that apworld version and try again")
            if "starting_area" in re_gen_passthrough:
                self.starting_area_item = re_gen_passthrough["starting_area"]
            for task_type in task_types:
                if f"max_{task_type}_level" in re_gen_passthrough:
                    getattr(self.options,f"max_{task_type}_level").value = re_gen_passthrough[f"max_{task_type}_level"]
                max_count = getattr(self.options,f"max_{task_type}_tasks")
                max_count.value = max_count.range_end
            self.options.brutal_grinds.value = re_gen_passthrough["brutal_grinds"]
            if "bingo_board" in re_gen_passthrough: #backwards compatibility
                self.bingo_board = re_gen_passthrough["bingo_board"] #type: ignore
                self.options.goal.value = re_gen_passthrough["goal"]
                self.options.bingo_size.value = re_gen_passthrough["bingo_size"]



    """
    This function pulls from LogicCSVToPython so that it sends the correct tag of the repository to the client.
    _Make sure to update that value whenever the CSVs change!_
    """

    def fill_slot_data(self):
        data = self.options.as_dict("brutal_grinds")
        data["data_csv_tag"] = data_csv_tag
        data["starting_area"] = str(self.starting_area_item) #these aren't actually strings, they just play them on tv
        data["goal"] = self.options.goal.value
        data["bingo_size"] = self.options.bingo_size.value
        data["bingo_board"] = self.bingo_board
        for task_type in task_types:
            data[f"max_{task_type}_level"] = getattr(self.options,f"max_{task_type}_level").value
        return data

    @staticmethod
    def interpret_slot_data(slot_data: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        return slot_data

    def create_regions(self) -> None:
        """
        called to place player's regions into the MultiWorld's regions list. If it's hard to separate, this can be done
        during generate_early or basic as well.
        """

        # First, create the "Menu" region to start
        menu_region = self.create_region("Menu")

        for region_row in region_rows:
            self.create_region(region_row.name)

        for resource_row in resource_rows:
            self.create_region(resource_row.name)

        # Removes the word "Area: " from the item name to get the region it applies to.
        # I figured tacking "Area: " at the beginning would make it _easier_ to tell apart. Turns out it made it worse
        # if area hasn't been set, then we shouldn't connect it
        if self.starting_area_item != "":
            if self.starting_area_item in chunksanity_special_region_names:
                starting_area_region = chunksanity_special_region_names[self.starting_area_item]
            else:
                starting_area_region = self.starting_area_item[6:]  # len("Area: ")
            starting_entrance = menu_region.create_exit(f"Start->{starting_area_region}")
            self.set_rule(starting_entrance, Has(self.starting_area_item))
            starting_entrance.connect(self.region_name_to_data[starting_area_region])

        # Create entrances between regions
        for region_row in region_rows:
            region = self.region_name_to_data[region_row.name]

            for outbound_region_name in region_row.connections:
                parsed_outbound = outbound_region_name.replace('*', '')
                entrance = region.create_exit(f"{region_row.name}->{parsed_outbound}")
                entrance.connect(self.region_name_to_data[parsed_outbound])

                item_name = self.region_rows_by_name[parsed_outbound].itemReq
                self.set_rule(entrance,generate_special_rules_for(entrance, region_row, outbound_region_name, self.options,Has(item_name.replace("*",""))))

            for resource_region in region_row.resources:
                if not resource_region:
                    continue

                entrance = region.create_exit(f"{region_row.name}->{resource_region.replace('*', '')}")
                if "*" not in resource_region:
                    entrance.connect(self.region_name_to_data[resource_region])
                else:
                    entrance.connect(self.region_name_to_data[resource_region.replace('*', '')])
                self.set_rule(entrance,generate_special_rules_for(entrance, region_row, resource_region, self.options))

        self.roll_locations()

    def write_spoiler(self, spoiler_handle: typing.TextIO):
        if self.options.goal.value not in [self.options.goal.option_bingo, self.options.goal.option_dragon_slayer_bingo]: return
        max_index = self.options.bingo_size.value
        spoiler_handle.write(f"Bingo Board for Player {self.player_name}\n{' '*49}")
        for i in range(max_index):
            spoiler_handle.write(f"|Bingo: Col {i+1}{' '*37}")
        spoiler_handle.write("\n")
        for i in range(max_index):
            spoiler_handle.write(f"Bingo: Row {i+1}{' '*37}")
            row = self.bingo_board[i]
            for el in row:
                spoiler_handle.write(f"|{el}{' '*(49-len(el))}")
            spoiler_handle.write("\n")
        spoiler_handle.write(f"Forward Diagonal{' '*(50*max_index)}Reverse Diagonal")


    def task_within_skill_levels(self, skills_required):
        # Loop through each required skill. If any of its requirements are out of the defined limit, return false
        for skill in skills_required:
            max_level_for_skill = getattr(self.options, f"max_{skill.skill.lower()}_level")
            if skill.level > max_level_for_skill:
                return False
        return True

    def roll_locations(self):
        generation_is_fake = hasattr(self.multiworld, "generation_is_fake")  # UT specific override
        locations_required = 0
        for item_row in item_rows:
            if item_row.name == self.starting_area_item:
                continue #skip starting area
            # If it's a filler item, set it aside for later
            if item_row.progression == ItemClassification.filler:
                continue

            # If it starts with "Care Pack", only add it if Care Packs are enabled
            if item_row.name.startswith("Care Pack"):
                if not self.options.enable_carepacks:
                    continue
            
            #ignore the bingo items for now
            if item_row.name.startswith("Bingo"):
                continue
            locations_required += item_row.amount
        if self.options.enable_duds: locations_required += self.options.dud_count
        if self.options.goal.value in [self.options.goal.option_bingo, self.options.goal.option_dragon_slayer_bingo]: 
            locations_required += (self.options.bingo_size.value * self.options.bingo_size.value) #square board

        locations_added = 0  # Keep track of the number of locations we add so we don't add more the number of items we're going to make
        pre_locations = [] #Used to keep track of which tasks will be on the bingo board because the player wanted it
        # Quests are always added first, before anything else is rolled
        for i, location_row in enumerate(location_rows):
            if location_row.category in {"quest"}:
                if self.task_within_skill_levels(location_row.skills):
                    self.create_and_add_location(i)
                    locations_added += 1
            elif location_row.category in {"goal"} and self.options.goal.value in [self.options.goal.option_dragon_slayer, self.options.goal.option_dragon_slayer_bingo]:
                if not self.task_within_skill_levels(location_row.skills):
                    raise OptionError(f"Goal location for {self.player_name} not allowed in skill levels") #it doesn't actually have any, but just in case for future
                self.create_and_add_location(i)
        if self.options.goal.value in [self.options.goal.option_bingo, self.options.goal.option_dragon_slayer_bingo]:
            bingo_tasks = [task for task in self.locations_by_category["bingo"]]
            for _ in range(2+(self.options.bingo_size.value * 2)): # diagonals + n rows and cols
                task = bingo_tasks.pop(0) #grab from front
                if self.add_location(task.name):
                    locations_added += 1 
        temp_plando_block = self.options.plando_items.value.copy()
        for opt in temp_plando_block:
            if isinstance(opt.count,int) and opt.count == len(opt.locations) or isinstance(opt.count,bool) and not opt.count:
                for location in opt.locations:
                    # ensure that every legal location plando'd is created
                    if location in self.location_rows_by_name and self.task_within_skill_levels(self.location_rows_by_name[location].skills) and self.add_location(location):
                        locations_added += 1
                        if "Tear of Guthix" in opt.items:
                            pre_locations.append(location)
                            self.options.plando_items.value.remove(opt) #remove Tear of Guthix plandos




        # Build up the weighted Task Pool
        rnd = self.random

        # Start with the minimum general tasks
        general_tasks = [task for task in self.locations_by_category["general"]]
        if not self.options.progressive_tasks:
            rnd.shuffle(general_tasks)
        else:
            general_tasks.reverse()
        general_tasks_added = 0
        while general_tasks_added<self.options.minimum_general_tasks and general_tasks:
            task = general_tasks.pop()
            if self.task_within_skill_levels(task.skills):
                if self.add_location(task.name):
                    locations_added += 1 
                    general_tasks_added += 1
        while generation_is_fake and len(general_tasks)>0:
            task = general_tasks.pop()
            if self.task_within_skill_levels(task.skills):
                if self.add_location(task.name):
                    locations_added += 1 
                    general_tasks_added += 1
        if general_tasks_added < self.options.minimum_general_tasks:
            raise OptionError(f"{self.player_name} doesn't have enough general tasks to create required minimum count"+
                              f", raise maximum skill levels or lower minimum general tasks")

        general_weight = self.options.general_task_weight.value if len(general_tasks) > 0 else 0

        tasks_per_task_type: typing.Dict[str, typing.List[LocationRow]] = {}
        weights_per_task_type: typing.Dict[str, int] = {}
        
        for task_type in task_types:
            max_amount_for_task_type = getattr(self.options, f"max_{task_type}_tasks")
            tasks_for_this_type = [task for task in self.locations_by_category[task_type]
                                   if self.task_within_skill_levels(task.skills)]
            max_amount_for_task_type = min(max_amount_for_task_type, len(tasks_for_this_type))
            if not self.options.progressive_tasks:
                rnd.shuffle(tasks_for_this_type)
            else:
                tasks_for_this_type.reverse()

            tasks_for_this_type = tasks_for_this_type[:max_amount_for_task_type]
            weight_for_this_type = getattr(self.options,
                                                       f"{task_type}_task_weight")
            if weight_for_this_type > 0 and tasks_for_this_type:
                tasks_per_task_type[task_type] = tasks_for_this_type
                weights_per_task_type[task_type] = weight_for_this_type

        # Build a list of collections and weights in a matching order for rnd.choices later
        all_tasks = []
        all_weights = []
        for task_type in task_types:
            if task_type in tasks_per_task_type:
                all_tasks.append(tasks_per_task_type[task_type])
                all_weights.append(weights_per_task_type[task_type])

        # Even after the initial forced generals, they can still be rolled randomly
        if general_weight > 0 and len(general_tasks)>0:
            all_tasks.append(general_tasks)
            all_weights.append(general_weight)

        if not generation_is_fake and locations_added > locations_required: #due to minimum general tasks we already have more than needed
            raise OptionError(f"Too many locations created for {self.player_name}, lower the minimum general tasks")

        while locations_added < locations_required or (generation_is_fake and len(all_tasks) > 0):
            if all_tasks:
                chosen_task = rnd.choices(all_tasks, all_weights)[0]
                if chosen_task:
                    task = chosen_task.pop()
                    if self.add_location(task.name):
                        locations_added += 1 

                # This isn't an else because chosen_task can become empty in the process of resolving the above block
                # We still want to clear this list out while we're doing that
                if not chosen_task:
                    index = all_tasks.index(chosen_task)
                    del all_tasks[index]
                    del all_weights[index]

            else: # We can ignore general tasks in UT because they will have been cleared already
                if len(general_tasks) == 0:
                    raise OptionError(f"There are not enough available tasks to fill the remaining pool for OSRS " +
                                    f"Please adjust {self.player_name}'s settings to be less restrictive of tasks.")
                task = general_tasks.pop()
                if self.add_location(task.name):
                    locations_added += 1 
        
        if self.options.goal.value  in [self.options.goal.option_bingo, self.options.goal.option_dragon_slayer_bingo]:
            total_bingo_size = self.options.bingo_size.value*self.options.bingo_size
            if len(pre_locations) > total_bingo_size:
                raise OptionError("Too Many bingo rewards plando'd for the size of grid")
            total_locations = rnd.sample( [loc for loc in self.get_locations() if loc.address is not None and loc.item is None and not loc.name.startswith("Bingo") and loc.name not in pre_locations],total_bingo_size - len(pre_locations))
            if len(pre_locations) > 0: #if we have plando'd bingo squares
                total_locations.extend([loc for loc in self.get_locations() if loc.address is not None and loc.name in pre_locations]) #add them back
                rnd.shuffle(total_locations) #and shuffle
            for i in range(self.options.bingo_size.value):
                for j in range(self.options.bingo_size.value):
                    temp_loc = total_locations.pop()
                    temp_loc.place_locked_item(self.create_item("Tear of Guthix"))
                    self.bingo_board[i].append(temp_loc.name)


    def add_location(self, location: str) -> bool:
        index = [i for i in range(len(location_rows)) if location_rows[i].name == location][0]
        return self.create_and_add_location(index)

    def create_items(self) -> None:
        filler_items:list[ItemRow] = []
        for item_row in item_rows:
            if item_row.name != self.starting_area_item:
                # If it's a filler item, set it aside for later
                if item_row.progression == ItemClassification.filler:
                    filler_items.append(item_row)
                    continue

                # If it starts with "Care Pack", only add it if Care Packs are enabled
                if item_row.name.startswith("Care Pack"):
                    if not self.options.enable_carepacks:
                        continue

                for c in range(item_row.amount):
                    item = self.create_item(item_row.name)
                    self.multiworld.itempool.append(item)
        if self.options.enable_duds:
            self.random.shuffle(filler_items)
            filler_items = filler_items[0:self.options.dud_count]
            for item_row in filler_items:
                item = self.create_item(item_row.name)
                self.multiworld.itempool.append(item)

    def get_filler_item_name(self) -> str:
        if self.options.enable_duds:
            return self.random.choice([item.name for item in item_rows if item.progression == ItemClassification.filler])
        else:
            return self.random.choice([ItemNames.Progressive_Weapons, ItemNames.Progressive_Magic,
                                       ItemNames.Progressive_Range_Weapon, ItemNames.Progressive_Armor,
                                       ItemNames.Progressive_Range_Armor, ItemNames.Progressive_Tools])

    def explain_rule(self, dest_name:str, state:CollectionState ):
        if self.options.goal.value not in [self.options.goal.option_bingo, self.options.goal.option_dragon_slayer_bingo]: return None
        from NetUtils import JSONMessagePart
        ret:list[JSONMessagePart] = []
        max_index = self.options.bingo_size.value
        if dest_name.lower() in ["/","forward","forward diagonal", "bingo: forward diagonal"]:
            ret.append({"type":"text","text":"Bingo : Forward Diagonal : \n"})
            for i in range(max_index):
                temp_str = self.bingo_board[i][(max_index-1)-i]
                temp_status = state.can_reach_location(temp_str,self.player)
                ret.extend([{"type":"text","text":f"{temp_str}"},{"type":"color","text":f" ({str(temp_status)}) \n","color":"green" if temp_status else "red"}])
        elif dest_name.lower() in ["\\","reverse","reverse diagonal", "bingo: reverse diagonal","backwards","backwards diagonal", "bingo: backwards diagonal"]:
            ret.append({"type":"text","text":"Bingo : Reverse Diagonal : \n"})
            for i in range(max_index):
                temp_str = self.bingo_board[i][i]
                temp_status = state.can_reach_location(temp_str,self.player)
                ret.extend([{"type":"text","text":f"{temp_str}"},{"type":"color","text":f" ({str(temp_status)}) \n","color":"green" if temp_status else "red"}])
        elif dest_name.lower().startswith("r ") or dest_name.lower().startswith("row "):
            _,row = dest_name.split(" ",2)
            if not row.isdecimal():
                return None
            row_i = int(row)-1 #zero indexing lol
            ret.append({"type":"text","text":f"Bingo : Row {row} : \n"})
            for i in range(max_index):
                temp_str = self.bingo_board[row_i][i]
                temp_status = state.can_reach_location(temp_str,self.player)
                ret.extend([{"type":"text","text":f"{temp_str}"},{"type":"color","text":f" ({str(temp_status)}) \n","color":"green" if temp_status else "red"}])
        elif dest_name.lower().startswith("c ") or dest_name.lower().startswith("col ") or dest_name.lower().startswith("column "):
            _,col = dest_name.split(" ",2)
            if not col.isdecimal():
                return None
            col_i = int(col)-1 #zero indexing lol
            ret.append({"type":"text","text":f"Bingo : Column {col} : \n"})
            for i in range(max_index):
                temp_str = self.bingo_board[i][col_i]
                temp_status = state.can_reach_location(temp_str,self.player)
                ret.extend([{"type":"text","text":f"{temp_str}"},{"type":"color","text":f" ({str(temp_status)}) \n","color":"green" if temp_status else "red"}])
        if ret:
            return ret
        else:
            return None


    def create_and_add_location(self, row_index) -> bool:
        location_row = location_rows[row_index]

        # Quest Points are handled differently now, but in case this gets fed an older version of the data sheet,
        # the points might still be listed in a different row
        if location_row.category == "points":
            return False
        # If we've already created the location don't make it again
        if location_row.name in self.multiworld.regions.location_cache[self.player]:
            return False

        # Create Location
        location_id = self.base_id + row_index
        if location_row.category == "goal":
            location_id = None
        location = OSRSLocation(self.player, location_row.name, location_id)
        self.location_name_to_data[location_row.name] = location

        # Add the location to its first region, or if it doesn't belong to one, to Menu
        region = self.region_name_to_data["Menu"]
        if location_row.regions:
            region = self.region_name_to_data[location_row.regions[0]]
        location.parent_region = region
        region.locations.append(location)

        # If it's a quest, generate a "Points" location we'll add an event to
        if location_row.category == "quest":
            points_name = location_row.name.replace("Quest:", "Points:")
            points_location = OSRSLocation(self.player, points_name)
            self.location_name_to_data[points_name] = points_location
            points_location.parent_region = region
            region.locations.append(points_location)
        return True

    def set_rules(self) -> None:
        """
        called to set access and item rules on locations and entrances.
        """

        for location_name, location in self.location_name_to_data.items():
            rule_list:list[Rule] = []
            location_row = self.location_rows_by_name[location_name]
            # Set up requirements for region
            for region_required_name in location_row.regions:
                region_required = self.region_name_to_data[region_required_name]
                rule_list.append(CanReachRegion(region_required.name))
            for skill_req in location_row.skills:
                rule_list.append(get_skill_rule(skill_req.skill, skill_req.level, self.options))
            for item_req in location_row.items:
                rule_list.append(Has(item_req))
            if location_row.qp:
                rule_list.append(Has("Quest Point", location_row.qp))
            if rule_list:
                self.set_rule(location,And(*rule_list))
            else:
                self.set_rule(location,True_()) #If we don't have any rule fragments to use, it's always accessable
        
        quest_attr_names = ["Cooks_Assistant", "Demon_Slayer", "Restless_Ghost", "Romeo_Juliet",
                            "Sheep_Shearer", "Shield_of_Arrav", "Ernest_the_Chicken", "Vampyre_Slayer",
                            "Imp_Catcher", "Prince_Ali_Rescue", "Dorics_Quest", "Black_Knights_Fortress",
                            "Witchs_Potion", "Knights_Sword", "Goblin_Diplomacy", "Pirates_Treasure",
                            "Rune_Mysteries", "Misthalin_Mystery", "Corsair_Curse", "X_Marks_the_Spot",
                            "Below_Ice_Mountain"]

        for quest_attr_name in quest_attr_names:
            qp_loc_name = getattr(LocationNames, f"QP_{quest_attr_name}")
            qp_loc = self.location_name_to_data.get(qp_loc_name)

            q_loc_name = getattr(LocationNames, f"Q_{quest_attr_name}")
            q_loc = self.location_name_to_data.get(q_loc_name)

            # Checks to make sure the task is actually in the list before trying to create its rules
            if qp_loc and q_loc:
                # Create the QP Event Item
                item_name = getattr(ItemNames, f"QP_{quest_attr_name}")
                qp_loc.place_locked_item(self.create_event(item_name))

                # If a quest is excluded, don't actually consider it for quest point progression
                if q_loc_name not in self.options.exclude_locations:
                    self.available_QP_locations.append(str(item_name))

                # Set the access rule for the QP Location
                self.set_rule(qp_loc, CanReachLocation(q_loc.name))

        qp = 0
        for qp_event in self.available_QP_locations:
            qp += int(qp_event[0])

        goal_list = []
        if self.options.goal.value in [self.options.goal.option_dragon_slayer, self.options.goal.option_dragon_slayer_bingo]:
            
            # place "Victory" at "Dragon Slayer" and set collection as win condition
            if qp < self.location_rows_by_name[LocationNames.Q_Dragon_Slayer].qp:
                raise OptionError(f"{self.player_name} doesn't have enough quests for reach goal, increase maximum skill levels")
            self.multiworld.get_location(LocationNames.Q_Dragon_Slayer, self.player) \
                .place_locked_item(self.create_event("Victory"))
            goal_list.append(Has("Victory"))
        if self.options.goal.value in [self.options.goal.option_bingo,self.options.goal.option_dragon_slayer_bingo]:
            goal_list.append(Has("Tear of Guthix", (self.options.bingo_size.value*self.options.bingo_size.value)))

            #Also we need to make the rules for the board itself
            
            for_rules:list[Rule] = []
            bak_rules:list[Rule] = []
            max_index = self.options.bingo_size.value-1
            for index in range(self.options.bingo_size.value):
                temp_loc = self.get_location(self.bingo_board[index][index])
                assert temp_loc.parent_region
                bak_rules.append(CanReachLocation(temp_loc.name))
                temp_loc = self.get_location(self.bingo_board[index][max_index-index])
                assert temp_loc.parent_region
                for_rules.append(CanReachLocation(temp_loc.name))
                row_rules:list[Rule] = []
                col_rules:list[Rule] = []
                for j_index in range(self.options.bingo_size.value):
                    temp_loc = self.get_location(self.bingo_board[index][j_index])
                    assert temp_loc.parent_region
                    row_rules.append(CanReachLocation(temp_loc.name))
                    temp_loc = self.get_location(self.bingo_board[j_index][index])
                    assert temp_loc.parent_region
                    col_rules.append(CanReachLocation(temp_loc.name))
                self.set_rule(self.get_location(f"Bingo: Row {index+1}"),And(*row_rules))
                self.set_rule(self.get_location(f"Bingo: Column {index+1}"),And(*col_rules))
            self.set_rule(self.get_location("Bingo: Forward Diagonal"), And(*for_rules))
            self.set_rule(self.get_location("Bingo: Reverse Diagonal"), And(*bak_rules))
            if hasattr(self.multiworld,"generation_is_fake"):
                #Make some entrances for the bingo board map tab, these are all useless logically but their ability to be transversed will still be important
                menu_region = self.get_region("Menu") #they're all just going to connect menu to itself
                for index in range(self.options.bingo_size.value):
                    for j_index in range(self.options.bingo_size.value):
                        loc_name=self.bingo_board[index][j_index]
                        fake_region = self.create_region(f"Bingo: {loc_name}")
                        menu_region.connect(fake_region,f"Bingo: R{index+1}C{j_index+1}",CanReachLocation(loc_name))


        if len(goal_list)<1:
            raise OptionError("No goal selected... Somehow")
        else:
            self.set_completion_rule(And(*goal_list))


        

    def create_region(self, name: str) -> "Region":
        region = Region(name, self.player, self.multiworld)
        self.region_name_to_data[name] = region
        self.multiworld.regions.append(region)
        return region

    def create_item(self, item_name: str) -> "Item":
        items = [item for item in item_rows if item.name == item_name]
        assert len(items) > 0, f"No matching item found for name {item_name} for player {self.player_name}"
        item = items[0]
        index = item_rows.index(item)
        return OSRSItem(item.name, item.progression, self.base_id + index, self.player)

    def create_event(self, event: str):
        # while we are at it, we can also add a helper to create events
        return OSRSItem(event, ItemClassification.progression, None, self.player)
    
    def collect(self, state: CollectionState, item: Item) -> bool:
        if item.name in self.available_QP_locations:
            qp = int(item.name[0])
            state.add_item(item="Quest Point",player=self.player,count=qp)
        return super().collect(state, item)
    
    def remove(self, state: CollectionState, item: Item) -> bool:
        if item.name in self.available_QP_locations:
            qp = int(item.name[0])
            state.remove_item(item="Quest Point",player=self.player,count=qp)
        return super().remove(state, item)