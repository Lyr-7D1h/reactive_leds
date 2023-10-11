#!/usr/bin/env python

from typing import List
import serial


class Connection:
    def __init__(self, serial_path: str, led_amount: int, disabled_leds: List[int]) -> None:
        self.disabled_leds = disabled_leds
        self.led_amount = led_amount - len(disabled_leds)
        try:
            print(
                f"Connecting to led strip with {led_amount} leds through {serial_path}"
            )
            self.serial = serial.Serial(
                serial_path,
                250000,
                timeout=1,
                dsrdtr=True,
                rtscts=True,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                write_timeout=3
            )
        except Exception as e:
            print(f"Could not open {serial_path}")
            print(e)
            raise e
        if not self.serial.is_open:
            self.serial.open()
        self.init()
        print("Connected")

    def __del__(self):
        print("Closing connection")
        self.serial.close()

    def clear(self):
        self.send([(0,0,0)] * self.led_amount)

    def available(self) -> bool:
        return self.serial.is_open

    def init(self):
        print("{0:b}".format(self.led_amount))
        print(self.led_amount)
        print(self.led_amount | 1<<16) 
        data = self.led_amount | 1<<15
        print("{0:b}".format(data))
        # 1000_0000_0011_0100
        print(data.to_bytes(2, "little"))
        self.serial.write(data.to_bytes(2, "big"))

    def write(self, data: list[int]):
        self.serial.write(bytearray(data))
        self.serial.flush()

    # Send color map
    def send(self, data: list[tuple[int, int, int]]):
        byte_data = bytearray([color for rgb in data for color in rgb])
        self.serial.write(byte_data)
        self.serial.flush()

    def fill(self, rgb: tuple[int, int, int]):
        data = [color for color in rgb for _ in range(0, self.led_amount)]
        self.write(data)

    def set(self, start: int, end: int, rgb: tuple[int, int, int]):
        data = []
        for _ in range(start, end):
            for c in rgb:
                data.append(c)
        self.write(data)

    # def show(self):
    #     self.serial.write(bytearray([255, 0, 0, 0, 0]))
    #     # probably don't need this
    #     self.serial.flush()
