
# in order to deal with what is actively in the game
from gameplay_classes import Locations, Fleets, Systems, Installations, Guilds

# in order to have the classes defined
from gameplay_classes import Ship, Fleet, Module, Stockpile, Material, Inhabitable, Installation, World, System, Guild, Location

# not sure if needed, the templates for each type.
from gameplay_classes import Ship_Classes, Module_Types, Stockpile_Types, Material_Types, Installation_Types, World_Types, System_Types, Star_Types

def game_frame():
    # run ship movement, combat, landings, and deliveries first
    for fleet in Fleets:
        fleet.turn()

    # next run inhabitables production and consumption, births, deaths, immigration, etc.
    for spacestation in Installations:
        spacestation.turn()
    
    # run ai
    for guild in Guilds:
        guild.turn()

    # so this is probably where pygame or another library is going to get info about user input.
    # use_player_inputs()
