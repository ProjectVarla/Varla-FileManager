from enum import Enum, auto
from os import getenv
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()
DEBUG_MODE: bool = getenv("DEBUG_MODE").lower() == "true"


class Verbosity(Enum):
    QUITE = auto()
    NORMAL = auto()
    VERBOSE = auto()


class Varla:
    verbosity: Verbosity = Verbosity.NORMAL
    debug_mode: bool = DEBUG_MODE

    @staticmethod
    def info(*str: str):
        if Varla.verbosity != Verbosity.QUITE:
            print("\033[1;32m[INFO] ✅\033[0m", *str)

    @staticmethod
    def error(*str: str):
        print("\033[1;31m[EROR] 🚨\033[0m", *str)

    @staticmethod
    def verbose(*str: str):
        if Varla.verbosity == Verbosity.VERBOSE:
            print("\033[1;33m[INFO] 📢\033[0m", *str)

    @staticmethod
    def debug(*payload: any, name: str = "") -> None:
        if Varla.debug_mode:
            print("\033[1;34m[DEBUG] 🚧 ******************************\033[0m")
            print("\033[1;34m", name, "\033[0m", sep="") if name else None
            for item in payload:
                pprint(item)
            print("\033[1;34m*****************************************\033[0m")
