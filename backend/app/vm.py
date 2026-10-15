import subprocess
from pathlib import Path

from app.qmp import qmp_command, QMPError

RUN_SCRIPT = Path(__file__).resolve().parents[2] / "image" / "run-vm.sh"

process = None


class VMError(Exception):
    pass


async def is_running():
    try:
        await qmp_command("query-status")
        return True
    except QMPError:
        return False


async def start():
    global process
    if await is_running():
        raise VMError("VM is already running")
    process = subprocess.Popen(
        [RUN_SCRIPT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )