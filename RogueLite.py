import tkinter as tk
import random
import json
import os

# Save file path
# SAVE_FILE = "C:/Users/Nick/Documents/VSCode_Files/RogueLite/game_state.json"
SAVE_FILE = "C:/Users/Nick/OneDrive/Desktop/Share/RogueLite/game_state.json"

# Constants
TIME = 0
CHAMBERS = [None] * 51
ENVIRONMENTS = ["Arctic", "Coastal", "Desert", "Forest", 
                "Grassland", "Hill", "Mountain", "Swamp", 
                "Underdark", "Underwater", "Urban"]
SAFE_PERC = {"Arctic": 4, "Coastal": 8, "Desert": 4, "Forest": 7, 
             "Grassland": 8, "Hill": 9, "Mountain": 6, "Swamp": 6, 
             "Underdark": 2, "Underwater": 0, "Urban": 10}
LIGHT_PERC = {"Arctic": [10, 25, 100], "Coastal": [34, 67, 100], "Desert": [75, 90, 100], 
              "Forest": [25, 75, 100], "Grassland": [34, 67, 100], "Hill": [34, 67, 100], 
              "Mountain": [34, 67, 100], "Swamp": [25, 75, 100], "Underdark": [0, 10, 100], 
              "Underwater": [34, 67, 100], "Urban": [34, 67, 100]}
MBOSS = {"Arctic": "Glacier Golem", "Coastal": "Tidal Mauler", "Desert": "Sandstrider Behemoth", "Forest": "The Bramblefang", 
         "Grassland": "Bladed Hopper", "Hill": "NEED THIS", "Mountain": "Thunderwing", "Swamp": "Rotmaw Gator", 
         "Underdark": "The Arcane Shard", "Underwater": "Thundercoil", "Urban": "The Jester"}
BOSS = {"Arctic": "Vastilda, Iceweaver Matron", "Coastal": "Captain Marrowgrip, Warden of Cursed Waters", "Desert": "Vozhir, the Cursed Jackal", "Forest": "Thyrvek, the Forest's Eye", 
        "Grassland": "Gravehorn, Hollow Alpha", "Hill": "NEED THIS", "Mountain": "Gulgrom, the Earthshaker", "Swamp": "Malzith, the Witch-Tyrant", 
        "Underdark": "Ozrith, the Consuming", "Underwater": "Shockmother, Queen of Currents", "Urban": "Raelix, Archblade Sentinel"}
ARCTIC_ENCOUNTERS = {"Easy": ["1 Shadow Demon - MM", "1 Banshee - BR", "1 Warlock of the Archfey - MOTM + 2 Blood Hawks - BR", "1 Yeti - BR", "1 Manticore - BR", 
                              "1 Winter Wolf - BR", "1 Saber-Toothed Tiger - BR", "1 White Dragon Wyrmling - BR", "1 White Guard Drake - MOTM", "2 Saber-Toothed Tigers - BR", 
                              "1 Griffon - BR + 1d4 Blood Hawks - BR", "1 Polar Bear - BR", "1d3 Brown Bears - BR", "1 Ogre Zombie - BR", "1d4+1 Ice Mephits - BR", 
                              "1d4 Owls - BR", "1 Giant Owl - BR", "2d4 Gnoll Witherlings - MOTM", "2 Gnoll Flesh Gnawers - MOTM + 1 Gnoll Hunter - MOTM", "1d4+1 Gnoll Hunters - MOTM"], 
                     "Medium": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], 
                     "Hard": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]}
COASTAL_ENCOUNTERS = {"Easy": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], 
                      "Medium": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], 
                      "Hard": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]}
DESERT_ENCOUNTERS = {"Easy": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], 
                     "Medium": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], 
                     "Hard": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]}
FOREST_ENCOUNTERS = {"Easy": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], 
                     "Medium": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], 
                     "Hard": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]}
GRASSLAND_ENCOUNTERS = {"Easy": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], 
                        "Medium": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], 
                        "Hard": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]}
HILL_ENCOUNTERS = {"Easy": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], 
                   "Medium": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], 
                   "Hard": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]}
