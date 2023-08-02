#!/usr/bin/env python

import serial


class Connection:
    def __init__(self) -> None:
        self.serial = serial.Serial("/dev/ttyUSB0", 9600)

    def __del__(self):
        self.serial.close()

    def reset(
        self,
    ):
        for i in range(0, 60):
            self.set(i, (10, 10, 10))
        self.show()

    def set(self, index: int, rgb: tuple[int, int, int]):
        if index == 255:
            raise Exception("Index 255 is reserved for showing")
        self.serial.write(
            bytearray(
                [
                    index,
                    rgb[0],
                    rgb[1],
                    rgb[2],
                ]
            )
        )

    def show(self):
        self.serial.write(bytearray([255, 0, 0, 0]))


connection = Connection()

connection.reset()

# n = 60
# i = 0
# for i in range(0, 60):
#     if i % 2 == 0:
#         connection.set(i, (200, 0, 0))
#     else:
#         connection.set(i, (0, 0, 200))
#     i += 1
#     i = i % n

# connection.show()
