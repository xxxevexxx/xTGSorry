import time
import psutil
import asyncio
import subprocess

from const import Const
from user.filters import commands
from pyrogram.types import Message
from pyrogram import Client, filters
from user.decorators import pyrogram_on_error


async def get_eth_load():
    net_io1 = psutil.net_io_counters()
    await asyncio.sleep(1)
    net_io2 = psutil.net_io_counters()
    kb_recv = "{:.1f}".format((net_io2.bytes_recv - net_io1.bytes_recv) / 1024)
    kb_sent = "{:.1f}".format((net_io2.bytes_sent - net_io1.bytes_sent) / 1024)
    return kb_recv, kb_sent


async def get_cpu_load():
    load = await asyncio.to_thread(psutil.cpu_percent, interval=3, percpu=True)
    return "{:.1f}".format(sum(load) / 4)


def get_disk_usage():
    disk_usage = psutil.disk_usage('/')
    return disk_usage.percent


def get_memory_usage():
    memory = psutil.virtual_memory()
    return "{:.1f}".format(memory.percent)


def get_temp():
    ssd = cpu = None
    sensors_data = subprocess.check_output(['sensors']).decode('utf-8').split("\n")
    for data in sensors_data:
        if "Composite" in data:
            ssd = data.split(" ")[4]
        if "Package id 0:" in data:
            cpu = data.split(" ")[4]
    return ssd.replace("+", ""), cpu.replace("+", "")


@Client.on_message(commands("..", ["server", "сервер"], 5))
@pyrogram_on_error
async def pyrogram_server(client: Client, message: Message):
    """
    :param name: Server
    :param level: 1
    :param command: .. server
    :param description: Отобразит нагрузку сервера
    """
    await client.xxx.method.edit(message, f"`[Server]` {Const.LOADING} Diagnostics started.")
    recv, send = await get_eth_load()
    ssd, cpu = get_temp()
    ssd_used = get_disk_usage()
    memory = get_memory_usage()
    load = await get_cpu_load()
    send_message = (
        f"`[Server]` Information about the server.\n"
        f"\n"
        f"{Const.SS} **ETH Recv**: {recv}kb/s\n"
        f"{Const.SS} **ETH Send**: {send}kb/s\n"
        f"{Const.SS} **SSD Temp**: {ssd}\n"
        f"{Const.SS} **SSD Used**: {ssd_used}%\n"
        f"{Const.SS} **CPU Temp**: {cpu}\n"
        f"{Const.SS} **CPU Load**: {load}%\n"
        f"{Const.SS} **MEM Load**: {memory}%\n"
    )
    return await client.xxx.method.edit(message, send_message)
