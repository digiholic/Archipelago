from dataclasses import dataclass
from typing import Any, Dict

from Options import Choice, Toggle, DefaultOnToggle, Range, NamedRange, PerGameCommonOptions,FreeText,Visibility,OptionDict
from .LogicCSV.regions_generated2 import skill_names
from schema import Schema,Optional,And

MAX_COMBAT_TASKS = 16

MAX_PRAYER_TASKS = 5
MAX_MAGIC_TASKS = 7
MAX_RUNECRAFT_TASKS = 8
MAX_CRAFTING_TASKS = 11
MAX_MINING_TASKS = 6
MAX_SMITHING_TASKS = 5
MAX_FISHING_TASKS = 6
MAX_COOKING_TASKS = 6
MAX_FIREMAKING_TASKS = 3
MAX_WOODCUTTING_TASKS = 3

NON_QUEST_LOCATION_COUNT = 49


class StartingArea(FreeText):
    """
    Which chunks are available at the start. The player may need to move through locked chunks to reach the starting
    area, but any areas that require quests, skills, or coins are not available as a starting location.

    NOTE: MEMBERS LOGIC ISSUE: WE DON'T ACTUALLY CARE ABOUT WHAT YOUR START COULD BE HAVE FUN!
    """
    display_name = "Starting Region"
    default = "Lumbridge Castle"
class GoalLocation(FreeText):
    """
    Which location name to consider to be the goal.
    """
    display_name = "Goal Location"
    default = "~|Dragon Slayer I|~ Complete the quest"

class DisableCulling(Toggle):
    """
    Disable the culling that reduces the size of the game
    DO NOT DO THIS UNLESS YOU HATE YOURSELF MORE THEN A NORMAL OSRS PLAYER
    """
    display_name = "Disable Culling"
    default = False

class MaxDropRate(Range):
    """
    The Maximum drop rate that will be considered logical access
    Be careful as to low a value might make your game unbeatable or at least VERY convoluted
    """
    display_name = "Maximum Drop Rate"
    default = 1024
    range_start = 1
    range_end = 10_000 #uncut onyx from the elven crystal chest

class FullMaxDropRate(Range):
    """
    Override for Maximum Drop Rate that allows for choosing values that are VERY ill advised
    Leave at 0 if you don't know what you're doing
    Use with extreme caution
    """
    dispaly_name = "Full Maximum Drop Rate"
    default = 0
    range_start = 0
    range_end = 100_000_000 #uncut onyx from a gem back
    visibility = Visibility(Visibility.all - Visibility.simple_ui)


class MaxTrainingLevels(OptionDict):
    """
    The maximum levels that you will be expected to train each skill
    """
    display_name = "Maximum Required Skill Levels"
    valid_keys = frozenset(skill_names)
    default = {skill_name:(99 if skill_name != "Combat" else 100) for skill_name in skill_names}
    schema = Schema({
        Optional(skill_name):And(int,lambda n: 100>= n >= 0,error="Skill Level must be integers in the range of 0-99.")
        for skill_name in skill_names
    })

    def __init__(self, value: Dict[str, Any]):
        self.value = {}
        for key,data in value.items():
            try:
                self.value[key] = MaxTrainingLevel.from_any(data).value
            except ValueError:
                self.value[key] = data

class MaxTrainingLevel(Range):
    default = 99
    range_start = 0
    range_end = 100
    visibility = Visibility.none

class QuestPointsPerLevel(NamedRange):
    """
    The Number of quest points to increase the training range
    """
    display_name = "Quest Points per Training Level"
    default = 10
    range_start = 1
    range_end = 327
    special_range_names = {
        "disable" :327
    }

class LevelsPerQuestPoint(Range):
    """
    The number of levels to be expected to be over trained for each set of quest points
    """
    display_name = "Levels per Training Set"
    default = 1
    range_start = 0
    range_end = 10

class BaseTrainingLevels(NamedRange):
    """
    The Number of levels over a given training method you would be expected to train over by default
    """
    display_name = "Base Training Levels"
    default = 9
    range_start = 0
    range_end = 99
    special_range_names = {
        "disable":99
    }

class StartWithTutorialIsland(DefaultOnToggle):
    """
    Whether to keep or discard the starting inventory from tutorial island
    """
    display_name = "Start with Tutorial Island Items"

