import tkinter as tk
import random
import json
import os

# Save file path
SAVE_FILE = "C:/Users/Nick/Documents/GitHub/RogueLite/game_state.json"
# SAVE_FILE = "C:/Users/Nick/OneDrive/Desktop/Share/RogueLite/RogueLite/game_state.json"

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
         "Grassland": "Bladed Hopper", "Hill": "Boulderback Roach", "Mountain": "Thunderwing", "Swamp": "Rotmaw Gator", 
         "Underdark": "The Arcane Shard", "Underwater": "Thundercoil", "Urban": "The Jester"}
BOSS = {"Arctic": "Vastilda, Iceweaver Matron", "Coastal": "Captain Marrowgrip, Warden of Cursed Waters", "Desert": "Vozhir, the Cursed Jackal", "Forest": "Thyrvek, the Forest's Eye", 
        "Grassland": "Gravehorn, Hollow Alpha", "Hill": "Grumgul, the Stone Maw", "Mountain": "Gulgrom, the Earthshaker", "Swamp": "Malzith, the Witch-Tyrant", 
        "Underdark": "Ozrith, the Consuming", "Underwater": "Shockmother, Queen of Currents", "Urban": "Raelix, Archblade Sentinel"}
ARCTIC_ENCOUNTERS = {"Easy": ["1 Shadow Demon - MM", "1 Banshee - BR", "1 Warlock of the Archfey - MOTM + 2 Blood Hawks - BR", "1 Yeti - BR", "1d2 Ogre - BR", 
                              "1 Winter Wolf - BR", "1 Saber-Toothed Tiger - BR", "1 White Dragon Wyrmling - BR", "1 White Guard Drake - MOTM", "2 Saber-Toothed Tigers - BR", 
                              "1 Griffon - BR + 1d4 Blood Hawks - BR", "1 Polar Bear - BR", "1d3 Brown Bears - BR", "1 Ogre Zombie - BR", "1d4+1 Ice Mephits - BR", 
                              "1d4 Owls - BR", "1 Giant Owl - BR", "2d4 Gnoll Witherlings - MOTM", "2 Gnoll Flesh Gnawers - MOTM + 1 Gnoll Hunter - MOTM", "1d4+1 Gnoll Hunters - MOTM"], 
                     "Medium": ["1 Frost Giant - BR", "2 Revenants - BR", "1 Bheur Hag - MOTM + 1 White Guard Drake - MOTM", "1 Mammoth - BR + 1 Warlock of the Archfey - MOTM", "2 Young Remorhaz - MM", 
                                "1 Young White Dragon - BR + 1 White Dragon Wyrmling - BR", "1 Chasme - MM + 1d4+1 Gnoll Witherlings - MOTM", "2 Shadow Demons - MM + 1d4 Gnoll Hunters - MOTM", "2 Banshees - BR + 1 Ogre Zombie - BR", "2 Warlocks of the Archfey - MOTM + 1d4 Ice Mephits - BR", 
                                "3 Yetis - BR + 1 Saber-Toothed Tiger - BR", "3 Winter Wolves - BR + 3 Gnoll Hunters - MOTM", "1d4 Ogres - BR + 2 Polar Bears - BR", "1d4+2 Saber-Toothed Tigers - BR", "1d4+2 White Dragon Wyrmlings - BR", 
                                "1d4+2 Griffons - BR", "4 Ogre Zombies - BR + 1d4+2 Gnoll Witherlings - MOTM", "2d4+2 Gnoll Flesh Gnawers - MOTM", "3d4+2 Gnoll Hunters - MOTM", "2d6+2 Ice Mephits - BR"], 
                     "Hard": ["1 Winter Eladrin - MOTM", "1 Abominable Yeti - MM", "1 Frost Salamander - MOTM", "1 Frost Giant - BR + 1 Winter Wolf - BR", "1 Bheur Hag - MOTM + 1d4+1 Ice Mephits - BR", 
                              "2 Young White Dragons - BR", "2 Chasme - MM", "2 Mammoths - BR", "2 Young Remorhaz - MM", "2 Revenants - BR", 
                              "3 Shadow Demons - BR + 1d4 Gnoll Witherlings - MOTM", "3 Banshees - BR + 1d4 Gnoll Witherlings - MOTM", "3 Warlocks of the Archfey - MOTM + 1d2 Giant Owls - BR", "4 Yetis - BR + 1 Polar Bear - BR + 1 Brown Bear - BR", "4 Winter Wolves - BR + 2 Gnoll Hunters - MOTM", 
                              "1d4+2 Ogres - BR", "1d4+2 Saber-Toothed Tigers - BR", "1d4+2 White Dragon Wyrmlings - BR", "1d4+2 Griffons - BR", "1d4+2 Ogre Zombies - BR"]}
