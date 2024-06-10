import random

class Territory:
    def __init__(self,
                 territory_name,
                 continent,
                 owner,
                 num_troops):
        self.TERRITORY_NAME = territory_name
        self.CONTINENT      = continent
        self.OWNER          = owner
        self.NUM_TROOPS     = num_troops

def init_map(players):
    # Randomly allocate players territories
    territories = [i for i in range(NUM_TERRITORIES)]
    random.shuffle(territories)

    for i, territory in enumerate(territories):
        players[i % 5] = 

    # Yellow Continent
    ALASKA                = Territory("Alaska", "Yellow")
    NORTHWEST_TERRITORY   = Territory("Northwest Territory", "Yellow")
    ALBERTA               = Territory("Alberta", "Yellow")
    GREENLAND             = Territory("Greenland", "Yellow")
    ONTARIO               = Territory("Ontario", "Yellow")
    QUEBEC                = Territory("Quebec", "Yellow")
    WESTERN_UNITED_STATES = Territory("Western United States", "Yellow")
    EASTERN_UNITED_STATES = Territory("Eastern United States", "Yellow")
    CENTRAL_AMERICA       = Territory("Central America", "Yellow")

    # Choose list/set
    return {
        ALASKA: 
            (
                NORTHWEST_TERRITORY,
                ALBERTA,
            ),
        NORTHWEST_TERRITORY:
            (
                ALASKA,
                ALBERTA,
                GREENLAND,
                ONTARIO
            ),
        ALBERTA:
            [
                ALASKA,
                NORTHWEST_TERRITORY,
                ONTARIO,
                WESTERN_UNITED_STATES
            ],
        GREENLAND:
            [
                NORTHWEST_TERRITORY,
                ONTARIO,
                QUEBEC
            ],
        ONTARIO:
            [
                NORTHWEST_TERRITORY,
                ALBERTA,
                QUEBEC,
                GREENLAND,
                WESTERN_UNITED_STATES,
                EASTERN_UNITED_STATES
            ],
        QUEBEC:
            [
                GREENLAND,
                ONTARIO,
                EASTERN_UNITED_STATES
            ],
        WESTERN_UNITED_STATES:
            [
                ALBERTA,
                ONTARIO,
                EASTERN_UNITED_STATES,
                CENTRAL_AMERICA
            ],
        EASTERN_UNITED_STATES:
            [
                ONTARIO,
                QUEBEC,
                CENTRAL_AMERICA
            ],
        CENTRAL_AMERICA:
            [
                WESTERN_UNITED_STATES,
                EASTERN_UNITED_STATES
            ]
    }