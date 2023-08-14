#!/usr/bin/env python3
"""Plot the live microphone signal(s) with matplotlib.

Matplotlib and NumPy have to be installed.

"""
import queue
import sys
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
    data = indata[:: config.downsample, config.channel]

    global average
    average = np.average(data) + abs(data.min()) * 0.5

    if config.debug:
        plotter_queue.put(data)
audio = Audio(config.device, channel=config.channel, on_update=audio_update, samplerate=config.samplerate)

def serial_update():
    while True:
        intensity = int(average * 255)
        connection.set(0, 60, (intensity, intensity, intensity))
        connection.show()

serial_thread = Thread(target=serial_update)

def close(_):
    connection.set(0, 60, (0,0,0))
    connection.__del__()
    if plot:
        plot.close()
    sys.exit(0)

plot = None
if config.debug:
    print("Running in debug mode")
    plot = Plot(
        interval=30,
        window=config.window,
        samplerate=audio.samplerate,
        downsample=config.downsample,
        data_queue=plotter_queue,
        on_close=close
    )


def main():
    try:
        with audio.stream:
            serial_thread.start()
            if plot:
                # Show plot in main thread
                plot.show()
            else:
                # Do nothing in main thread
                while True:
                    time.sleep(200)

    except Exception as e:
        config.parser.exit(type(e).__name__ + ": " + str(e))


if __name__ == "__main__":
    main()
