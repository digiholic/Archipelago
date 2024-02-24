import typing


class ModJson(typing.NamedTuple):
    """
    Class representing the JSON file the Archipelago Not Included Mod expects to use.
    Will be serialized to json and put in output directory
    """
    AP_seed: str
    AP_slotName: str
    technologies: typing.Dict[str, typing.List[str]]