COASTAL_ENCOUNTERS = {"Easy": ["1 Draconian Dreadnought - FTOD", "1 Blue Dragon Wyrmling - BR", "1 Merrenoloth - BR", "1 Swashbuckler - MOTM", "1 Draconian Infiltrator - FTOD", 
                               "1 Dragonflesh Graftor - FTOD", "1 Manticore - BR", "1d4 Eagles - BR", "1d2 Giant Eagles - BR", "1 Quetzalcoatlus - MOTM", 
                               "3d4+2 Poisonous Snakes - BR", "2d4 Dretch - BR", "2d4 Dimetrodon - MOTM", "1 Draconian Mage - FTOD + 1 Draconian Foot Soldier - FTOD", "1d4+1 Draconian Foot Soldiers - FTOD", 
                               "1d2+1 Harpies - BR", "1d6 Giant Crabs - BR", "7d4 Crabs - BR", "1 Tortle Druid - MOTM + 2 Tortles - MOTM", "1d4+1 Tortles - MOTM"], 
                      "Medium": ["1 Cyclops - BR + 1d4+1 Tortles - MOTM", "1 Animated Breath (DM's Choice) - FTOD + 1 Draconian Mage - FTOD", "1 Draconian Mastermind - FTOD + 1d4 Draconian Foot Soldiers - FTOD", "1 Dragonflesh Abomination - FTOD + 1 Dragonflesh Graftor - FTOD", "1 Hezrou - BR", 
                                 "2 Dragonblood Oozes - FTOD", "2 Draconian Dreadnoughts - FTOD + 1 Draconian Mage - FTOD + 1d2 Dimetrodon - MOTM", "1 Vrock - BR + 1d4+1 Dretch - BR", "3 Blue Dragon Wyrmlings - BR + 1 Draconian Mage - FTOD + 1 Draconian Foot Soldier - FTOD", "3 Merrenoloth - MOTM + 1d4 Dretch - BR", 
                                 "3 Swashbucklers - MOTM + 3 Giant Eagles - BR", "3 Draconian Infiltrators - FTOD + 3 Draconian Foot Soldiers - FTOD", "3 Dragonflesh Graftors - FTOD + 1d4 Poisonous Snakes - BR", "3 Manticores - BR + 1d2+1 Harpies - BR", "1d4+2 Draconian Mages - FTOD", 
                                 "1d4+2 Tortle Druids - MOTM", "2d4+2 Harpies - BR", "3d4+2 Draconian Foot Soldiers - FTOD", "4d6+3 Dretch - BR", "3d8+3 Tortles - MOTM"], 
                      "Hard": ["1 Young Blue Dragon - BR", "1 Hydroloth - MOTM", "1 Hezrou - BR + 1 Dretch - BR", "2 Cyclops - BR", "2 Animated Breaths (DM's Choice) - FTOD", 
                               "2 Draconian Masterminds - FTOD", "2 Dragonflesh Abominations - FTOD", "2 Vrocks - BR", "2 Dragonblood Oozes - FTOD", "3 Draconain Dreadnoughts - FTOD + 1d2 Draconian Foot Soldiers - FTOD", 
                               "4 Blue Dragon Wyrmlings - BR + 1 Draconian Mage - FTOD + 1 Draconian Foot Soldier - FTOD", "4 Merrenoloths - MOTM + 1d4 Dretch - BR", "4 Swashbucklers - MOTM + 1 Quetzalcoatlus - MOTM + 1 Giant Eagle - BR", "4 Draconian Infiltrators - FTOD + 1 Draconian Mage - FTOD + 1 Draconian Foot Soldier - FTOD", "1d2+3 Dragonflesh Graftors - FTOD", 
                               "4 Manticores - BR + 1d4+1 Giant Crabs - BR", "1d4+2 Draconian Mages - FTOD + 2 Draconian Foot Soldiers - FTOD", "1d4+2 Tortle Druids - MM + 2 Tortles - MM", "2d6+6 Draconian Foot Soldiers - FTOD", "2d10+15 Dretch - BR"]}
DESERT_ENCOUNTERS = {"Easy": ["1 Dybbuk - MOTM", "1 Gnoll Fang of Yeenoghu - MM", "1 Lamia - BR", "1 Yuan-ti Mind Whisperer - MOTM", "1 Yuan-ti Nightmare Speaker - MOTM", 
                              "1 Giant Scorpion - BR", "7d4 Scorpions - BR", "1 Mummy - BR + 1 Vulture - BR", "1 Yuan-ti Malison - MM", "7d4 Vultures - BR", 
                              "1 Yuan-ti Broodguard - MOTM + 1 Yuan-ti Pureblood - MM", "1 Gnoll Pack Lord - MM + 1d2 Gnolls - BR", "1 Blue Guard Drake - MOTM", "1 Berbalang - MOTM + 1 Death Dog - BR", "1d2+1 Death Dogs - BR", 
                              "2 Giant Vultures - BR + 1d4 Vultures - BR", "1d2+1 Yuan-ti Purebloods - MM", "2d6+2 Camels - BR", "1d4+1 Gnolls - BR", "1d4+1 Dust Mephits - BR"], 
                     "Medium": ["2 Dust Devils - MOTM", "2 Fire Elementals - BR", "1 Medusa - BR + 1d4 Dust Mephits - BR", "2 Tlincalli - MOTM", "1 Yuan-Ti Abomination - MM", 
                                "2 Yuan-Ti Pit Masters - MOTM", "2 Spawns of Kyuss - MOTM", "1 Fire Elemental Myrmidon - MOTM + 1 Dust Mephit - BR", "2 Dybbuk - MOTM + 2 Death Dogs - BR", "2 Lamias - BR + 1d4 Dust Mephits - BR", 
                                "2 Gnoll Fangs of Yeenoghu - MM + 1d4 Gnolls - BR", "2 Yuan-Ti Whisperers - MOTM + 2 Yuan-Ti Purebloods - MM", "2 Yuan-Ti Nightmare Speakers - MOTM + 2 Yuan-Ti Purebloods - MM", "3 Yuan-Ti Malisons - MM + 3 Yuan-Ti Purebloods - MM", "3 Mummies - BR + 1d2+1 Dust Mephits - BR", 
                                "3 Giant Scorpions - BR + 1d4+3 Scorpions - BR", "1d4+2 Berbalangs - MOTM", "1d4+2 Yuan-Ti Broodguard - MOTM", "3 Gnoll Pack Lords - MM + 1d4+3 Gnolls - BR", "1d4+6 Death Dogs - BR"], 
                     "Hard": ["1 Summer Eladrin - MOTM", "1 Flind - MOTM", "1 Fire Elemental Myrmidon - MOTM + 1d2+3 Dust Mephits - BR", "1 Yuan-Ti Abomination - MM + 1 Yuan-Ti Nightmare Speaker - MOTM", "2 Medusas - BR", 
                              "1 Dust Devil - MOTM + 1d4+5 Dust Mephits - BR", "2 Fire Elementals - BR", "2 Tlincalli - MOTM", "1 Yuan-Ti Pit Master - MOTM + 1 Yuan-Ti Whisperer - MOTM + 2 Yuan-Ti Purebloods - MM", "2 Spawns of Kyuss - MOTM", 
                              "3 Dybbuks - MOTM + 1 Giant Vulture - BR", "3 Lamias - BR + 1d2 Dust Mephits - BR", "2 Gnoll Fangs of Yeenoghu - MM + 2 Gnoll Pack Lords - MM + 2 Gnolls - BR", "2 Yuan-Ti Whisperers - MOTM + 1 Yuan-Ti Broodguard - MOTM + 1d2+1 Yuan-Ti Purebloods - MM", "2 Yuan-Ti Nightmare Speakers - MOTM + 1 Yuan-Ti Malison - MM + 1d2 Yuan-Ti Purebloods - MM", 
                              "4 Yuan-Ti Malisons - MM + 1 Yuan-Ti Broodguard - MOTM + 1 Yuan-Ti Pureblood - MM", "4 Mummies - BR + 2 Giant Vultures - BR", "4 Giant Scorpions + 2 Dust Mephits - BR", "5 Yuan-Ti Broodguards - MOTM + 2 Yuan-Ti Purebloods - MM", "3 Gnoll Pack Lords - MM + 1d4+5 Gnolls - BR"]}