MOUNTAIN_ENCOUNTERS = {"Easy": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], 
                       "Medium": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], 
                       "Hard": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]}
SWAMP_ENCOUNTERS = {"Easy": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], 
                    "Medium": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], 
                    "Hard": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]}
UNDERDARK_ENCOUNTERS = {"Easy": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], 
                        "Medium": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], 
                        "Hard": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]}
UNDERWATER_ENCOUNTERS = {"Easy": ["3d8 Quippers - BR", "Deep Scion - MOTM", "Killer Whale - BR", "1 Black Dragon Wyrmling - BR + 1 Swarm of Quippers - BR", "2 Deep Dragon Wyrmlings - FTOD", 
                                  "1 Sahuagin - BR + 1 Sahuagin Priestess - BR", "1 Merrow - BR + 1 Reef Shark - BR", "1d4+1 Sahuagin - BR", "1 Hunter Shark - BR", "1d4+1 Reef Sharks - BR", 
                                  "1 Plesiosaurus - BR", "2 Giant Octopuses - BR", "2 Sea Spawn - MOTM", "2 Swarms of Quippers - BR", "2d4 Giant Sea Horses - BR", 
                                  "1d4+4 Steam Mephits - BR", "1d4+2 Merfolk - BR + 2 Reef Sharks - BR", "1 Hunter Shark - BR + 1d4 Quippers - BR", "Dragon Turtle Wyrmling - FTOD", "2 Sea Hags - MM"], 
                         "Medium": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], 
                         "Hard": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]}
URBAN_ENCOUNTERS = {"Easy": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], 
                    "Medium": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], 
                    "Hard": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]}
ENCOUNTERS = {"Arctic": ARCTIC_ENCOUNTERS, "Coastal": COASTAL_ENCOUNTERS, "Desert": DESERT_ENCOUNTERS, 
              "Forest": FOREST_ENCOUNTERS, "Grassland": GRASSLAND_ENCOUNTERS, "Hill": HILL_ENCOUNTERS, 
              "Mountain": MOUNTAIN_ENCOUNTERS, "Swamp": SWAMP_ENCOUNTERS, "Underdark": UNDERDARK_ENCOUNTERS, 
              "Underwater": UNDERWATER_ENCOUNTERS, "Urban": URBAN_ENCOUNTERS}

# Randomize dungeon
def randomize_dungeon():
    global CHAMBERS, TIME
    TIME = 0 # Reset time
    CHAMBERS = [None] * 51 # Reset the dungeon

    CHAMBERS[0] = {"number": 0, "name": "Start", "difficulty": "None", 
                   "environment": "None", "effects": ["None"], "safe": "Yes",
                   "light": "Bright Light", "layout": 1, "enemies": ["None"], "loot": ["None"], "hours": 0}
    
    name = ""
    difficulty = ""
    environment = ""
    effects = []
    safe = ""
    light = ""
    layout = 0
    enemies = ""
    loot = []

    # Counters
    mBossCount = 1
    bossCount = 1

    for i in range(50):
        # Chamber Name
        if i == 49:
            name = "Final Boss"
        elif mBossCount != 5 and bossCount != 10:
            name = "Chamber"
        elif mBossCount == 5 and bossCount != 10:
            name = "Mini Boss"
            mBossCount = 0
        else:
            name = "Boss"
            mBossCount = 0
            bossCount = 0

        # Chamber Difficulty
        if i < 10: difficulty = "Easy"
        elif i < 40: difficulty = "Medium"
        else: difficulty = "Hard"
        
        # Update environment after every 5 chambers
        if i % 5 == 0:
            environment = generate_environment()
            if environment == "Coastal": hours = random.randint(1,4) + 1 # Salt Air Effect
            else: hours = 0 # All other environments

        # Light Level
        light = lightLevel(environment)

        # Environmental Effects
        effects = env_effects(difficulty, environment, light)
        
        # Safe Chamber
        safe = isSafe(name, environment)

        # Select Chamber Layout
        if i != 49: layout = random.randint(1,5)
        else: layout = 1

        # Enemies
        enemies = generate_enemies(name, difficulty, environment)

        # Update Chamber
        CHAMBERS[i+1] = {"number": i+1, "name": name, "difficulty": difficulty, 
                         "environment": environment, "effects": effects, "safe": safe, 
                         "light": light, "layout": layout, "enemies": enemies, "loot": loot, "hours": hours}

        # Increment Counters
        mBossCount = mBossCount + 1
        bossCount = bossCount + 1

