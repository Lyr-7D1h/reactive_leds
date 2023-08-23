#!/usr/bin/env python
import glob
import sounddevice as sd
import argparse

from config import get_config

from connection import Connection
from reactive_led import ReactiveLed


serial_devices = glob.glob("/dev/ttyUSB*")
if len(serial_devices) > 0:
    default_serial = serial_devices[0]
else:
    default_serial = "/dev/ttyUSB1"

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


args = parser.parse_args()

config = get_config()
if args.subcommand == "list":
    if args.listings == "output":
        print(sd.query_devices())
        parser.exit(0)
    elif args.listings == "serial":
        # FIXME: add me
        for d in glob.glob("/dev/ttyUSB*"):
            print(d)
        parser.exit(0)
elif args.subcommand == "eval":
    connection = Connection(config.serial, 60)
    while True:
        led_start = int(input("Led Start: "))
        led_end = int(input("Led End: "))
        r = int(input("R: "))
        g = int(input("G: "))
        b = int(input("B: "))
        connection.set(led_start, led_end, (r, g, b))
        connection.show()
else:
    ReactiveLed(config)
