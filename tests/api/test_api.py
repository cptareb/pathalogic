import json
from src.api.spirecodex import *

run_hash = "4f5cd5325c1d6946"
test_params = {
    "lang":"en",
    "run_hash":run_hash 
}
maps = GET_maps(run_hash, test_params)
endpoint = f"runs/{run_hash}/replay"

print(len(maps))

