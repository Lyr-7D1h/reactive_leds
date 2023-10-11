import glob
from typing import List, Optional
from pydantic import BaseModel
import sounddevice as sd
import argparse

import toml

from connection import Connection


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


serial_devices = glob.glob("/dev/tty*USB*")
if len(serial_devices) > 0:
    default_serial = serial_devices[0]
else:
    default_serial = "/dev/ttyUSB0"

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[],
)
parser.add_argument("-c", "--config", type=str)
subparsers = parser.add_subparsers(title="Subcommands", dest="subcommand")

list = subparsers.add_parser("list", help="List")
list.add_argument("listings", choices=["serial", "output"])

subparsers.add_parser("eval", help="Set specific leds")

run = subparsers.add_parser("run", help="Run the program")


class Config(BaseModel):
    # input device (numeric ID or substring)
    device: str | int
    # path to serial device
    serial: str = default_serial
    # input channels to plot (default: the first)
    channel: int = 1
    # enable debugging messages and plot data
    debug: bool = False
    # visible time slot (default: %(default)s ms)
    window: float = 200
    # sampling rate of audio device
    samplerate: Optional[int] = None
    # display every Nth sample (default: %(default)s)
    downsample: int = 10
    amount_leds: int = 60
    disabled_leds: List[int]  = []


def get_config():
    with open("config.toml", "r") as f:
        toml_data = f.read()
        return Config(**toml.loads(toml_data))
