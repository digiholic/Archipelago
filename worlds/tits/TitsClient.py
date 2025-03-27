from __future__ import annotations

import asyncio
import logging
import typing
import json

import websockets

from CommonClient import CommonContext, gui_enabled, get_base_parser, server_loop, ClientCommandProcessor


# webserver imports
import urllib.parse

from Utils import async_start

logger = logging.getLogger("Client")

DEBUG = False
ITEMS_HANDLING = 0b111


class TitsCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: TitsGameContext):
        super().__init__(ctx)
        self.ctx = ctx

    def _cmd_tits(self):
        logger.info("Checking T.I.T.S. status...")
        async_start(self.ctx.connect_to_api(), name="connecting")


class TitsGameContext(CommonContext):
    from kvui import GameManager
    game = ""
    httpServer_task: typing.Optional["asyncio.Task[None]"] = None
    tags = CommonContext.tags
    command_processor = TitsCommandProcessor
    titSocket = None

    def __init__(self, server_address, password):
        super().__init__(server_address, password)


    async def connect_to_api(self):
        try:
            self.titSocket = await websockets.connect("ws://localhost", port=42069, ping_timeout=None, ping_interval=None,
                                          ssl=None, max_size=self.max_size)
            self.get_trigger_list();

        except Exception:
            logger.info("Unable to connect. Ensure T.I.T.S. is running and API is enabled")

    def get_trigger_list(self):
        if self.titSocket is not None:
            self.titSocket.send(request_trigger_list("0"))
            result = self.titSocket.recv()
            logger.info(result)
            self.titSocket.close()

def request_trigger_list(self, id: str) -> str:
    return json.dumps({"apiName": "TITSPublicApi", "apiVersion": "1.0", "requestID": id,
                       "messageType": "TITSTriggerListRequest"})

async def main(args):
    ctx = TitsGameContext(args.connect, args.password)
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