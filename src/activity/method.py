import json
def scrpy(col):
    with open("index.json","r",encoding="utf-8") as f:
        acts = json.load(f)
    for act in acts:
        col.insert_one(act)
    


