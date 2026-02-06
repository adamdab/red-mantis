import logging

red = "\x1b[31m"
green = "\x1b[32m"
pink = "\x1b[35m"
reset = "\x1b[0m"


banner = fr"""
{red}______         _ {reset} {green}___  ___            _   _     {reset}
{red}| ___ \       | |{reset} {green}|  \/  |           | | (_)    {reset}
{red}| |_/ /___  __| |{reset} {green}| .  . | __ _ _ __ | |_ _ ___ {reset}
{red}|    // _ \/ _` |{reset} {green}| |\/| |/ _` | '_ \| __| / __|{reset}
{red}| |\ \  __/ (_| |{reset} {green}| |  | | (_| | | | | |_| \__ \{reset}
{red}\_| \_\___|\__,_|{reset} {green}\_|  |_/\__,_|_| |_|\__|_|___/{reset}                                                
"""

def print_startup(args):
    _print_banner()
    _print_args(args)

def _print_banner():
    print(banner)

def _print_args(args):
    for arg, value in vars(args).items():
        print(f"{arg}:{pink}{value}{reset}")
    print()


def configure_logging(silent: bool) -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING if silent else logging.INFO)
    
    class ColoredFormatter(logging.Formatter):
        COLOR_RESET = "\x1b[0m"
        COLORS = {
            logging.DEBUG: "\x1b[90m",
            logging.INFO: "\x1b[32m",
            logging.WARNING: "\x1b[33m",
            logging.ERROR: "\x1b[31m",
            logging.CRITICAL: "\x1b[31;1m",
        }

        def format(self, record: logging.LogRecord) -> str:
            level_color = self.COLORS.get(record.levelno, "")
            record.levelname = f"{level_color}{record.levelname}{self.COLOR_RESET}"
            return super().format(record)

    fmt = "%(asctime)s | %(levelname)s | %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    handler = logging.StreamHandler()
    handler.setFormatter(ColoredFormatter(fmt=fmt, datefmt=datefmt))

    logger.handlers = []
    logger.addHandler(handler)
