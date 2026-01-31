import json

def load_data():
    with open("watchlists_v2.json", 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open("watchlists_v2.json", 'w', encoding='utf-8') as f:
        return json.dump(data, f, indent=4, ensure_ascii=False)