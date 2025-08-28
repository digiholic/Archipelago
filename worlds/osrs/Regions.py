from typing import NamedTuple


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