class BrutalGrinds(Toggle):
    """
    Whether to allow skill tasks without having reasonable access to the usual skill training path.
    For example, if enabled, you could be forced to train smithing without an anvil purely by smelting bars,
    or training fishing to high levels entirely on shrimp.
    """
    display_name = "Allow Brutal Grinds"
    visibility = Visibility.none


class ProgressiveTasks(Toggle):
    """
    Whether skill tasks should always be generated in order of easiest to hardest.
    If enabled, you would not be assigned "Mine Gold" without also being assigned
    "Mine Silver", "Mine Coal", and "Mine Iron". Enabling this will result in a generally shorter seed, but with
    a lower variety of tasks.
    """
    display_name = "Progressive Tasks"
    visibility = Visibility.none


class EnableDuds(Toggle):
    """
    Whether to include filler "Dud" items that serve no purpose but allow for more tasks in the pool.
    """
    display_name = "Enable Duds"
    visibility = Visibility.none


class DudCount(Range):
    """
    How many "Dud" items to include in the pool. This setting is ignored if "Enable Duds" is not included
    """
    display_name = "Dud Item Count"
    visibility = Visibility.none
    range_start = 0
    range_end = 30
    default = 10


class EnableCarePacks(Toggle):
    """
    Whether or not to include useful "Care Pack" items that allow you to trade over specific items.
    Note: Requires your account NOT to be an Ironman. Also, requires access to another account to trade over the items,
    or gold to purchase off of the grand exchange.
    """
    display_name = "Enable Care Packs"
    visibility = Visibility.none

class MaxCombatLevel(Range):
    """
    The highest combat level of monster to possibly be assigned as a task.
    If set to 0, no combat tasks will be generated.
    """
    display_name = "Max Required Enemy Combat Level"
    visibility = Visibility.none
    range_start = 0
    range_end = 1520
    default = 50


class MaxCombatTasks(Range):
    """
    The maximum number of Combat Tasks to possibly be assigned.
    If set to 0, no combat tasks will be generated.
    This only determines the maximum possible, fewer than the maximum could be assigned.
    """
    display_name = "Max Combat Task Count"
    visibility = Visibility.none
    range_start = 0
    range_end = MAX_COMBAT_TASKS
    default = MAX_COMBAT_TASKS


class CombatTaskWeight(Range):
    """
    How much to favor generating combat tasks over other types of task.
    Weights of all Task Types will be compared against each other, a task with 50 weight
    is twice as likely to appear as one with 25.
    """
    display_name = "Combat Task Weight"
    visibility = Visibility.none
    range_start = 0
    range_end = 99
    default = 50


class MaxPrayerTasks(Range):
    """
    The maximum number of Prayer Tasks to possibly be assigned.
    If set to 0, no Prayer tasks will be generated.
    This only determines the maximum possible, fewer than the maximum could be assigned.
    """
    display_name = "Max Prayer Task Count"
    visibility = Visibility.none
    range_start = 0
    range_end = MAX_PRAYER_TASKS
    default = MAX_PRAYER_TASKS


class PrayerTaskWeight(Range):
    """
    How much to favor generating Prayer tasks over other types of task.
    Weights of all Task Types will be compared against each other, a task with 50 weight
    is twice as likely to appear as one with 25.
    """
    display_name = "Prayer Task Weight"
    visibility = Visibility.none
    range_start = 0
    range_end = 99
    default = 50


class MaxMagicTasks(Range):
    """
    The maximum number of Magic Tasks to possibly be assigned.
    If set to 0, no Magic tasks will be generated.
    This only determines the maximum possible, fewer than the maximum could be assigned.
    """
    display_name = "Max Magic Task Count"
    visibility = Visibility.none
    range_start = 0
    range_end = MAX_MAGIC_TASKS
    default = MAX_MAGIC_TASKS


class MagicTaskWeight(Range):
    """
    How much to favor generating Magic tasks over other types of task.
    Weights of all Task Types will be compared against each other, a task with 50 weight
    is twice as likely to appear as one with 25.
    """
    display_name = "Magic Task Weight"
    visibility = Visibility.none
    range_start = 0
    range_end = 99
    default = 50


class MaxRunecraftTasks(Range):
    """
    The maximum number of Runecraft Tasks to possibly be assigned.
    If set to 0, no Runecraft tasks will be generated.
    This only determines the maximum possible, fewer than the maximum could be assigned.
    """
    display_name = "Max Runecraft Task Count"
    visibility = Visibility.none
    range_start = 0
    range_end = MAX_RUNECRAFT_TASKS
    default = MAX_RUNECRAFT_TASKS


