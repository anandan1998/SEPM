import time


class timer:
    def __init__(self, duration):
        self.duration = duration * 60  # Convert minutes to seconds
        self.start_time = None
        self.paused_time = None
        self.paused_duration = 0

    def start_timer(self):
        if self.start_time is None:
            self.start_time = time.time()
        elif self.paused_time is not None:
            self.paused_duration += time.time() - self.paused_time
            self.paused_time = None

    def check_remaining_time(self):
        if self.start_time is None:
            return self.duration
        elif self.paused_time is not None:
            elapsed = self.paused_time - self.start_time - self.paused_duration
        else:
            elapsed = time.time() - self.start_time - self.paused_duration
        remaining = max(0, self.duration - elapsed)
        return remaining

    def pause_timer(self):
        if self.start_time is not None and self.paused_time is None:
            self.paused_time = time.time()

    def timer_elapsed(self):
        return self.check_remaining_time() == 0
