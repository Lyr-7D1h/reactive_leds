import glob
import sounddevice as sd
import argparse

from connection import Connection


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


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

subparsers = parser.add_subparsers(title="Subcommands", dest="subcommand")

list = subparsers.add_parser("list", help="List")
list.add_argument("listings", choices=["serial", "output"])

eval = subparsers.add_parser("eval", help="Set specific leds")
eval.add_argument(
    "-s", "--serial", type=str, default=default_serial, help="path to serial device"
)

run = subparsers.add_parser("run", help="Run the program")
run.add_argument(
    "-d", "--device", type=int_or_str, help="input device (numeric ID or substring)"
)
run.add_argument(
    "-s", "--serial", type=str, default=default_serial, help="path to serial device"
)
run.add_argument(
    "-c",
    "--channel",
    type=int,
    # nargs="*",
    default=1,
    metavar="CHANNEL",
    help="input channels to plot (default: the first)",
)
run.add_argument(
    "--debug",
    default=False,
    help="enable debugging messages and plot data",
    action=argparse.BooleanOptionalAction,
)
run.add_argument(
    "-w",
    "--window",
    type=float,
    default=200,
    metavar="DURATION",
    help="visible time slot (default: %(default)s ms)",
)
run.add_argument("-b", "--blocksize", type=int, help="block size (in samples)")
run.add_argument("-r", "--samplerate", type=float, help="sampling rate of audio device")
run.add_argument(
    "-n",
    "--downsample",
    type=int,
    default=10,
    metavar="N",
    help="display every Nth sample (default: %(default)s)",
)
config = parser.parse_args()

if config.subcommand == "list":
    if config.listings == "output":
        print(sd.query_devices())
        parser.exit(0)
    elif config.listings == "serial":
        # FIXME: add me
        for d in glob.glob("/dev/ttyUSB*"):
            print(d)
        parser.exit(0)
elif config.subcommand == "eval":
    connection = Connection(config.serial, 60)
    while True:
        led_start = int(input("Led Start: "))
        led_end = int(input("Led End: "))
        r = int(input("R: "))
        g = int(input("G: "))
        b = int(input("B: "))
        connection.set(led_start, led_end, (r, g, b))
        connection.show()