class RunecraftTaskWeight(Range):
    """
    How much to favor generating Runecraft tasks over other types of task.
    Weights of all Task Types will be compared against each other, a task with 50 weight
    is twice as likely to appear as one with 25.
    """
    display_name = "Runecraft Task Weight"
    visibility = Visibility.none
    range_start = 0
    range_end = 99
    default = 50


class MaxCraftingTasks(Range):
    """
    The maximum number of Crafting Tasks to possibly be assigned.
    If set to 0, no Crafting tasks will be generated.
    This only determines the maximum possible, fewer than the maximum could be assigned.
    """
    display_name = "Max Crafting Task Count"
    visibility = Visibility.none
    range_start = 0
    range_end = MAX_CRAFTING_TASKS
    default = MAX_CRAFTING_TASKS


class CraftingTaskWeight(Range):
    """
    How much to favor generating Crafting tasks over other types of task.
    Weights of all Task Types will be compared against each other, a task with 50 weight
    is twice as likely to appear as one with 25.
    """
    display_name = "Crafting Task Weight"
    visibility = Visibility.none
    range_start = 0
    range_end = 99
    default = 50


class MaxMiningTasks(Range):
    """
    The maximum number of Mining Tasks to possibly be assigned.
    If set to 0, no Mining tasks will be generated.
    This only determines the maximum possible, fewer than the maximum could be assigned.
    """
    display_name = "Max Mining Task Count"
    visibility = Visibility.none
    range_start = 0
    range_end = MAX_MINING_TASKS
    default = MAX_MINING_TASKS


class MiningTaskWeight(Range):
    """
    How much to favor generating Mining tasks over other types of task.
    Weights of all Task Types will be compared against each other, a task with 50 weight
    is twice as likely to appear as one with 25.
    """
    display_name = "Mining Task Weight"
    visibility = Visibility.none
    range_start = 0
    range_end = 99
    default = 50


class MaxSmithingTasks(Range):
    """
    The maximum number of Smithing Tasks to possibly be assigned.
    If set to 0, no Smithing tasks will be generated.
    This only determines the maximum possible, fewer than the maximum could be assigned.
    """
    display_name = "Max Smithing Task Count"
    visibility = Visibility.none
    range_start = 0
    range_end = MAX_SMITHING_TASKS
    default = MAX_SMITHING_TASKS


class SmithingTaskWeight(Range):
    """
    How much to favor generating Smithing tasks over other types of task.
    Weights of all Task Types will be compared against each other, a task with 50 weight
    is twice as likely to appear as one with 25.
    """
    display_name = "Smithing Task Weight"
    visibility = Visibility.none
    range_start = 0
    range_end = 99
    default = 50


class MaxFishingTasks(Range):
    """
    The maximum number of Fishing Tasks to possibly be assigned.
    If set to 0, no Fishing tasks will be generated.
    This only determines the maximum possible, fewer than the maximum could be assigned.
    """
    display_name = "Max Fishing Task Count"
    visibility = Visibility.none
    range_start = 0
    range_end = MAX_FISHING_TASKS
    default = MAX_FISHING_TASKS


class FishingTaskWeight(Range):
    """
    How much to favor generating Fishing tasks over other types of task.
    Weights of all Task Types will be compared against each other, a task with 50 weight
    is twice as likely to appear as one with 25.
    """
    display_name = "Fishing Task Weight"
    visibility = Visibility.none
    range_start = 0
    range_end = 99
    default = 50


class MaxCookingTasks(Range):
    """
    The maximum number of Cooking Tasks to possibly be assigned.
    If set to 0, no Cooking tasks will be generated.
    This only determines the maximum possible, fewer than the maximum could be assigned.
    """
    display_name = "Max Cooking Task Count"
    visibility = Visibility.none
    range_start = 0
    range_end = MAX_COOKING_TASKS
    default = MAX_COOKING_TASKS


class CookingTaskWeight(Range):
    """
    How much to favor generating Cooking tasks over other types of task.
    Weights of all Task Types will be compared against each other, a task with 50 weight
    is twice as likely to appear as one with 25.
    """
    display_name = "Cooking Task Weight"
    visibility = Visibility.none
    range_start = 0
    range_end = 99
    default = 50


