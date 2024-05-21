import asyncio
import logging
import traceback
import typing
from collections.abc import Callable

import Utils
from CommonClient import CommonContext, gui_enabled, get_base_parser, server_loop, ClientCommandProcessor
import os
import time
import sys
from typing import Dict, Optional, List
from BaseClasses import Region, Location, ItemClassification

from BaseClasses import CollectionState, MultiWorld, LocationProgressType
from worlds.generic.Rules import exclusion_rules, locality_rules
from Options import StartInventoryPool
from settings import get_settings
from Utils import __version__, output_path
from worlds import AutoWorld
from worlds.bulk_checker import CheckerWorld
from collections import Counter

from Generate import main as GMain, mystery_argparse

# webserver imports
import urllib.parse

logger = logging.getLogger("Client")

DEBUG = False
ITEMS_HANDLING = 0b111


class CheckerCommandProcessor(ClientCommandProcessor):

    def _cmd_inventory(self):
        """Print the list of current items in the inventory"""
        logger.info("Current Inventory:")
        all_items, prog_items, events = updateChecker(self.ctx)
        for item, count in sorted(all_items.items()):
            logger.info(str(count) + "x: " + item)

    def _cmd_prog_inventory(self):
        """Print the list of current items in the inventory"""
        logger.info("Current Inventory:")
        all_items, prog_items, events = updateChecker(self.ctx)
        for item, count in sorted(prog_items.items()):
            logger.info(str(count) + "x: " + item)

    def _cmd_event_inventory(self):
        """Print the list of current items in the inventory"""
        logger.info("Current Inventory:")
        all_items, prog_items, events = updateChecker(self.ctx)
        for event in sorted(events):
            logger.info(event)

    def _cmd_send_checks(self):
        logger.info("Sending Confirmed Checks:")
        for location in self.ctx.checks_to_send:
            logger.info(self.ctx.location_names[location])
        # Actually send it
        Utils.async_start(self.ctx.send_msgs([{
            "cmd": "LocationChecks",
            "locations": self.ctx.checks_to_send
        }]), name="Sending Locations")


class CheckerGameContext(CommonContext):
    from kvui import GameManager
    game = ""
    httpServer_task: typing.Optional["asyncio.Task[None]"] = None
    tags = CommonContext.tags | {"Checker"}
    command_processor = CheckerCommandProcessor
    checker_page = None
    watcher_task = None
    gen_error = None
    output_format = "Both"
    hide_excluded = False
    re_gen_passthrough = None
    checks_to_send: list[int]

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.items_handling = ITEMS_HANDLING
        self.locations_checked = []
        self.locations_available = []
        self.datapackage = []
        self.player_id = None
        self.checks_to_send = []

    def clear_page(self):
        if self.checker_page is not None:
            self.checker_page.resetData()

    def log_to_tab(self, line: str, sort: bool = False):
        if self.checker_page is not None:
            self.checker_page.addLine(line, sort)

    def build_gui(self, manager: GameManager):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.tabbedpanel import TabbedPanelItem
        from kivy.uix.recycleview import RecycleView

        class CheckerLayout(BoxLayout):
            pass

        class CheckerView(RecycleView):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.data = []
                self.data.append({"text": "Checker v0.1.4 Initializing"})

            def resetData(self):
                self.data.clear()

            def addLine(self, line: str, sort: bool = False):
                self.data.append({"text": line})
                if sort:
                    self.data.sort(key=lambda e: e["text"])

        checker_page = TabbedPanelItem(text="Checker Page")

        try:
            checker = CheckerLayout(orientation="horizontal")
            checker_view = CheckerView()
            checker.add_widget(checker_view)
            self.checker_page = checker_view
            checker_page.content = checker
            if self.gen_error is not None:
                for line in self.gen_error.split("\n"):
                    self.log_to_tab(line, False)
        except Exception as e:
            tb = traceback.format_exc()
            print(tb)
        manager.tabs.add_widget(checker_page)

        from kvui import HintLog
        # hook hint tab

        def update_available_hints(log: HintLog, hints: typing.Set[typing.Dict[str, typing.Any]]):
            data = []
            for hint in hints:
                in_logic = int(hint["location"]) in self.locations_available \
                    if int(hint["finding_player"]) == self.player_id else False
                data.append({
                    "receiving": {
                        "text": log.parser.handle_node({"type": "player_id", "text": hint["receiving_player"]})},
                    "item": {"text": log.parser.handle_node(
                        {"type": "item_id", "text": hint["item"], "flags": hint["item_flags"]})},
                    "finding": {"text": log.parser.handle_node({"type": "player_id", "text": hint["finding_player"]})},
                    "location": {"text": log.parser.handle_node({"type": "location_id", "text": hint["location"]})},
                    "entrance": {"text": log.parser.handle_node({"type": "color" if hint["entrance"] else "text",
                                                                 "color": "blue", "text": hint["entrance"]
                        if hint["entrance"] else "Vanilla"})},
                    "found": {
                        "text": log.parser.handle_node({"type": "color", "color": "green" if hint["found"] else
                                                        "yellow" if in_logic else "red",
                                                        "text": "Found" if hint["found"] else "In Logic" if in_logic
                                                        else "Not Found"})},
                })

            data.sort(key=log.hint_sorter, reverse=log.reversed)
            for i in range(0, len(data), 2):
                data[i]["striped"] = True
            data.insert(0, log.header)
            log.data = data

        HintLog.refresh_hints = update_available_hints

    def run_gui(self):
        from kvui import GameManager

        class CheckerManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Bulk Checker Client"

            def build(self):
                container = super().build()
                self.tabs.do_default_tab = True
                self.tabs.current_tab.height = 40
                self.tabs.tab_height = 40
                self.ctx.build_gui(self)

                return container

        self.ui = CheckerManager(self)
        self.load_kv()
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")
        return self

    def load_kv(self):
        from kivy.lang import Builder
        import pkgutil

        data = pkgutil.get_data(CheckerWorld.__module__, "Checker.kv").decode()
        Builder.load_string(data)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(CheckerGameContext, self).server_auth(password_requested)

        await self.get_game()
        await self.get_username()
        await self.send_connect()

    async def get_game(self):
        if not self.auth:
            logger.info('Enter game name:')
            self.game = await self.console_input()

    def on_package(self, cmd: str, args: dict):
        if cmd == 'Connected':
            updateChecker(self)
        elif cmd == 'RoomUpdate':
            updateChecker(self)

    async def disconnect(self, allow_autoreconnect: bool = False):
        if "Checker" in self.tags:
            self.game = ""
            self.re_gen_passthrough = None
        await super().disconnect(allow_autoreconnect)


def updateChecker(ctx: CheckerGameContext):
    ctx.clear_page()
    for location in ctx.checked_locations:
        ctx.log_to_tab("[x] "+ctx.location_names[location])
    for location in ctx.missing_locations:
        ctx.log_to_tab("[ ] "+ctx.location_names[location] + " ("+str(location)+")")


async def main(args):
    ctx = CheckerGameContext(args.connect, args.password)
    ctx.auth = args.name
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    await ctx.exit_event.wait()
    await ctx.shutdown()


def launch():
    parser = get_base_parser(description="Gameless Archipelago Client, for text interfacing.")
    parser.add_argument('--name', default=None, help="Slot Name to connect as.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")
    args = parser.parse_args()

    if args.url:
        url = urllib.parse.urlparse(args.url)
        args.connect = url.netloc
        if url.username:
            args.name = urllib.parse.unquote(url.username)
        if url.password:
            args.password = urllib.parse.unquote(url.password)

    asyncio.run(main(args))
