from worlds.LauncherComponents import Component, components, Type, launch_subprocess


def launch_client():
    from .TitsClient import launch as TCMain
    launch_subprocess(TCMain, name="T.I.T.S. Integrated Text Service")

class TitsWorld:
    pass

components.append(Component("T.I.T.S. Integreted Text Service", None, func=launch_client, component_type=Type.CLIENT))
