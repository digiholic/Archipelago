from dataclasses import dataclass

from Options import Choice, Toggle, Range, PerGameCommonOptions


class Goal(Choice):
    """

    """
    display_name = "Goal"
    research_all = 0
    monument = 1
    space = 2
    default = 0


@dataclass
class ONIOptions(PerGameCommonOptions):
    pass
