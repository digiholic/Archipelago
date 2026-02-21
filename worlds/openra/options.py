from dataclasses import dataclass

from Options import PerGameCommonOptions, OptionList, Choice, DefaultOnToggle, Toggle, Range, OptionGroup


class IncludedCampaigns(OptionList):
    """
    Which Campaigns to include in the run.

    Available options are:
    - Allied Campaign
    - Soviet Campaign
    - Counterstrike Allied Missions
    - Counterstrike Soviet Missions
    - Aftermath Allied Missions
    - Aftermath Soviet Missions
    - Ant Missions
    """
    display_name = "Included Campaigns"
    valid_keys = {"Allied Campaign", "Soviet Campaign", "Counterstrike Allied Missions",
                  "Counterstrike Soviet Missions", "Aftermath Allied Missions", "Aftermath Soviet Missions",
                  "Ant Missions"}
    default = ["Allied Campaign", "Soviet Campaign"]

class SplitMissionType(Choice):
    """
    How to handle the "Variant" missions, where multiple maps are available for the same or similar mission objectives.

    - Any: Split missions are treated as the same, and clearing any one of them counts for all of them.
    - All: Each variant of a split mission is treated as a separate mission with their own unlocks and checks
    """
    display_name = "Split Mission Type"
    option_any = 0
    option_all = 1

    default = option_any

class EnableCrossFactionTech(DefaultOnToggle):
    """
    If enabled, unlocked Ally tech will be available in Soviet missions and vice-versa.
    """
    display_name = "Enable Cross Faction Tech"

class EnableAntTech(Toggle):
    """
    If enabled, the "Ant" army sub-faction from the bonus missions will be available for the player to unlock
    """
    display_name = "Enable Ant Tech"

class NumberOfCampaigns(Range):
    """
    How many Campaigns need to be beaten to goal the run.
    If the value is 0, this will be treated as "All included campaigns".
    If the value is greater than the number of included campaigns, it will also be treated as "All included campaigns".
    """
    display_name = "Number of Campaigns"
    range_start = 0
    range_end = 7

class CampaignClearCondition(Choice):
    """
    What counts as "Clearing" a Campaign?

    - All Missions - Beat every mission in the campaign
    - Final Mission - Beat the final mission of the campaign
    """
    display_name = "Campaign Clear Condition"
    option_all = 0
    option_final = 1

    default = option_all

@dataclass
class OpenRAOptions(PerGameCommonOptions):
    included_campaigns: IncludedCampaigns
    split_mission_type: SplitMissionType
    enable_cross_faction_tech: EnableCrossFactionTech
    enable_ant_tech: EnableAntTech
    number_of_campaigns: NumberOfCampaigns
    campaign_clear_condition: CampaignClearCondition

option_groups = [
    OptionGroup("Mission Settings",
                [IncludedCampaigns, SplitMissionType]),
    OptionGroup("Technology Settings",
                [EnableCrossFactionTech, EnableAntTech]),
    OptionGroup("Goal Settings",
                [NumberOfCampaigns, CampaignClearCondition]),
]

option_presets = {
    "Quick": {
        "included_campaigns": ["Allied Campaign", "Soviet Campaign"],
        "number_of_campaigns": 1,
        "campaign_clear_condition": 0
    },
    "Full": {
        "included_campaigns": ["Allied Campaign", "Soviet Campaign", "Counterstrike Allied Missions",
                  "Counterstrike Soviet Missions", "Aftermath Allied Missions", "Aftermath Soviet Missions",
                  "Ant Missions"],
        "number_of_campaigns": 0,
        "campaign_clear_condition": 0
    },
}