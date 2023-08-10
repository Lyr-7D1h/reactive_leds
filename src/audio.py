import queue
import sys

import sounddevice as sd
import numpy as np
from config import config


class Audio:
    def __init__(self, device: str, on_update) -> None:
        self.on_update = on_update
        sd.default.device = device
        self.device = sd.query_devices(sd.default.device, "output")
        self.samplerate: float = self.device["default_samplerate"]
        # https://python-sounddevice.readthedocs.io/en/0.3.15/api/streams.html
        self.stream = sd.InputStream(
            channels=config.channel,
            device=self.device["index"],
            samplerate=self.samplerate,
            callback=self.update,
        )
        print("Listening on '", device, "' with sample rate", int(self.samplerate))

    def __enter__(self):
        print("Starting audio stream")
        self.stream.start()

    def __exit__(self, type, value, traceback):
        print("Stopping audio stream")
        self.stream.close()

    def update(self, indata: np.ndarray, frames: int, time, status: sd.CallbackFlags):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        # print(indata)
        self.on_update(indata, frames, time)


# try:
#     stream = sd.InputStream(
#         channels=args.channel,
#         samplerate=samplerate,
#         callback=audio_update,
#     )
#     ani = FuncAnimation(
#         fig, update_plot, interval=args.interval, blit=True, save_count=length
#     )
#     with stream:
#         plt.show()

# except Exception as e:
#     a.parser.exit(type(e).__name__ + ": " + str(e))
