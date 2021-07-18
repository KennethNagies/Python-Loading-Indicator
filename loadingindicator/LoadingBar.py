import os, sys
from .LoadingIndicator import LoadingIndicator

class LoadingBar(LoadingIndicator):
    SPINNER = ['|', '/', '-', '\\']
    def __init__(self, max_progress):
        self._max_progress = max_progress
        self._current_progress = 0
        self._printed = False
        self._current_spinner_index = 0

    def draw(self):
        sys.stdout.write(str(self))
        sys.stdout.flush()
        self._current_spinner_index = (self._current_spinner_index + 1) % len(self.SPINNER)

    def set_progress(self, progress):
        self._current_progress = min(self._max_progress, progress)

    def get_bar(self, terminal_width, loaded_percent):
        bar_length = terminal_width - 2
        if (bar_length < 0):
            return "X"
        elif (bar_length == 0):
            return "[]"
        filled_bar_length = int(bar_length * loaded_percent)
        empty_bar_length = bar_length - filled_bar_length
        return f"[{'#' * filled_bar_length}{' ' * empty_bar_length}]"

    def get_header(self, terminal_width, loaded_percent):
        if (terminal_width < 5):
            return ""
        spinner_char = self.SPINNER[self._current_spinner_index]
        empty_space = ' ' * (terminal_width - 5)
        percent_text = f"{int(loaded_percent * 100):>3}%"
        return f"{spinner_char}{empty_space}{percent_text}"

    def __str__(self):
        terminal_width = os.get_terminal_size()[0]
        if (self._current_progress == 0):
            loaded_percent = 0
        else:
            loaded_percent = self._current_progress / self._max_progress
        if (self._printed):
            indicator = "\033[F"
        else:
            indicator = ""
        header = self.get_header(terminal_width, loaded_percent)
        bar = self.get_bar(terminal_width, loaded_percent)
        if (len(header) > 0):
            indicator += f"{header}{os.linesep}{bar}"
        else:
            indicator += bar
        self._printed = True
        if (loaded_percent == 1):
            indicator += os.linesep
        return indicator