# Generate Environment
def generate_environment():
    environment = random.choice(ENVIRONMENTS)
    return environment

# Update Environmental Effects
def env_effects(difficulty, environment, light):
    percRoll = random.randint(1,100)
    effects = []
    dif = 0
    if environment == "Arctic": # Arctic effects
        if difficulty == "Easy": dif = 10
        elif difficulty == "Medium": dif = 12
        else: dif = 14
        effects.append("Frozen Wounds: Cold-based attacks deal an additional 1d6 cold damage. All healing is halved.")
        icy_ground = "Icy Ground: Movement speed is reduced by 10 feet. Creatures must succeed on a DC " + str(dif) + " Dexterity saving throw at the start of their turn or fall prone."
        effects.append(icy_ground)
        if percRoll <= 70: effects.append("Whiteout Conditions: Visibility is reduced to 30 feet due to heavy snow. Ranged attacks beyond this range have disadvantage.")
    elif environment == "Coastal": # Coastal effects
        if percRoll <= 60: effects.append("Fog of the Sea: A thick fog reduces visibility to 15 feet, imposing disadvantage on Wisdom (Perception) checks and ranged attacks.")
    elif environment == "Desert": # Desert effects
        effects.append("Scorching Heat: Fire spells deal an extra 1d6 fire damage. All cold-based spells have a 50% chance to fail.")
        effects.append("Shifting Sands: The sands shift unpredictably, making it difficult to maintain balance. At the start of their turn, creatures must succeed on a DC 13 Dexterity saving throw or have their movement speed halved until the start of their next turn. Additionally, creatures have disadvantage on Dexterity (Acrobatics) checks.")
        if percRoll <= 65: effects.append("Sandstorm: A sandstorm reduces visibility to 10 feet, imposing disadvantage on all attack rolls and Wisdom (Perception) checks. Ranged attacks beyond 10 feet automatically miss.")
    elif environment == "Forest": # Forest effects
        effects.append("Living Forest: The forest is alive, causing plants to move slightly. Any creature that doesn't move at least 10 feet on its turn must make a DC 15 Dexterity saving throw or be restrained by roots or vines. As an action, a creature can escape on a DC 13 Strength (Athletics) check.")
        if light == "Bright Light": effects.append("Dappled Light: Sunlight filtered through leaves causes shifting shadows, providing half cover to all creatures (+2 to AC and Dexterity saving throws).")
        effects.append("Pollen Clouds: The forest is filled with dense clouds of pollen, lightly obscuring the area.")
    elif environment == "Grassland": # Grassland effects
        effects.append("Tall Grass: The grass provides heavy concealment. Creatures that move through it have advantage on Dexterity (Stealth) checks, but disadvantage on Wisdom (Perception) checks.")
        if percRoll <= 40: effects.append("Lightning Storms: A lightning storm erupts. Each creature must succeed on a DC 14 Dexterity saving throw or take 2d6 lightning damage.")
        effects.append("Wildfires: If a fire spell is cast, a 5 foot wildfire ignites within 5 feet of the impact point in an unoccupied space. Wildfires spread 5 feet outward in all directions each turn at initiative count 20. Any creature starting its turn within 5 feet of wildfires takes 1d6 fire damage. Any fires in the grassland cause the area to fill with smoke, heavily obscuring the area around the fire (within 5 feet) and blinding all creatures within the smoke.")
    elif environment == "Hill": # Hill effects
        effects.append("Thunderous Echoes: The sound of thunder is amplified by the terrain. Whenever a loud noice occurs (such as a thunder spell or a weapon clash), all creatures within 60 feet must make a DC 13 Constitution saving throw or take 1d8 thunder damage and be deafended for 1d4 rounds. Deafened creatures are immune to this effect.")
        effects.append("Rocky Outcrops: The hills are dotted with jagged rocks that make combat treacherous. Any creature that moves at least 10 feet on a hill must make a DC 12 Dexterity saving throw or slip and take 1d4 piercing damage from the sharp rocks.")
        effects.append("Steep Inclines: Ascending steep slopes requires extra effort. Moving uphill costs double movement, and creatures must make a DC 12 Strength (Athletics) check or be unable to move more than 10 feet uphill during their turn.")
    elif environment == "Mountain": # Mountain effects
        effects.append("Treacherous Cliffs: Climbing checks in this area are made with disadvantage unless proper equipment is used.")
        effects.append("Avalanche: Loud noises or heavy impacts (thunder, or similar noise) may trigger an avalanche, 20% chance. Creatures must succeed on a DC 15 Dexterity saving throw to avoid 4d6 bludgeoning damage and be buried (restrained, DC 15 Strength (Athletics) check to escape).")
    elif environment == "Swamp": # Swamp effects
        effects.append("Rotting Air: The swamp air is filled with the smell of decay. All creatures have disadvantage on Constitution saving throws to resist disease or poison.")
        effects.append("Insect Swarm: Swarms of biting insects harass characters, giving them disadvantage on concentration checks and on attack rolls.")
    elif environment == "Underdark": # Underdark effects
        effects.append("Bioluminescent Glow: Fungi and minerals emit a dim, eerie light. This providees dim light in a 30 foot radius, providing disadvantage on Dexterity (Stealth) checks and advantage on Wisdom (Perception) checks relying on sight.")
    elif environment == "Underwater": # Underwater effects
        effects.append("Dark Abyss: The deep waters (below 20 feet) are pitch black. Light spells provide only half their normal illumination, and all non-magical light sources are extinguished. Creatures without darkvision are blinded.")
        effects.append("Electrified Currents: The water occasionally becomes charged with electrical energy. At the end of each round, there's a 20% chance that an electrified current surges through the area. All creatures in the water must succeed on a DC 13 Constitution saving throw or take 2d6 lightning damage and be stunned until the start of their next turn.")
        effects.append("Tangled Kelp: Dense kelp forests create natural hazards. Moving through these areas requires a DC 13 Strength (Athletics) check, and creatures that fail are restrained until they succeed on the same check at the end of their turn.")
    else: # Urban effects
        effects.append("Collapsing Floors: The old dungeon floors are unstable. Each time a creature moves more than 10 feet, there's a 10% chance the floor gives way beneath them. The creature must succeed on a DC 14 Dexterity saving throw or fall 20 feet, taking 2d6 bludgeoning damage.")
        effects.append("Arcane Residue: The dungeon is laced with residual magical energy from past spells. Creatures must succeed on a DC 15 Intelligence (Arcana) check when casting a spell or have the spell misfire, causing a random effect chosen by the DM (such as targeting a random creature or creating a wild magic surge).")
    return effects

