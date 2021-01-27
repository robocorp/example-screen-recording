# +
import os
import sys
import time
import threading
import queue

import numpy as np
import cv2
import mss
from pynput.mouse import Controller


# -

class UsageError(Exception):
    def __init__(self, msg):
        self.msg = msg

class suppress_stderr(object):

    def __init__(self):
        # Open a null file
        self.null_fd = os.open(os.devnull, os.O_RDWR)
        # Save the actual stderr (2) file descriptor.
        self.save_fd = os.dup(2)

    def __enter__(self):
        # Assign the null pointer to stderr.
        os.dup2(self.null_fd, 2)

    def __exit__(self, *_):
        # Re-assign the real stderr back to (2)
        os.dup2(self.save_fd, 2)
        # Close all file descriptors
        os.close(self.null_fd)
        os.close(self.save_fd)

def is_truthy(item):
    if isinstance(item, str):
        return item.upper() not in ['FALSE', 'NONE', 'NO', '']
    return bool(item)


class video_recorder:
    def __init__(self):
        self.capture_thread = None
        self.output_thread = None

        self.buffer = None
        self.filename = None
        self.monitor = None
        self.width = 0
        self.height = 0
        self.max_frame = 0
        self.fps = 0
        self.force_fps = False
        self.stop_capture = None

    def start_recorder(self, filename="output/video.webm", max_length=60, monitor=1, scale=1.0, fps=4, force_fps="False", fourcc="VP80"):
        self.filename = filename
        self.scale = float(scale)
        self.fps = int(fps)
        self.force_fps = is_truthy(force_fps)
        self.fourcc = fourcc

        with mss.mss() as sct:
            # Part of the screen to capture
            self.monitor = sct.monitors[int(monitor)]
            self.left = self.monitor["left"]
            self.top = self.monitor["top"]
            self.right = self.left + self.monitor["width"]
            self.bottom = self.top + self.monitor["height"]
            self.width = int(self.monitor["width"] * self.scale)
            self.height = int(self.monitor["height"] * self.scale)

        self.max_frame = self.fps * int(max_length)
        self.buffer = queue.Queue()

        self.stop_capture = threading.Event()

        self.output_thread = threading.Thread(name="Writer", target=self._write_file)
        self.capture_thread = threading.Thread(name="Capturer", target=self._capture)
        self.output_thread.start()
        self.capture_thread.start()

    def stop_recorder(self):
        self.stop_capture.set()
        self.capture_thread.join()
        self.output_thread.join()

    def cancel_recorder(self):
        self.stop_recorder()
        os.remove(self.filename)

    def _write_file(self):
        cur_frame = 0
        prev_frame = None

        fourcc = cv2.VideoWriter_fourcc(*'VP80')

        with suppress_stderr():
            out = cv2.VideoWriter(self.filename, fourcc, self.fps, (self.width, self.height))

        while cur_frame < self.max_frame:
            data = self.buffer.get()
            if data is None:
                break

            ts, img, mouse = data
            frame = np.array(img)

            if self.force_fps:
                while ts > (cur_frame + 1) / self.fps:
                    cur_frame += 1
                    out.write(out_frame)
            else:
                if prev_frame is not None and (prev_frame==frame).all():
                    continue

            cur_frame += 1
            prev_frame = frame

            frame = cv2.resize(frame, (self.width, self.height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            x, y = mouse
            if self.left <= x < self.right and self.top <= y < self.bottom:
                x = int((x - self.left) * self.scale)
                y = int((y - self.top) * self.scale)
                r = int(self.width * self.scale / 100)
                w = max(1, round(self.width * self.scale / 500))
                cv2.circle(frame, (x, y), r, (0, 0, 255), w)

            out_frame = cv2.putText(frame, '{0:.2f}'.format(ts), (10, 30),  cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 4)
            out.write(out_frame)

        self.stop_capture.set()
        out.release()

    def _capture(self):
        mouse = Controller()
        with mss.mss() as sct:
            frame_number = 0
            start_time = time.time()

            while not self.stop_capture.is_set():
                trigger_time = start_time + frame_number / self.fps
                while time.time() < trigger_time:
                    time.sleep(0.001)

                # Get raw pixels from the screen, save it to a Numpy array
                # frame = np.array(sct.grab(self.monitor))
                self.buffer.put_nowait((
                    time.time() - start_time,
                    sct.grab(self.monitor),
                    mouse.position
                ))

                frame_number += 1

        self.buffer.put_nowait(None)


def main():
    rec = video_recorder()
    rec.start_recorder("video.webm", fps=20, scale=0.5, force_fps="True")

    time.sleep(4)

    rec.stop_recorder()


if __name__ == "__main__":
    main()


