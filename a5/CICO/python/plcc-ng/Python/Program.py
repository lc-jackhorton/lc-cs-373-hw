
import runtime.base as _plcc
from runtime.base import LanguageError
from _Start import _Start

from Env import Env


class Program(_Start):

    _rule_name = "Program"
    _fields = []

    def __init__(self):
        super().__init__()

    env = Env.initEnv()