FOREST_ENCOUNTERS = {"Easy": ["1 Girallon - MOTM", "1 Displacer Beast - MM", "1 Bearded Devil - BR", "1 Flail Snail - MOTM", "1 Ettercap - BR + 1 Giant Spider - BR", 
                              "1 Ankheg - BR + 1 Giant Spider - BR", "1 Grick - BR + 1d2 Giant Poisonous Snakes - BR", "1 Green Dragon Wyrmling - BR + 1 Giant Wasp - BR", "2 Dire Wolves - BR + 1d2+1 Wolves - BR", "2 Tigers - BR", 
                              "2 Giant Spiders - BR + 1 Giant Wasp - BR", "1 Owlbear - BR", "1d4+1 Black Bears - BR", "1d4+1 Apes - BR", "1d4+1 Giant Wasps - BR", 
                              "1d4+4 Wolves - BR", "2d4 Giant Poisonous Snakes - BR", "1d4 Vine Blights - MM + 2 Needle Blights - MM", "1d4+4 Needle Blights - MM + 1d2 Twig Blights - BR", "3d4+2 Twig Blights - BR"], 
                     "Medium": ["1 Shoosuva - MOTM", "1 Young Green Dragon - BR", "1 Giant Ape - BR + 1 Ape - BR", "1 Grick Alpha - BR + 1 Grick - BR", "2 Shambling Mounds - BR", 
                                "2 Wood Woads - MOTM", "2 Balguras - BR", "2 Girallons - MOTM + 1d4 Apes - BR", "3 Displacer Beasts - MM + 1d4 Twig Blights - BR", "3 Owlbears - BR + 1d2+1 Black Bears - BR", 
                                "3 Bearded Devils - BR + 1d2+1 Needle Blights - MM", "3 Flail Snails - MOTM + 1d2+1 Giant Poisonous Snakes - BR", "1d4+2 Green Dragon Wyrmlings - BR", "1d4+2 Gricks - BR", "1d4+2 Ankhegs - BR", 
                                "1d2+2 Ettercaps - BR + 2 Giant Spiders - BR", "1d6+4 Giant Spiders - BR", "1d4+4 Dire Wolves - BR + 4 Wolves - BR", "3d4+2 Giant Wasps - BR", "1d4+3 Vine Blights - MM + 1d4+4 Needle Blights - MM + 1d4+6 Twig Blights - BR"], 
                     "Hard": ["1 Autumn Eladrin - MOTM", "1 Glabrezu - BR", "1 Shoosuva - MOTM + 1 Dire Wolf - BR", "1 Young Green Dragon - BR + 1 Green Dragon Wyrmling - BR", "1 Giant Ape - BR + 1d4+1 Apes - BR", 
                              "1 Grick Alpha - BR + 1 Grick - BR + 1d4 Giant Poisonous Snakes - BR", "1 Shambling Mound - BR + 2 Vine Blights - MM + 1d4 Needle Blights - MM + 1d4 Twig Blights - BR", "1 Wood Woad - MOTM + 2 Vine Blights - MM + 1d4 Needle Blights - MM + 1d4 Twig Blights - BR", "1 Barlgura - BR + 1 Girallon - MOTM + 1d4 Apes - BR", "3 Girallons - MOTM + 1d2 Apes - BR", 
                              "4 Displacer Beasts - MM + 1 Green Dragon Wyrmling - BR + 1 Tiger - BR", "4 Owlbears - BR + 1d2 Black Bears - BR", "4 Bearded Devils - BR + 1 Ettercap - BR + 1 Giant Spider - BR", "3 Flail Snails - MOTM + 1d4+3 Giant Poisonous Snakes - BR", "1d4+3 Green Dragon Wyrmlings - BR", 
                              "1d4+2 Gricks - BR + 2 Giant Poisonous Snakes - BR", "4 Ankhegs - BR + 1d4+2 Giant Wasps - BR", "4 Ettercaps - BR + 1d2+2 Giant Spiders - BR", "1d4+4 Dire Wolves - BR + 1d4+2 Wolves - BR", "2d4+9 Giant Wasps - BR"]}