# Check for safety
def isSafe(name, environment):
    safe = "No"
    safeRoll = random.randint(1,100)
    if name == "Chamber" and safeRoll <= SAFE_PERC.get(environment):
        safe = "Yes"
    return safe

# Find Light Level
def lightLevel(environment):
    light = ""
    lightRoll = random.randint(1,100)
    if lightRoll <= LIGHT_PERC.get(environment)[0]:
        light = "Bright Light"
    elif lightRoll <= LIGHT_PERC.get(environment)[1]:
        light = "Dim Light"
    else:
        light = "Darkness"
    return light

# Generate Enemies
def generate_enemies(name, difficulty, environment):
    result = ""
    if name == "Mini Boss": result = MBOSS.get(environment)
    elif name == "Boss": result = BOSS.get(environment)
    elif name == "Final Boss": result = "Xanathar"
    else:
        encounterRoll = random.randint(0,19)
        result = ENCOUNTERS.get(environment).get(difficulty)[encounterRoll]
    return result
####################### Button Commands #######################

####################### LOAD AND SAVE GAME #######################
# Load game state
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r") as file:
        game_state = json.load(file)
        CHAMBERS = game_state["chambers"]  # Restore dungeon layout
        TIME = game_state["time"]  # Restore time
else:
    randomize_dungeon()
    game_state = {"current_chamber": CHAMBERS[0], "chambers": CHAMBERS, "time": TIME}

