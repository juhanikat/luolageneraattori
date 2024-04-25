"""Constants that are used by other modules."""


# Default arguments used for generating the dungeon.
DEFAULT_ARGS = {
    "room_min_size": "2",
    "room_max_size": "4",
    "room_exact_size": "0",
    "map_size_x": "50",
    "map_size_y": "50"
}

# Weights given to different types of cells on the map.
ROOM_WEIGHT = 3
PATH_WEIGHT = 0.5
EMPTY_WEIGHT = 1

# Maximum values that the ui accepts.
MAX_MAP_SIZE_X = 500
MAX_MAP_SIZE_Y = 500
MAX_AMOUNT_OF_ROOMS = 200
