import json

def isValidPath(start_coords:str, end_coords:str, nodes:list[dict]) -> bool:
    '''
    Recursively determines whether the input path is possible (i.e., you can progress from start to end node)
    Returns True for valid, False otherwise.
    start_coords :: string representation of start coordinate (ex "0,6")
    end_coords :: same deal but for end coordinate
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