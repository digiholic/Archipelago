import csv
import json
import os

from typing import Dict,List,Any,NamedTuple

class RegionRow(NamedTuple):
    id: str
    name: str

class ResourceRow(NamedTuple):
    name: str

class RuleElement(NamedTuple):
    type: str
    value: str

class DropElement(NamedTuple):
    dest: str
    rate: int
    rule: list[RuleElement]

class MonsterRow(NamedTuple):
    name: str
    class_name: str
    drops: list[DropElement]

class RewardElement(NamedTuple):
    skill_name: str
    skill_level: int

class LocationRow(NamedTuple):
    name: str
    category: str
    parent_region:str
    description:str
    rule: list[RuleElement]
    kudos_reward: int
    quest_point_reward: int
    combat_point_reward: int

class EntranceRow(NamedTuple):
    source: str
    dest: str
    rule: list[RuleElement]

class TrainingRow(NamedTuple):
    product: str
    skill_name: str
    required_level: int
    parent_region: str
    task_name: str
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
    "Firemaking","Woodcutting","Combat"
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
    "Super strength[+]","Waterskin[+]","Watering cans[+]","Super energy[+]","Anti-venom+[+]",
    "Bastion potion[+]","Battlemage potion[+]","Super combat potion[+]","Super restore[+]",
    "Ancient brew[+]","Superantipoison[+]","Combat potion[+]","Fishing potion[+]","Hunter potion[+]",
    "Magic essence[+]","Prayer potion[+]","Relicym's balm[+]","Stamina potion[+]","Strength potion[+]",
    "Super antifire potion[+]","Antipoison[+]","Attack potion[+]","Energy potion[+]",
    "Extended antifire[+]","Extended super antifire[+]","GuthixRest[+]","CharterShips[+]"
]

banned_groups:list[str]=[
    "Blessed dragonhide chaps[+]","Enchanted robes[+]","Holy book[+]","Unholy book[+]","Robes of darkness[+]","Samurai armour[+]",
    "HeraldicRuneShield[+]","HeraldicRuneHelm[+]","Stole[+]","Mitre[+]","Headband[+]","Crozier[+]","Bob shirt[+]","Boater[+]",
    "God book[+]"
]

banned_tasks:list[str]=[
    "Cook a ~|cooked wild kebbit|~",


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
    "Wield a ~|magic comp bow|~","Wield a ~|willow comp bow|~","Wield a ~|yew comp bow|~","(All Pets) Obtain a ~|bloodhound|~",
    "(All Pets) Obtain a ~|tangleroot|~","(Skilling Pets) Obtain a ~|tangleroot|~","(Slayer) Obtain an ~|eternal gem|~","(Slayer) Obtain an ~|imbued heart|~",
    "(All Pets) Obtain a ~|moxi|~","(Amoxliatl) Obtain a ~|moxi|~","Create a saturated heart*","Wear ~|blessed dragonhide chaps|~","Wear ~|enchanted robes|~",
    "Wear ~|robes of darkness|~","Wear ~|samurai armour|~","Craft a ~|slayer ring (eternal)|~","Bless an ~|unholy symbol|~","Bless a ~|holy symbol|~",
    "Build a ~|Trailblazer globe (Construction)|~","Build a ~|Trailblazer rug|~","~|STASH#Hard|~: North-east corner of the Kharazi Jungle",
    "~|STASH#Hard|~: In the middle of Jiggig","~|STASH#Hard|~: Volcano in the north-eastern Wilderness","~|STASH#Hard|~: Agility Pyramid",
    "~|STASH#Elite|~: Entrance of the cavern under the whirlpool","~|STASH#Elite|~: Shayzien War Tent","~|STASH#Elite|~: Entrance of the cave of Damis",
    "~|STASH#Elite|~: South-east corner of the Monastery","~|STASH#Master|~: On top of the Northern wall of Castle Drakan","~|STASH#Master|~: Outside K'ril Tsutsaroth's room",
    "~|STASH#Master|~: Outside the Wilderness axe hut","~|STASH#Master|~: Outside the Mudknuckles' hut","~|STASH#Master|~: King Black Dragon's lair",
    "Armour Case: ~|Giant stopwatch|~","Magic Wardrobe: ~|Dark infinity hat|~","Magic Wardrobe: ~|Dark infinity top|~","Magic Wardrobe: ~|Dark infinity bottoms|~",
    "Magic Wardrobe: ~|Light infinity hat|~","Magic Wardrobe: ~|Light infinity top|~","Magic Wardrobe: ~|Light infinity bottoms|~","Magic Wardrobe: ~|Mystic hat (or)|~",
    "Magic Wardrobe: ~|Mystic robe top (or)|~","Magic Wardrobe: ~|Mystic robe bottom (or)|~","Magic Wardrobe: ~|Mystic gloves (or)|~","Magic Wardrobe: ~|Mystic boots (or)|~",
    "F2P Only","Obtain a ~|Golden Gnome|~","Buy the 1st upgrade to ~|bank space|~ for 1m","Buy the 2nd upgrade to ~|bank space|~ for 2m","Buy the 3rd upgrade to ~|bank space|~ for 5m",
    "Buy the 4th upgrade to ~|bank space|~ for 10m","Buy the 5th upgrade to ~|bank space|~ for 20m","Buy the 6th upgrade to ~|bank space|~ for 50m","Buy the 7th upgrade to ~|bank space|~ for 100m",
    "Buy the 8th upgrade to ~|bank space|~ for 200m","Buy the 9th upgrade to ~|bank space|~ for 500m","Trade-in for platinum token*","Build a ~|tip jar|~",
    "Create ~|avernic treads (pe)|~","Create ~|avernic treads (pe)(et)|~","Create ~|avernic treads (pr)(pe)|~","Create ~|avernic treads (max)|~",
    "Unlock the oak variant of the ~|greenman mask|~","Unlock the willow variant of the ~|greenman mask|~","Unlock the maple variant of the ~|greenman mask|~",
    "Unlock the yew variant of the ~|greenman mask|~","Unlock the magic variant of the ~|greenman mask|~","(Doom of Mokhaiotl) Obtain ~|dom|~","(All Pets) Obtain ~|dom|~"



]

