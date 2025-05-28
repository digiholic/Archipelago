import json
import os

from typing import Dict,List,Any,NamedTuple

class RegionRow(NamedTuple):
    id: str
    name: str

class ResourceRow(NamedTuple):
    name: str

class DropElement(NamedTuple):
    dest: str
    chance: float

class MonsterRow(NamedTuple):
    name: str
    class_name: str
    drops: list[DropElement]

class RewardElement(NamedTuple):
    skill_name: str
    skill_level: int

class RuleElement(NamedTuple):
    type: str
    value: str

class LocationRow(NamedTuple):
    name: str
    category: str
    parent_region:str
    rule: list[RuleElement]
    kudos_reward: int
    quest_point_reward: int

class EntranceRow(NamedTuple):
    source: str
    dest: str
    rule: list[RuleElement]

class TrainingRow(NamedTuple):
    product: str
    skill_name: str
    required_level: int
    rule: list[RuleElement]


this_dir = os.path.dirname(os.path.abspath(__file__))

chunks:Dict[str, Any] = {}
resource_list:List[ResourceRow] = []
regions_list:list[RegionRow] = []

monsters:list[str] = []
monster_to_find:list[str] = []
resources:list[str] = []
missing_resources:list[str] = []
regions:dict[str, str] = {}
f2p_skill_names:list[str]=[
    "Attack","Strength","Defence","Ranged","Prayer","Magic","Runecraft",
    "Hitpoints","Crafting","Mining","Smithing","Fishing","Cooking",
    "Firemaking","Woodcutting"
]
skill_names:list[str]=f2p_skill_names+[
    "Agility","Herblore","Thieving","Fletching","Slayer","Farming","Construction","Hunter"
]
non_skill_task_types:list[str]=[
    "Combat","Nonskill","Extra","Diary","Quest"
]

bidirectional_groups:list[str]=[
    "Agility potion[+]","Antidote+[+]","Antidote++[+]","Antifire potion[+]","Defence potion[+]",
    "Magic potion[+]","Ranging potion[+]","Restore potion[+]","Super attack[+]","Super defence[+]",
    "Super strength[+]","Waterskin[+]","Watering can[+]","Super energy[+]","Anti-venom+[+]",
    "Bastion potion[+]","Battlemage potion[+]","Super combat potion[+]","Super restore[+]",
    "Ancient brew[+]","Superantipoison[+]","Combat potion[+]","Fishing potion[+]","Hunter potion[+]",
    "Magic essence[+]","Prayer potion[+]","Relicym's balm[+]","Stamina potion[+]","Strength potion[+]",
    "Super antifire potion[+]","Antipoison[+]","Attack potion[+]","Energy potion[+]",
    "Extended antifire[+]","Extended super antifire[+]","GuthixRest[+]","CharterShips[+]"
]

banned_tasks:list[str]=[
    "Clue nest loot","Use a ~|3rd age pickaxe|~","Make a ~|3rd age felling axe|~","Make a ~|3rd age felling axe|~ (alt)",
    "Chop with a ~|3rd age axe|~","Chop with a ~|3rd age felling axe|~","(Master Treasure Trails) Obtain a ~|ring of 3rd age|~",
    "Slay a ~|mutated terrorbird|~","Slay a ~|mutated tortoise|~","(Skilling Pets) Obtain a ~|heron|~","(All Pets) Obtain a ~|heron|~",
    "(All Pets) Obtain a ~|rock golem|~","(Skilling Pets) Obtain a ~|rock golem|~","(All Pets) Obtain a ~|beaver|~",
    "(Skilling Pets) Obtain a ~|beaver|~","(All Pets) Obtain a ~|giant squirrel|~","(Skilling Pets) Obtain a ~|giant squirrel|~",
    "(All Pets) Obtain a ~|rocky|~","(Skilling Pets) Obtain a ~|rocky|~","(Random Events) Obtain a ~|camo top|~",
    "(All Pets) Obtain a ~|rift guardian|~","(Skilling Pets) Obtain a ~|rift guardian|~","(Random Events) Obtain ~|camo bottoms|~",
    "(Random Events) Obtain a ~|camo helmet|~","(Random Events) Obtain a ~|lederhosen top|~","(Random Events) Obtain ~|lederhosen shorts|~",
    "(Random Events) Obtain a ~|lederhosen hat|~","(Random Events) Obtain a ~|zombie shirt|~","(Random Events) Obtain ~|zombie trousers|~",
    "(Random Events) Obtain a ~|zombie mask|~","(Random Events) Obtain ~|zombie gloves|~","(Random Events) Obtain ~|zombie boots|~",
    "(Random Events) Obtain a ~|mime mask|~","(Random Events) Obtain a ~|mime top|~","(Random Events) Obtain ~|mime legs|~",
    "(Random Events) Obtain ~|mime gloves|~","(Random Events) Obtain ~|mime boots|~","(Random Events) Obtain a ~|frog token|~",
    "(Random Events) Obtain a ~|stale baguette|~","(Random Events) Obtain a ~|beekeeper's hat|~","(Random Events) Obtain a ~|beekeeper's top|~",
    "(Random Events) Obtain ~|beekeeper's legs|~","(Random Events) Obtain ~|beekeeper's gloves|~","(Random Events) Obtain ~|beekeeper's boots|~",
    "Infuse ranger boots into ~|Pegasian boots|~","Wear ~|ranger boots|~","Wear ~|pegasian boots|~","Obtain a ~|black pickaxe|~","Use a ~|black pickaxe|~",
    "Wear a ~|rangers' tunic|~","Wear a ~|robin hood hat|~","Wear ~|ranger gloves|~","Wield a ~|magic comp bow|~","Wield a ~|willow comp bow|~",
    "Wield a ~|magic comp bow|~","Wield a ~|willow comp bow|~","Wield a ~|yew comp bow|~","(All Pets) Obtain a ~|bloodhound|~"

]