GRASSLAND_ENCOUNTERS = {"Easy": ["1 Stegosaurus - MOTM", "1 Ankylosaurus - MOTM", "2 Scarecrows - MM + 1d2 Cockatrice - BR", "1d2+1 Lions - BR", "1 Leucrotta - MOTM", 
                                 "1 Allosaurus - BR + 2 Velociraptors - MOTM", "2 Deinonychus - MOTM + 1d2+1 Velociraptors - MOTM", "1d4+4 Velociraptors - MOTM", "2d4 Pteranodons - BR", "1d6+2 Hadrosaurus - MOTM", 
                                 "1 Hobgoblin Devastator - MOTM", "1 Hobgoblin Captain - MM", "1 Bugbear Chief - MM", "1 Hobgoblin Iron Shadow - MOTM + 1 Worg - BR", "2 Bugbears - BR + 1 Worg - BR + 1d2 Goblins - BR", 
                                 "2 Goblin Bosses - MM + 1 Worg - BR + 1d2 Goblins - BR", "1d4+1 Hobgoblins - BR + 1 Goblin - BR", "3 Worgs - BR + 3 Goblins - BR", "1d4+4 Goblins - BR", "1d4+1 Cockatrice - BR"], 
                        "Medium": ["1 Chimera - BR + 1 Hobgoblin Captain - MM", "2 Gorgons - BR", "1 Hobgoblin Warlord - MM + 1 Hobgoblin Devastator - MOTM", "1 Brontosaurus - MOTM + 1 Bugbear Chief - BR", "2 Triceratops - BR", 
                                   "1 Tyrannosaurus Rex - BR", "1 Liondrake - FTOD + 1 Hobgoblin Captain - MM", "2 Stegosaurus - MOTM + 1d2 Bugbears - BR + 1 Worg - BR", "2 Hobgoblin Devastators - MOTM + 1 Hobgoblin Iron Shadow - MOTM", "2 Hobgoblin Captains - MM + 1d2 Hobgoblin Iron Shadows - MOTM + 1d2 Hobgoblins - MM", 
                                   "3 Leucrotta - MOTM + 1d2+1 Worgs - BR", "3 Ankylosaurus - MOTM + 1d2+1 Hobgoblins - BR", "3 Bugbear Chiefs - MM + 1d2+1 Bugbears - BR", "4 Hobgoblin Iron Shadows - MOTM + 1d2+1 Hobgoblins - BR", "4 Allosaurus - BR + 2 Bugbears - BR", 
                                   "1d4+4 Deinonychus - MOTM + 1d2+2 Velociraptor - MOTM", "1d4+3 Bugbears - BR + 1d2+2 Worgs - BR", "1d4+6 Scarecrows - MM", "1d4+6 Lions - BR", "1d4+6 Hobgoblins - MM + 1d4+3 Goblins - BR"], 
                        "Hard": ["1 Spring Eladrin - MOTM", "1 Nycaloth - MM", "1 Tyrannosaurus Rex - BR + 1 Hobgoblin Captain - MM", "1 Liondrake - FTOD + 1 Hobgoblin Devastator - MOTM", "2 Chimeras - BR", 
                                 "2 Brontosaurus - MOTM", "1 Hobgoblin Warlord - MM + 1 Hobgoblin Captain - MM + 1d2+2 Hobgoblins - BR", "1 Triceratops - BR + 1 Stegosaurus - MOTM + 1 Hobgoblin Iron Shadow - MOTM + 1 Hobgoblin - BR", "2 Gorgons - BR", "3 Stegosaurus - MOTM + 1 Hobgoblin - BR + 1 Pteranodon - BR", 
                                 "2 Hobgoblin Devastators - MOTM + 1 Hobgoblin Captain - MM + 1 Hobgoblin Iron Shadow - MOTM + 1 Hobgoblin - BR", "4 Hobgoblin Captains - MM + 1 Hobgoblin Iron Shadow - MOTM + 1 Deinonychus - MOTM", "4 Leucrottas - MOTM + 2 Worgs - BR", "4 Ankylosaurus - MOTM + 2 Hobgoblins - BR", "2 Bugbear Chiefs - MM + 1d4+2 Bugbears - BR", 
                                 "1d2+4 Hobgoblin Iron Shadows - MOTM", "1d4+2 Allosaurus - BR + 1 Goblin - BR", "1d4+7 Deinonychus - MOTM + 1d2+1 Velociraptors - MOTM", "1d4+6 Bugbears - BR + 1d2+1 Worgs - BR", "1d6+6 Scarecrows - MM"]}
HILL_ENCOUNTERS = {"Easy": ["1 Neogi - MOTM + 1 Neogi Hatchling - MOTM", "1 Neogi Master - MOTM", "2d6+2 Neogi Hatchlings - MOTM", "2 Xvart Warlocks of Raxivort - MOTM + 1d4 Xvarts - MOTM", "3d4+2 Xvarts - MOTM", 
                            "1 Yeth Hound - MOTM", "1 Barghest - MOTM", "1 Wereboar - BR", "1 Werewolf - BR", "1 Iron Cobra - MOTM", 
                            "1 Stone Defender - MOTM", "1 Nightmare - BR", "1d2 Phase Spiders - BR", "1d2+1 Rutterkin - MOTM", "1d2+1 Spined Devils - MM", 
                            "1d2 Giant Boar - BR", "2d4 Giant Wolf Spiders - BR", "2 Giant Hyenas - BR + 1d4 Hyenas - BR", "7d4 Hyenas - BR", "1d2+1 Bronze Scouts - MOTM"], 
                   "Medium": ["2 Oaken Bolters - MOTM", "2 Galeb Duhr - BR", "2 Bulettes - BR", "2 Hill Giants - BR", "1 Howler - MOTM", 
                              "1 Mouth of Grolantor - MOTM + 1 Yeth Hound - MOTM", "1 Eath Elemental Myrmidon - MOTM", "2 Wereboars - BR + 1d2 Giant Boars - BR", "2 Yeth Hounds - MOTM + 1d2 Giant Hyenas - BR + 1d2+1 Hyenas - BR", "2 Iron Cobras - MOTM + 1d2+1 Bronze Scouts - MOTM", 
                              "2 Stone Defenders - MOTM + 1d2 Xvart Warlocks of Raxivort - MOTM + 1d2+1 Xvarts - MOTM", "2 Barghest - MOTM + 1d4 Giant Wolf Spiders - BR", "1 Neogi Master - MOTM + 1d2 Neogi - MOTM + 1d2+1 Neogi Hatchlings - MOTM", "3 Neogi - MOTM + 1d4 Neogi Hatchlings - MOTM", "1d2+2 Werewolves - BR", 
                              "3 Phase Spiders - BR + 1d2+1 Giant Wolf Spiders - BR", "3 Nightmares - BR + 1 Spined Devil - BR", "1d4+2 Spined Devils - BR", "1d4+2 Rutterkin - MOTM", "1d4+2 Giant Boars - BR"], 
                   "Hard": ["1 Stone Golem - BR", "1 Clay Golem - BR", "1 Howler - MOTM + 1 Rutterkin - MOTM", "1 Earth Elemental Myrmidon - MOTM + 1 Stone Defender - MOTM", "2 Mouths of Grolantor - MOTM", 
                            "1 Oaken Bolter - MOTM + 1 Iron Cobra - MOTM + 2 Bronze Scouts - MOTM", "1 Galeb Duhr - BR + 1 Stone Defender - MOTM + 2 Bronze Scouts - MOTM", "2 Bulettes - BR", "2 Hill Giants - BR", "2 Wereboars - BR + 2 Giant Boars - BR", 
                            "2 Yeth Hounds - MOTM + 1d2+2 Giant Hyenas - BR", "2 Iron Cobras - MOTM + 1d2+2 Bronze Scouts - MOTM", "3 Stone Defenders - MOTM + 1d2+1 Giant Wolf Spiders - BR", "3 Barghests - MOTM + 1d2+1 Hyenas - BR", "2 Neogi Masters - MOTM + 1 Neogi - MOTM + 1d2+1 Neogi Hatchlings - MOTM", 
                            "4 Neogi - MOTM + 2 Neogi Hatchlings - MOTM", "4 Werewolves - BR + 1 Rutterkin - MOTM + 1 Xvart Warlock of Raxivort - MOTM", "4 Phase Spiders - BR + 2 Giant Wolf Spiders - BR", "4 Nightmares - BR + 2 Xvart Warlocks of Raxivort - MOTM", "1d2+4 Spined Devils - BR + 2 Xvarts - MOTM"]}
