"""
    Ensures a target level can be reached with available resources
    """
from worlds.generic.Rules import CollectionRule, add_rule
from .Names import RegionNames, ItemNames
from rule_builder.rules import *


def get_fishing_skill_rule(level, options) -> Rule:
    if options.max_fishing_level < level:
        return False_()

    if options.brutal_grinds or level < 5:
        return CanReachRegion(RegionNames.Shrimp)
    if level < 20:
        return And(CanReachRegion(RegionNames.Shrimp), CanReachRegion(RegionNames.Port_Sarim))
    else:
        return And(CanReachRegion(RegionNames.Shrimp), CanReachRegion(RegionNames.Port_Sarim), CanReachRegion(RegionNames.Fly_Fish))


def get_mining_skill_rule(level, options) -> Rule:
    if options.max_mining_level < level:
        return False_()

    if options.brutal_grinds or level < 15:
        return Or( CanReachRegion(RegionNames.Bronze_Ores), CanReachRegion(RegionNames.Clay_Rock))
    else:
        # Iron is the best way to train all the way to 99, so having access to iron is all you need to check for
        return And(Or(CanReachRegion(RegionNames.Bronze_Ores), CanReachRegion(RegionNames.Clay_Rock)),CanReachRegion(RegionNames.Iron_Rock))


def get_woodcutting_skill_rule(level, options) -> Rule:
    if options.max_woodcutting_level < level:
        return False_()

    if options.brutal_grinds or level < 15:
        return CanReachRegion(RegionNames.Tree)
    if level < 30:
        return CanReachRegion(RegionNames.Oak_Tree)
    else:
        return And(CanReachRegion(RegionNames.Oak_Tree), CanReachRegion(RegionNames.Willow_Tree))


def get_smithing_skill_rule(level, options) -> Rule:
    if options.max_smithing_level < level:
        return False_()

    if options.brutal_grinds:
        return And(CanReachRegion(RegionNames.Bronze_Ores), CanReachRegion(RegionNames.Furnace))
    if level < 15:
        # Lumbridge has a special bronze-only anvil. This is the only anvil of its type so it's not included
        # in the "Anvil" resource region. We still need to check for it though.
        return And(CanReachRegion(RegionNames.Bronze_Ores), CanReachRegion(RegionNames.Furnace), Or(CanReachRegion(RegionNames.Anvil),CanReachRegion(RegionNames.Lumbridge)))
    if level < 30:
        # For levels between 15 and 30, the lumbridge anvil won't cut it. Only a real one will do
        return And(CanReachRegion(RegionNames.Bronze_Ores), CanReachRegion(RegionNames.Iron_Rock), CanReachRegion(RegionNames.Furnace), CanReachRegion(RegionNames.Anvil))
    else:
        return And(CanReachRegion(RegionNames.Bronze_Ores), CanReachRegion(RegionNames.Iron_Rock), CanReachRegion(RegionNames.Coal_Rock), CanReachRegion(RegionNames.Furnace), CanReachRegion(RegionNames.Anvil))


def get_crafting_skill_rule(level, options) -> Rule:
    if options.max_crafting_level < level:
        return False_()

    # Crafting is really complex. Need a lot of sub-rules to make this even remotely readable
    can_spin = And(CanReachRegion(RegionNames.Sheep), CanReachRegion(RegionNames.Spinning_Wheel))

    can_pot = And(CanReachRegion(RegionNames.Clay_Rock), CanReachRegion(RegionNames.Barbarian_Village))

    can_tan = And(CanReachRegion(RegionNames.Milk), CanReachRegion(RegionNames.Al_Kharid))

    mould_access = Or(CanReachRegion(RegionNames.Al_Kharid), CanReachRegion(RegionNames.Rimmington))

    can_silver = And(CanReachRegion(RegionNames.Silver_Rock), CanReachRegion(RegionNames.Furnace), mould_access)

    can_gold = And(CanReachRegion(RegionNames.Gold_Rock), CanReachRegion(RegionNames.Furnace), mould_access)

    if options.brutal_grinds or level < 5:
        return Or( can_spin, can_pot, can_tan)

    can_smelt_gold = get_smithing_skill_rule(40, options)
    can_smelt_silver = get_smithing_skill_rule(20, options)
    if level < 16:
        return Or( can_pot, can_tan, And(can_gold, can_smelt_gold))
    else:
        return Or( can_tan, And(can_silver, can_smelt_silver), And(can_gold, can_smelt_gold))


