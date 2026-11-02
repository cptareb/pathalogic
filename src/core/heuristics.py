from itertools import product

heuristics = {
    "pattern_weights":{
        "act1" : {
            "too_many_fights":{
                ("ancient","monster", "monster", "monster", "monster"): -1,
                ("ancient","monster", "monster", "monster", "monster","_","elite"): -3,
                ("ancient","monster", "monster", "monster", "monster", "monster"): -100,
                ("elite", "monster", "elite"): -2
            },

            "strong_start":{
                ("ancient","monster","monster","monster","restsite","elite"): 1,
                ("ancient","monster", "monster", "monster", "shop", "restsite", "elite"): 5,
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
# def expandPattern(pattern):
#     print("pattern to expand", pattern)
#     options = [(node,)
#         for node in pattern
#     ]
#     print("options", options)
#     output = {
#         tuple(n for n in variant if n is not None)
#         for variant in product(*options)
#     }
#     print("output", output)
#     return output


# def matchesPattern(path, pattern):
#     for variant in expandPattern(pattern):
#         n = len(variant)

#         if n <= len(path) and any(
#             tuple(path[i:i + n]) == variant
#             for i in range(len(path) - n + 1)
#         ):
#             return True

#     return False

# def describeAsPatterns(path:list[str], act:str) -> list[list[str]]:
#     '''
#     Describes a path as a series of patterns, such that no node can be part of two patterns
#     The idea is to capture as much of the path in gradeable patterns as possible for easy eval
#     '''
#     #sliding window? 
#     #if one pattern is totally subsumed by another pattern, we default to the bigger pattern
#     def getBiggestPattern(act:str, category:str) -> int: 
#         '''
#         helper fxn for finding sliding window size
#         '''
#         patterns = heuristics["pattern_weights"][act][category]
#         max_len = 0
#         for pattern in patterns:
#             if len(pattern) > max_len:
#                 max_len = len(pattern)
#         return max_len

#     max_window_len = max([getBiggestPattern(act, cat) for cat in heuristics["pattern_weights"][act].keys()])
#     output = []
#     i = 0 
#     while (i < len(path)):
#         i += 1


def selectPatterns(path: list[str], patterns: dict[tuple[str]]) -> tuple[list[tuple[tuple[str], int, int, int]], int]:
    '''
    Select the highest valued set of non-overlapping pattern occurrences
    in a given path, using weighted intervals. 
    Returns a tuple with 2 objects:
    - the pattern set, as tup (pattern, start, end, score) for description. End idx exclusive. No idx overlap.
    - value of the pattern set, per heuristics

    path :: list of path event names (eg ["ancient", "combat", "rest"...])
    patterns :: heuristics within a certain category in a certain act
    '''

    n = len(path)

    #init
    matches = [[] for _ in range(n + 1)]

    #Find every occurrence of every pattern...
    for pattern, score in patterns.items():
        pattern = tuple(pattern)
        length = len(pattern)

        if length == 0:
            raise ValueError("empty pattern")

        for start in range(n - length + 1):
            end = start + length

            if tuple(path[start:end]) == pattern:
                matches[end].append((start, pattern, score))

    # DP
    # dp[i] = optimal score using the first i nodes.
    dp = [(0,0)] * (n + 1)

    #tracking path (would look like [(0, "ancient"->5xcombats, -2)]) for each pattern detected
    choices = [None] * (n + 1)

    #for each position...
    for i in range(1, n + 1):

        #inherit prev position's values by default
        dp[i] = dp[i - 1]

        for start, pattern, score in matches[i]:
            prev_seen, prev_score = dp[start]

            #looking at a "candidate" node for extending a maybe-extant pattern
            #eg we might have prev_seen rep some nodes RE, candidate R, we'd include bc plus score
            candidate = (
                prev_seen + len(pattern), #proposed extension of the pattern
                prev_score + score #actual score of resulting pattern
            )

            if candidate > dp[i]: #lexicographical comparison. Essentially, we only care about length but still track score as tiebreaker
                dp[i] = candidate #...set...
                choices[i] = (start, pattern, score) #...and record thusly

    #reconstruct the selected sequence
    selected = []
    i = n

    while i > 0:
        choice = choices[i]

        if choice is None:
            i -= 1
        else:
            start, pattern, score = choice

            selected.append((pattern, start, i, score))
            i = start

    selected.reverse()
    # print("selected", selected)
    return selected, dp[n][1]




def evaluateCategory(path:list[str], category:str, act:str) -> int:
    '''
    Grade a path according to an input category
    So MMMMM would be neutral under "safe start", but minus under "too many combats"
    Returns a composite score for the path; higher = better in all circumstances

    path :: list of strings of path events (["ancient", "combat", "rest"] whatev)
    category :: which category to grade this path by (too many combats, safe start...)
    '''
    rubric = heuristics["pattern_weights"][act][category]
    return selectPatterns(path, rubric)[1]