MOUNTAIN_ENCOUNTERS = {"Easy": ["1 Red Dragon Wyrmling - BR", "1 Ettin - BR", "1 Basilisk - BR", "1d2 Peryton - MM", "1 Red Guard Drake - MOTM", 
                                "1 Orc War Chief - MM", "1 Orc Eye of Gruumsh - MM + 1 Orc - BR", "1 Orog - MM + 1 Orc - BR", "1d4+1 Orcs - BR", "1d2 Cave Bears - MM", 
                                "1 Adult Kruthik - MOTM + 1d4+1 Young Kruthiks - MOTM", "3d4+2 Young Kruthiks - MOTM", "2 Chokers - MOTM + 1d3 Star Spawn Grue - MOTM", "1d2+1 Stone Cursed - MOTM", "2d4 Star Spawn Grues - MOTM", 
                                "2 Firenewt Warlocks of Imix - MOTM + 1 Firenewt Warrior - MOTM", "2 Giant Striders - MOTM + 2 Firenewt Warriors - MOTM", "1d4+2 Firenewt Warriors", "1d4+1 Magmin - BR", "2d6+2 Manes - MM"], 
                       "Medium": ["1 Stone Giant - BR", "1 Air Elemental Myrmidon - MOTM", "1 Wyvern - BR + 1d4+1 Orcs - BR", "1 Annis Hag - MOTM + 1d4+1 Magmin - BR", "1 Kruthik Hive Lord - MOTM + 1d2 Adult Kruthik - MOTM + 1d2 Young Kruthik - MOTM", 
                                  "2 Air Elementals - BR", "2 Tanarukks - MOTM", "1 Star Spawn Mangler - MOTM + 1d4+4 Star Spawn Grues - MOTM", "2 Red Dragon Wyrmlings - BR + 1d2+1 Firenewt Warlocks of Imix - MOTM", "2 Ettin - BR + 1d4 Orcs - BR", 
                                  "1 Orc War Chief - MM + 1d2 Orc Eyes of Gruumsh - MM + 1 Orog - MM + 1d2 Orcs - BR", "3 Basilisks - BR + 3 Stone Cursed - MOTM", "4 Adult Kruthiks - MOTM + 1d4+2 Young Kruthiks - MOTM", "4 Orc Eyes of Gruumsh - MM + 1d2+1 Orcs - BR", "4 Orogs - MM + 1d2+1 Orcs - BR", 
                                  "4 Perytons - MM + 1d4+2 Manes - MM", "1d6+4 Stone Cursed - MOTM", "3d4+2 Orcs - BR", "2d6+2 Magmin - MM", "4d10+14 Young Kruthiks - MOTM"], 
                       "Hard": ["1 Young Red Dragon - BR", "1 Star Spawn Hulk - MOTM", "1 Fire Giant - BR", "1 Cloud Giant - BR", "1 Stone Giant Dreamwalker - MOTM", 
                                "1 Stone Giant - BR + 1 Ettin - BR", "1 Air Elemental Myrmidon - MOTM + 1 Red Dragon Wyrmling - BR", "2 Wyverns - BR", "2 Annis Hags - MOTM", "2 Air Elementals - BR", 
                                "2 Tanarukks - MOTM", "1 Kruthik Hive Lord - MOTM + 1d2+1 Adult Kruthiks - MOTM + 1d2 Young Kruthiks - MOTM", "1 Star Spawn Mangler - MOTM + 1d4+6 Star Spawn Grues - MOTM", "3 Red Dragon Wyrmlings - BR + 1d2 Magmin - BR", "3 Ettin - BR + 1d2 Orcs - BR", 
                                "1 Orc War Chief - MM + 1 Orog - MM + 1 Orc Eye of Gruumsh - MM + 1d4+3 Orcs - BR", "4 Basilisks - BR + 1d2 Stone Cursed - MOTM", "6 Adult Kruthiks - MOTM + 2 Young Kruthiks - MOTM", "4 Orc Eyes of Gruumsh - MM + 1d2+6 Orcs - BR", "4 Orogs - MM + 1d2+6 Orcs - BR"]}
