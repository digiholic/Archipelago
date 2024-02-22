import typing

from BaseClasses import Location
from .Names import LocationNames


class ONILocation(Location):
    game: str = "Oxygen Not Included"


class LocationData(typing.NamedTuple):
    id: int
    name: str

