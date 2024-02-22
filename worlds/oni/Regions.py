import typing

from BaseClasses import CollectionState
from .Locations import LocationNames
from .Items import ItemNames
from .Names import RegionNames


class RegionInfo(typing.NamedTuple):
    name: str


all_regions = [

]

regions_by_name: typing.Dict[str, RegionInfo] = {region.name: region for region in all_regions}
