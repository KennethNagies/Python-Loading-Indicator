import os, sys
from .LoadingIndicator import LoadingIndicator

class LoadingBar(LoadingIndicator):
    def __init__(self, max_progress):
        self._max_progress = max_progress
        self._current_progress = 0
        self._printed = False


    def draw(self):
        sys.stdout.write(str(self))
        sys.stdout.flush()

    def set_progress(self, progress):
        self._current_progress = min(self._max_progress, progress)

    def __str__(self):
        terminal_width = os.get_terminal_size()[0]
        bar_length = terminal_width - 2
        if (bar_length < 0):
            return "X"
        elif (bar_length == 0):
            return "[]"
        if (self._current_progress == 0):
            loaded_percent = 0
        else:
            loaded_percent = self._current_progress / self._max_progress
        filled_bar_length = int(bar_length * loaded_percent)
        empty_bar_length = bar_length - filled_bar_length
        if (self._printed):
            bar = "\r"
        else:
            bar = ""
        bar = bar + f"[{'#' * filled_bar_length}{' ' * empty_bar_length}]"
        self._printed = True
        if (loaded_percent == 1):
            bar += os.linesep
        return bar