banned_chunks: list[str] = [
    "chunk_12436","chunk_5530"
]

quest_list:list[LocationRow] = []
sub_quest_list:list[LocationRow] = []
non_quest_list:list[LocationRow] = []
non_quest_names:list[str] = []
non_quest_dupes:list[str] = []

training_methods:list[TrainingRow] = []
training_outputs: list[str] = []
dupe_training_methods: list[str] = []

rr_entrances: list[EntranceRow] = []
re_entrances: list[EntranceRow] = []
ee_entrances: list[EntranceRow] = []
rm_entrances: list[EntranceRow] = []
me_entrances: list[EntranceRow] = []
mm_entrances: list[EntranceRow] = []

monster_rows: list[MonsterRow] = []
non_monster_rows: list[MonsterRow] = []

defered_region_connections: list[tuple[str,str]] = []

# todo : fix this later but for now have some manually placed entrances

ee_entrances.append(EntranceRow("Seed[+]","Hespori seed",[]))
resources.append("Hespori seed")
resource_list.append(ResourceRow("Hespori seed"))
regions["Victory"]="Victory"
regions["Nothing :("] = "Nothing :("


def str_format(s) -> str:
    if not s:
        s = ""
    ret_str = s.replace("'", "\\'")
    return f"'{ret_str}'"


def str_list_to_py(str_list) -> str:
    ret_str = "["
    for s in str_list:
        ret_str += str_format(s)
    ret_str += "]"
    return ret_str

def str_rules(ss:list[RuleElement]) -> str:
    return "["+(",".join([f"RuleElement({str_format(s.type)},{str_format(s.value)})" for s in ss])) +"]"

def str_drops(ss:list[DropElement]) -> str:
    return "["+(",".join([f"DropElement({str_format(s.dest)},{str(s.chance)})" for s in ss]))+"]"

def convert_chunk_id(id:str)->str:
    return f"chunk_{id}"

def convert_monster_name(name:str)->str:
    return f"kill_{name}"

def convert_drop_table(drop_table):
    return_table = {}
    for key, value in drop_table.items():
        part_table = {}
        rate, quant = value.split("@",1)
        part_table[quant] = rate
        return_table[key] = part_table
    return return_table

def iterate_drop_table(drop_table):
    exception_list = ["always","varies","rare","unknown","uncommon","common","very rare","random"]
    drop_list = []
    for drop_item, rates_table in drop_table.items():
        noted_rate = 0
        raw_rate = 0
        for quant, rate in rates_table.items():
            if "~" in rate:
                rate = rate[1:]
            if rate.lower() not in exception_list and "/" not in rate:
                breakpoint()
                continue
            if "(noted)" in quant: 
                if rate.lower() in exception_list:
                    noted_rate = 1 #TODO : fix this
                else:        #evil shit directly from qwint <3
                    noted_rate += float.__truediv__(*([float(i) for i in rate.split("/")]))
            else:
                if rate.lower() in exception_list:
                    raw_rate = 1 #also this one
                else:        #turns "4/128" -> 32.0
                    raw_rate += float.__truediv__(*([float(i) for i in rate.split("/")]))
        if noted_rate > 0:
            drop_list.append(DropElement(drop_item+" (noted)",pow(min(noted_rate,1),-1)))
        if raw_rate > 0:
            drop_list.append(DropElement(drop_item,pow(min(raw_rate,1),-1)))
        if drop_item not in resources:
            if drop_item in regions:
                print(drop_item)
                breakpoint()
            resources.append(drop_item)
            resource_list.append(ResourceRow(drop_item))
        if drop_item in missing_resources:
            missing_resources.remove(drop_item)
    return drop_list

def chunk_init(chunk_name,chunk_id,chunk):
    if chunk_id in banned_chunks:
        return
    chunk["Chunk_Name"] = chunk_name
    chunk["Contents"] = []
    if chunk_name not in regions:
        regions[chunk_name] = chunk_id
    if "Connect" in chunk:
        for connected_chunk in chunk["Connect"].keys():
            connected_chunk = convert_chunk_id(connected_chunk)
            defered_region_connections.append((chunk_id,connected_chunk))
    if "Object" in chunk:
        for object in chunk["Object"].keys():
            if not object in resources:
                resources.append(object)
                resource_list.append(ResourceRow(object))
            chunk["Contents"].append(object)
            re_entrances.append(EntranceRow(chunk_id,object,[]))
    if "Spawn" in chunk:
        for object in chunk["Spawn"].keys():
            if object not in resources:
                resources.append(object)
                resource_list.append(ResourceRow(object))
            chunk["Contents"].append(object)
            re_entrances.append(EntranceRow(chunk_id,object,[]))
    if "Monster" in chunk:
        for monster in chunk["Monster"].keys():
            monster = convert_monster_name(monster)
            if not monster in monsters:
                monsters.append(monster)
                monster_to_find.append(monster)
            chunk["Contents"].append(monster)
            rm_entrances.append(EntranceRow(chunk_id,monster,[]))
    if "NPC" in chunk:
        for npc in chunk["NPC"].keys():
            if "Object" in chunk and npc in chunk["Object"]:
                continue
            if not npc in resources:
                resources.append(npc)
                resource_list.append(ResourceRow(npc))
            chunk["Contents"].append(npc)
            re_entrances.append(EntranceRow(chunk_id,npc,[]))
    if "Shop" in chunk:
        for shop in chunk["Shop"].keys():
            if not shop in resources:
                resources.append(shop)
                resource_list.append(ResourceRow(shop))
            chunk["Contents"].append(shop)
            re_entrances.append(EntranceRow(chunk_id,shop,[]))
    #if chunk_id == "chunk_12698":
    #    breakpoint()
    chunks[chunk_id]=chunk
    regions_list.append(RegionRow(chunk_id,chunk_name))