class MaxFiremakingTasks(Range):
    """
    The maximum number of Firemaking Tasks to possibly be assigned.
    If set to 0, no Firemaking tasks will be generated.
    This only determines the maximum possible, fewer than the maximum could be assigned.
    """
    display_name = "Max Firemaking Task Count"
    visibility = Visibility.none
    range_start = 0
    range_end = MAX_FIREMAKING_TASKS
    default = MAX_FIREMAKING_TASKS


class FiremakingTaskWeight(Range):
    """
    How much to favor generating Firemaking tasks over other types of task.
    Weights of all Task Types will be compared against each other, a task with 50 weight
    is twice as likely to appear as one with 25.
    """
    display_name = "Firemaking Task Weight"
    visibility = Visibility.none
    range_start = 0
    range_end = 99
    default = 50


class MaxWoodcuttingTasks(Range):
    """
    The maximum number of Woodcutting Tasks to possibly be assigned.
    If set to 0, no Woodcutting tasks will be generated.
    This only determines the maximum possible, fewer than the maximum could be assigned.
    """
    display_name = "Max Woodcutting Task Count"
    visibility = Visibility.none
    range_start = 0
    range_end = MAX_WOODCUTTING_TASKS
    default = MAX_WOODCUTTING_TASKS


class WoodcuttingTaskWeight(Range):
    """
    How much to favor generating Woodcutting tasks over other types of task.
    Weights of all Task Types will be compared against each other, a task with 50 weight
    is twice as likely to appear as one with 25.
    """
    display_name = "Woodcutting Task Weight"
    visibility = Visibility.none
    range_start = 0
    range_end = 99
    default = 50


class MinimumGeneralTasks(Range):
    """
    How many guaranteed general progression tasks to be assigned (total level, total XP, etc.).
    General progression tasks will be used to fill out any holes caused by having fewer possible tasks than needed, so
    there is no maximum.
    """
    display_name = "Minimum General Task Count"
    visibility = Visibility.none
    range_start = 0
    range_end = NON_QUEST_LOCATION_COUNT
    default = 10


class GeneralTaskWeight(Range):
    """
    How much to favor generating General tasks over other types of task.
    Weights of all Task Types will be compared against each other, a task with 50 weight
    is twice as likely to appear as one with 25.
    """
    display_name = "General Task Weight"
    visibility = Visibility.none
    range_start = 0
    range_end = 99
    default = 50


@dataclass
class OSRSOptions(PerGameCommonOptions):
    starting_area: StartingArea
    goal_location: GoalLocation
    disable_culling: DisableCulling
    max_drop_rate: MaxDropRate
    full_drop_rate: FullMaxDropRate
    maximum_training_levels: MaxTrainingLevels
    qp_per_level: QuestPointsPerLevel
    levels_per_qp: LevelsPerQuestPoint
    base_training_levels: BaseTrainingLevels
    tutorial_island_items: StartWithTutorialIsland
    brutal_grinds: BrutalGrinds
    progressive_tasks: ProgressiveTasks
    enable_duds: EnableDuds
    dud_count: DudCount
    enable_carepacks: EnableCarePacks
    max_combat_level: MaxCombatLevel
    max_combat_tasks: MaxCombatTasks
    combat_task_weight: CombatTaskWeight
    max_prayer_tasks: MaxPrayerTasks
    prayer_task_weight: PrayerTaskWeight
    max_magic_tasks: MaxMagicTasks
    magic_task_weight: MagicTaskWeight
    max_runecraft_tasks: MaxRunecraftTasks
    runecraft_task_weight: RunecraftTaskWeight
    max_crafting_tasks: MaxCraftingTasks
    crafting_task_weight: CraftingTaskWeight
    max_mining_tasks: MaxMiningTasks
    mining_task_weight: MiningTaskWeight
    max_smithing_tasks: MaxSmithingTasks
    smithing_task_weight: SmithingTaskWeight
    max_fishing_tasks: MaxFishingTasks
    fishing_task_weight: FishingTaskWeight
    max_cooking_tasks: MaxCookingTasks
    cooking_task_weight: CookingTaskWeight
    max_firemaking_tasks: MaxFiremakingTasks
    firemaking_task_weight: FiremakingTaskWeight
    max_woodcutting_tasks: MaxWoodcuttingTasks
    woodcutting_task_weight: WoodcuttingTaskWeight
    minimum_general_tasks: MinimumGeneralTasks
    general_task_weight: GeneralTaskWeight
