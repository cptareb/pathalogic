from src.core.path_selection import *

map = {'t': 'map', 's': 3, 'ms': 627, 'floor': 0, 'act': 1, 'gen': 1, 'boss': 'WATERFALL_GIANT_BOSS', 'ancient': 'NEOW', 'ancient_coord': '3,0', 'boss_coord':'3,16', 'nodes': [{'coord': '0,6', 'kind': 'monster', 'children': ['1,7', '0,7']}, {'coord': '0,7', 'kind': 'monster', 'children': ['0,8']}, {'coord': '0,8', 'kind': 'elite', 'children': ['1,9']}, {'coord': '0,10', 'kind': 'restsite', 'children': ['0,11']}, {'coord': '0,11', 'kind': 'elite', 'children': ['1,12']}, {'coord': '1,1', 'kind': 'monster', 'children': ['1,2']}, {'coord': '1,2', 'kind': 'unknown', 'children': ['1,3']}, {'coord': '1,3', 'kind': 'monster', 'children': ['2,4']}, {'coord': '1,5', 'kind': 'monster', 'children': ['0,6']}, {'coord': '1,7', 'kind': 'restsite', 'children': ['0,8']}, {'coord': '1,9', 'kind': 'treasure', 'children': ['0,10', '2,10']}, {'coord': '1,12', 'kind': 'restsite', 'children': ['2,13']}, {'coord': '1,14', 'kind': 'shop', 'children': ['1,15']}, {'coord': '1,15', 'kind': 'restsite', 'children': ['3,16']}, {'coord': '2,1', 'kind': 'monster', 'children': ['2,2']}, {'coord': '2,2', 'kind': 'monster', 'children': ['2,3']}, {'coord': '2,3', 'kind': 'monster', 'children': ['2,4']}, {'coord': '2,4', 'kind': 'monster', 'children': ['1,5', '2,5']}, {'coord': '2,5', 'kind': 'monster', 'children': ['2,6']}, {'coord': '2,6', 'kind': 'elite', 'children': ['2,7']}, {'coord': '2,7','kind': 'unknown', 'children': ['2,8']}, {'coord': '2,8', 'kind': 'unknown', 'children': ['1,9']}, {'coord': '2,10', 'kind': 'monster', 'children': ['2,11']}, {'coord': '2,11', 'kind': 'monster', 'children': ['3,12']}, {'coord': '2,13', 'kind': 'elite', 'children': ['3,14', '1,14']}, {'coord': '3,1', 'kind': 'monster', 'children': ['4,2']}, {'coord': '3,12', 'kind': 'restsite', 'children': ['3,13']}, {'coord': '3,13', 'kind': 'monster', 'children': ['3,14']}, {'coord': '3,14', 'kind': 'unknown', 'children': ['3,15']}, {'coord': '3,15', 'kind': 'restsite', 'children': ['3,16']}, {'coord': '4,2', 'kind': 'shop', 'children': ['5,3']}, {'coord': '4,5', 'kind': 'unknown', 'children': ['4,6']}, {'coord': '4,6', 'kind': 'unknown', 'children': ['5,7']}, {'coord': '5,1', 'kind': 'monster', 'children': ['5,2']}, {'coord': '5,2', 'kind': 'monster', 'children': ['5,3']}, {'coord': '5,3', 'kind': 'monster', 'children': ['5,4', '6,4']}, {'coord': '5,4', 'kind': 'monster', 'children': ['6,5', '4,5']}, {'coord': '5,6', 'kind': 'unknown', 'children': ['6,7']}, {'coord': '5,7', 'kind': 'restsite', 'children': ['5,8']}, {'coord': '5,8', 'kind': 'unknown', 'children': ['6,9']}, {'coord': '5,10', 'kind': 'restsite', 'children': ['5,11', '6,11']}, {'coord': '5,11', 'kind': 'monster', 'children': ['5,12']}, {'coord': '5,12', 'kind': 'elite', 'children': ['6,13']}, {'coord': '5,14', 'kind': 'monster', 'children': ['5,15']}, {'coord': '5,15', 'kind': 'restsite', 'children': ['3,16']}, {'coord': '6,4', 'kind': 'unknown', 'children': ['6,5']}, {'coord': '6,5', 'kind': 'monster', 'children': ['6,6', '5,6']}, {'coord': '6,6', 'kind': 'restsite', 'children': ['6,7']}, {'coord': '6,7', 'kind': 'elite', 'children': ['6,8', '5,8']}, {'coord': '6,8', 'kind': 'shop', 'children': ['6,9']}, {'coord': '6,9', 'kind': 'treasure', 'children': ['5,10', '6,10']}, {'coord': '6,10', 'kind': 'elite', 'children': ['6,11']}, {'coord': '6,11', 'kind': 'monster', 'children': ['6,12']}, {'coord': '6,12','kind': 'unknown', 'children': ['6,13']}, {'coord': '6,13', 'kind': 'unknown', 'children': ['6,14', '5,14']}, {'coord': '6,14', 'kind': 'elite', 'children': ['5,15']}, {'coord': '3,0', 'kind': 'ancient', 'children': ['1,1', '2,1', '3,1', '5,1']}, {'coord': '3,16', 'kind': 'boss', 'children': []}]}

def test_isValidPath():
    start = "0,6"
    end = "1,7"
    assert isValidPath(start, end, map["nodes"])
    start = "0,6"
    end = "1,8"
    assert not isValidPath(start, end, map["nodes"])
    print("Test cases passed")

def test_getAllPaths():
    start = "1,1"
    print(getAllPaths(start, map["nodes"]))

def test_getPathInfo():
    path = getAllPaths("1,1", map["nodes"])[0]
    info = getPathInfo(path, map["nodes"])
    print(info)

test_getPathInfo()
    