banned_chunks: list[str] = [
    "chunk_12436","chunk_5530","chunk_6473","chunk_6489","chunk_6488","chunk_6487","chunk_6486","chunk_6745","chunk_6744","chunk_6743","chunk_6742",
    "chunk_6494","chunk_9495","chunk_9496","chunk_9752","chunk_9751","chunk_9750","chunk_7006","chunk_7006","chunk_7008","chunk_7766","chunk_7767",
    "chunk_8022","chunk_8023","chunk_8280","chunk_8536","chunk_6557","chunk_6556","chunk_6813","chunk_6812","chunk_12127","chunk_7234",
    "chunk_7242","chunk_7243","chunk_7244","chunk_8009","chunk_8268","chunk_8012","chunk_6808","chunk_6809","chunk_9113","chunk_6552","chunk_6553",
    "chunk_6810","chunk_6851","chunk_6223","chunk_14242","chunk_14243","chunk_7513","chunk_7514","chunk_7769","chunk_7770","chunk_8025","chunk_8026",
    "chunk_6494","chunk_6495","chunk_6496","chunk_6750","chunk_6751","chunk_6752","chunk_7006","chunk_7007","chunk_7008","chunk_6729","chunk_6731",
    "chunk_6985","chunk_6994","chunk_7484","chunk_7490","chunk_7494","chunk_7499","chunk_7500","chunk_7501","chunk_7502","chunk_7504","chunk_7564",
    "chunk_7565","chunk_7820","chunk_7821","chunk_8076","chunk_8077","chunk_8332","chunk_8333","chunk_7748","chunk_7752","chunk_7755","chunk_7758",
    "chunk_7763","chunk_7754","chunk_8010","chunk_8011","chunk_8014","chunk_8270","chunk_8526","chunk_8782","chunk_9038","chunk_9294","chunk_9550",
    "chunk_9806","chunk_8015","chunk_8261","chunk_8269","chunk_8276","chunk_8278","chunk_8493","chunk_8493-1","chunk_8493-3","chunk_8749","chunk_9005-1",
    "chunk_7496","chunk_8008","chunk_8519","chunk_8520","chunk_8521","chunk_8524","chunk_8525","chunk_8534","chunk_9357","chunk_9358","chunk_9359",
    "chunk_9360","chunk_9613","chunk_9614","chunk_9615","chunk_9616","chunk_9869","chunk_9870","chunk_9871","chunk_9872","chunk_10125","chunk_10126",
    "chunk_10127","chunk_10128","chunk_10381","chunk_10382","chunk_10383","chunk_10384","chunk_10637","chunk_10638","chunk_10639","chunk_10640",
    "chunk_9799","chunk_9805","chunk_9812","chunk_10055","chunk_10311","chunk_10567","chunk_11335","chunk_11591","chunk_12105","chunk_12182",
    "chunk_12619","chunk_13130","chunk_13133","chunk_13134","chunk_13135","chunk_13136","chunk_13137","chunk_13138","chunk_13139","chunk_13140",
    "chunk_13141","chunk_13145","chunk_13379","chunk_13386","chunk_13390","chunk_13391","chunk_13393","chunk_13394","chunk_13395","chunk_13396",
    "chunk_13397","chunk_13401","chunk_13643","chunk_13644","chunk_13645","chunk_13646","chunk_13647","chunk_13878","chunk_13899",
    "chunk_13900","chunk_14156","chunk_14398","chunk_14476","chunk_14477","chunk_14478","chunk_14732","chunk_14733","chunk_14734","chunk_14995",
    "chunk_15007","chunk_15248","chunk_16013","chunk_16014","chunk_16269","chunk_16270","chunk_16782","chunk_17038","chunk_8794","chunk_8795",
    "chunk_8796","chunk_8797","chunk_8798","chunk_9050","chunk_9051","chunk_9052","chunk_9053","chunk_9054","chunk_9306","chunk_9307","chunk_9308",
    "chunk_9309","chunk_9310","chunk_9562","chunk_9563","chunk_9564","chunk_9565","chunk_9566","chunk_9818","chunk_9819","chunk_9820","chunk_9821",
    "chunk_9822","chunk_10074","chunk_10075","chunk_10076","chunk_10077","chunk_10078","chunk_10330","chunk_10331","chunk_10332","chunk_10333",
    "chunk_10334","chunk_8789","chunk_12637","chunk_12638","chunk_12639","chunk_12640","chunk_12893","chunk_12894","chunk_12895","chunk_12896",
    "chunk_13149","chunk_13150","chunk_13151","chunk_13152","chunk_13405","chunk_13406","chunk_13407","chunk_13408","chunk_9541","chunk_9540",
    "chunk_9797","chunk_9796","chunk_9287","chunk_9293","chunk_9549","chunk_9370","chunk_9551","chunk_9552","chunk_9807","chunk_9808","chunk_10063",
    "chunk_10064","chunk_12132","chunk_11424","chunk_10658","chunk_12995","chunk_13250","chunk_12126","chunk_9558","chunk_9620","chunk_9621",
    "chunk_9622","chunk_9623","chunk_9878","chunk_9879","chunk_9624","chunk_9625","chunk_9880","chunk_9881","chunk_9626","chunk_10310","chunk_10566",
    "chunk_9634","chunk_9635","chunk_9890","chunk_9891","chunk_9802","chunk_9823","chunk_9824","chunk_9874","chunk_10056","chunk_10058","chunk_10070",
    "chunk_10071","chunk_10135","chunk_10136","chunk_10138","chunk_10139","chunk_10301","chunk_10314","chunk_10335","chunk_10336","chunk_10591",
    "chunk_10592","chunk_10643","chunk_10644","chunk_10645","chunk_10899","chunk_10900","chunk_10901","chunk_10652","chunk_10653","chunk_10819",
    "chunk_10828","chunk_10831","chunk_10575","chunk_10846","chunk_10847","chunk_10848","chunk_11102","chunk_11103","chunk_11104","chunk_11358",
    "chunk_11359","chunk_11360","chunk_11616","chunk_10894","chunk_11150","chunk_11151","chunk_10895","chunk_10649","chunk_10650","chunk_10905",
    "chunk_10907","chunk_10908","chunk_11163","chunk_11164","chunk_11059-2","chunk_11081","chunk_11154","chunk_11161","chunk_11417","chunk_11673",
    "chunk_11416","chunk_11672","chunk_11671","chunk_11165","chunk_11343","chunk_11345","chunk_11346","chunk_11347","chunk_11601","chunk_11602",
    "chunk_11603","chunk_11408","chunk_11409","chunk_11582","chunk_11593","chunk_11666","chunk_11850","chunk_11851","chunk_11852","chunk_12106",
    "chunk_12107","chunk_12108","chunk_12362","chunk_12363","chunk_12364","chunk_11853","chunk_11854","chunk_11855","chunk_12109","chunk_12110",
    "chunk_12111","chunk_11857","chunk_11413","chunk_11414","chunk_11669","chunk_11925","chunk_12181","chunk_11930","chunk_12113","chunk_12117",
    "chunk_12369","chunk_12441","chunk_12442","chunk_12443","chunk_12698","chunk_12954","chunk_13210","chunk_12441","chunk_12442","chunk_12443",
    "chunk_12444","chunk_12698","chunk_12954","chunk_13210","chunk_12955","chunk_12448","chunk_12621","chunk_12622","chunk_12623","chunk_13133",
    "chunk_13134","chunk_13135","chunk_12636","chunk_12892","chunk_12690","chunk_12946","chunk_13202","chunk_12696","chunk_12701","chunk_12702",
    "chunk_12703","chunk_12957","chunk_12958","chunk_12959","chunk_12737","chunk_12738","chunk_12993","chunk_12994","chunk_12613","chunk_12869",
    "chunk_13125","chunk_12611","chunk_12612","chunk_13122","chunk_13123","chunk_12867","chunk_12951","chunk_12953","chunk_13128","chunk_13148",
    "chunk_13199","chunk_13204","chunk_13460","chunk_13205","chunk_13404","chunk_13462","chunk_13463","chunk_13469","chunk_13470","chunk_13725",
    "chunk_13726","chunk_13641","chunk_13642","chunk_13643","chunk_13644","chunk_13645","chunk_13646","chunk_13647","chunk_13658","chunk_13659",
    "chunk_13914","chunk_13915","chunk_14154","chunk_14393","chunk_13977","chunk_13978","chunk_14232","chunk_14233","chunk_14487","chunk_14488",
    "chunk_13721","chunk_14653","chunk_14654","chunk_14909","chunk_14910","chunk_14999","chunk_15000","chunk_15001","chunk_15255","chunk_15256",
    "chunk_15257","chunk_15511","chunk_15512","chunk_15513","chunk_15262","chunk_15263","chunk_15515","chunk_11605","chunk_13197","chunk_11595",
    "chunk_7257","chunk_4759","chunk_5022","chunk_5023","chunk_5278","chunk_5535","chunk_5536","chunk_12633"
]

