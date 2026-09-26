import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from runtime.base import LanguageError
from runtime.registry import Registry
from Program import Program
from Exp import Exp
from LitExp import LitExp
from VarExp import VarExp
from PrimappExp import PrimappExp
from Rands import Rands
from Prim import Prim
from AddPrim import AddPrim
from SubPrim import SubPrim
from Add1Prim import Add1Prim
from Sub1Prim import Sub1Prim

registry = Registry()
registry.register(Program, LitExp, VarExp, PrimappExp, Rands, AddPrim, SubPrim, Add1Prim, Sub1Prim)

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
