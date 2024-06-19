from enum import Enum
from engine.game.deck import Deck

def create_cards():
    territory_cards = {
        "Alaska": {"territory_id": 0, "troop": "Infantry", "troop_count": 1},
        "Alberta": {"territory_id": 1, "troop": "Cavalry", "troop_count": 5},
        "Central America": {"territory_id": 2, "troop": "Artillery", "troop_count": 10},
        "Eastern United States": {"territory_id": 3, "troop": "Artillery", "troop_count": 10},
        "Greenland": {"territory_id": 4, "troop": "Cavalry", "troop_count": 5},
        "Northwest Territory": {"territory_id": 5, "troop": "Artillery", "troop_count": 10},
        "Ontario": {"territory_id": 6, "troop": "Cavalry", "troop_count": 5},
        "Quebec": {"territory_id": 7, "troop": "Cavalry", "troop_count": 5},
        "Western United States": {"territory_id": 8, "troop": "Artillery", "troop_count": 10},
        "Great Britain": {"territory_id": 9, "troop": "Artillery", "troop_count": 10},
        "Iceland": {"territory_id": 10, "troop": "Infantry", "troop_count": 1},
        "Northern Europe": {"territory_id": 11, "troop": "Artillery", "troop_count": 10},
        "Scandinavia": {"territory_id": 12, "troop": "Cavalry", "troop_count": 5},
        "Southern Europe": {"territory_id": 13, "troop": "Artillery", "troop_count": 10},
        "Ukraine": {"territory_id": 14, "troop": "Cavalry", "troop_count": 5},
        "Western Europe": {"territory_id": 15, "troop": "Artillery", "troop_count": 10},
        "Afghanistan": {"territory_id": 16, "troop": "Cavalry", "troop_count": 5},
        "China": {"territory_id": 17, "troop": "Infantry", "troop_count": 1},
        "India": {"territory_id": 18, "troop": "Cavalry", "troop_count": 5},
        "Irkutsk": {"territory_id": 19, "troop": "Cavalry", "troop_count": 5},
        "Japan": {"territory_id": 20, "troop": "Artillery", "troop_count": 10},
        "Kamchatka": {"territory_id": 21, "troop": "Infantry", "troop_count": 1},
        "Middle East": {"territory_id": 22, "troop": "Infantry", "troop_count": 1},
        "Mongolia": {"territory_id": 23, "troop": "Infantry", "troop_count": 1},
        "Siam": {"territory_id": 24, "troop": "Infantry", "troop_count": 1},
        "Siberia": {"territory_id": 25, "troop": "Cavalry", "troop_count": 5},
        "Ural": {"territory_id": 26, "troop": "Cavalry", "troop_count": 5},
        "Yakutsk": {"territory_id": 27, "troop": "Cavalry", "troop_count": 5},
        "Argentina": {"territory_id": 28, "troop": "Infantry", "troop_count": 1},
        "Brazil": {"territory_id": 29, "troop": "Artillery", "troop_count": 10},
        "Venezuela": {"territory_id": 30, "troop": "Infantry", "troop_count": 1},
        "Peru": {"territory_id": 31, "troop": "Infantry", "troop_count": 1},
        "Congo": {"territory_id": 32, "troop": "Infantry", "troop_count": 1},
        "East Africa": {"territory_id": 33, "troop": "Infantry", "troop_count": 1},
        "Egypt": {"territory_id": 34, "troop": "Infantry", "troop_count": 1},
        "Madagascar": {"territory_id": 35, "troop": "Cavalry", "troop_count": 5},
        "North Africa": {"territory_id": 36, "troop": "Cavalry", "troop_count": 5},
        "South Africa": {"territory_id": 37, "troop": "Artillery", "troop_count": 10},
        "Eastern Australia": {"territory_id": 38, "troop": "Artillery", "troop_count": 10},
        "New Guinea": {"territory_id": 39, "troop": "Infantry", "troop_count": 1},
        "Indonesia": {"territory_id": 40, "troop": "Artillery", "troop_count": 10},
        "Western Australia": {"territory_id": 41, "troop": "Artillery", "troop_count": 10},
        "Wildcard": {"territory_id": None, "troop": None, "troop_count": None},
        "Wildcard": {"territory_id": None, "troop": None, "troop_count": None}
    }

    return Deck(territory_cards)
    
    
    