banned_drop_items:list[str]=[
    "SuperiorDropTable+","GemDropTableLegends+","Clue nest loot","Crystal impling","Alomone","Basilisk Youngling","Big Snake","Colossal Chocco Chicken",
    "Dagannoth mother","Damis","Demon of Balance","Demon of Darkness","Demon of Light","Derwen","Durial321","Evil Chicken (Recipe for Disaster)",
    "Forgotten Soul (Soul Wars)","Gang boss","Gangster","Giant Sea Snake","Glod","Golem","Justiciar Zachariah","Kebbit","Nazastarool",
    "Nylocas Vasilias","Pestilent Bloat","Pheasant","Porazdir","Shaeded Beast","Slash Bash","Sotetseg","The Maiden of Sugadinti","The Mimic",
    "Undead Zealot","Verzik Vitur","Wolf (Soul Wars)","Xarpus","Zombie (Zogre Flesh Eaters)","Tanglefoot"
]

banned_thieving_objects:list[str]=[
    "Anja","Agnar","Berry","Borrokar","Cuffs","Curator Haig Halen","Dr Fenkenstrain","Drunken man","Fairy Godfather","Freidir","Gnome child",
    "Gnome woman","Guard (Shayzien)","Head Guard","Hengel","Inga","Jeff","Jennella","Lanzig","Lensa","Narf","Pontak","Sandy","Sassilik",
    "Sigmund","Student","Guard (Hosidius)","Twig","Woman","Zealot","Rusty"
]

