import json
import typing
from dataclasses import dataclass


class ModJson:
    """
    Class representing the JSON file the Archipelago Not Included Mod expects to use.
    Will be serialized to json and put in output directory
    """
    AP_seed: str
    AP_slotName: str
    technologies: typing.Dict[str, typing.List[str]]

    def __init__(self, seed, slot, tech):
        self.AP_seed = seed
        self.AP_slotName = slot
        self.technologies = tech

    def to_json(self, indent):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=indent)
