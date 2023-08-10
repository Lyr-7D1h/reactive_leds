import sounddevice as sd
import argparse


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "-l",
    "--list-devices",
    action="store_true",
    help="show list of audio devices and exit",
)

config, remaining = parser.parse_known_args()
if config.list_devices:
    print(sd.query_devices())
    parser.exit(0)

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser],
)
parser.add_argument(
    "channel",
    type=int,
    default=1,
    nargs="*",
    metavar="CHANNEL",
    help="input channels to plot (default: the first)",
)
parser.add_argument(
    "-d", "--device", type=int_or_str, help="input device (numeric ID or substring)"
)
parser.add_argument(
    "-s", "--serial", type=str, default="/dev/ttyUSB1", help="path to serial device"
)
parser.add_argument(
    "--debug",
    default=False,
    help="enable debugging messages and plot data",
    action=argparse.BooleanOptionalAction,
)
parser.add_argument(
    "-w",
    "--window",
    type=float,
    default=200,
    metavar="DURATION",
    help="visible time slot (default: %(default)s ms)",
)
parser.add_argument("-b", "--blocksize", type=int, help="block size (in samples)")
parser.add_argument(
    "-r", "--samplerate", type=float, help="sampling rate of audio device"
)
parser.add_argument(
    "-n",
    "--downsample",
    type=int,
    default=10,
    metavar="N",
    help="display every Nth sample (default: %(default)s)",
)
config = parser.parse_args(remaining)