SWAMP_ENCOUNTERS = {"Easy": ["1 Wight - BR", "1 Green Hag - BR", "1 Redcap - MOTM", "1 Shadow Mastiff Alpha - MOTM", "1 Black Dragon Wyrmling - BR", 
                             "1 Ghast - BR + 1 Ghoul - BR", "2 Ghouls - BR + 1d4 Stirges - BR", "1d4+1 Crocodiles - BR", "1 Black Guard Drake - MOTM + 1 Swarm of Rot Gubs - MOTM", "1 Will-O'-Wisp - BR", 
                             "1 Green Guard Drake - MOTM + 1 Swarm of Rot Grubs - MOTM", "1 Shadow Mastiff - MOTM + 1d4 Stirges - BR", "1 Meenlock - MOTM", "2 Giant Toads - BR + 2 Mud Mephits - MM", "1d3 Meazels - MOTM", 
                             "2d4 The Wretched - MOTM", "1d4+1 Swarms of Rot Grubs - MOTM", "1d4+4 Mud Mephits - MM", "2d4 Oblex Spawn - MOTM", "3d4+2 Stirges - BR"], 
                    "Medium": ["1 Corpse Flower - MOTM", "1 Hydra - BR", "1 Young Black Dragon - BR + 1 Black Dragon Wyrmling - BR", "1 The Lost - MOTM + 1 The Wretched - MOTM", "1 Venom Troll - MOTM", 
                               "1 Maurezhi - MOTM", "1 Bodak - MOTM + 1d4+1 Stirges - BR", "1 Adult Oblex - MOTM + 2d4 Oblex Spawn - MOTM", "2 Trolls - BR", "2 Giant Crocodiles - BR", 
                               "2 Allips - MOTM", "2 Catoblepases - MOTM", "1 Shadow Mastiff Alpha - MOTM + 1d2+2 Shadow Mastiffs - MOTM", "1d4+2 Shadow Mastiffs - MOTM", "2 Night Hags - BR", 
                               "2 Redcaps - MOTM + 1d2+1 Meazels - MOTM", "2 Wights - BR + 1d2+1 Ghouls - BR", "1d4+2 Ghasts - BR", "2d4+2 Ghouls - BR", "2 Barbed Devils - BR"], 
                    "Hard": ["1 Elder Oblex - MOTM", "1 Froghemoth - MOTM", "1 The Lonely - MOTM", "1 Rot Troll - MOTM", "1 Corpse Flower - MOTM + 1 Green Hag - BR", 
                             "1 Hydra - BR + 1 Swarm of Rot Grubs - MOTM", "1 Venom Troll - MOTM + 1 Green Hag - BR", "1 Young Black Dragon - BR + 1 Black Dragon Wyrmling - BR", "1 Maurezhi - MOTM + 5 Stirges - BR", "1 The Lost - MOTM + 1d2+3 The Wretched - MOTM", 
                             "2 Bodaks - MOTM", "1 Adult Oblex - MOTM + 1d4+6 Oblex Spawn - MOTM", "1 Allip - MOTM + 1 Shadow Mastiff Alpha - MOTM + 1d2 Shadow Mastiffs - MOTM", "1 Troll - BR + 1d4+6 Mud Mephits - MM", "2 Night Hags - BR", 
                             "2 Barbed Devils - BR", "2 Catoblepases - MOTM", "1 Giant Crocodile - BR + 1d4+5 Crocodiles - BR", "4 Wights - BR + 1 Ghast - BR + 1 Ghoul - BR", "4 Redcaps - MOTM + 1 Meenlock - MOTM + 1 Meazel - MOTM"]}
UNDERDARK_ENCOUNTERS = {"Easy": ["1 Black Pudding - BR", "1 Bone Naga - BR", "1 Chuul - BR", "1 Flameskull - BR", "1 Bulezau - MOTM", 
                                 "1 Spectator - BR + 1 Gazer - MOTM", "1d4+1 Gazers - MOTM", "1 Grell - MM", "1 Hell Hound - BR", "1 Hook Horror - MM + 1 Gray Ooze - BR", 
                                 "1 Cave Fisher - MOTM", "1 Choldrith - MOTM + 1 Chitine - MOTM", "1d4+1 Chitine - MOTM", "1d2 Carrion Crawler - MM", "1d2 Nothic - BR", 
                                 "1 Gibbering Mouther - BR + 1d2 Gray Ooze - BR", "1d4+1 Gray Oozes - BR", "1d4+1 Darkmantles - BR", "1d4+1 Magma Mephits - BR", "2 Fire Snakes - MM + 1d2 Magma Mephit - BR"], 
                        "Medium": ["1 Armanite - MOTM + 1 Hell Hound - BR", "1 Cloaker - BR", "1 Fomorian - MM", "1 Mind Flayer Arcanist - MM", "1 Mind Flayer - MM + 1 Grell - MM", 
                                   "1 Spirit Naga - BR", "1 Dhergoloth - MOTM", "1 Draegloth - MOTM + 1 Bulezau - MOTM", "1 Drider - BR + 1d4 Gray Ooze - BR", "1 Gauth - MOTM + 1d4 Gazers - MOTM", 
                                   "2 Vampire Spawn - BR", "1 Salamander - BR + 1d4 Fire Snakes - MM + 1 Magma Mephit - BR", "1 Earth Elemental - BR + 1d4+1 Magma Mephits - BR", "2 Gem Stalkers - FTOD", "1 Wraith - BR + 1 Flameskull - BR", 
                                   "2 Mindwitnesses - MOTM", "1 Umber Hulk - MM + 1 Choldrith - MOTM + 1d2 Chitine - MOTM", "2 Otyugh - BR", "1 Roper - BR + 2 Nothic - BR", "1 Xorn - BR + 1 Bone Naga - BR"], 
                        "Hard": ["1 Death Kiss - MOTM", "1 Yochlol - MM", "1 Alhoon - MOTM", "1 Ulitharid - MOTM", "1 Mind Flayer Arcanist - MM + 1 Grell - MM", 
                                 "1 Cloaker - BR + 1 Cave Fisher - MOTM", "1 Fomorian - MM + 1 Hook Horror - MM", "1 Spirit Naga - BR + 1 Nothic - BR", "1 Mind Flayer - MM + 1 Chuul - BR", "1 Armanite - MOTM + 1 Hell Hound - BR", 
                                 "1 Dhergoloth - MOTM + 1 Hook Horror - MM", "1 Draegloth - MOTM + 1 Bone Naga - BR", "2 Gauths - MOTM", "2 Driders - BR", "1 Mindwitness - MOTM + 1 Chuul - BR + 1 Gibbering Mouther - BR + 1 Gray Ooze - BR", 
                                 "1 Earth Elemental - BR + 2 Hook Horrors - BR + 1d2 Darkmantles - BR", "1 Wraith - BR + 1 Flameskull - BR + 1d2 Fire Snakes - MM", "2 Vampire Spawn - BR", "1 Otyugh - BR + 2 Spectators - BR + 1d2 Gazers - MOTM", "1 Salamander - BR + 2 Fire Snakes - MM + 1d2+3 Magma Mephits - BR"]}
