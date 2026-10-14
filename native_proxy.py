from __future__ import annotations

import argparse
import asyncio
import json
import sys
from urllib.parse import urlsplit

from demo.config import project_scope

HOST = urlsplit(project_scope()[0]).hostname
AUTHORITY = f"{HOST}:443"


async def socks_connect(port: int):
    reader, writer = await asyncio.open_connection("127.0.0.1", port)
    try:
        writer.write(b"\x05\x01\x00")
        await writer.drain()
        if await reader.readexactly(2) != b"\x05\x00":
            raise ConnectionError("SOCKS authentication negotiation failed")
        name = HOST.encode("ascii")
        writer.write(b"\x05\x01\x00\x03" + bytes([len(name)]) + name + b"\x01\xbb")
        await writer.drain()
        version, result, reserved, kind = await reader.readexactly(4)
        if (version, result, reserved) != (5, 0, 0):
            raise ConnectionError(f"SOCKS target connection failed: {result}")
        if kind == 1:
            length = 4
        elif kind == 4:
            length = 16
        elif kind == 3:
            length = (await reader.readexactly(1))[0]
        else:
            raise ConnectionError("Invalid SOCKS address type")
        await reader.readexactly(length + 2)
        return reader, writer
    except BaseException:
        writer.close()
        await writer.wait_closed()
        raise


async def relay(reader, writer):
    while data := await reader.read(65536):
        writer.write(data)
        await writer.drain()
    if writer.can_write_eof():
        writer.write_eof()


async def handle(reader, writer, *, socks_port: int):
    upstream = None
    established = False
    try:
        header = await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), timeout=10)
        parts = header.split(b"\r\n", 1)[0].decode("ascii").split(" ")
        if len(parts) != 3 or parts[0] != "CONNECT" or parts[1].lower() != AUTHORITY:
            writer.write(b"HTTP/1.1 403 Forbidden\r\nContent-Length: 0\r\nConnection: close\r\n\r\n")
            await writer.drain()
            print(json.dumps({"event": "denied_nonapproved_connect"}), flush=True)
            return
        remote, upstream = await asyncio.wait_for(socks_connect(socks_port), timeout=15)
        writer.write(b"HTTP/1.1 200 Connection Established\r\n\r\n")
        await writer.drain()
        established = True
        print(json.dumps({"event": "approved_connect", "origin": AUTHORITY}), flush=True)
        await asyncio.wait_for(
            asyncio.gather(relay(reader, upstream), relay(remote, writer)), timeout=1260
        )
    except (OSError, UnicodeError, asyncio.TimeoutError, asyncio.IncompleteReadError,
            asyncio.LimitOverrunError) as error:
        print(json.dumps({"event": "proxy_error", "type": type(error).__name__}), file=sys.stderr, flush=True)
        if not established:
            writer.write(b"HTTP/1.1 502 Bad Gateway\r\nContent-Length: 0\r\nConnection: close\r\n\r\n")
            await writer.drain()
    finally:
        if upstream is not None:
            upstream.close()
            await upstream.wait_closed()
        writer.close()
        await writer.wait_closed()


async def main(args):
    server = await asyncio.start_server(
        lambda reader, writer: handle(reader, writer, socks_port=args.socks_port),
        "127.0.0.1", args.port, limit=8192,
    )
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exact-origin CONNECT bridge; TLS is never terminated.")
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--socks-port", type=int, required=True)
    arguments = parser.parse_args()
    if any(not 1024 <= port <= 65535 for port in (arguments.port, arguments.socks_port)):
        parser.error("Require unused high loopback ports.")
    asyncio.run(main(arguments))
