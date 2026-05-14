"""
Semantic mapping for YAMNet classes to canonical CC labels.
Groups 521 specific classes into ~20 stable categories.
"""

# Map of YAMNet Display Names → Canonical CC Labels.
# Keys must match the 'display_name' field from YAMNet's class map CSV exactly.
LABEL_GROUPS = {
    # --- Impacts & Explosions ---
    "Explosion": "[Gunshot/Explosion]",
    "Gunshot, gunfire": "[Gunshot/Explosion]",
    "Machine gun": "[Gunshot/Explosion]",
    "Fusillade": "[Gunshot/Explosion]",
    "Firecracker": "[Gunshot/Explosion]",
    "Fireworks": "[Gunshot/Explosion]",
    "Artillery fire": "[Gunshot/Explosion]",
    "Cap gun": "[Gunshot/Explosion]",
    "Burst, pop": "[Impact/Pop]",
    "Boom": "[Impact/Pop]",
    "Thud": "[Impact/Pop]",
    "Slam": "[Impact/Pop]",
    "Hammer": "[Metallic Impact]",
    "Clang": "[Metallic Impact]",
    "Clatter": "[Metallic Impact]",
    "Dishes, pots, and pans": "[Metallic Impact]",
    "Cutlery, silverware": "[Metallic Impact]",
    "Glass": "[Glass Breaking]",
    "Shatter": "[Glass Breaking]",
    "Breaking": "[Glass Breaking]",
    "Chink and clink": "[Glass Breaking]",
    "Ding-dong": "[Bell/Chime]",
    "Bell": "[Bell/Chime]",
    "Church bell": "[Bell/Chime]",
    "Cowbell": "[Bell/Chime]",

    # --- Vehicles & Mechanical ---
    "Motor vehicle (road)": "[Vehicle]",
    "Car": "[Vehicle]",
    "Truck": "[Vehicle]",
    "Bus": "[Vehicle]",
    "Engine": "[Vehicle]",
    "Motorcycle": "[Vehicle]",
    "Race car, auto racing": "[Vehicle]",
    "Car alarm": "[Car Alarm]",
    "Horn": "[Horn/Honking]",
    "Car passing by": "[Vehicle]",
    "Vehicle horn, car horn, honking": "[Horn/Honking]",
    "Bicycle": "[Mechanical]",
    "Skateboard": "[Mechanical]",
    "Tools": "[Mechanical]",
    "Drill": "[Mechanical]",
    "Chainsaw": "[Mechanical]",
    "Power tool": "[Mechanical]",

    # --- Nature ---
    "Rain": "[Rain]",
    "Raindrop": "[Rain]",
    "Heavy rain": "[Rain]",
    "Wind": "[Wind]",
    "Rustling leaves": "[Wind]",
    "Thunderstorm": "[Thunder]",
    "Thunder": "[Thunder]",
    "Lightning": "[Thunder]",
    "Ocean": "[Water/Ocean]",
    "Water": "[Water/Ocean]",
    "Stream": "[Water/Ocean]",
    "Waterfall": "[Water/Ocean]",
    "Fire": "[Fire]",
    "Crackle": "[Fire]",

    # --- Animals ---
    "Dog": "[Animal Sound]",
    "Bark": "[Animal Sound]",
    "Howl": "[Animal Sound]",
    "Growling": "[Animal Sound]",
    "Cat": "[Animal Sound]",
    "Meow": "[Animal Sound]",
    "Purr": "[Animal Sound]",
    "Caterwaul": "[Animal Sound]",
    "Roar": "[Animal Sound]",
    "Animal": "[Animal Sound]",
    "Bird": "[Bird Sound]",
    "Crow": "[Bird Sound]",
    "Chirp, tweet": "[Bird Sound]",
    "Birdsong": "[Bird Sound]",
    "Squawk": "[Bird Sound]",
    # Snake / reptile sounds — this was the missing category
    "Hiss": "[Snake/Hiss]",
    "Snake": "[Snake/Hiss]",
    "Rattle": "[Snake/Hiss]",
    "Rattlesnake": "[Snake/Hiss]",
    "Insect": "[Insect Sound]",
    "Cricket": "[Insect Sound]",
    "Mosquito": "[Insect Sound]",

    # --- Human Non-Speech ---
    "Crowd": "[Crowd]",
    "Cheering": "[Crowd]",
    "Applause": "[Applause]",
    "Clapping": "[Applause]",
    "Laughter": "[Laughter]",
    "Chuckle, chortle": "[Laughter]",
    "Giggle": "[Laughter]",
    "Crying, sobbing": "[Crying]",
    "Whimper": "[Crying]",
    "Screaming": "[Scream]",
    "Shout": "[Shout]",
    "Whistling": "[Whistle]",
    "Walk, footsteps": "[Footsteps]",
    "Run": "[Footsteps]",
    "Gasp": "[Gasp]",
    "Groan": "[Groan]",
    "Snoring": "[Snoring]",
    "Cough": "[Cough]",
    "Sneeze": "[Sneeze]",

    # --- Emergency ---
    "Siren": "[Siren]",
    "Emergency vehicle": "[Siren]",
    "Police car (siren)": "[Siren]",
    "Ambulance (siren)": "[Siren]",
    "Fire engine, fire truck (siren)": "[Siren]",
    "Alarm": "[Alarm]",
    "Smoke detector, smoke alarm": "[Alarm]",
    "Beeping": "[Alarm]",

    # --- Music ---
    "Music": "[Music]",
    "Musical instrument": "[Music]",
    "Singing": "[Music]",
    "Drum": "[Music]",
    "Guitar": "[Music]",
    "Piano": "[Music]",
}

# Classes not in LABEL_GROUPS collapse to this — prevents raw YAMNet labels
# (like 'Inside, small room') from inflating group scores and beating real events.
DEFAULT_GROUP = "_ambient_"

# Internal: classes that are ambient/background and should be ignored entirely
_IGNORE_GROUPS = {"_ambient_"}

def get_canonical_label(yamnet_label: str) -> str:
    """Map a raw YAMNet display_name to a canonical CC label.
    Returns DEFAULT_GROUP for unmapped ambient classes.
    """
    return LABEL_GROUPS.get(yamnet_label, DEFAULT_GROUP)
