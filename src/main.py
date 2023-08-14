#!/usr/bin/env python3
"""Plot the live microphone signal(s) with matplotlib.

Matplotlib and NumPy have to be installed.

"""
import queue
import sys
from threading import Thread
import time
from typing import TypedDict
import numpy as np
from config import config
from audio import Audio
from connection import Connection
from plot import Plot


class State(TypedDict):
    should_close: bool


class ReactiveLed:
    def __init__(self) -> None:
        self.state: State = {"should_close": False}
        self.data_queue: queue.Queue = queue.Queue()
        self.plotter_queue: queue.Queue = queue.Queue()
        self.average = 0

        self.audio = Audio(
            config.device,
            channel=config.channel,
            on_update=self.audio_update,
            samplerate=config.samplerate,
        )
        if config.debug:
            print("Running in debug mode")
            self.plot = Plot(
                interval=30,
                window=config.window,
                samplerate=self.audio.samplerate,
                downsample=config.downsample,
                data_queue=self.plotter_queue,
                on_close=self.close,
            )
        self.connection = Connection(config.serial, 60)
        try:
            with self.audio.stream:
                if self.plot:
                    serial_thread = Thread(target=self.serial_update)
                    serial_thread.start()
                    # Show plot in main thread
                    self.plot.show()
                else:
                    self.serial_update()
        except KeyboardInterrupt:
            self.close()
        except Exception as e:
            print(e)
            self.close()

    def close(self, *args):
        self.state["should_close"] = True
        time.sleep(0.4)
        if self.connection.available():
            self.connection.set(0, 60, (0, 0, 0))
        self.connection.__del__()
        self.audio.close()
        if self.plot:
            self.plot.close()
        sys.exit(0)

    def audio_update(self, indata: np.ndarray, frames: int, time):
        data = indata[:: config.downsample, config.channel - 1]

        if self.plot:
            self.plotter_queue.put(data)
            self.data_queue.put(data)

    def serial_update(self):
        """Manual loop"""
        while True:
            if self.state["should_close"]:
                print("Closing serial_update loop")
                break
            try:
                data: np.ndarray = self.data_queue.get_nowait()
            except queue.Empty:
                time.sleep(0.01)
                continue

            average = np.average(data) + abs(data.min()) * 0.5
            intensity = int(average * 255)

            try:
                self.connection.set(0, 60, (intensity, intensity, intensity))
                self.connection.show()
            except Exception as e:
                print(e)
                self.close()


if __name__ == "__main__":
    ReactiveLed()