UNDERWATER_ENCOUNTERS = {"Easy": ["3d8 Quippers - BR", "Deep Scion - MOTM", "Killer Whale - BR", "2d4 Constrictor Snakes - BR", "2 Deep Dragon Wyrmlings - FTOD", 
                                  "1 Sahuagin - BR + 1 Sahuagin Priestess - BR", "1 Merrow - BR + 1 Reef Shark - BR", "1d4+1 Sahuagin - BR", "1 Hunter Shark - BR", "1d4+1 Reef Sharks - BR", 
                                  "1 Plesiosaurus - BR", "2 Giant Octopuses - BR", "2 Sea Spawn - MOTM", "2 Swarms of Quippers - BR", "2d4 Giant Sea Horses - BR", 
                                  "1d4+4 Steam Mephits - BR", "1d4+2 Merfolk - BR + 2 Reef Sharks - BR", "1 Water Weird - MM", "Dragon Turtle Wyrmling - FTOD", "2 Sea Hags - MM"], 
                         "Medium": ["1 Young Sea Serpent - FTOD", "1 Water Elemental Myrmidon - MOTM + 1 Water Weird - MM", "1 Young Deep Dragon - FTOD + 1 Deep Dragon Wyrmling - FTOD", "2 Giant Sharks - BR", "2 Water Elementals - BR", 
                                    "1 Sahuagin Baron - MM + 1 Sahuagin Priestess - BR + 1d4 Sahuagin - BR", "2 Kraken Priests - MOTM", "2 Dragon Turtle Wyrmlings - FTOD + 1d4 Reef Sharks - BR", "3 Deep Scion - MOTM + 3 Sea Spawn - MOTM", "3 Killer Whales - BR + 1d4 Steam Mephits - BR", 
                                    "3 Water Weirds - MM + 1 Sea Hag - MM", "1d2+2 Sahuagin Priestesses - BR + 3 Sahuagin - BR", "1d2+2 Merrow - BR + 3 Reef Sharks - BR", "1d4 Hunter Sharks - BR + 3 Reef Sharks - BR", "2 Plesiosaurus - BR + 1d4+2 Swarms of Quippers - BR", 
                                    "1d2+1 Sea Hags (Coven if 3) - MM", "2d4+2 Sea Spawn - MOTM", "2d4+2 Swarms of Quippers - BR", "3d4+2 Sahuagin - BR", "4d6+2 Steam Mephits - BR"], 
                         "Hard": ["1 Aboleth - BR", "1 Young Dragon Turtle - FTOD", "1 Young Sea Serpent - FTOD + 1 Water Weird - MM", "1 Young Deep Dragon - FTOD + 2 Deep Dragon Wyrmlings - FTOD", "1 Water Elemental Myrmidon - MOTM + 1 Dragon Turtle Wyrmling - FTOD", 
                                  "1 Sahuagin Baron - MM + 1d2+1 Sahuagin Priestesses - BR + 2 Sahuagin - BR", "1 Water Elemental - BR + 2 Water Weirds - MM + 1d2+1 Steam Mephits - BR", "1 Kraken Priest - MOTM + 1 Dragon Turtle Wyrmling - FTOD + 1 Sea Hag - MM + 1 Giant Octopus - BR", "1 Giant Shark - BR + 1d2+1 Hunter Sharks - BR + 2 Reef Sharks - BR", "3 Dragon Turtle Wyrmlings - FTOD + 1d2+1 Steam Mephits - BR", 
                                  "3 Sea Hags (Coven) - BR + 1d2+1 Steam Mephits - BR", "4 Deep Scions - MOTM + 1 Merrow - BR + 1 Sea Spawn - MOTM", "4 Killer Whales - BR + 1 Merrow - BR + 1 Swarm of Quippers - BR", "4 Water Weirds - MM + 2 Steam Mephits - BR", "5 Sahuagin Priestesses - MM + 1d2+3 Sahuagin - BR", 
                                  "5 Merrow - BR + 1d2+3 Reef Sharks - BR", "5 Hunter Sharks - BR + 1d4+1 Reef Sharks - BR", "1d2+4 Plesiosaurus - BR", "1d4+7 Sea Spawn - MOTM + 1 Giant Sea Horse - BR", "1d6+6 Swarms of Quippers - BR"]}