# Save game state function
def save_game_state():
    game_state["chambers"] = CHAMBERS  # Store current dungeon
    game_state["time"] = TIME # Store current time
    with open(SAVE_FILE, "w") as file:
        json.dump(game_state, file, indent=4)
##################################################################

# Get chamber hours
def getHours(chamber):
    return chamber.get("hours")

# Set chamber hours
def setHours(chamber, hours):
    chamber["hours"] = hours

# Advance time an hour
def advance_time(current):
    global TIME
    TIME = current + 1

    roll = random.randint(1,100)
    dif = 0

    chamber = game_state["current_chamber"]
    environment = chamber.get("environment")
    difficulty = chamber.get("difficulty")
    number = chamber.get("number")

    hours = getHours(chamber) - 1
    setHours(chamber, hours)

    # Update future chambers in environment region of 5
    future_chambers = 0
    newNumber = number
    while newNumber % 5 != 0: # Find number of chambers left in the 5
        future_chambers = future_chambers + 1
        newNumber = newNumber + 1
    if future_chambers > 0: # Check if there are future chambers in the 5
        for i in range(future_chambers): # Update hours for each future chamber found
            chamber = CHAMBERS[number + i + 1]
            setHours(chamber, hours)

    # Environmental time-based effects
    if environment == "Coastal":
        if roll <= 20: 
            if difficulty == "Easy": dif = 1
            elif difficulty == "Medium": dif = 2
            else: dif = 4
            random_event("Tidal Surge: Creatures must succeed on a DC 14 Strength saving throw or be pushed 10 feet in a random direction and take " + str(dif) + "d4 bludgeoning damage.")
        if hours == 0:
            random_event("Salt Air: All non-magical metal equipment corrodes slowly. Such equipment gains a -1 penalty to attack and damage rolls, or AC.")
    elif environment == "Desert":
        if difficulty == "Easy": dif = 4
        elif difficulty == "Medium": dif = 6
        else: dif = 8
        random_event("Scorching Heat: Creatures without fire resistance/immunity take 1d" + str(dif) + " fire damage.")
    elif environment == "Forest": random_event("Pollen Clouds: All creatures must make a DC 13 Constitution saving throw or be poisoned for 1 hour.")
    elif environment == "Grassland":
        if roll <= 20: random_event("Wildfires: A wildfire ignites in an unoccupied space of the DM's choice.")
    elif environment == "Mountain":
        random_event("Thin Air: After 1 hour of strenuous activity, creatures must succeed on a DC 12 Constitution saving throw or gain one level of exhaustion due to the lack of oxygen. Mountain Dwarves are immune.")
    elif environment == "Swamp":
        six_roll = random.randint(1,6)
        if six_roll > 4: random_event("Sinking Ground: The ground in a 10 foot radius around a random creature becomes quicksand. Creatures must succeed on a DC 15 Strength check to escape or be restrained.")
    elif environment == "Underdark":
        if roll <= 20: random_event("Cave In: Creatures within a 20 foot radius must make a DC 14 Dexterity saving throw or take 2d6 bludgeoning damage and be restrained under debris (escape DC 15 Strength (Athletics)).")
        random_event("Toxic Air: The air is filled with toxic spores and gases. All creatures must succeed on a DC 14 Constitution saving throw or gain one level of exhaustion. Creatures immune to poison are immune to this effect.")
    elif environment == "Urban":
        if roll <= 25: random_event("Rat Swarms: The dungeon is infested with aggressive rat swarms. A rat swarm emerges from the walls or floors, attacking the nearest creature. Use the stats for a swarm of rats in the Monster Manual for this swarm.")

