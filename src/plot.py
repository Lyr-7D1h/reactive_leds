import queue
import numpy as np
from config import config
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt


class Plot:
    def __init__(
        self,
        interval: float,
        window: float,
        samplerate: float,
        downsample: float,
        data_queue: queue.Queue,
    ) -> None:
        length = int(window * samplerate / (1000 * downsample))
        self.plotdata = np.zeros((length, 2))
        self.data_queue = data_queue

        fig, ax = plt.subplots()
        self.lines = ax.plot(self.plotdata)

        ax.axis((0, len(self.plotdata), -1, 1))
        ax.set_yticks([0])
        ax.yaxis.grid(True)
        ax.tick_params(
            bottom=False,
            top=False,
            labelbottom=False,
            right=False,
            left=False,
            labelleft=False,
        )
        fig.tight_layout(pad=0)
        self.anim = FuncAnimation(
            fig,
            self.update,
            interval=interval,
            blit=True,
            save_count=length,
        )

    def show(self):
        plt.show()

    def update(self, frame):
        """This is called by matplotlib for each plot update.

        Typically, audio callbacks happen more frequently than plot updates,
        therefore the queue tends to contain multiple blocks of audio data.

        """
        while True:
            try:
                data: np.ndarray = self.data_queue.get_nowait()
            except queue.Empty:
                break

            shift = len(data)
            self.plotdata = np.roll(self.plotdata, -shift, axis=0)
            self.plotdata[-shift:, 0] = data
            # moving average
            self.plotdata[-shift:, 1] = np.average(data) + abs(data.min())

            # plotdata[-shift:, 1] = [data.max() for x in data]
        for column, line in enumerate(self.lines):
            line.set_ydata(self.plotdata[:, column])
        return self.lines
