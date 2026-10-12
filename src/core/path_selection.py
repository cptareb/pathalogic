import json

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