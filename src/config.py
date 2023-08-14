import sounddevice as sd
import argparse


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


# list.
#     "",
#     "--list-devices",
#     action="store_true",
#     help="show list of audio devices and exit",
# )

# config, remaining = parser.parse_known_args()
# if config.list_devices:
#     print(sd.query_devices())
#     parser.exit(0)

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[],
)

subparsers = parser.add_subparsers(title="Subcommands", dest="subcommand")

list = subparsers.add_parser("list", help="List")
list.add_argument("listings", choices=["serial", "output"])

run = subparsers.add_parser("run", help="Run the program")
run.add_argument(
    "-d", "--device", type=int_or_str, help="input device (numeric ID or substring)"
)
run.add_argument(
    "-s", "--serial", type=str, default="/dev/ttyUSB1", help="path to serial device"
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
run.add_argument(
    "-r", "--samplerate", type=float, help="sampling rate of audio device"
)
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
        print("Listing serials")
        parser.exit(0)