with open(os.path.join(this_dir, "chunkpicker-chunkinfo-export.json"), 'r') as localJSON:
    exportedJSON = json.load(localJSON)
    for chunk_id,chunk in exportedJSON["chunks"].items():
        chunk_name = ""
        if "Nickname" in chunk:
            chunk_name = chunk["Nickname"]
        elif "Name" in chunk:
            chunk_name = chunk["Name"]
        if "Sections" in chunk:
            if len(chunk) > 2: #should be nickname and sections
                chunk_init(chunk_name,convert_chunk_id(chunk_id),chunk)#but there might be something else
            for section_id, section in chunk["Sections"].items():
                chunk_init(chunk_name,convert_chunk_id(chunk_id+"-"+section_id),section)
        else:
            chunk_init(chunk_name,convert_chunk_id(chunk_id),chunk)
    for source_chunk, dest_chunk in defered_region_connections:
        if dest_chunk not in chunks:
            if f"{dest_chunk}-1" not in chunks:
                print("PANIC!! " + dest_chunk)
            else:
                dest_chunk = f"{dest_chunk}-1"
        rr_entrances.append(EntranceRow(source_chunk,dest_chunk,[]))
    for shop, inventory in exportedJSON["shopItems"].items():
        if shop not in resources:
            print("PANIC! : " + shop)
            continue
        for shop_item in inventory.keys():
            if shop_item not in resources:
                resources.append(shop_item)
                resource_list.append(ResourceRow(shop_item))
            ee_entrances.append(EntranceRow(shop,shop_item,[]))
    for macro_name, macro_list in exportedJSON["codeItems"]["itemsPlus"].items():
        if macro_name not in resources:
            resources.append(macro_name)
            resource_list.append(ResourceRow(macro_name))
        if macro_name in bidirectional_groups: #reversable macro group, e.g. decanting
            for sub_item in macro_list: 
                if sub_item not in resources:
                    resources.append(sub_item)
                    resource_list.append(ResourceRow(sub_item))
                ee_entrances.append(EntranceRow(macro_name,sub_item,[]))
        for sub_item in macro_list:
            ee_entrances.append(EntranceRow(sub_item,macro_name,[]))
            if sub_item not in resources:
                missing_resources.append(sub_item)
    for macro_name, macro_list in exportedJSON["codeItems"]["chunksPlus"].items():
        macro_name = convert_chunk_id(macro_name)
        if macro_name not in chunks:
            chunk = {"Chunk_Name":None,"Contents":[]}
            chunks[macro_name] = chunk
            regions_list.append(RegionRow(macro_name,"")) #keep name empty so it doesn't make an item to access it
        for sub_chunk in macro_list:
            sub_chunk = convert_chunk_id(sub_chunk)
            if sub_chunk not in chunks:
                if f"{sub_chunk}-1" not in chunks:
                    print("PANIC!!! : " + sub_chunk)
                    continue
                else:
                    sub_chunk = sub_chunk + "-1"
            if sub_chunk in bidirectional_groups:
                rr_entrances.append(EntranceRow(macro_name,sub_chunk,[]))
            rr_entrances.append(EntranceRow(sub_chunk,macro_name,[])) #backwards normal because these are seach filters, not access
    for macro_name, macro_list in exportedJSON["codeItems"]["npcsPlus"].items():
        if macro_name not in resources:
            resources.append(macro_name)
            resource_list.append(ResourceRow(macro_name))
        for sub_item in macro_list:
            ee_entrances.append(EntranceRow(sub_item,macro_name,[]))
            if sub_item not in resources:
                missing_resources.append(sub_item)
    for macro_name, macro_list in exportedJSON["codeItems"]["objectsPlus"].items():
        if macro_name not in resources:
            resources.append(macro_name)
            resource_list.append(ResourceRow(macro_name))
        for sub_item in macro_list:
            ee_entrances.append(EntranceRow(sub_item,macro_name,[]))
            if sub_item not in resources:
                missing_resources.append(sub_item)
    for macro_name, macro_list in exportedJSON["codeItems"]["dropTables"].items():
        if macro_name not in resources:
            resources.append(macro_name)
            resource_list.append(ResourceRow(macro_name))
        drop_list = iterate_drop_table(convert_drop_table(macro_list))
        non_monster_rows.append(MonsterRow(macro_name,"Macro",drop_list))
    for macro_name, macro_list in exportedJSON["codeItems"]["monstersPlus"].items():
        macro_name = convert_monster_name(macro_name)
        if macro_name not in monsters:
            monsters.append(macro_name)
            monster_rows.append(MonsterRow(macro_name,"Macro",[]))
        for monster in macro_list:
            monster = convert_monster_name(monster)
            if monster in monsters:
                mm_entrances.append(EntranceRow(monster,macro_name,[]))
            
    for category, drop_tables in exportedJSON["skillItems"].items():
        for drop_source, drop_table in drop_tables.items():
            drop_list = iterate_drop_table(drop_table)
            if drop_source not in resources:
                resources.append(drop_source)
                resource_list.append(ResourceRow(drop_source))
            drop_source_category:str = drop_source
            if "#" in drop_source:
                drop_source_category = drop_source_category.split("#")[0] #just want the first section
            non_monster_rows.append(MonsterRow(drop_source,drop_source_category,drop_list))
    for drop_source, drop_table in exportedJSON["drops"].items():
        drop_list = iterate_drop_table(drop_table)
        drop_source = convert_monster_name(drop_source)
        drop_source_category:str = drop_source
        if drop_source not in monsters:
            continue
        if drop_source in monster_to_find:
            monster_to_find.remove(drop_source)
        if "#" in drop_source:
            drop_source_category = drop_source_category.split("#")[0] #just want the first section
        monster_rows.append(MonsterRow(drop_source,drop_source_category,drop_list))
    for chunk_id,sections in exportedJSON["sections"].items():
        for section_id,connections in sections.items():
            section_name = f"{chunk_id}-{section_id}"
            if section_id == "0":
                section_name = chunk_id
            section_name = convert_chunk_id(section_name)
            if section_name not in chunks:
                print("PANIC! : "+ section_name)
                continue
            for connection in connections:
                connection = convert_chunk_id(connection)
                if connection not in chunks:
                    if f"{connection}-1" in chunks:
                        connection += "-1"
                    else:
                        print("PANIC! : " + connection)
                        continue
                if "Connect" not in chunks[section_name]:
                    chunks[section_name]["Connect"] = {}
                chunks[section_name]["Connect"][connection] = True
                rules = []
                if connection in chunks:
                    connection_name = chunks[connection]["Chunk_Name"]
                    if connection_name:
                        rules.append(RuleElement("has",f"Area: {connection_name}"))
                rr_entrances.append(EntranceRow(section_name,connection,rules))
    for task_type, task_list in exportedJSON["challenges"].items():
        if task_type == "Quest" or task_type == "Diary":
            for quest_name, quest_data in task_list.items():
                target_list = sub_quest_list
                category = "subquest"
                parent_region = None
                rule_list = []
                if "Complete" in quest_name:
                    target_list = quest_list
                    category = "quest"
                if "Tasks" in quest_data:
                    for req,req_type in quest_data["Tasks"].items():
                        rule_list.append(RuleElement("can_reach",req))
                if "Skills" in quest_data:
                    for skill,skill_level in quest_data["Skills"].items():
                        rule_list.append(RuleElement("skill",f"{skill}_{str(skill_level)}"))
                if "Chunks" in quest_data:
                    for chunk in quest_data["Chunks"]:
                        if "[+]" in chunk and not chunk.endswith("[+]"):
                            chunk,_ = chunk.rsplit("x",1)
                        if parent_region is None:
                            parent_region = convert_chunk_id(chunk)
                        rule_list.append(RuleElement("chunk",convert_chunk_id(chunk)))
                if "NPCs" in quest_data:
                    for npc in quest_data["NPCs"]:
                        if parent_region is None:
                            parent_region = npc
                        rule_list.append(RuleElement("can_reach",npc))
                if "Objects" in quest_data:
                    for object in quest_data["Objects"]:
                        if parent_region is None:
                            parent_region = object
                        rule_list.append(RuleElement("can_reach",object))
                if "Items" in quest_data:
                    for item in quest_data["Items"]:
                        if "[+]" in item and not item.endswith("[+]"):
                            item,_ = item.rsplit("x",1)
                        if parent_region is None:
                            parent_region = item
                        rule_list.append(RuleElement("can_reach",item))
                if "Monsters" in quest_data:
                    for monster in quest_data["Monsters"]:
                        monster = convert_monster_name(monster)
                        if parent_region is None:
                            parent_region = monster
                        rule_list.append(RuleElement("can_reach",monster))
                if "QuestPointsNeeded" in quest_data:
                    rule_list.append(RuleElement("questPoints",str(quest_data["QuestPointsNeeded"])))
                if "KudosNeeded" in quest_data:
                    rule_list.append(RuleElement("kudos",str(quest_data["KudosNeeded"])))
                #todo CombatPointsNeeded
                if "Reward" in quest_data:
                    for item in quest_data["Reward"]:
                        if item not in resources:
                            resources.append(item)
                            resource_list.append(ResourceRow(item))
                        re_entrances.append(EntranceRow("Menu",item,rule_list))
                kudos_reward = 0
                quest_point_reward = 0
                if "QuestPoints" in quest_data:
                    quest_point_reward = int(quest_data["QuestPoints"])
                if "Kudos" in quest_data:
                    kudos_reward = int(quest_data["Kudos"])
                #todo CombatPoints
                if parent_region:
                    parent_region = parent_region.rstrip("*")
                target_list.append(LocationRow(quest_name,category,parent_region,rule_list,kudos_reward,quest_point_reward))
                for field in quest_data.keys():
                    if field not in [
                        "BaseQuest","Description","NPCs","Tasks","Items","Not F2P",
                        "NoBoost","QuestPointsNeeded","QuestPoints","XpReward","Reward",
                        "Chunks","Skills","Monsters","Objects","SkillsBoost","KudosNeeded",
                        "ManualShow","Not Skiller","Category","Kudos","CombatPoints","CombatPointsNeeded"
                        ]:
                        print(field)
                        print(quest_name)
                        breakpoint()
        elif task_type == "Combat":
            #todo
            pass
        elif task_type in skill_names:
            for task_name, task_data in task_list.items():
                if task_name in banned_tasks:
                    continue
                parent_region = None
                rule_list = []
                if "Chunks" in task_data:
                    for chunk in task_data["Chunks"]:
                        if parent_region is None:
                            parent_region = convert_chunk_id(chunk)
                        rule_list.append(RuleElement("chunk",convert_chunk_id(chunk)))
                if "NPCs" in task_data:
                    for npc in task_data["NPCs"]:
                        if parent_region is None:
                            parent_region = npc
                        rule_list.append(RuleElement("can_reach",npc))
                if "Level" in task_data:
                    rule_list.append(RuleElement("skill",f"{task_type}_{str(task_data["Level"])}"))
                if "Objects" in task_data:
                    for object in task_data["Objects"]:
                        if parent_region is None:
                            parent_region = object
                        rule_list.append(RuleElement("can_reach",object))
                if "Skills" in task_data:
                    for skill,skill_level in task_data["Skills"].items():
                        rule_list.append(RuleElement("skill",f"{skill}_{str(skill_level)}"))
                if "Items" in task_data:
                    for item in task_data["Items"]:
                        if parent_region is None:
                            parent_region = item
                        rule_list.append(RuleElement("can_reach",item))
                if "Tasks" in task_data:
                    for req,req_type in task_data["Tasks"].items():
                        rule_list.append(RuleElement("can_reach",req))
                if "Mix" in task_data:
                    for mix in task_data["Mix"]: #These are macros for pickpocketing EXACTLY
                        rule_list.append(RuleElement("can_reach",mix))
                if "Monsters" in task_data:
                    if task_type == "Slayer":
                        if len(task_data["Monsters"])>1:
                            print(task_name)
                            breakpoint()
                    for monster in task_data["Monsters"]:
                        monster = convert_monster_name(monster)
                        if parent_region is None:
                            parent_region = monster
                        if monster in monster_to_find:
                            monster_category:str = monster
                            if "#" in monster:
                                monster_category = monster.split("#")[0] #just want the first section
                            monster_rows.append(MonsterRow(monster,monster_category,[]))
                            monster_to_find.remove(monster)
                        rule_list.append(RuleElement("can_reach",monster))
                if "Primary" in task_data and task_data["Primary"]:
                    #primary training method
                    output = "None"
                    level = 0
                    if "Output" in task_data:
                        output = task_data["Output"]
                    if "Level" in task_data:
                        level = task_data["Level"]
                    if output in training_outputs:
                        if output not in dupe_training_methods:
                            dupe_training_methods.append(output)
                        continue
                    else:
                        training_methods.append(TrainingRow(output,task_type,level,rule_list))
                        training_outputs.append(output)
                if task_name in non_quest_names: #have to do it down here so we can do training methods
                    if task_name not in non_quest_dupes:
                        non_quest_dupes.append(task_name)
                    continue #for now just ignore it and hope it goes away (it won't)
                if "Output" in task_data:
                    output = task_data["Output"]
                    if output not in resources:
                        if output in regions:
                            print(output)
                            breakpoint()
                        resources.append(output)
                        resource_list.append(ResourceRow(output))
                    if output in missing_resources:
                        missing_resources.remove(output)
                    re_entrances.append(EntranceRow("Menu",output,rule_list))
                if "Output Object" in task_data:
                    output_obj = task_data["Output Object"]
                    if output_obj not in resources:
                        if output_obj in regions:
                            print(output_obj)
                            breakpoint()
                        resources.append(output_obj)
                        resource_list.append(ResourceRow(output_obj))
                    if output_obj in missing_resources:
                        missing_resources.remove(output_obj)
                    re_entrances.append(EntranceRow("Menu",output_obj,rule_list))
                if parent_region:
                    parent_region = parent_region.rstrip("*")
                non_quest_list.append(LocationRow(task_name,task_type,parent_region,rule_list,0,0))
                non_quest_names.append(task_name)
                for field in task_data.keys():
                    if field not in [
                            "Chunks","Level","Primary","Output","Objects","Skills",
                            "Priority","Not F2P","NoPet","Items","NoBoost","Category",
                            "Tasks","NPCs","Not Equip","AlwaysValid","Output Object",
                            "NoXp","Monsters","BackupParent","ManualInvalid",
                            "ManualNonProcessing","Source","Mix","InfoLink"
                        ]:
                        print(field)
                        print(task_name)
                        breakpoint()
        elif task_type in non_skill_task_types:
            for task_name, task_data in task_list.items():
                if task_name in banned_tasks:
                    continue
                if task_name in non_quest_names:
                    if task_name not in non_quest_dupes:
                        non_quest_dupes.append(task_name)
                    continue #for now just ignore duplicates and hope they go away
                if "Category" in task_data and "Collection Log Clues" in task_data["Category"]:
                    continue
                parent_region = None
                rule_list = []
                if "ForcedSecondary" in task_data and task_data["ForcedSecondary"]:
                    continue #Used in sources that aren't real but technically exist... just ignore them
                if "ClueTier" in task_data or "ClueType" in task_data:
                    continue #Clues don't exist and they cannot hurt me
                if "StarRegion" in task_data:
                    continue #I don't actually know what these are for so right now we're ignoring them
                if "Chunks" in task_data:
                    for chunk in task_data["Chunks"]:
                        if parent_region is None:
                            parent_region = convert_chunk_id(chunk)
                        rule_list.append(RuleElement("chunk",convert_chunk_id(chunk)))
                if "NPCs" in task_data:
                    for npc in task_data["NPCs"]:
                        if parent_region is None:
                            parent_region = npc
                        rule_list.append(RuleElement("can_reach",npc))
                if "Objects" in task_data:
                    for object in task_data["Objects"]:
                        if parent_region is None:
                            parent_region = object
                        rule_list.append(RuleElement("can_reach",object))
                if "Skills" in task_data:
                    for skill,skill_level in task_data["Skills"].items():
                        rule_list.append(RuleElement("skill",f"{skill}_{str(skill_level)}"))
                if "Items" in task_data:
                    for item in task_data["Items"]:
                        if parent_region is None:
                            parent_region = item
                        rule_list.append(RuleElement("can_reach",item))
                if "Tasks" in task_data:
                    for req,req_type in task_data["Tasks"].items():
                        if "[+]" in req and not req.endswith("[+]"):
                            req,_ = req.rsplit("x",1)
                        rule_list.append(RuleElement("can_reach",req))
                if "Monsters" in task_data:
                    for monster in task_data["Monsters"]:
                        monster = convert_monster_name(monster)
                        if parent_region is None:
                            parent_region = monster
                        if monster in monster_to_find:
                            monster_category:str = monster
                            if "#" in monster:
                                monster_category = monster.split("#")[0] #just want the first section
                            monster_rows.append(MonsterRow(monster,monster_category,[]))
                            monster_to_find.remove(monster)
                        rule_list.append(RuleElement("can_reach",monster))
                if "QuestPointsNeeded" in task_data:
                    rule_list.append(RuleElement("questPoints",str(task_data["QuestPointsNeeded"])))
                #todo: TotalLevelNeeded
                #todo: CombatLevelNeeded
                if "Output" in task_data:
                    output = task_data["Output"]
                    if output not in resources:
                        if output in regions:
                            print(output)
                            breakpoint()
                        resources.append(output)
                        resource_list.append(ResourceRow(output))
                    if output in missing_resources:
                        missing_resources.remove(output)
                    re_entrances.append(EntranceRow("Menu",output,rule_list))
                if "Output Object" in task_data:
                    output_obj = task_data["Output Object"]
                    if output_obj not in resources:
                        if output_obj in regions:
                            print(output_obj)
                            breakpoint()
                        resources.append(output_obj)
                        resource_list.append(ResourceRow(output_obj))
                    if output_obj in missing_resources:
                        missing_resources.remove(output_obj)
                    re_entrances.append(EntranceRow("Menu",output_obj,rule_list))
                if "Reward" in task_data:
                    for item in task_data["Reward"]:
                        if item not in resources:
                            resources.append(item)
                            resource_list.append(ResourceRow(item))
                        re_entrances.append(EntranceRow("Menu",item,rule_list))
                if "ConnectsSections" in task_data and task_data["ConnectsSections"]:
                    if "Sections" not in task_data:
                        print("PANIC!! " + task_name)
                        continue
                    section_list = task_data["Sections"]
                    if len(section_list) != 2:
                        print(task_name)
                        breakpoint()
                    source_chunk = convert_chunk_id(section_list[0])
                    dest_chunk = convert_chunk_id(section_list[1])
                    if source_chunk not in chunks or dest_chunk not in chunks:
                        print(task_name)
                        breakpoint()
                    source_name = chunks[source_chunk]["Chunk_Name"]
                    source_rule = rule_list.copy()
                    if source_name:
                        source_rule.append(RuleElement("has",f"Area: {source_name}"))
                    dest_name = chunks[dest_chunk]["Chunk_Name"]
                    dest_rule = rule_list.copy()
                    if dest_name:
                        dest_rule.append(RuleElement("has",f"Area: {dest_name}"))
                    rr_entrances.append(EntranceRow(source_chunk,dest_chunk,dest_rule))
                    rr_entrances.append(EntranceRow(dest_chunk,source_chunk,source_rule))
                if "UnlocksArea" in task_data:
                    source_chunk = "Menu"
                    if "Chunks" in task_data:
                        if len(task_data["Chunks"]) == 1:
                            source_chunk = convert_chunk_id(task_data["Chunks"][0])
                    dest_chunk = convert_chunk_id(task_name)
                    if dest_chunk not in chunks or (source_chunk not in chunks and source_chunk != "Menu"):
                        print(task_name)
                        breakpoint()
                    rr_entrances.append(EntranceRow(source_chunk,dest_chunk,rule_list))
                kudos_reward = 0
                if "Kudos" in task_data:
                    kudos_reward = int(task_data["Kudos"])
                if "ConnectsSections" not in task_data and "UnlocksArea" not in task_data: #don't make these as locations
                    if parent_region:
                        parent_region = parent_region.rstrip("*")
                    non_quest_list.append(LocationRow(task_name,task_type,parent_region,rule_list,kudos_reward,0))
                    non_quest_names.append(task_name)
                for field in task_data.keys():
                    if field not in [
                            "Chunks","Output","Objects","Skills","Description","XpReward","NonShop",
                            "Priority","Not F2P","NoPet","Items","NoBoost","Category","Set",
                            "Tasks","NPCs","Not Equip","AlwaysValid","Output Object","Kudos",
                            "NoXp","Monsters","BackupParent","ManualInvalid","UnlocksArea",
                            "ManualNonProcessing","Source","InfoLink","ConnectsSections","Sections",
                            "QuestPointsNeeded","TotalLevelNeeded","CombatLevelNeeded","Reward",
                            "ForcedSecondary","ClueTier","ClueType","StarRegion","Label","Requirements",
                            "Not Skiller"
                        ]:
                        print(field)
                        print(task_name)
                        breakpoint()


                   
