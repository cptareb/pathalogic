from src.core.heuristics import *
from src.core.path_selection import *
from tests.core.test_path_selection import map

def test_evaluatePath():
    path = getAllPaths("1,1",map["nodes"])[0]
    nodes = getPathInfo(path, map["nodes"])
    nodes_tups = tuple([n["kind"] for n in nodes])
    print(nodes_tups)
    patterns = heuristics["pattern_weights"]["act1"]["too_many_fights"]
    print(evaluateCategory(nodes_tups, patterns, policy="min"))