# Load next chamber
def next_chamber():
    if game_state["current_chamber"].get("number") != 50:
        nextNum = game_state["current_chamber"].get("number") + 1
    else:
        nextNum = 0
        randomize_dungeon()
    print(CHAMBERS[nextNum]) ################################################### TESTING
    game_state["current_chamber"] = CHAMBERS[nextNum]
    update_ui()
    if (game_state["current_chamber"].get("name") in ("Mini Boss", "Boss", "Final Boss")):
        advance_time(TIME) # Advance an hour when entering any boss chamber
    save_game_state()

# Rests
def short_rest():
    chamber = game_state["current_chamber"]
    isChamber = chamber.get("name") == "Chamber"
    notSafe = chamber.get("safe") == "No"
    difficulty = chamber.get("difficulty")
    environment = chamber.get("environment")
    roll = random.randint(1,20)

    advance_time(TIME)
    
    if isChamber and notSafe and roll >= 15: random_encounter(difficulty, environment) # Random encounter

def long_rest():
    chamber = game_state["current_chamber"]
    isChamber = chamber.get("name") == "Chamber"
    notSafe = chamber.get("safe") == "No"
    difficulty = chamber.get("difficulty")
    environment = chamber.get("environment")
    rolls = []

    for i in range(8):
        rolls.append(random.randint(1,20))

        advance_time(TIME)

    if isChamber and notSafe:
        for roll in rolls:
            if roll >= 15:
                random_encounter(difficulty, environment) # Random encounter
                break # Only once per rest attempt
###############################################################

# Function to create a random encounter
def random_encounter(difficulty, environment):
    popup = tk.Toplevel(root)
    popup.title("Random Encounter")
    popup.geometry("960x540")  # Set size of the popup
    
    encounterRoll = random.randint(0,19)
    encounter = ENCOUNTERS.get(environment).get(difficulty)[encounterRoll]

    label = tk.Label(popup, text=encounter, wraplength=1000, font=("Arial", 14))
    label.pack(pady=20)
    
    close_button = tk.Button(popup, text="Close", command=popup.destroy)
    close_button.pack()

# Function to create a random event
def random_event(event):
    popup = tk.Toplevel(root)
    popup.title("Random Event")
    popup.geometry("960x540")  # Set size of the popup

    label = tk.Label(popup, text=event, wraplength=1000, font=("Arial", 14))
    label.pack(pady=20)
    
    close_button = tk.Button(popup, text="Close", command=popup.destroy)
    close_button.pack()

####################### GUI #######################
# Update UI
def update_ui():
    chamber = game_state["current_chamber"]
    chamber_info.set(f"Number: {chamber['number']}\nChamber: {chamber['name']}\nDifficulty: {chamber['difficulty']}\nEnvironment: {chamber['environment']}\nEffects: \n\t{'\n\t'.join(chamber['effects'])}\nSafe: {chamber['safe']}\nLight: {chamber['light']}\nLayout: {chamber['layout']}\nEnemies: {chamber['enemies']}\nLoot: {', '.join(chamber['loot'])}")

# Initialize GUI
root = tk.Tk()
root.title("Rogue-lite D&D Campaign Manager")
root.geometry("960x540")  # Increased window size

# Display chamber info
chamber_info = tk.StringVar()
update_ui()
label = tk.Label(root, textvariable=chamber_info, wraplength=1000, justify="left", padx=10, pady=10)
label.pack()

# Button to generate next chamber
btn_generate = tk.Button(root, text="Generate Next Chamber", command=next_chamber)
btn_generate.pack(pady=20)

# Button to advance time
btn_short = tk.Button(root, text="Advance Time", command=advance_time(TIME))
btn_short.pack()

# Button to short rest
btn_short = tk.Button(root, text="Short Rest", command=short_rest)
btn_short.pack()

# Button to long rest
btn_long = tk.Button(root, text="Long Rest", command=long_rest)
btn_long.pack()

# Button to save
btn_long = tk.Button(root, text="Save", command=save_game_state)
btn_long.pack(pady=10)

# Run application
root.mainloop()
