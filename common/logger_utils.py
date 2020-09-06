from logging import Formatter

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

#The background is set with 40 plus the number of the color, and the foreground with 30

#These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"


def formatter_message(use_color=True):
    message = "[$BOLD%(asctime)-0s$RESET] %(levelname)-0s ($BOLD%(filename)s$RESET:%(lineno)d): %(message)s"
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace(
            "$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message


COLORS = {
    'WARNING': YELLOW,
    'INFO': GREEN,
    'DEBUG': MAGENTA,
    'CRITICAL': YELLOW,
    'ERROR': RED
}


class CustomFormatter(Formatter):
    def __init__(self, use_color=True, datefmt=None):
        msg = formatter_message(use_color)
        Formatter.__init__(self, msg, datefmt=datefmt)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (
                30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return Formatter.format(self, record)


color_formatter = CustomFormatter(datefmt="%Y-%m-%0d %H:%M:%S")
default_formatter = CustomFormatter(
    use_color=False, datefmt="%Y-%m-%0d %H:%M:%S")
