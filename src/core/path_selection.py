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
    "_" is considered a filler node (can be anything)
    '''
    pattern = list_strip(pattern, "_") #since _X_X_ is essentially the presence of X_X pattern
    i, j = 0, len(pattern) #say, MMM would be 0, 3
    
    #sc
    if j > len(path_nodes):
        return False

    
    #normal case
    if not "_" in pattern:
    
        while j <= len(path_nodes):
            obs = [node["kind"] for node in path_nodes[i:j]] #012 then 123 then 234 etc. Not worrying about optimizing bc O(1)
            if obs==pattern: return True
            i += 1
            j += 1
        return False

    #filler case
    else:
        while j <= len(path_nodes):
            obs = [node["kind"] for node in path_nodes[i:j]] #so say it's RME
            #for every event in obs, check if it has a match or a filler in pattern
            #if every event comes out OK, return true
            comp = [kind for kind in pattern if kind!="_"]
            dropped = hasPattern(comp, path_nodes)
            if comp in obs:  return True
            acceptable = True
            for k in range(len(obs)):
                if (obs[k] != pattern[k]) and (pattern[k] != "_"):
                    acceptable = False
                    break
            if acceptable or dropped:
                return True
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
        pattern = list_strip(pattern, "_") #since _X_X_ is essentially the presence of X_X pattern
        i, j = 0, len(pattern) #say, MMM would be 0, 3
        
        #sc
        if j > len(path_nodes):
            return False
    
        
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
                obs = [node["kind"] for node in path_nodes[i:j]] #so say it's RME
                obs_coords = [node["coord"] for node in path_nodes[i:j]]
                #for every event in obs, check if it has a match or a filler in pattern
                #if every event comes out OK, return true
                comp = [kind for kind in pattern if kind!="_"]
                dropped = hasPattern(comp, path_nodes)
                if comp in obs:  output.append(obs_coords)
                acceptable = True
                for k in range(len(obs)):
                    if (obs[k] != pattern[k]) and (pattern[k] != "_"):
                        acceptable = False
                        break
                if acceptable or dropped:
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
    
def evaluatePath(path, act_heuristics):
    policies = {
        "too_many_fights": "min",
        "strong_start": "max",
        "safe_elite": "max",
    }

    return sum(
        evaluateCategory(
            path,
            patterns,
            policies.get(category, "max"),
        )
        for category, patterns in act_heuristics.items()
    )