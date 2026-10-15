import asyncio
import json

QMP_SOCK = "/tmp/qmp.sock"
QMP_HANDSHAKE = "qmp_capabilities"


class QMPError(Exception):
    pass


async def qmp_command(command, sock_path=QMP_SOCK):
    try:
        reader, writer = await asyncio.open_unix_connection(sock_path)
    except (FileNotFoundError, ConnectionRefusedError):
        raise QMPError("VM is not running")

    try:
        await reader.readline()
        for cmd in (QMP_HANDSHAKE, command):
            writer.write((json.dumps({"execute": cmd}) + "\n").encode())
            await writer.drain()
            while True:
                line = await reader.readline()
                if not line:
                    raise QMPError("connection closed")
                msg = json.loads(line)
                if "event" not in msg:
                    break
            if "error" in msg:
                raise QMPError(msg["error"]["desc"])
        return msg["return"]
    finally:
        writer.close()