reverse_connect_chunks:list[str]=[
    "chunk_Death's Office"
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

task_macros: dict[str,list[str]] = {}

task_unlock_item: dict[str,list[RuleElement]] = {}
task_unlock_drops: dict[str,dict[str,list[RuleElement]]] = {}
task_unlock_drops_generic: dict[str,list[RuleElement]] = {}

task_unlock_monster: dict[str,dict[str,list[RuleElement]]] = {}
task_unlock_npc: dict[str,dict[str,list[RuleElement]]] = {}
task_unlock_object: dict[str,dict[str,list[RuleElement]]] = {}
task_unlock_shop: dict[str,dict[str,list[RuleElement]]] = {}
task_unlock_spawn: dict[str,dict[str,list[RuleElement]]] = {}


slayer_level_req: dict[str,int] = {}

monster_rows: list[MonsterRow] = []
non_monster_rows: list[MonsterRow] = []
non_monster_names: list[str] = []

defered_region_connections: list[tuple[str,str]] = []

# todo : fix this later but for now have some manually placed entrances
# todo : fix implied telegrab e.g. ardougne zoo jogre

monster_rows.append(MonsterRow("kill_Monster[+]","Macro",[]))

regions["Nothing :("] = "Nothing :("

item_csv_rows = []

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
    return "["+(",".join([f"DropElement({str_format(s.dest)},{str(s.rate)},{str_rules(s.rule)})" for s in ss]))+"]"

def convert_chunk_id(id:str)->str:
    return f"chunk_{id}"

def convert_monster_name(name:str)->str:
    return f"kill_{name}"

def convert_loot_name(name:str)->str:
    return f"loot_{name}"

def convert_drop_table(drop_table):
    return_table = {}
    for key, value in drop_table.items():
        part_table = {}
        rate, quant = value.split("@",1)
        part_table[quant] = rate
        return_table[key] = part_table
    return return_table

def iterate_drop_table(drop_table,drop_source):
    exception_list = ["always","varies","rare","unknown","uncommon","common","very rare","random"]
    drop_list = []
    if set(drop_table.keys()).intersection(banned_drop_items):
        return [] #if there is any key that's on the banned list, quit out early
    for drop_item, rates_table in drop_table.items():
        normal_item = True
        if drop_item in non_monster_names:
            drop_item = convert_loot_name(drop_item)
            normal_item = False
        noted_rate = 0
        raw_rate = 0
        rule_list = []
        if drop_item in task_unlock_drops_generic:
            rule_list.extend(task_unlock_drops_generic[drop_item])
        if drop_item in task_unlock_drops and drop_source in task_unlock_drops[drop_item]:
            rule_list.extend(task_unlock_drops[drop_item][drop_source])
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
            if not normal_item:
                noted_rate = pow(noted_rate,2) #if it's a macro, assume it's going to be at least as bad
            resolved_noted_rate = int(pow(min(noted_rate,1),-1))
            drop_list.append(DropElement(drop_item+" (noted)",resolved_noted_rate,rule_list))
        if raw_rate > 0:
            if not normal_item:
                raw_rate = pow(raw_rate,2)
            resolved_raw_rate = int(pow(min(raw_rate,1),-1))
            drop_list.append(DropElement(drop_item,resolved_raw_rate,rule_list))
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
        for obj in chunk["Object"].keys():
            if not obj in resources:
                resources.append(obj)
                resource_list.append(ResourceRow(obj))
            chunk["Contents"].append(obj)
            if obj in task_unlock_object and chunk_id in task_unlock_object[obj]:
                re_entrances.append(EntranceRow(chunk_id,obj,task_unlock_object[obj][chunk_id]))
            else:
                re_entrances.append(EntranceRow(chunk_id,obj,[]))
    if "Spawn" in chunk:
        for spawn in chunk["Spawn"].keys():
            if spawn not in resources:
                resources.append(spawn)
                resource_list.append(ResourceRow(spawn))
            chunk["Contents"].append(spawn)
            if spawn in task_unlock_spawn and chunk_id in task_unlock_spawn[spawn]:
                re_entrances.append(EntranceRow(chunk_id,spawn,task_unlock_spawn[spawn][chunk_id]))
            else:
                re_entrances.append(EntranceRow(chunk_id,spawn,[]))
    if "Monster" in chunk:
        for monster in chunk["Monster"].keys():
            monster = convert_monster_name(monster)
            if not monster in monsters:
                monsters.append(monster)
                monster_to_find.append(monster)
                mm_entrances.append(EntranceRow(monster,"kill_Monster[+]",[]))
            chunk["Contents"].append(monster)
            if monster in task_unlock_monster and chunk_id in task_unlock_monster[monster]:
                rm_entrances.append(EntranceRow(chunk_id,monster,task_unlock_monster[monster][chunk_id]))
            else:
                rm_entrances.append(EntranceRow(chunk_id,monster,[]))
    if "NPC" in chunk:
        for npc in chunk["NPC"].keys():
            if "Object" in chunk and npc in chunk["Object"]:
                continue
            if not npc in resources:
                resources.append(npc)
                resource_list.append(ResourceRow(npc))
            chunk["Contents"].append(npc)
            if npc in task_unlock_npc and chunk_id in task_unlock_npc[npc]:
                re_entrances.append(EntranceRow(chunk_id,npc,task_unlock_npc[npc][chunk_id]))
            else:
                re_entrances.append(EntranceRow(chunk_id,npc,[]))
    if "Shop" in chunk:
        for shop in chunk["Shop"].keys():
            if not shop in resources:
                resources.append(shop)
                resource_list.append(ResourceRow(shop))
            chunk["Contents"].append(shop)
            if shop in task_unlock_shop and chunk_id in task_unlock_shop[shop]:
                re_entrances.append(EntranceRow(chunk_id,shop,task_unlock_shop[shop][chunk_id]))
            else:
                re_entrances.append(EntranceRow(chunk_id,shop,[]))
    #if chunk_id == "chunk_12698":
    #    breakpoint()
    chunks[chunk_id]=chunk
    regions_list.append(RegionRow(chunk_id,chunk_name))

with open(os.path.join(this_dir, "chunkpicker-chunkinfo-export.json"), 'r') as localJSON:
    exportedJSON = json.load(localJSON)
    for slayer_monster, slayer_level in exportedJSON["slayerMonsters"].items():
        if slayer_level>1:
            slayer_level_req[slayer_monster] = slayer_level
    for category,lock_blob in exportedJSON["taskUnlocks"].items():
        if category == "Items":
            for item, rules in lock_blob.items():
                rule_list = []
                for rule in rules:
                    for req,req_type in rule.items():
                        if req in banned_tasks:
                            continue
                        if "[+]" in req:
                            if req not in task_macros:
                                print(req)
                                breakpoint()
                            rule_list.append(RuleElement("task_macro",req))
                        else:
                            rule_list.append(RuleElement("task",req))
                if not rule_list:
                    continue #The rule list is empty if it's only banned tasks
                if "^" not in item:
                    task_unlock_item[item] = rule_list
                elif item.endswith("^"):
                    item = item.rstrip("^")
                    task_unlock_drops_generic[item] = rule_list
                else:
                    i,m = item.split("^",2)
                    if i not in task_unlock_drops:
                        task_unlock_drops[i] = {}
                    task_unlock_drops[i][convert_monster_name(m)] = rule_list
        else:
            for value, value_blob in lock_blob.items():
                for locked_chunk, rules in value_blob.items():
                    locked_chunk = convert_chunk_id(locked_chunk)
                    rule_list = []
                    for rule in rules:
                        for req,req_type in rule.items():
                            if req in banned_tasks:
                                continue
                            if "[+]" in req:
                                if req not in task_macros:
                                    print(req)
                                    breakpoint()
                                rule_list.append(RuleElement("task_macro",req))
                            else:
                                rule_list.append(RuleElement("task",req))
                    if not rule_list:
                        continue
                    relevent_dict = None
                    if category == "Monsters":
                        relevent_dict = task_unlock_monster
                    elif category == "NPCs":
                        relevent_dict = task_unlock_npc
                    elif category == "Objects":
                        relevent_dict = task_unlock_object
                    elif category == "Shops":
                        relevent_dict = task_unlock_shop
                    elif category == "Spawns":
                        relevent_dict = task_unlock_spawn
                    if relevent_dict == None:
                        print("PANIC! "+value)
                        breakpoint()
                        continue
                    if value not in relevent_dict:
                        relevent_dict[value] = {}
                    relevent_dict[value][locked_chunk] = rule_list
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
        if source_chunk in banned_chunks or dest_chunk in banned_chunks or source_chunk in reverse_connect_chunks:
            continue
        if dest_chunk not in chunks:
            if f"{dest_chunk}-1" not in chunks:
                print("PANIC!! " + dest_chunk)
            else:
                dest_chunk = f"{dest_chunk}-1"
        dest_name = chunks[dest_chunk]["Chunk_Name"]
        if dest_name:
            rr_entrances.append(EntranceRow(source_chunk,dest_chunk,[RuleElement("has",f"Area: {dest_name}")]))
        else:
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
        if macro_name in banned_groups:
            continue
        if macro_name not in resources:
            resources.append(macro_name)
            resource_list.append(ResourceRow(macro_name))
        if macro_name in bidirectional_groups: #reversable macro group, e.g. decanting
            for sub_item in macro_list: 
                if sub_item not in resources:
                    resources.append(sub_item)
                    resource_list.append(ResourceRow(sub_item))
                if sub_item in missing_resources:
                    missing_resources.remove(sub_item)
                ee_entrances.append(EntranceRow(macro_name,sub_item,[]))
        for sub_item in macro_list:
            ee_entrances.append(EntranceRow(sub_item,macro_name,[]))
            if sub_item not in resources and sub_item not in missing_resources:
                missing_resources.append(sub_item)
    for macro_name, macro_list in exportedJSON["codeItems"]["tasksPlus"].items():
        if macro_name in banned_groups:
            continue
        loc_list = []
        for loc in macro_list:
            loc_list.append(loc)
        task_macros[macro_name] = loc_list
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
                sub_chunk_name = chunks[sub_chunk]["Chunk_Name"]
                if sub_chunk_name:
                    rr_entrances.append(EntranceRow(macro_name,sub_chunk,[RuleElement("has",f"Area: {sub_chunk_name}")]))
                else:
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
        if macro_name in banned_drop_items:
            continue
        non_monster_names.append(macro_name)
        macro_name = convert_loot_name(macro_name)
        if macro_name not in resources:
            resources.append(macro_name)
            resource_list.append(ResourceRow(macro_name))
        drop_list = iterate_drop_table(convert_drop_table(macro_list),macro_name)
        if drop_list:
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
            if drop_source in banned_drop_items:
                continue
            if category == "Thieving" and drop_source in banned_thieving_objects:
                continue
            old_drop_source = drop_source
            drop_source = convert_loot_name(drop_source)
            drop_list = iterate_drop_table(drop_table,drop_source)
            if drop_list:
                if old_drop_source in non_monster_names:
                    continue
                non_monster_names.append(old_drop_source)
                if drop_source not in resources:
                    resources.append(drop_source)
                    resource_list.append(ResourceRow(drop_source))
                drop_source_category:str = drop_source
                if "#" in drop_source:
                    drop_source_category = drop_source_category.split("#")[0] #just want the first section
                non_monster_rows.append(MonsterRow(drop_source,drop_source_category,drop_list))
                if category == "Slayer" and convert_monster_name(old_drop_source) in monster_to_find:
                    monster_name = convert_monster_name(old_drop_source)
                    monster_to_find.remove(monster_name)
                    if monster_name not in resources:
                        resources.append(monster_name)
                        resource_list.append(ResourceRow(monster_name))
                    rule_list = []
                    if old_drop_source in slayer_level_req:
                        rule_list.append(RuleElement("skill",f"Slayer_{str(slayer_level_req[old_drop_source])}"))
                    me_entrances.append(EntranceRow(monster_name,drop_source,rule_list)) 
    for drop_source, drop_table in exportedJSON["drops"].items():
        if drop_source in banned_drop_items:
            continue
        old_drop_source = drop_source
        drop_source = convert_monster_name(drop_source)
        drop_list = iterate_drop_table(drop_table,drop_source)
        if drop_list:
            drop_source_category:str = drop_source
            if drop_source not in monsters:
                continue
            if drop_source in monster_to_find:
                monster_to_find.remove(drop_source)
            if "#" in drop_source:
                drop_source_category = drop_source_category.split("#")[0] #just want the first section
            monster_rows.append(MonsterRow(drop_source,drop_source_category,drop_list))
            non_quest_list.append(LocationRow(f"Kill ~|{old_drop_source}|~","Kill",drop_source,"",[],0,0,0))
    for chunk_id,sections in exportedJSON["sections"].items():
        for section_id,connections in sections.items():
            section_name = f"{chunk_id}-{section_id}"
            if section_id == "0":
                section_name = chunk_id
            section_name = convert_chunk_id(section_name)
            if section_name not in chunks:
                print("PANIC! : "+ section_name)
                continue
            for raw_connection in connections:
                connection = convert_chunk_id(raw_connection)
                if connection not in chunks:
                    if f"{connection}-1" in chunks:
                        connection += "-1"
                    else:
                        print("PANIC! : " + connection)
                        continue
                if "Connect" not in chunks[section_name]:
                    chunks[section_name]["Connect"] = {}
                chunks[section_name]["Connect"][raw_connection] = True
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
                description = ""
                parent_region = None
                rule_list = []
                if "Complete" in quest_name:
                    target_list = quest_list
                    category = "quest"
                if "Tasks" in quest_data:
                    for req,req_type in quest_data["Tasks"].items():
                        if req in banned_tasks:
                            continue
                        if "[+]" in req:
                            if req not in task_macros:
                                print(req)
                                breakpoint()
                            rule_list.append(RuleElement("task_macro",req))
                        else:
                            rule_list.append(RuleElement("task",req))
                if "Skills" in quest_data:
                    for skill,skill_level in quest_data["Skills"].items():
                        if skill_level > 1:
                            rule_list.append(RuleElement("skill",f"{skill}_{str(skill_level)}"))
                if "Chunks" in quest_data:
                    for chunk in quest_data["Chunks"]:
                        if "[+]" in chunk and not chunk.endswith("[+]"):
                            chunk,_ = chunk.rsplit("x",1)
                            #todo fix this
                        chunk = convert_chunk_id(chunk)
                        if chunk not in chunks:
                            chunk = chunk+"-1"
                            if chunk not in chunks:
                                print(chunk[:-2])
                                breakpoint()
                        if parent_region is None:
                            parent_region = chunk
                        rule_list.append(RuleElement("chunk",chunk))
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
                        item = item.rstrip("*")
                        if "[+]" in item and not item.endswith("[+]"):
                            try:
                                item,_ = item.rsplit("x",1)
                                #todo fix this
                            except:
                                breakpoint()
                        if parent_region is None:
                            parent_region = item
                        rule_list.append(RuleElement("can_reach",item))
                if "Monsters" in quest_data:
                    for monster in quest_data["Monsters"]:
                        monster = convert_monster_name(monster)
                        if parent_region is None:
                            parent_region = monster
                        rule_list.append(RuleElement("kill",monster))
                if parent_region:
                    parent_region = parent_region.rstrip("*")
                    rule_list = [value for value in rule_list if value.value != parent_region]
                else:
                    parent_region = "Menu"
                if "QuestPointsNeeded" in quest_data:
                    rule_list.append(RuleElement("questPoints",str(quest_data["QuestPointsNeeded"])))
                if "KudosNeeded" in quest_data:
                    rule_list.append(RuleElement("kudos",str(quest_data["KudosNeeded"])))
                if "CombatPointsNeeded" in quest_data:
                    rule_list.append(RuleElement("combatPoints",str(quest_data["CombatPointsNeeded"])))
                if "Reward" in quest_data:
                    for item in quest_data["Reward"]:
                        if item not in resources:
                            resources.append(item)
                            resource_list.append(ResourceRow(item))
                        if item in missing_resources:
                            missing_resources.remove(item)
                        re_entrances.append(EntranceRow(parent_region,item,rule_list))
                kudos_reward = 0
                quest_point_reward = 0
                combat_point_reward = 0
                if "QuestPoints" in quest_data:
                    quest_point_reward = int(quest_data["QuestPoints"])
                if "Kudos" in quest_data:
                    kudos_reward = int(quest_data["Kudos"])
                if "CombatPoints" in quest_data:
                    combat_point_reward = int(quest_data["CombatPoints"])
                if "Description" in quest_data:
                    description = quest_data["Description"]
                target_list.append(LocationRow(quest_name,category,parent_region,description,rule_list,kudos_reward,quest_point_reward,combat_point_reward))

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
        elif task_type in skill_names:
            for task_name, task_data in task_list.items():
                if task_name in banned_tasks:
                    continue
                if "Category" in task_data and "Quest Skill Reqs" in task_data["Category"]:
                    continue #these aren't real, and aren't needed
                parent_region = None
                description = ""
                parent_region_type = None
                rule_list = []
                if "Chunks" in task_data:
                    for chunk in task_data["Chunks"]:
                        chunk = convert_chunk_id(chunk)
                        if chunk not in chunks:
                            chunk = chunk+"-1"
                            if chunk not in chunks:
                                print(chunk[:-2])
                                breakpoint()
                        if parent_region is None:
                            parent_region = chunk
                            parent_region_type = "r"
                        rule_list.append(RuleElement("chunk",chunk))
                if "NPCs" in task_data:
                    for npc in task_data["NPCs"]:
                        if parent_region is None:
                            parent_region = npc
                            parent_region_type = "e"
                        rule_list.append(RuleElement("can_reach",npc))
                if "Level" in task_data:
                    if task_data["Level"]>1:
                        rule_list.append(RuleElement("skill",f"{task_type}_{str(task_data['Level'])}"))
                if "Objects" in task_data:
                    for object in task_data["Objects"]:
                        if parent_region is None:
                            parent_region = object
                            parent_region_type = "e"
                        rule_list.append(RuleElement("can_reach",object))
                if "Skills" in task_data:
                    for skill,skill_level in task_data["Skills"].items():
                        if skill_level>1:
                            rule_list.append(RuleElement("skill",f"{skill}_{str(skill_level)}"))
                if "Items" in task_data:
                    for item in task_data["Items"]:
                        item = item.rstrip("*")
                        if parent_region is None:
                            parent_region = item
                            parent_region_type = "e"
                        rule_list.append(RuleElement("can_reach",item))
                if "Tasks" in task_data:
                    for req,req_type in task_data["Tasks"].items():
                        if req in banned_tasks:
                            continue
                        if "[+]" in req:
                            if req not in task_macros:
                                print(req)
                                breakpoint()
                            rule_list.append(RuleElement("task_macro",req))
                        else:
                            rule_list.append(RuleElement("task",req))
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
                            parent_region_type = "m"
                        if monster in monster_to_find:
                            monster_category:str = monster
                            if "#" in monster:
                                monster_category = monster.split("#")[0] #just want the first section
                            monster_rows.append(MonsterRow(monster,monster_category,[]))
                            monster_to_find.remove(monster)
                        rule_list.append(RuleElement("kill",monster))
                if parent_region:
                    parent_region = parent_region.rstrip("*")
                    rule_list = [value for value in rule_list if value.value != parent_region]
                else:
                    parent_region = "Menu"
                    parent_region_type = "r"
                if "Primary" in task_data and task_data["Primary"]:
                    #primary training method
                    output = "None"
                    level = 0
                    if "Output" in task_data:
                        output = task_data["Output"]
                    if "Level" in task_data:
                        level = task_data["Level"]
                    training_methods.append(TrainingRow(output,task_type,level,parent_region,task_name,rule_list))
                    if output != "None": training_outputs.append(output)
                if task_name in non_quest_names: #have to do it down here so we can do training methods
                    if task_name not in non_quest_dupes:
                        non_quest_dupes.append(task_name)
                    continue #for now just ignore it and hope it goes away (it won't)
                if "Output" in task_data:
                    output = task_data["Output"]
                    if output in non_monster_names:
                        output = convert_loot_name(output)
                    if output not in resources:
                        if output in regions:
                            print(output)
                            breakpoint()
                        resources.append(output)
                        resource_list.append(ResourceRow(output))
                    if output in missing_resources:
                        missing_resources.remove(output)
                    if output in task_unlock_item:
                        rule_list = rule_list + task_unlock_item[output]
                    if parent_region_type == "r":
                        re_entrances.append(EntranceRow(parent_region,output,rule_list))
                    elif parent_region_type == "e":
                        ee_entrances.append(EntranceRow(parent_region,output,rule_list))
                    elif parent_region_type == "m":
                        me_entrances.append(EntranceRow(parent_region,output,rule_list))
                    else:
                        print(task_name)
                        breakpoint()
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
                    if parent_region_type == "r":
                        re_entrances.append(EntranceRow(parent_region,output_obj,rule_list))
                    elif parent_region_type == "e":
                        ee_entrances.append(EntranceRow(parent_region,output_obj,rule_list))
                    elif parent_region_type == "m":
                        me_entrances.append(EntranceRow(parent_region,output_obj,rule_list))
                    else:
                        print(task_name)
                        breakpoint()
                if "Description" in task_data:
                    description = task_data["Description"]
                non_quest_list.append(LocationRow(task_name,task_type,parent_region,description,rule_list,0,0,0))
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
                if "Category" in task_data and "Starting Items" in task_data["Category"] and "Output" in task_data:
                    re_entrances.append(EntranceRow("Starting Items",task_data["Output"],[]))
                    continue
                parent_region = None
                parent_region_type = None
                description = ""
                rule_list = []
                if "ForcedSecondary" in task_data and task_data["ForcedSecondary"]:
                    continue #Used in sources that aren't real but technically exist... just ignore them
                if "ClueTier" in task_data or "ClueType" in task_data:
                    continue #Clues don't exist and they cannot hurt me
                if "StarRegion" in task_data:
                    continue #I don't actually know what these are for so right now we're ignoring them
                if "Chunks" in task_data:
                    for chunk in task_data["Chunks"]:
                        chunk = convert_chunk_id(chunk)
                        if chunk not in chunks:
                            chunk = chunk+"-1"
                            if chunk not in chunks:
                                print(chunk[:-2])
                                breakpoint()
                        if parent_region is None:
                            parent_region = chunk
                            parent_region_type = "r"
                        rule_list.append(RuleElement("chunk",chunk))
                if "NPCs" in task_data:
                    for npc in task_data["NPCs"]:
                        if parent_region is None:
                            parent_region = npc
                            parent_region_type = "e"
                        rule_list.append(RuleElement("can_reach",npc))
                if "Objects" in task_data:
                    for object in task_data["Objects"]:
                        if parent_region is None:
                            parent_region = object
                            parent_region_type = "e"
                        rule_list.append(RuleElement("can_reach",object))
                if "Skills" in task_data:
                    for skill,skill_level in task_data["Skills"].items():
                        if skill_level>1:
                            rule_list.append(RuleElement("skill",f"{skill}_{str(skill_level)}"))
                if "Items" in task_data:
                    for item in task_data["Items"]:
                        item = item.rstrip("*")
                        if parent_region is None:
                            parent_region = item
                            parent_region_type = "e"
                        rule_list.append(RuleElement("can_reach",item))
                if "Tasks" in task_data:
                    for req,req_type in task_data["Tasks"].items():
                        if req in banned_tasks:
                            continue
                        if "[+]" in req:
                            if not req.endswith("[+]"):
                                req,count = req.rsplit("x",1)
                                if req not in task_macros:
                                    print(req)
                                    breakpoint()
                                rule_list.append(RuleElement("task_macrox"+count,req))
                            else:
                                if req not in task_macros:
                                    print(req)
                                    breakpoint()
                                rule_list.append(RuleElement("task_macro",req))
                        else:
                            rule_list.append(RuleElement("task",req))
                if "Monsters" in task_data:
                    for monster in task_data["Monsters"]:
                        monster = convert_monster_name(monster)
                        if parent_region is None:
                            parent_region = monster
                            parent_region_type = "m"
                        if monster in monster_to_find:
                            monster_category:str = monster
                            if "#" in monster:
                                monster_category = monster.split("#")[0] #just want the first section
                            monster_rows.append(MonsterRow(monster,monster_category,[]))
                            monster_to_find.remove(monster)
                        rule_list.append(RuleElement("kill",monster))
                if "QuestPointsNeeded" in task_data:
                    rule_list.append(RuleElement("questPoints",str(task_data["QuestPointsNeeded"])))
                if parent_region:
                    parent_region = parent_region.rstrip("*")
                    rule_list = [value for value in rule_list if value.value != parent_region]
                else:
                    parent_region = "Menu"
                    parent_region_type = "r"
                #todo: TotalLevelNeeded
                if "Output" in task_data:
                    output = task_data["Output"]
                    if output in non_monster_names:
                        output = convert_loot_name(output)
                    if output not in resources:
                        if output in regions:
                            print(output)
                            print(regions[output])
                            breakpoint()
                        resources.append(output)
                        resource_list.append(ResourceRow(output))
                    if output in missing_resources:
                        missing_resources.remove(output)
                    if output in task_unlock_item:
                        rule_list = rule_list + task_unlock_item[output]
                    if parent_region_type == "r":
                        re_entrances.append(EntranceRow(parent_region,output,rule_list))
                    elif parent_region_type == "e":
                        ee_entrances.append(EntranceRow(parent_region,output,rule_list))
                    elif parent_region_type == "m":
                        me_entrances.append(EntranceRow(parent_region,output,rule_list))
                    else:
                        print(task_name)
                        breakpoint()
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
                    if parent_region_type == "r":
                        re_entrances.append(EntranceRow(parent_region,output_obj,rule_list))
                    elif parent_region_type == "e":
                        ee_entrances.append(EntranceRow(parent_region,output_obj,rule_list))
                    elif parent_region_type == "m":
                        me_entrances.append(EntranceRow(parent_region,output_obj,rule_list))
                    else:
                        print(task_name)
                        breakpoint()
                if "Reward" in task_data:
                    for item in task_data["Reward"]:
                        if item not in resources:
                            resources.append(item)
                            resource_list.append(ResourceRow(item))
                        if item in missing_resources:
                            missing_resources.remove(item)
                        if parent_region_type == "r":
                            re_entrances.append(EntranceRow(parent_region,item,rule_list))
                        elif parent_region_type == "e":
                            ee_entrances.append(EntranceRow(parent_region,item,rule_list))
                        elif parent_region_type == "m":
                            me_entrances.append(EntranceRow(parent_region,item,rule_list))
                        else:
                            print(task_name)
                            breakpoint()
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
                    dest_chunk = convert_chunk_id(task_name)
                    if dest_chunk not in chunks or "Connect" not in chunks[dest_chunk]:
                        print(task_name)
                        breakpoint()
                    dest_rule_list = rule_list.copy()
                    dest_name = chunks[dest_chunk]["Chunk_Name"]
                    if dest_name:
                        dest_rule_list.append(RuleElement("has",f"Area: {dest_name}"))
                    for backwards_chunk in chunks[dest_chunk]["Connect"].keys():
                        backwards_chunk = convert_chunk_id(backwards_chunk)
                        if backwards_chunk in banned_chunks:
                            continue
                        if backwards_chunk not in chunks:
                            backwards_chunk += "-1"
                            if backwards_chunk not in chunks:
                                print("PANIC!! " + backwards_chunk)
                                breakpoint()
                        rr_entrances.append(EntranceRow(backwards_chunk,dest_chunk,dest_rule_list))

                kudos_reward = 0
                if "Kudos" in task_data:
                    kudos_reward = int(task_data["Kudos"])
                if "Description" in task_data:
                    description = task_data["Description"]
                if "ConnectsSections" not in task_data and "UnlocksArea" not in task_data: #don't make these as locations
                    non_quest_list.append(LocationRow(task_name,task_type,parent_region,"",rule_list,kudos_reward,0,0))
                    non_quest_names.append(task_name)
                for field in task_data.keys():
                    if field not in [
                            "Chunks","Output","Objects","Skills","Description","XpReward","NonShop",
                            "Priority","Not F2P","NoPet","Items","NoBoost","Category","Set",
                            "Tasks","NPCs","Not Equip","AlwaysValid","Output Object","Kudos",
                            "NoXp","Monsters","BackupParent","ManualInvalid","UnlocksArea",
                            "ManualNonProcessing","Source","InfoLink","ConnectsSections","Sections",
                            "QuestPointsNeeded","TotalLevelNeeded","Reward",
                            "ForcedSecondary","ClueTier","ClueType","StarRegion","Label","Requirements",
                            "Not Skiller","RequiredMonsterSource"
                        ]:
                        print(field)
                        print(task_name)
                        breakpoint()


                   
if len(missing_resources) > 0:
    print("PANIC! MISSING "+str(len(missing_resources))+" items!")

if len(monster_to_find) > 0:
    print("PANIC! MISSING "+str(len(monster_to_find)) + " monsters!")

with open(os.path.join(this_dir, "locations_csv.csv"), "w+", newline='') as loc_file:
    csv_writer = csv.writer(loc_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    for row in quest_list:
        # If there's a "#" that means it's a tier of diary or combat achievements, not a real quest
        if "#" in row.name:
            csv_writer.writerow([row.name, row.category, "", "", "", "", "ManualTask"])
        else:
            shortened_quest_name = "Quest: " + row.name[2:row.name.index("|~")]
            csv_writer.writerow([shortened_quest_name, row.category, "", "", "", "", "QuestTask"])

    for row in non_quest_list:
        target = row.name[row.name.find("~|") + 2:row.name.rfind("|~")]
        csv_row = [row.name, row.category, "", "", "", ""]
        if row.name.startswith("Kill") or row.name.startswith("Slay"):
            csv_row.extend(["KillTask", target])
        elif row.name.startswith("Wield") or row.name.startswith("Wear"):
            csv_row.extend(["EquipItemTask", row.category, target])
        elif row.name.startswith("Cook") or row.name.startswith("Bake"):
            csv_row.extend(["ChatMessageTask", row.category, "You successfully cook a "+target])
        elif row.name.startswith("Catch"):
            csv_row.extend(["ChatMessageTask", row.category, "You catch a "+target])
        # Exclude spells that cast "From a Blighted [] Sack"
        elif row.name.startswith("Cast") and "from a" not in row.name:
            csv_row.extend(["SpellTask", target])
        # Text is different for superheat items
        elif row.name.startswith("Smelt") and "superheat" not in row.name:
            target_metal = target.replace(" bar","")
            csv_row.extend(["ChatMessageTask", row.category, "You retreive a bar of "+target_metal])
        elif row.name.startswith("Mine"):
            target_ore = target.replace(" ore", "")
            csv_row.extend(["ChatMessageTask", row.category, "You manage to mine some "+target_ore])
        # You'd think prayers would be easy but I'd need to find the varbits for all of them so we'll get that later
        #elif row.name.startswith("Activate"):
        #    csv_row.extend()
        # If the task just says "Obtain" and doesn't care where, we can detect it
        elif "Obtain" in row.name and "from" not in row.name:
            csv_row.extend(["GetItemTask", row.category, target])
        else:
            csv_row.extend(["ManualTask"])

        csv_writer.writerow(csv_row)

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
                item_csv_rows.append([str_format("Area: "+region_name), "1", "progression", "Area", chunk_id.replace("chunk_","").split("-")[0]])

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

            regPyFile.write("me_entrances: list[EntranceRow] = [\n")

            for entrance_row in me_entrances:
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
                row_line += str_format(quest_row.description)
                row_line += ","
                row_line += str_rules(quest_row.rule)
                row_line += ","
                row_line += str(quest_row.kudos_reward)
                row_line += ","
                row_line += str(quest_row.quest_point_reward)
                row_line += ","
                row_line += str(quest_row.combat_point_reward)
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
                row_line += str_format(quest_row.description)
                row_line += ","
                row_line += str_rules(quest_row.rule)
                row_line += ","
                row_line += str(quest_row.kudos_reward)
                row_line += ","
                row_line += str(quest_row.quest_point_reward)
                row_line += ","
                row_line += str(quest_row.combat_point_reward)
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
                row_line += str_format(quest_row.description)
                row_line += ","
                row_line += str_rules(location_row.rule)
                row_line += ","
                row_line += str(location_row.kudos_reward)
                row_line += ","
                row_line += str(location_row.quest_point_reward)
                row_line += ","
                row_line += str(location_row.combat_point_reward)
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
                row_line += str_format(training_method.parent_region)
                row_line += ","
                row_line += str_format(training_method.task_name)
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

            regPyFile.write("task_macros: dict[str, list[str]] = {\n")
            for task_macro,task_macro_list in task_macros.items():
                regPyFile.write(f"\t{str_format(task_macro)}:[{','.join([str_format(i) for i in task_macro_list])}],\n")
            regPyFile.write("}\n\n")
                
            
            regPyFile.write("skill_names: list[str] = [")
            for skill_name in skill_names:
                regPyFile.write(f"{str_format(skill_name)},")
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

            regPyFile.write("non_monster_names: list[str] = [\n")
            for non_monster_name in non_monster_names:
                regPyFile.write(f"\t{str_format(non_monster_name)},\n")
            regPyFile.write("]\n\n")

with open(os.path.join(this_dir, "items_csv.csv"), "w+", newline='') as loc_file:
    csv_writer = csv.writer(loc_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    for row in item_csv_rows:
        csv_writer.writerow(row)

#with open(os.path.join(this_dir, "resources_generated2.py"),"w+") as resPyFile:
#            resPyFile.write('"""\nThis file was auto generated by LogicCSVToPython.py\n"""\n')
#            resPyFile.write("from ..Regions import ResourceRow\n")
#            resPyFile.write("\n")
#            resPyFile.write("resource_rows = [\n")
#            for row in resources:
#                row_line = f'ResourceRow("{row}")'
#                resPyFile.write(f"\t{row_line},\n")
#            resPyFile.write("]\n")