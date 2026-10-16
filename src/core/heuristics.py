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
                ("ancient","monster","monster","monster","shop","elite"): 1,
                ("monster", "monster", "monster", "shop", "restsite", "elite"): 5,
            },

            "safe_elite":{
                ("restsite", "elite") : 1,
                ("restsite", "elite", "restsite"): 3,
                ("restsite", "elite", "_", "restsite"): 2,
                ("elite", "restsite", "boss"): 1
            },
         
        },
        "act2" : {
                },
        "act3" : {     
                }
    }
}


#These are tools that match a sequence of nodes to its most "extreme" path
#eg if I have MMMMM, it will select the heuristic for MMMMM rather than for its subset MMMM
def expandPattern(pattern):
    options = [
        (None, node) if node == "_" else (node,)
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
            return True

    return False


def evaluateCategory(path, patterns, policy="max"):
    weights = [
        weight
        for pattern, weight in patterns.items()
        if matchesPattern(path, pattern)
    ]

    if not weights:
        return 0

    if policy == "max":
        return max(weights)
    elif policy == "min":
        return min(weights)
    elif policy == "extreme":
        return max(weights, key=abs)
    else:
        raise ValueError(f"Unknown policy: {policy}")