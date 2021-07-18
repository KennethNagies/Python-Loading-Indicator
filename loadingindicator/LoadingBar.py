import os, sys
from .LoadingIndicator import LoadingIndicator

class LoadingBar(LoadingIndicator):
    SPINNER = ['|', '/', '-', '\\']
    TITLE_TRUNCATOR = "..."
    TITLE_PADDING = 3
    SPINNER_WIDTH = 3
    PERCENT_INDICATOR_WIDTH = 4

    def __init__(self, max_progress, title = ""):
        self._max_progress = max_progress
        self._title = title
        self._current_progress = 0
        self._printed = False
        self._current_spinner_index = 0
        self._last_printed_indicator = ""

    def draw(self):
        sys.stdout.write(str(self))
        sys.stdout.flush()
        self._last_printed_indicator = str(self)
        self._current_spinner_index = (self._current_spinner_index + 1) % len(self.SPINNER)

    def set_progress(self, progress):
        self._current_progress = min(self._max_progress, progress)

    def set_title(self, title):
        self._title = title

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
        if (terminal_width < self.SPINNER_WIDTH + self.PERCENT_INDICATOR_WIDTH):
            return ""
        spinner = f"[{self.SPINNER[self._current_spinner_index]}]"
        empty_space = ' ' * (terminal_width - self.SPINNER_WIDTH - self.PERCENT_INDICATOR_WIDTH)
        percent_text = f"{int(loaded_percent * 100):>3}%"
        minimum_width_with_title = self.SPINNER_WIDTH + self.PERCENT_INDICATOR_WIDTH + (2 * self.TITLE_PADDING) + len(self.TITLE_TRUNCATOR)
        if (terminal_width >= minimum_width_with_title and len(self._title) > 0):
            max_title_length = terminal_width - minimum_width_with_title
            if (len(self._title) > max_title_length):
                title = f"{self._title[0:max_title_length]}{self.TITLE_TRUNCATOR}"
            else:
                title = self._title
            title_section_length = terminal_width - self.PERCENT_INDICATOR_WIDTH - self.SPINNER_WIDTH
            return f"{spinner}{title:^{title_section_length}}{percent_text}"
        return f"{spinner}{empty_space}{percent_text}"

    def __str__(self):
        terminal_width = os.get_terminal_size()[0]
        if (self._current_progress == 0):
            loaded_percent = 0
        else:
            loaded_percent = self._current_progress / self._max_progress
        indicator = ""
        if (self._printed):
            indicator += "\033[F"
        prev_length = len(self._last_printed_indicator)
        if (prev_length > 0 and self._last_printed_indicator[prev_length - 1] == os.linesep):
            indicator += "\033[F"
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

