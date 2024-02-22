import typing

from BaseClasses import Item, ItemClassification
from .Names import ItemNames, RegionNames


class ONIItem(Item):
    game: str = "Oxygen Not Included"


class ItemData(typing.NamedTuple):
    id: int
    itemName: str
    progression: ItemClassification


all_items: typing.List[ItemData] = [

]

item_table: typing.Dict[str, ItemData] = {item.itemName: item for item in all_items}
items_by_id: typing.Dict[int, ItemData] = {item.id: item for item in all_items}
