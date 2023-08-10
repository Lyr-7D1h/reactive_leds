#!/usr/bin/env python3
"""Plot the live microphone signal(s) with matplotlib.

Matplotlib and NumPy have to be installed.

"""
import queue
from threading import Thread
import time
import numpy as np
from config import config
from audio import Audio
from connection import Connection
from plot import Plot


plotter_queue: queue.Queue = queue.Queue()
average = 0

connection = Connection(config.serial, 60)


def audio_update(indata: np.ndarray, frames: int, time):
    data = indata[:: config.downsample, 0]

    global average
    average = np.average(data) + abs(data.min()) * 0.5
    # intensity = int(average * 255)
    # connection.all((intensity, intensity, intensity))

    if config.debug:
        plotter_queue.put(data)


def serial_update():
    while True:
        intensity = int(average * 255)
        print(intensity)
        connection.set(0, 60, (intensity, intensity, intensity))
        connection.show()


def main():
    audio = Audio(config.device, on_update=audio_update)
    plot = None
    if config.debug:
        print("Running in debug mode")
        print("Adding plot")
        plot = Plot(
            interval=30,
            window=config.window,
            samplerate=audio.samplerate,
            downsample=config.downsample,
            data_queue=plotter_queue,
        )

    try:
        with audio.stream:
            t = Thread(target=serial_update)
            t.start()
            if plot:
                plot.show()

    except Exception as e:
        config.parser.exit(type(e).__name__ + ": " + str(e))


if __name__ == "__main__":
    main()