URBAN_ENCOUNTERS = {"Easy": ["1 Deathlock - MOTM", "1 Deathlock Wight - MOTM", "1 Incubus - BR", "1 Succubus - BR", "1 Babau - MOTM", 
                             "1 Helmed Horror - MM", "1 Merregon - MOTM", "1 Slithering Tracker - MOTM", "1d2 Mimics - BR", "1 Guard Drake - MOTM", 
                             "1d2 Gargoyles - BR", "1 Cult Fanatic - BR + 1d4 Cultists - BR", "2d6+2 Cultists - BR", "3d4+2 Giant Rats - BR", "2d6+2 Diseased Giant Rats - BR", 
                             "2 Animated Armor - BR + 1d4 Flying Swords - BR", "2d4 Flying Swords - BR", "1d4+4 Zombies - BR", "1d6+2 Skeletons - BR", "1d6+2 Smoke Mephits - MM"], 
                    "Medium": ["1 Hoard Mimic - FTOD", "1 Canoloth - MOTM", "1 Chain Devil - BR", "1 Eyedrake - FTOD", "1 Deathlock Mastermind - MOTM", 
                               "1 Black Abishai - MOTM + 1 Cult Fanatic - BR", "1 White Abishai - MOTM + 1d4+1 Cultists - BR", "1 Oni - BR", "1 Shield Guardian - BR + 1 Deathlock Wight - MOTM", "1 Invisible Stalker - BR + 1d4+1 Smoke Mephits - MM", 
                               "2 Mezzoloths - MM", "1 Beholder Zombie - MM + 1d4+4 Zombies - BR", "2 Banderhobbs - MOTM", "1 Cambion - MM + 2 Cult Fanatics - BR + 1d2 Cultists - BR", "2 Flesh Golems - BR", 
                               "2 Deathlocks - MOTM + 1d4 Skeletons - BR", "2 Helmed Horrors - MM + 2 Animated Armor - BR + 2 Flying Swords - BR", "2 Merregons - MOTM + 1 Cult Fanatic - BR + 1d2 Cultists - BR", "2 Babau - MOTM + 1 Cult Fanatic - BR + 1d2 Cultists - BR", "1d2+1 Deathlock Wights - MOTM + 1d2+1 Skeletons - BR"], 
                    "Hard": ["1 Orthon - MOTM", "1 Bone Devil - BR", "1 Champion - MOTM", "1 Deathlock Mastermind - MOTM + 1 Deathlock Wight - MOTM", "1 Chain Devil - BR + 1 Cult Fanatic - BR", 
                             "1 Eyedrake - FTOD + 1 Mimic - BR", "1 Hoard Mimic - FTOD + 1 Guard Drake - MOTM", "1 Canoloth - MOTM + 1 Cult Fanatic - BR", "1 Black Abishai - MOTM + 1 Cult Fanatic - BR + 1d4 Cultists - BR", "1 Shield Guardian - BR + 1 Succubus - BR", 
                             "1 Oni - BR + 1 Babau - MOTM", "2 Invisible Stalkers - BR", "2 White Abishais - MOTM", "1 Banderhobb - MOTM + 1d4+6 Smoke Mephits - MM", "1 Cambion - MM + 1 Incubus - BR + 1 Cult Fanatic - BR + 1d2 Cultists - BR", 
                             "1 Beholder Zombie - MM + 1d4+6 Zombies - BR", "1 Flesh Golem - BR + 1 Helmed Horror - MM + 1 Gargoyle - BR + 1d2 Diseased Giant Rats - BR", "1 Mezzoloth - MM + 1 Merregon - MOTM + 1 Cult Fanatic - BR + 1d2 Cultists - BR", "2 Deathlocks - MOTM + 1 Deathlock Wight - MOTM + 1d2+1 Skeletons - BR", "2 Babaus - MOTM + 2 Cult Fanatics - BR + 1d2 Cultists - BR"]}
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
                   "light": "Bright Light", "layout": 1, "enemies": "None", "loot": ["None"], "hours": 0}
    
    name = ""
    difficulty = ""
    environment = ""
    effects = []
    safe = ""
    light = ""
    layout = 0
    enemies = "None"
    loot = []

    # Counters
    mBossCount = 1
    bossCount = 1

    for i in range(50):
        tarrasqueRoll = random.randint(1,1000)
        if tarrasqueRoll == 69: # Is a Tarrasque
            CHAMBERS[i+1] = {"number": i+1, "name": "Tarrasque Room", "difficulty": "Death", 
                             "environment": "Tarrasque Mouth", "effects": ["Death"], "safe": "Never",
                             "light": "Darkness", "layout": 1, "enemies": "Tarrasque", "loot": ["None"], "hours": 0}
        else: # Not a Tarrasque
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
            enemies = generate_enemies(name, difficulty, environment, safe)

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
def generate_enemies(name, difficulty, environment, safe):
    result = "None"

    if safe == "Yes": return result # No enemies if safe

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

# Restart and randomize dungeon
def restart_dungeon():
    randomize_dungeon()
    game_state["current_chamber"] = CHAMBERS[0]
    game_state["chambers"] = CHAMBERS
    game_state["time"] = TIME
    update_ui()
    save_game_state() # Save game after restart

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

# Button to randomize dungeon and start over
btn_generate = tk.Button(root, text="Restart & Randomize Dungeon", command=restart_dungeon)
btn_generate.pack(pady=(20,10))

# Button to generate next chamber
btn_generate = tk.Button(root, text="Generate Next Chamber", command=next_chamber)
btn_generate.pack(pady=(15,25))

# Button to advance time
btn_short = tk.Button(root, text="Advance Time", command=advance_time(TIME))
btn_short.pack()

label = tk.Label(root, text = "No Random Encounter For Advance Time")
label.pack()

label = tk.Label(root, text = "Resting")
label.pack(pady=(10,0))

# Button to short rest
btn_short = tk.Button(root, text="Short Rest", command=short_rest)
btn_short.pack(pady=(0,5))

# Button to long rest
btn_long = tk.Button(root, text="Long Rest", command=long_rest)
btn_long.pack()

# Button to save
btn_long = tk.Button(root, text="Save", command=save_game_state)
btn_long.pack(pady=(20,0))

# Run application
root.mainloop()
