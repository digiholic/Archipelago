from __future__ import annotations

import asyncio
import logging
import typing
import json

import websockets

from CommonClient import CommonContext, gui_enabled, get_base_parser, server_loop, ClientCommandProcessor

from Utils import async_start

logger = logging.getLogger("Client")

DEBUG = False
ITEMS_HANDLING = 0b111

trigger_ap_receive = "AP-Receive"
trigger_ap_receive_progression = "AP-Receive-Progression"
trigger_ap_receive_useful = "AP-Receive-Useful"
trigger_ap_receive_filler = "AP-Receive-Filler"
trigger_ap_receive_trap = "AP-Receive-Trap"
trigger_ap_goal = "AP-Goal"
trigger_ap_deathlink = "AP-Deathlink"


class TitsCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: TitsGameContext):
        super().__init__(ctx)
        self.ctx = ctx

    def _cmd_tits_connect(self, optional_port=42069):
        """Connect to the T.I.T.S. API on a given port. If no port is provided, it will use the default port."""
        async_start(self.ctx.connect_to_api(optional_port), name="connecting to tits")

    def _cmd_tits_status(self):
        """Displays the currenct connection status and lists all found endpoint triggers"""
        self.ctx.tits_status()

    def _cmd_tits_alias(self, alias=""):
        """Specifies a name for the API call.
        This only matters if you intend to be running multiple T.I.T.S. applications
        and multiple T.I.T.S. Clients on the same device, and need to differentiate which ones are which."""
        self.ctx.titsAlias = alias

    def _cmd_tits_help(self):
        """Provides information about active endpoints and how to connect."""
        logger.info(f"This client will send the following T.I.T.S. Triggers when connected to a multiworld:")
        logger.info(f"    - {trigger_ap_receive}:             When receiving any item")
        logger.info(f"    - {trigger_ap_receive_progression}: When receiving a Progression item")
        logger.info(f"    - {trigger_ap_receive_useful}:      When receiving a useful item")
        logger.info(f"    - {trigger_ap_receive_filler}:      When receiving a filler item")
        logger.info(f"    - {trigger_ap_receive_trap}:        When receiving a Trap")
        logger.info(f"    - {trigger_ap_goal}:                When completing your goal")
        logger.info(f"    - {trigger_ap_deathlink}:           When receiving a Death")
        logger.info("")
        logger.info(
            "Any triggers that are not set in T.I.T.S. will be skipped. You need only implement the ones you intend to use")


async def main(args):
    ctx = TitsGameContext(args.connect, args.password)
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    await ctx.exit_event.wait()
    await ctx.shutdown()


def launch():
    import colorama

    parser = get_base_parser(description="Gameless Archipelago Client, for throwing things at VTubers.")
    args = parser.parse_args()
    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()


class TitsGameContext(CommonContext):
    game = ""
    httpServer_task: typing.Optional["asyncio.Task[None]"] = None
    tags = CommonContext.tags | {"TextOnly", "DeathLink"}
    items_handling = 0b111  # receive all items for /received
    want_slot_data = False  # Can't use game specific slot_data
    command_processor = TitsCommandProcessor
    titsPort = 42069
    titsSocket = None
    titsTriggers: typing.Dict[str, str]
    # The ID passed to the API. Only needs to change if you're controlling multiple TITS clients from the same window
    titsAlias = "AP Tits Client"

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.titsTriggers = dict()

    def on_print_json(self, args: dict):
        super(TitsGameContext, self).on_print_json(args)

        # If it's an Item and we're receiving it
        if args.get("type", "") == "ItemSend" and self.slot_concerns_self(args["receiving"]) \
                and self.slot_concerns_self(args["item"].player):
            async_start(self.send_trigger(trigger_ap_receive), name="Sending AP-Receive")

            flags = [part["flags"] for part in args["data"] if "flags" in part]
            if flags and all(flag == 0b001 for flag in flags):
                async_start(self.send_trigger(trigger_ap_receive_progression), name="Sending AP-Receive-Progression")
            if flags and all(flag == 0b010 for flag in flags):
                async_start(self.send_trigger(trigger_ap_receive_useful), name="Sending AP-Receive-Useful")
            if flags and all(flag == 0b100 for flag in flags):
                async_start(self.send_trigger(trigger_ap_receive_trap), name="Sending AP-Receive-Trap")
            if flags and all(flag == 0 for flag in flags):
                async_start(self.send_trigger(trigger_ap_receive_filler), name="Sending AP-Receive-Filler")

        # If we just goaled
        if args.get("type", "") == "Goal" and (
                self.slot_concerns_self(args["team"]) or self.slot_concerns_self(args["slot"])):
            async_start(self.send_trigger(trigger_ap_goal), name="Sending AP-Goal")

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        super().on_deathlink(data)
        # We want to send a deathlink trigger regardless of who died
        async_start(self.send_trigger(trigger_ap_deathlink), name="Sending AP-Deathlink")

    def tits_status(self):
        if self.titsSocket is not None:
            logger.info(f"T.I.T.S. is connected and listening on port {self.titsSocket.port}")
            for name, trigger_id in self.titsTriggers.items():
                logger.info(f"Found Trigger {name}: {trigger_id}")

    async def connect_to_api(self, port):
        try:
            self.titsPort = port
            logger.info(f"Connecting to TITS on port {self.titsPort} ")
            self.titsSocket = await websockets.connect(f"ws://localhost:{self.titsPort}/websocket",
                                                       max_size=self.max_size)
            await self.get_trigger_list()

        except Exception as e:
            print(e)
            logger.info(f"Unable to connect. Ensure T.I.T.S. is running and API is enabled and on port {self.titsPort}")
            self.titsSocket = None

    async def get_trigger_list(self):
        if self.titsSocket is not None:
            await self.titsSocket.send(request_trigger_list(self.titsAlias))
            result = await self.titsSocket.recv()
            data = json.loads(result)
            # logger.info(result)
            for trigger in data["data"]["triggers"]:
                logger.info("Found Trigger: " + trigger["name"])
                self.titsTriggers[trigger["name"]] = trigger["ID"]

    async def send_trigger(self, trigger_name):
        logger.debug(f"Sending T.I.T.S. Trigger {trigger_name}")
        if self.titsSocket is not None:
            if trigger_name in self.titsTriggers:
                await self.titsSocket.send(activate_trigger(self.titsAlias, self.titsTriggers[trigger_name]))
            else:
                logger.debug(f"Skipping sending T.I.T.S. Trigger {trigger_name} since no endpoint was found")

    def make_gui(self):
        ui = super().make_gui()

        class CCApp(ui):
            def print_json(self, data):
                text = self.json_to_kivy_parser(data)

                self.log_panels["Archipelago"].on_message_markup(text)
                self.log_panels["All"].on_message_markup(text)

        return CCApp

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(TitsGameContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)
        if cmd == "Connected":
            self.game = self.slot_info[self.slot].game
            async_start(self.connect_to_api(self.titsPort), name="connecting to tits")

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.game = ""
        await super().disconnect(allow_autoreconnect)

    async def connection_closed(self):
        await super().connection_closed()
        await self.titsSocket.close()


def request_trigger_list(id: str) -> str:
    return json.dumps({"apiName": "TITSPublicApi", "apiVersion": "1.0", "requestID": id,
                       "messageType": "TITSTriggerListRequest"})


def activate_trigger(id: str, trigger_id: str) -> str:
    return json.dumps({"apiName": "TITSPublicApi", "apiVersion": "1.0",
                       "requestID": id, "messageType": "TITSTriggerActivateRequest",
                       "data": {
                           "triggerID": trigger_id
                       }})
