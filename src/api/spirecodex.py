import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("SPIRECODEX_KEY")
url = "https://spire-codex.com/api/"

def GET_json(endpoint:str, params:dict):
    '''
    sends a GET request to spirecodex
    endpoint :: api endpoint (see docs)
    params :: HTTP params for that particular endpoint (again, see docs)
    '''
    headers = {
        "X-API-Key": API_KEY,
        "Accept":"application/json"
    }

    mod_url = url + endpoint

    response = requests.get(mod_url, headers=headers, params=params)
    return response

def GET_maps(run_hash:str, params:dict):
    '''
    Returns map JSONs associated with a particular run
    run_hash :: run hash 
    params :: HTTP params - see docs
    '''
    endpoint = f"runs/{run_hash}/replay"
    run = GET_json(endpoint, params) #this will contain empty lines, needs to be cleaned b4 JSONify
    maps = []
    for line in run.text.strip().split("\n"):
        if line:  
            line_json = json.loads(line)
            if line_json["t"] == "map":
                maps.append(json.loads(line))

    return maps
    