import queue
import sys
from threading import Thread
import time
from typing import TypedDict
import numpy as np
from config import Config
from audio import Audio
from connection import Connection
from effects.fire import Fire
from plot import Plot


class State(TypedDict):
    should_close: bool


class ReactiveLed:
    def __init__(self, config: Config) -> None:
        self.config = config
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
        self.connection = Connection(config.serial, 60, self.config.disabled_leds)
        # self.effect = Fire(self.config, self.connection)
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
            print("Keyboard interrupt")
            self.close()
        except Exception as e:
            print(e)
            self.close()

    def close(self, *args):
        print("Quiting gracefully")
        self.state["should_close"] = True
        time.sleep(0.4)
        if self.connection.available():
            self.connection.clear()
        self.audio.close()
        if self.plot:
            self.plot.close()
        sys.exit(0)

    def audio_update(self, indata: np.ndarray, frames: int, time):
        data = indata[:: self.config.downsample, self.config.channel - 1]

        if self.plot:
            self.plotter_queue.put(data)
            self.data_queue.put(data)

    def serial_update(self):
        self.connection.clear()
        print("Starting serial update loop")
        """Manual loop"""
        while True:
            if self.state["should_close"]:
                print("Closing serial_update loop")
                break
            try:
                data: np.ndarray = self.data_queue.get_nowait()
            except queue.Empty:
                continue

            # 0.0 - 1.0
            average = (np.average(data) + abs(data.min())) * 0.5

            intensity = int(average * 255)
            rgb = (intensity, intensity, intensity)

            # range = [
            #     (250, 250, 110),
            #     (225, 244, 112),
            #     (201, 238, 115),
            #     (178, 231, 119),
            #     (156, 223, 124),
            #     (134, 215, 128),
            #     (114, 207, 133),
            #     (94, 198, 136),
            #     (74, 189, 140),
            #     (55, 179, 142),
            #     (35, 170, 143),
            #     (11, 160, 143),
            #     (0, 150, 142),
            #     (0, 140, 139),
            #     (0, 130, 136),
            #     (0, 120, 130),
            #     (16, 110, 124),
            #     (27, 100, 116),
            #     (34, 91, 108),
            #     (39, 81, 98),
            #     (42, 72, 88),
            # ]
            # range.reverse()
            # rgb = range[int(len(range) * average)]
            # print(rgb)
            # r = np.linspace(0, 255, 50)
            # g = np.linspace(0, 20, 50)
            # b = np.linspace(0, 20, 50)
            # rgb = np.column_stack((r, g, b))
            # rgb = rgb[int(average * 50)].astype(int)

            # try:
                # self.connection.fill(rgb)
                # self.connection.show()
            # except Exception as e:
            #     print(e)
            #     self.close()

            # self.effect.update()

            # rgb = (
            #     min(int(2.0 * average * 255), 255),
            #     min(int(1.8 * (1 - average) * 255), 255),
            #     0,
            # )
            # rgb = (0, 0, 0)
