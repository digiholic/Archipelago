import typing

class RegionRow(typing.NamedTuple):
    id: str
    name: str

class ResourceRow(typing.NamedTuple):
    name: str

class DropElement(typing.NamedTuple):
    dest: str
    chance: int

class MonsterRow(typing.NamedTuple):
    name: str
    class_name: str
    drops: list[DropElement]

class RewardElement(typing.NamedTuple):
    skill_name: str
    skill_level: int

class QuestRow(typing.NamedTuple):
    name: str
    rewards: list[RewardElement]

class RuleElement(typing.NamedTuple):
    type: str
    value: str

class SubQuestRow(typing.NamedTuple):
    name: str
    parent_quest: str
    rule: list[RuleElement]

class EntranceRow(typing.NamedTuple):
    source: str
    dest: str
    rule: list[RuleElement]

class TrainingRow(typing.NamedTuple):
    product: str
    skill_name: str
    normal_level: int
    brutal_level: int
    meme_level: int

class LocationRow(typing.NamedTuple):
    name: str
    rule: list[RuleElement]