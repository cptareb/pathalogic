from itertools import product

heuristics = {
    "pattern_weights":{
        "act1" : {
            "too_many_fights":{
                ("ancient","monster", "monster", "monster", "monster"): -1,
                ("ancient","monster", "monster", "monster", "monster","_","elite"): -3,
                ("ancient","monster", "monster", "monster", "monster", "monster"): -2,
                ("elite", "monster", "elite"): -2
            },

            "strong_start":{
                ("ancient","monster","monster","monster","_","elite"): 1,
                ("ancient","monster", "monster", "monster", "shop", "restsite", "elite"): 5,
                ("ancient","monster","_","monster","monster","monster","monster","restsite"):0
            },

            "safe_elite":{
                ("restsite", "elite") : 2,
                ("restsite", "elite", "restsite"): 3,
                ("restsite", "elite", "_", "restsite"): 4,
                ("elite", "restsite", "boss"): 1
            },
         
        },
        "act2" : {
            "too_many_fights":{
                            ("ancient","monster", "monster", "monster"): -2,
                            ("ancient","monster", "monster", "monster", "monster","_","elite"): -4,
                            ("ancient","monster", "monster", "monster", "monster", "monster"): -3,
                            ("elite", "monster", "elite"): -2
                        },

            "strong_start":{
                            ("ancient","monster","monster","_","_","elite"): 1,
                            ("ancient","monster","_","monster","_","_"): 1,
                            ("ancient","monster", "monster", "shop", "restsite", "elite"): 5,
                        },

            "safe_elite":{
                            ("restsite", "elite") : 1,
                            ("restsite", "elite", "restsite"): 3,
                            ("restsite", "elite", "_", "restsite"): 3,
                            ("elite", "restsite", "boss"): 1
                        }
                },
        "act3" : {
            "safe_elite":{
                            ("restsite", "elite") : 1,
                            ("restsite", "elite", "restsite"): 3,
                            ("restsite", "elite", "_", "restsite"): 2,
                            ("elite", "restsite", "boss"): 1
                        }     
                }
    }
}


#These are tools that match a sequence of nodes to its most "extreme" path
#eg if I have MMMMM, it will select the heuristic for MMMMM rather than for its subset MMMM
def expandPattern(pattern):
    options = [(node,)
        for node in pattern
    ]

    return {
        tuple(n for n in variant if n is not None)
        for variant in product(*options)
    }


def matchesPattern(path, pattern):
    for variant in expandPattern(pattern):
        n = len(variant)

        if n <= len(path) and any(
            tuple(path[i:i + n]) == variant
            for i in range(len(path) - n + 1)
        ):
            # print("Highest path detected", path)
            # print("Contains pattern", pattern)
            return True

    return False


def evaluateCategory(path:list[str], category:str, act:str) -> int:
    '''
    Grade a path according to an input category
    So MMMMM would be neutral under "safe start", but minus under "too many combats"
    Returns a composite score for the path; higher = better in all circumstances

    path :: list of strings of path events (["ancient", "combat", "rest"] whatev)
    category :: which category to grade this path by (too many combats, safe start...)
    '''
    rubric = heuristics["pattern_weights"][act][category]
    weights = [
        weight
        for pattern, weight in rubric.items()
        if matchesPattern(path, pattern)
    ]
    return sum(weights)