if len(missing_resources) > 0:
    print("PANIC! MISSING "+str(len(missing_resources))+" items!")

if len(monster_to_find) > 0:
    print("PANIC! MISSING "+str(len(monster_to_find)) + " monsters!")

with open(os.path.join(this_dir, "regions_generated2.py"), "w+") as regPyFile:
            regPyFile.write('"""\nThis file was auto generated by LogicCSVToPython.py\n"""\n')
            regPyFile.write("from ..Regions import RegionRow,ResourceRow,EntranceRow,LocationRow,TrainingRow,RuleElement,MonsterRow,DropElement\n")
            regPyFile.write("from BaseClasses import ItemClassification\n")
            regPyFile.write("from ..Items import ItemRow\n")
            regPyFile.write("\n")
            regPyFile.write("region_rows: list[RegionRow] = [\n")

            for region_row in regions_list:
                row_line = "RegionRow("
                row_line += str_format(region_row.id)
                row_line += ","
                row_line += str_format(region_row.name)
                row_line += ")"
                regPyFile.write(f"\t{row_line},\n")
            
            regPyFile.write("]\n\n")

            regPyFile.write("resource_rows: list[ResourceRow] = [\n")

            for resouce_row in resource_list:
                row_line = "ResourceRow("
                row_line += str_format(resouce_row.name)
                row_line += ")"
                regPyFile.write(f"\t{row_line},\n")
            
            regPyFile.write("]\n\n")

            regPyFile.write("item_rows: list[ItemRow] = [\n")

            for region_name, chunk_id in regions.items():
                row_line = "ItemRow("
                row_line += str_format("Area: "+region_name)
                if region_name != "Nothing :(":
                    row_line += ", 1, ItemClassification.progression,"
                else:
                    row_line += ", 0, ItemClassification.filler,"
                row_line += str_format(chunk_id)
                row_line += ")"
                regPyFile.write(f"\t{row_line},\n")
            
            regPyFile.write("]\n\n")

            regPyFile.write("rr_entrances: list[EntranceRow] = [\n")

            for entrance_row in rr_entrances:
                row_line = "EntranceRow("
                row_line += str_format(entrance_row.source)
                row_line += ","
                row_line += str_format(entrance_row.dest)
                row_line += ","
                row_line += str_rules(entrance_row.rule)
                row_line += ")"
                regPyFile.write(f"\t{row_line},\n")
            
            regPyFile.write("]\n\n")

            regPyFile.write("re_entrances: list[EntranceRow] = [\n")

            for entrance_row in re_entrances:
                row_line = "EntranceRow("
                row_line += str_format(entrance_row.source)
                row_line += ","
                row_line += str_format(entrance_row.dest)
                row_line += ","
                row_line += str_rules(entrance_row.rule)
                row_line += ")"
                regPyFile.write(f"\t{row_line},\n")
            
            regPyFile.write("]\n\n")

            regPyFile.write("ee_entrances: list[EntranceRow] = [\n")

            for entrance_row in ee_entrances:
                if entrance_row.source in missing_resources or entrance_row.dest in missing_resources:
                    continue
                row_line = "EntranceRow("
                row_line += str_format(entrance_row.source)
                row_line += ","
                row_line += str_format(entrance_row.dest)
                row_line += ","
                row_line += str_rules(entrance_row.rule)
                row_line += ")"
                regPyFile.write(f"\t{row_line},\n")
            
            regPyFile.write("]\n\n")

            regPyFile.write("rm_entrances: list[EntranceRow] = [\n")

            for entrance_row in rm_entrances:
                row_line = "EntranceRow("
                row_line += str_format(entrance_row.source)
                row_line += ","
                row_line += str_format(entrance_row.dest)
                row_line += ","
                row_line += str_rules(entrance_row.rule)
                row_line += ")"
                regPyFile.write(f"\t{row_line},\n")
            
            regPyFile.write("]\n\n")

            regPyFile.write("mm_entrances: list[EntranceRow] = [\n")

            for entrance_row in mm_entrances:
                if entrance_row.dest in monster_to_find:
                    continue
                row_line = "EntranceRow("
                row_line += str_format(entrance_row.source)
                row_line += ","
                row_line += str_format(entrance_row.dest)
                row_line += ","
                row_line += str_rules(entrance_row.rule)
                row_line += ")"
                regPyFile.write(f"\t{row_line},\n")
            
            regPyFile.write("]\n\n")

            regPyFile.write("sub_quests: list[LocationRow] = [\n")

            for quest_row in sub_quest_list:
                row_line = "LocationRow("
                row_line += str_format(quest_row.name)
                row_line += ","
                row_line += str_format(quest_row.category)
                row_line += ","
                row_line += str_format(quest_row.parent_region)
                row_line += ","
                row_line += str_rules(quest_row.rule)
                row_line += ","
                row_line += str(quest_row.kudos_reward)
                row_line += ","
                row_line += str(quest_row.quest_point_reward)
                row_line += ")"
                regPyFile.write(f"\t{row_line},\n")
            
            regPyFile.write("]\n\n")

            regPyFile.write("quests: list[LocationRow] = [\n")

            for quest_row in quest_list:
                row_line = "LocationRow("
                row_line += str_format(quest_row.name)
                row_line += ","
                row_line += str_format(quest_row.category)
                row_line += ","
                row_line += str_format(quest_row.parent_region)
                row_line += ","
                row_line += str_rules(quest_row.rule)
                row_line += ","
                row_line += str(quest_row.kudos_reward)
                row_line += ","
                row_line += str(quest_row.quest_point_reward)
                row_line += ")"
                regPyFile.write(f"\t{row_line},\n")
            
            regPyFile.write("]\n\n")

            regPyFile.write("non_quests: list[LocationRow] = [\n")

            for location_row in non_quest_list:
                row_line = "LocationRow("
                row_line += str_format(location_row.name)
                row_line += ","
                row_line += str_format(location_row.category)
                row_line += ","
                row_line += str_format(location_row.parent_region)
                row_line += ","
                row_line += str_rules(location_row.rule)
                row_line += ","
                row_line += str(location_row.kudos_reward)
                row_line += ","
                row_line += str(location_row.quest_point_reward)
                row_line += ")"
                regPyFile.write(f"\t{row_line},\n")
            
            regPyFile.write("]\n\n")

            regPyFile.write("location_rows: list[LocationRow] = quests + non_quests\n\n")

            regPyFile.write("training_methods: list[TrainingRow] = [\n")

            for training_method in training_methods:
                row_line = "TrainingRow("
                row_line += str_format(training_method.product)
                row_line += ","
                row_line += str_format(training_method.skill_name)
                row_line += ","
                row_line += str(training_method.required_level)
                row_line += ","
                row_line += str_rules(training_method.rule)
                row_line += ")"
                regPyFile.write(f"\t{row_line},\n")
            
            regPyFile.write("]\n\n")

            regPyFile.write("non_monster_drops: list[MonsterRow] = [\n")

            for non_monster_drop in non_monster_rows:
                row_line = "MonsterRow("
                row_line += str_format(non_monster_drop.name)
                row_line += ","
                row_line += str_format(non_monster_drop.class_name)
                row_line += ","
                row_line += str_drops(non_monster_drop.drops)
                row_line += ")"
                regPyFile.write(f"\t{row_line},\n")
            
            regPyFile.write("]\n\n")

            regPyFile.write("monster_drops: list[MonsterRow] = [\n")

            for monster_drop in monster_rows:
                row_line = "MonsterRow("
                row_line += str_format(monster_drop.name)
                row_line += ","
                row_line += str_format(monster_drop.class_name)
                row_line += ","
                row_line += str_drops(monster_drop.drops)
                row_line += ")"
                regPyFile.write(f"\t{row_line},\n")
            
            #add the missing ones as empty drop tables

            for monster in monster_to_find:
                row_line = "MonsterRow("
                row_line += str_format(monster)
                row_line += ","
                row_line += str_format(monster)
                row_line += ",[])"
                regPyFile.write(f"\t{row_line},\n")
            
            regPyFile.write("]\n\n")

            regPyFile.write("missing_items: list[str] = [\n")
            for missing_item in missing_resources:
                regPyFile.write(f"\t{str_format(missing_item)},\n")
            regPyFile.write("]\n\n")

            regPyFile.write("missing_monsters: list[str] = [\n")
            for monster in monster_to_find:
                regPyFile.write(f"\t{str_format(monster)},\n")
            regPyFile.write("]\n\n")

            regPyFile.write("non_quest_dupes: list[str] = [\n")
            for dupe_task in non_quest_dupes:
                regPyFile.write(f"\t{str_format(dupe_task)},\n")
            regPyFile.write("]\n\n")

            regPyFile.write("training_dupes: list[str] = [\n")
            for dupe_training in dupe_training_methods:
                regPyFile.write(f"\t{str_format(dupe_training)},\n")
            regPyFile.write("]\n\n")


            

#with open(os.path.join(this_dir, "resources_generated2.py"),"w+") as resPyFile:
#            resPyFile.write('"""\nThis file was auto generated by LogicCSVToPython.py\n"""\n')
#            resPyFile.write("from ..Regions import ResourceRow\n")
#            resPyFile.write("\n")
#            resPyFile.write("resource_rows = [\n")
#            for row in resources:
#                row_line = f'ResourceRow("{row}")'
#                resPyFile.write(f"\t{row_line},\n")
#            resPyFile.write("]\n")