import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from runtime.base import LanguageError
from runtime.registry import Registry
from Start import Start
from One import One
from Two import Two
from Three import Three
from Blah import Blah
from Goo import Goo
from Many import Many
from Classes import Classes
from Silly import Silly
from Rule import Rule
from Stuff import Stuff

registry = Registry()
registry.register(One, Two, Three, Goo, Many, Classes, Silly, Rule, Stuff)

print(json.dumps({"kind": "ready"}), flush=True)

try:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            tree = registry.deserialize(json.loads(line))
            result = tree._run()
            if not isinstance(result, str):
                raise TypeError(f"_run() must return a string, got {type(result).__name__}")
            print(json.dumps({"kind": "result", "value": result}), flush=True)
        except LanguageError as e:
            print(json.dumps({"kind": "error", "type": type(e).__name__, "message": str(e)}), flush=True)
        except Exception as e:
            print(json.dumps({"kind": "specification_error", "type": type(e).__name__, "message": str(e)}), flush=True)
            sys.exit(1)
except KeyboardInterrupt:
    print("User interrupted execution by ^C.", flush=True)
    sys.exit(130)
