import json
from src.helper.generic import list_strip
from src.core.heuristics import *

def isValidPath(start_coords:str, end_coords:str, nodes:list[dict]) -> bool:
    '''
    Recursively determines whether the input path is possible (i.e., you can progress from start to end node)
    Returns True for valid, False otherwise.
    start_coords :: string representation of start coordinate (ex "0,6")
    end_coords :: same deal but for end coordinate
    nodes :: node list from the map JSON
    '''

    if start_coords == end_coords:
        return True

    for node in nodes:
        if node["coord"] == start_coords:
            return any(
                isValidPath(child, end_coords, nodes)
                for child in node["children"]
            )

    return False

def getAllPaths(start_coords:str, nodes:list[dict]) -> list[list[str]]:
    '''
    Returns all complete path possibilities on the map using DFS
    start_coords :: root node
    nodes :: node list from map JSON
    '''

    for node in nodes:
        if node["coord"] == start_coords: #everything up to here is locating start_coords node
            if not node["children"]:
                return [[start_coords]]
            paths = []
            for child in node["children"]:
                for path in getAllPaths(child, nodes):
                    paths.append([start_coords] + path)
            return paths

    return []

def getPathInfo(path:list[str], nodes:list[dict]) -> list[dict]:
    '''
    Given a simple coordinate path, gets in-depth info for that path from full map dict
    Useful for investigating particular paths in detail
    path :: simple coordinate path
    nodes :: full map dict
    '''
    output = []
    for coord in path:
        for node in nodes:
            if node["coord"]==coord:
                output.append(node)
    return output

def hasPattern(pattern:list[str], path_nodes:list[dict]) -> bool:
    '''
    Given an input "pattern", returns whether a path contains that pattern
    For example, MMMM pattern, R_E pattern, RERE pattern, QQQ+ pattern
    pattern :: list of sequential node "kinds" e.g., "monster", "restsite"
    path_nodes :: list of sequential nodes in a path
    Note - this won't work if you pass a nested array as path_nodes; this fxn works on one path at a time
    "_" is considered a filler safe node (can be anything that isn't a known combat)
    '''
    i, j = 0, len(pattern) #say, MMM would be 0, 3
    
    #sc
    if j > len(path_nodes):
        return False

    
    #normal case
    if "_" not in pattern:
    
        while j <= len(path_nodes):
            obs = [node["kind"] for node in path_nodes[i:j]] #012 then 123 then 234 etc. Not worrying about optimizing bc O(1)
            if obs==pattern: return True
            i += 1
            j += 1
        return False

    #filler case
    else:
        acceptable = False
        while j <= len(path_nodes):
            obs = [node["kind"] for node in path_nodes[i:j]]
            acceptable = True #whether the observation would fit the pattern's request

            #comparing obs to safety fillers
            for i in range(len(obs)): #so for each node in obs...
                if pattern[i] == "_": #if the pattern requests a safe node...
                    if obs[i] in {"combat", "boss", "elite"}: #if safe node dne, pattern dne at that location
                        acceptable = False
                        break #look for pattern in next index
                elif pattern[i] != obs[i]: #if there's a mismatch among nodes pattern doesn't rq as safe...
                    acceptable = False
                    break
            if acceptable: return True #if the pattern has been located, return appropriately
            i+=1
            j+=1
            
        return False 

def locatePattern(pattern:list[str], path_nodes:list[dict]) -> list[list[str]]:
    '''
    returns the coordinates of all nodes involved in a particular pattern in a given path
    e.g., if a pattern existed at 1,1 -> 2,1 -> 3,2, would return ["1,1", "2,1,", "3,2"]
    pattern :: see hasPattern: same deal
    path_nodes :: see hasPattern: same deal
    '''
    if hasPattern(pattern, path_nodes):
        output = []
        i, j = 0, len(pattern) #say, MMM would be 0, 3
        
        #sc
        if j > len(path_nodes):
            return []
    
        
        #normal case
        if not "_" in pattern:
            while j <= len(path_nodes):
                obs = [node["kind"] for node in path_nodes[i:j]] #012 then 123 then 234 etc. Not worrying about optimizing bc O(1)
                obs_coords = [node["coord"] for node in path_nodes[i:j]]
                if obs==pattern: output.append(obs_coords)
                i += 1
                j += 1
    
        #filler case
        else:
            while j <= len(path_nodes):
                acceptable = False
                while j <= len(path_nodes):
                    obs = [node["kind"] for node in path_nodes[i:j]]
                    obs_coords = [node["coord"] for node in path_nodes[i:j]]
                    acceptable = True #whether the observation would fit the pattern's request
        
                    #comparing obs to safety fillers
                    for i in range(len(obs)): #so for each node in obs...
                        if pattern[i] == "_": #if the pattern requests a safe node...
                            if obs[i] in {"combat", "boss", "elite"}: #if safe node dne, pattern dne at that location
                                acceptable = False
                                break #look for pattern in next index
                        elif pattern[i] != obs[i]: #if there's a mismatch among nodes pattern doesn't rq as safe...
                            acceptable = False
                            break
                    if acceptable: 
                        output.append(obs_coords)
                    i+=1
                    j+=1
        return output
    else:
        return []

def locateOptionality(path_nodes:list[dict]) -> list[list[str]]:
    '''
    Given a path, returns the coordinates of all "optional" nodes, i.e., nodes with >1 child
    path_nodes :: list of path node dictionaries, like from getPathInfo fxn
    '''
    optional_nodes = []
    for n in path_nodes:
        options = n.get("children", [])
        if len(options) > 1:
            optional_nodes.append(n["coord"])
    return optional_nodes
    
def evaluatePath(path:list[str], act:str) -> int:
    '''
    Calculates the grade for a particular path based on some heuristics
    Sums the positive and negative weights associated with each category for said path
    E.g., if a path has 2 instances of +1 safe elite and 1 instance of -2 too many combats, would score as 0
    Returns that sum
    Think of it as grading by a rubric of heuristics. See heuristics.py for more info

    path :: list of events constituting the path (ex: ["ancient","combat","event","rest",...])
    act :: which act path is being graded in (will affect score) "act1" "act2" "act3"
    heuristics :: full heuristic dict, used for combing through categories
    '''
    categories = heuristics["pattern_weights"][act].keys()

    return sum(
        evaluateCategory(
            path,
            category,
            act
        )
        for category in categories
    )

def grabAllPathGrades(actmap:dict) -> list[list[str]]:
    '''
    Returns coordinate sequence for all possible paths in act
    map :: full map dict
    '''
    output = {}
    act = f"act{actmap["act"]}"
    all_paths = getAllPaths("3,0", actmap["nodes"]) #3,0 is constant coords for ancient
    for p in all_paths:
        info = getPathInfo(p,actmap["nodes"])
        events = [n["kind"] for n in info]
        grade = evaluatePath(events, act)
        output[tuple(p)] = grade
    return output

def locateAllBestPaths(map:dict) -> list[list[str]]:
    '''
    Returns coordinate sequence for best path per act heuristics
    On a tie, returns rightmost (most recently scanned) path
    map: full map 
    '''
    path_grades = grabAllPathGrades(map)
    max_val = max(path_grades.values())
    best_val_paths = [k for k, v in path_grades.items() if v==max_val]
    return best_val_paths
