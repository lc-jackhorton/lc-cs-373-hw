
import runtime.base as _plcc
from runtime.base import LanguageError



class Many(_plcc.Node):

    _rule_name = "Many"
    _fields = ["ruleList", "ofList", "stuffList"]

    def __init__(self, ruleList, ofList, stuffList):
        super().__init__()
        self.ruleList = ruleList
        self.ofList = ofList
        self.stuffList = stuffList