def get_cooking_skill_rule(level, options) -> Rule:
    if options.max_cooking_level < level:
        return False_()

    if options.brutal_grinds or level < 15:
        return Or(
            CanReachRegion(RegionNames.Milk),
            CanReachRegion(RegionNames.Egg),
            CanReachRegion(RegionNames.Shrimp),
            And(
                CanReachRegion(RegionNames.Wheat),
                CanReachRegion(RegionNames.Windmill)
            )
        )
    else:

        return And(
            Or(
                And(CanReachRegion(RegionNames.Fly_Fish), get_fishing_skill_rule(20, options)),
                CanReachRegion(RegionNames.Port_Sarim)
            ), 
            Or(
                CanReachRegion(RegionNames.Milk),
                CanReachRegion(RegionNames.Egg),
                CanReachRegion(RegionNames.Shrimp),
                And(CanReachRegion(RegionNames.Wheat), CanReachRegion(RegionNames.Windmill))
            )
        )


def get_runecraft_skill_rule(level, options) -> Rule:
    if options.max_runecraft_level < level:
        return False_()
    if not options.brutal_grinds:
        # Ensure access to the relevant altars
        if level >= 5:
            return And(Has(ItemNames.QP_Rune_Mysteries), CanReachRegion(RegionNames.Falador_Farm), CanReachRegion(RegionNames.Lumbridge_Swamp))
        if level >= 9:
            return And(Has(ItemNames.QP_Rune_Mysteries), CanReachRegion(RegionNames.Falador_Farm), CanReachRegion(RegionNames.Lumbridge_Swamp), CanReachRegion(RegionNames.East_Of_Varrock))
        if level >= 14:
            return And(Has(ItemNames.QP_Rune_Mysteries), CanReachRegion(RegionNames.Falador_Farm), CanReachRegion(RegionNames.Lumbridge_Swamp), CanReachRegion(RegionNames.East_Of_Varrock), CanReachRegion(RegionNames.Al_Kharid))

    return And(Has(ItemNames.QP_Rune_Mysteries), CanReachRegion(RegionNames.Falador_Farm))


def get_magic_skill_rule(level, options) -> Rule:
    if options.max_magic_level < level:
        return False_()

    return CanReachRegion(RegionNames.Mind_Runes)


def get_firemaking_skill_rule(level, options) -> Rule:
    if options.max_firemaking_level < level:
        return False_()
    if not options.brutal_grinds:
        if level >= 30:
            can_chop_willows = get_woodcutting_skill_rule(30, options)
            return And(CanReachRegion(RegionNames.Willow_Tree), can_chop_willows)
        if level >= 15:
            can_chop_oaks = get_woodcutting_skill_rule(15, options)
            return And(CanReachRegion(RegionNames.Oak_Tree), can_chop_oaks)
    # If brutal grinds are on, or if the level is less than 15, you can train it.
    return True_()


def get_skill_rule(skill, level, options) -> Rule:
    if level <= 1:
        return True_()
    if skill.lower() == "fishing":
        return get_fishing_skill_rule(level, options)
    if skill.lower() == "mining":
        return get_mining_skill_rule(level, options)
    if skill.lower() == "woodcutting":
        return get_woodcutting_skill_rule(level, options)
    if skill.lower() == "smithing":
        return get_smithing_skill_rule(level, options)
    if skill.lower() == "crafting":
        return get_crafting_skill_rule(level, options)
    if skill.lower() == "cooking":
        return get_cooking_skill_rule(level, options)
    if skill.lower() == "runecraft":
        return get_runecraft_skill_rule(level, options)
    if skill.lower() == "magic":
        return get_magic_skill_rule(level, options)
    if skill.lower() == "firemaking":
        return get_firemaking_skill_rule(level, options)

    return True_()


