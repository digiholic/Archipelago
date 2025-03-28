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


class TitsCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: TitsGameContext):
        super().__init__(ctx)
        self.ctx = ctx

    def _cmd_tits_connect(self):
        async_start(self.ctx.connect_to_api(), name="connecting to tits")

    def _cmd_tits_status(self):
        self.ctx.tits_status()


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
    from kvui import GameManager
    game = ""
    httpServer_task: typing.Optional["asyncio.Task[None]"] = None
    tags = CommonContext.tags | {"TextOnly"}
    items_handling = 0b111  # receive all items for /received
    want_slot_data = False  # Can't use game specific slot_data
    command_processor = TitsCommandProcessor
    titsPort = 42069
    titsSocket = None
    titsTriggers: typing.Dict[str, str]

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.titsTriggers = dict()

    def on_print_json(self, args: dict):
        super(TitsGameContext, self).on_print_json(args)

        """
        if args.get("type", "") == "ItemSend" and self.slot_concerns_self(args["receiving"]) \
            and self.slot_concerns_self(args["item"].player):
            logger.info("Receiving item!")
            flags = [part["flags"] for part in args if "flags" in part]
            if flags and not all(flag & 0b001 for flag in flags):
                logger.info("Is Progressive")
            if flags and not all(flag & 0b010 for flag in flags):
                logger.info("Is Useful")
            if flags and not all(flag & 0b100 for flag in flags):
                logger.info("Is Filler")
        # Peel apart the args and find out the item. Check its classification and send corresponding events
        """
        if args.get("type", "") == "ItemSend":
            async_start(self.send_trigger(), name="Sending Throws")

    def tits_status(self):
        if self.titsSocket is not None:
            logger.info(f"T.I.T.S. is connected and listening on port {self.titsSocket.port}")
            for name, trigger_id in self.titsTriggers.items():
                logger.info(f"Found Trigger {name}: {trigger_id}")

    async def connect_to_api(self):
        try:
            logger.info(f"Connecting to TITS on port{self.titsPort} ")
            self.titsSocket = await websockets.connect(f"ws://localhost:{self.titsPort}/websocket", max_size=self.max_size)
            await self.get_trigger_list()

        except Exception as e:
            print(e)
            logger.info(f"Unable to connect. Ensure T.I.T.S. is running and API is enabled and on port {self.titsPort}")
            self.titsSocket = None

    async def get_trigger_list(self):
        if self.titsSocket is not None:
            await self.titsSocket.send(request_trigger_list("0"))
            result = await self.titsSocket.recv()
            data = json.loads(result)
            # logger.info(result)
            for trigger in data["data"]["triggers"]:
                logger.info("Found Trigger: "+trigger["name"])
                self.titsTriggers[trigger["name"]] = trigger["ID"]

    async def send_trigger(self):
        if self.titsSocket is not None:
            await self.titsSocket.send(activate_trigger("0", self.titsTriggers["Throw a lot of things!"]))

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

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.game = ""
        await super().disconnect(allow_autoreconnect)

def request_trigger_list(id: str) -> str:
    return json.dumps({"apiName": "TITSPublicApi", "apiVersion": "1.0", "requestID": id,
                       "messageType": "TITSTriggerListRequest"})

def activate_trigger(id: str, trigger_id: str) -> str:
    return json.dumps({"apiName": "TITSPublicApi", "apiVersion": "1.0",
                       "requestID": id, "messageType": "TITSTriggerActivateRequest",
                       "data": {
                           "triggerID": trigger_id
                       }})