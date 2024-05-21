
from worlds.LauncherComponents import Component, components, Type, launch_subprocess


def launch_client():
    from .CheckerClient import launch as TCMain
    launch_subprocess(TCMain, name="Bulk Location Checker client")

class CheckerWorld:
    pass

components.append(Component("Bulk Location Checker", None, func=launch_client, component_type=Type.CLIENT))