def generate_special_rules_for(entrance, region_row, outbound_region_name, options, base_rule=None) -> Rule:
    rule_list:list[Rule] = []
    if base_rule is not None:
        rule_list.append(base_rule)
    if outbound_region_name == RegionNames.Cooks_Guild:
        rule_list.append( get_cooking_skill_rule(32, options))
        # Since there's goblins in this chunk, checking for hat access is superfluous, you'd always have it anyway
    elif outbound_region_name == RegionNames.Crafting_Guild:
        rule_list.append( get_crafting_skill_rule(40, options))
        # Literally the only brown apron access in the entirety of f2p is buying it in varrock
        rule_list.append( CanReachRegion(RegionNames.Central_Varrock))
    elif outbound_region_name == RegionNames.Corsair_Cove:
        # Need to be able to start Corsair Curse in addition to having the item
        rule_list.append( CanReachRegion(RegionNames.Falador_Farm))
    elif outbound_region_name == "Camdozaal*":
        rule_list.append( Has(ItemNames.QP_Below_Ice_Mountain))
    elif region_row.name == "Dwarven Mountain Pass" and outbound_region_name == "Anvil*":
        rule_list.append( Has(ItemNames.QP_Dorics_Quest))
    elif outbound_region_name == "Rune Essence":
        rule_list.append( Has(ItemNames.QP_Rune_Mysteries))
    elif outbound_region_name == RegionNames.Crandor:
        rule_list.append( And(
                CanReachRegion(RegionNames.South_Of_Varrock),
                CanReachRegion(RegionNames.Edgeville),
                CanReachRegion(RegionNames.Lumbridge),
                CanReachRegion(RegionNames.Rimmington),
                CanReachRegion(RegionNames.Monastery),
                CanReachRegion(RegionNames.Dwarven_Mines),
                CanReachRegion(RegionNames.Port_Sarim),
                CanReachRegion(RegionNames.Draynor_Village),
                Has("Quest Point", 32)
            )
        )


    # Special logic for canoes
    canoe_regions = [RegionNames.Lumbridge, RegionNames.South_Of_Varrock, RegionNames.Barbarian_Village,
                     RegionNames.Edgeville, RegionNames.Wilderness]
    if region_row.name in canoe_regions:
        # Skill rules for greater distances
        woodcutting_rule_d1 = get_woodcutting_skill_rule(12, options)
        woodcutting_rule_d2 = get_woodcutting_skill_rule(27, options)
        woodcutting_rule_d3 = get_woodcutting_skill_rule(42, options)
        woodcutting_rule_all = get_woodcutting_skill_rule(57, options)

        if region_row.name == RegionNames.Lumbridge:
            # Canoe Tree access for the Location
            if outbound_region_name == RegionNames.Canoe_Tree:
                rule_list.append(
                    Or(
                        And(CanReachRegion(RegionNames.South_Of_Varrock), woodcutting_rule_d1),
                        And(CanReachRegion(RegionNames.Barbarian_Village), woodcutting_rule_d2),
                        And(CanReachRegion(RegionNames.Edgeville), woodcutting_rule_d3),
                        And(CanReachRegion(RegionNames.Wilderness), woodcutting_rule_all)
                    )
                )

            # Access to other chunks based on woodcutting settings
            elif outbound_region_name == RegionNames.South_Of_Varrock:
                rule_list.append( woodcutting_rule_d1)
            elif outbound_region_name == RegionNames.Barbarian_Village:
                rule_list.append( woodcutting_rule_d2)
            elif outbound_region_name == RegionNames.Edgeville:
                rule_list.append( woodcutting_rule_d3)
            elif outbound_region_name == RegionNames.Wilderness:
                rule_list.append( woodcutting_rule_all)

        elif region_row.name == RegionNames.South_Of_Varrock:
            if outbound_region_name == RegionNames.Canoe_Tree:
                rule_list.append(
                    Or(
                        And(CanReachRegion(RegionNames.Lumbridge), woodcutting_rule_d1),
                        And(CanReachRegion(RegionNames.Barbarian_Village), woodcutting_rule_d1),
                        And(CanReachRegion(RegionNames.Edgeville), woodcutting_rule_d2),
                        And(CanReachRegion(RegionNames.Wilderness), woodcutting_rule_d3)
                    )
                )

            # Access to other chunks based on woodcutting settings
            elif outbound_region_name == RegionNames.Lumbridge:
                rule_list.append( woodcutting_rule_d1)
            elif outbound_region_name == RegionNames.Barbarian_Village:
                rule_list.append( woodcutting_rule_d1)
            elif outbound_region_name == RegionNames.Edgeville:
                rule_list.append( woodcutting_rule_d3)
            elif outbound_region_name == RegionNames.Wilderness:
                rule_list.append( woodcutting_rule_all)
        elif region_row.name == RegionNames.Barbarian_Village:
            if outbound_region_name == RegionNames.Canoe_Tree:
                rule_list.append(
                    Or(
                        And(CanReachRegion(RegionNames.Lumbridge), woodcutting_rule_d2),
                        And(CanReachRegion(RegionNames.South_Of_Varrock), woodcutting_rule_d1),
                        And(CanReachRegion(RegionNames.Edgeville), woodcutting_rule_d1),
                        And(CanReachRegion(RegionNames.Wilderness), woodcutting_rule_d2)
                    )
                )

            # Access to other chunks based on woodcutting settings
            elif outbound_region_name == RegionNames.Lumbridge:
                rule_list.append( woodcutting_rule_d2)
            elif outbound_region_name == RegionNames.South_Of_Varrock:
                rule_list.append( woodcutting_rule_d1)
            # Edgeville does not need to be checked, because it's already adjacent
            elif outbound_region_name == RegionNames.Wilderness:
                rule_list.append( woodcutting_rule_d3)
        elif region_row.name == RegionNames.Edgeville:
            if outbound_region_name == RegionNames.Canoe_Tree:
                rule_list.append(
                    Or(
                        And(CanReachRegion(RegionNames.Lumbridge), woodcutting_rule_d3),
                        And(CanReachRegion(RegionNames.South_Of_Varrock), woodcutting_rule_d2),
                        And(CanReachRegion(RegionNames.Barbarian_Village), woodcutting_rule_d1),
                        And(CanReachRegion(RegionNames.Wilderness), woodcutting_rule_d1)
                    )
                )

            # Access to other chunks based on woodcutting settings
            elif outbound_region_name == RegionNames.Lumbridge:
                rule_list.append( woodcutting_rule_d3)
            elif outbound_region_name == RegionNames.South_Of_Varrock:
                rule_list.append( woodcutting_rule_d2)
            # Barbarian Village does not need to be checked, because it's already adjacent
            # Wilderness does not need to be checked, because it's already adjacent
        elif region_row.name == RegionNames.Wilderness:
            if outbound_region_name == RegionNames.Canoe_Tree:
                rule_list.append(
                    Or(
                        And(CanReachRegion(RegionNames.Lumbridge), woodcutting_rule_all),
                        And(CanReachRegion(RegionNames.South_Of_Varrock), woodcutting_rule_d3),
                        And(CanReachRegion(RegionNames.Barbarian_Village), woodcutting_rule_d2),
                        And(CanReachRegion(RegionNames.Edgeville), woodcutting_rule_d1)
                    )
                )

            # Access to other chunks based on woodcutting settings
            elif outbound_region_name == RegionNames.Lumbridge:
                rule_list.append( woodcutting_rule_all)
            elif outbound_region_name == RegionNames.South_Of_Varrock:
                rule_list.append( woodcutting_rule_d3)
            elif outbound_region_name == RegionNames.Barbarian_Village:
                rule_list.append( woodcutting_rule_d2)
            # Edgeville does not need to be checked, because it's already adjacent
    if len(rule_list)>0:
        return And(*rule_list)
    else:
        return True_()
