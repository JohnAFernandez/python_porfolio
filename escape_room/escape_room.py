# Copyright (c) 2023, John Andrew Fernandez
# All rights reserved.

import os
from interactibles import interactive_object

inventory = []
end_game_object = "Door"

autosave_enabled = True

STARTING_GAME_TIME = 30
game_time = STARTING_GAME_TIME
loss_counter = 0
version_string = "0.2.1"

# Game State Management Variables
# we don't need a proper game state machine, just a helper variable to tell run_game_state where to go next.
GAME_START_STATE = -1  # should be set to this value only when starting the program
MAIN_MENU_STATE = 0
NEW_GAME_STATE = 1
GAMEPLAY_STATE = 2
GAME_MENU_STATE = 3
EXIT_GAME_STATE = 4

# Save game constants
SAVE_GAME_VERSION = "v1"
SAVE_GAME_VALIDATION_STRING = "JFERSG"
SAVE_GAME_VALIDATION_LENGTH = len(
    SAVE_GAME_VALIDATION_STRING) + len(SAVE_GAME_VERSION)
SAVE_GAME_EXTENSION = ".ersg"
DEFAULT_GAME_NAME = "ESCAPE ROOM CLASSIC"


valid_game_states = ("GAME_START_STATE", "IN_GAME",
                     "IN_MAIN_MENU", "IN_GAME_MENU", "EXIT")


class save_state:
    def __init__(self):
        self.game_time = 0
        self.interactibles = {}
        self.inventory = []


def exit_game():
    global next_game_state
    next_game_state = EXIT_GAME_STATE


def go_to_main_menu():
    global next_game_state
    next_game_state = MAIN_MENU_STATE


def go_to_new_game():
    global next_game_state
    next_game_state = NEW_GAME_STATE


def go_to_gameplay():
    global next_game_state
    next_game_state = GAMEPLAY_STATE


def go_to_in_game_menu():
    global next_game_state
    next_game_state = GAME_MENU_STATE


# display the in-game menu text
def display_in_game_menu():
    print("")
    print("Game Menu")
    print("")
    print("A) Save Game")
    print("B) Load Game")
    print("C) Options")
    print("D) Tips")
    print("E) End Current Game")
    print("F) Quit Program")
    print("G) Return To Game")
    print("")


def save_game(manual_save):
    global interactive_objects
    global game_time

    if manual_save:
        failcount = 0
        while True:
            filename = input("\nChoose a filename: ").lower()

            if len(filename) < 1:
                print("Filename cannot be empty.")
                failcount += 1

                if failcount > 3:
                    print("Too many bad attempts, aborting save!")
                    return False
            else:
                break

    else:
        filename = "autosave"

    filename += ".ersg"

    f = open(filename, "w")
    f.write(
        f"{SAVE_GAME_VALIDATION_STRING}{SAVE_GAME_VERSION}\n{str(game_time)}\n")
    f.write(str(len(interactive_objects)))
    f.write("\n")
    for thing in interactive_objects:
        f.write(thing.name + ",")
        f.write(str(thing.current_level))
        if thing.enabled:
            f.write(",1")
        else:
            f.write(",0")
        f.write("\n")

    f.write(str(len(inventory))+"\n")
    for thing in inventory:
        f.write(thing)
        f.write("\n")
    f.write("\n\n")
    f.close()

    return True

# Enumerate the save game modes
PARSE_SAVE_GAME_TIME = 0
PARSE_SAVE_GAME_INTERACTIBLES = 1
PARSE_SAVE_GAME_INVENTORY = 2
END_PARSE = 3


def validate_game_time(time):
    if type(time) == int and time < STARTING_GAME_TIME:
        return True
    else:
        return False
    

def validate_interactibles(interactibles):
    if len(interactibles) != len(interactive_objects):
        print(f"Number of interactive objects is mismatched in game data and save file. {len(interactive_objects)} vs {len(interactibles)}")
        return False

    if type(interactibles) == dict:
        for thing in interactibles:
            found = False
            for thing2 in interactive_objects:
                if thing == thing2.name or thing == thing2.changes_to:
                    found = True
                    if thing2.number_of_levels < interactibles[thing][0]:
                        print(f"Bad current level for {thing}.")
                        return False
                    
            if found == False:
                print(f"Could not find {thing} in game data")
                return False      

    else:
        return False
    
    return True

def validate_inventory(inventory):
    if type(inventory) == list:
        found = False

        for thing in inventory:
            for interactible in interactive_objects:
                if thing in interactible.rewards:
                    found = True
                    break
            
            if found == False:
                return False

    else:
        return False
    
    return True


def apply_parsed_game(saved_game):
    global game_time
    global inventory
    game_time = saved_game.game_time

    for thing in saved_game.interactibles:
        for thing2 in interactive_objects:
            if thing == thing2.name or thing == thing2.changes_to:
                thing2.enabled = saved_game.interactibles[thing][1] == 1
                thing2.current_level = saved_game.interactibles[thing][0]
                break

    # at times we will need to force the new name of an object back onto it.
    for thing in interactive_objects:
        if thing.change_level > -1 and thing.current_level >= thing.change_level:
            thing.name = thing.changes_to
            thing.selector = thing.selector_changes_to

    inventory = saved_game.inventory


def parse_and_restore_save_file(saved_string):
    position = saved_string.find("\n") + 1
    parsed_game = save_state()
    parse_mode = PARSE_SAVE_GAME_TIME
    total_from_file = 0
    section_count = 0

    while position < len(saved_string):
        if position < 0 or position >= len(saved_string):
            print("Save File could not be parsed.")
            return False

        next_position = saved_string[position:].find("\n") + position

        # if this is negative, it does not necessarily mean that the file is corrupt.
        # this could be the last iteration of the loop.
        if next_position < 0:
            next_position = len(saved_string)

        working_string = saved_string[position: next_position]

        if parse_mode == PARSE_SAVE_GAME_TIME:
            if not working_string.isnumeric():
                print("Save file has an invalid game time, cannot parse, aborting.")
                return False

            parsed_game.game_time = int(working_string)
            parse_mode += 1
            position = next_position + 1
            continue

        elif parse_mode == PARSE_SAVE_GAME_INTERACTIBLES:
            # at this point, we would just be picking up the size of the next section
            if total_from_file == 0:
                if not working_string.isnumeric():
                    print(
                        "Save file has an invalid interactible objects count, cannot parse, aborting.")
                    return False

                total_from_file = int(working_string)

                # if this is empty then the section is empty and we move on to the next one
                if total_from_file == 0:
                    parse_mode += 1

                position = next_position + 1
                continue
            else:
                comma_position = working_string.find(",")

                if (comma_position < 0):
                    print(
                        "Save game is missing commas in interactible objects lists. Aborting load.")
                    return False

                interactible_name = working_string[0:comma_position]

                last_comma_position = comma_position
                comma_position = working_string.find(
                    ",", last_comma_position + 1)

                if (comma_position < 0):
                    print(
                        "Save game is missing commas in interactible objects lists. Aborting load.")
                    return False

                last_comma_position += 1
                if comma_position == last_comma_position:
                    print(
                        "Save game is missing a interatible object level, aborting load.")
                    return False

                if not working_string[last_comma_position: comma_position].isnumeric():
                    print(
                        "Save game file has a non-numeric level for an interactible object, aborting load")
                    return False

                level = int(working_string[last_comma_position:comma_position])

                if not working_string[comma_position + 1:].isnumeric():
                    print(
                        "Save game file has a non-numeric for the enabled flag, aborting load")
                    return False

                enabled = True if working_string[comma_position +
                                                 1:] == "1" else False

                parsed_game.interactibles[interactible_name] = (level, enabled)
        elif parse_mode == PARSE_SAVE_GAME_INVENTORY:
            if total_from_file == 0:
                if not working_string.isnumeric():
                    print(
                        "Save file has an invalid inventory objects count, cannot parse, aborting.")
                    return False

                total_from_file = int(working_string)

                if total_from_file == 0:
                    break
            else:
                parsed_game.inventory.append(working_string)
        else:
            print("WOKKA!  You've hit a bug!  FERNANDEZ messed up.")
            return False

        section_count += 1
        if section_count >= total_from_file:
            total_from_file = 0
            section_count = 0 
            parse_mode += 1
            if parse_mode >= END_PARSE:
                break

        position = next_position + 1

    if not validate_game_time(parsed_game.game_time):
        print("Parsed game time is invalid, aborting load.") 
        return False
    if not validate_interactibles(parsed_game.interactibles): 
        print("Parsed interactible objects are invalid, aborting load.")
        return False
    if not validate_inventory(parsed_game.inventory): 
        print("Parsed inventory is invalid, aborting load.")
        return False

    # Success is guaranteed at this point!
    reset_game()
    apply_parsed_game(parsed_game)
    return True


def load_game():
    the_list = os.listdir()

    incorrect_version_files = 0

    # yeah, I know that looks scary.  Reverse iterate to not invalidate the index x
    for x in range(len(the_list) - 1, -1, -1):
        # make sure we have enough digits to check the extension, then get a slice of the last portion
        if not ((len(the_list[x]) > 5 and the_list[x][-5:] == SAVE_GAME_EXTENSION)):
            the_list.pop(x)
            continue

        test = open(the_list[x], "r").read()

        if len(test) < SAVE_GAME_VALIDATION_LENGTH:
            the_list.pop(x)
            continue

        # !! If the save game version is ever bumped, this logic will have to be changed
        if test[0:8] != SAVE_GAME_VALIDATION_STRING + SAVE_GAME_VERSION:
            the_list.pop(x)
            incorrect_version_files += 1
            continue

    if len(the_list) < 1:
        if (incorrect_version_files > 0):
            print("No files to load, but some files from a different save version have been found.  Perhaps you need to use a different version of escape room.")
        else:
            print("No files to load.")

        return False

    print("Files to choose from:\n")

    x = 0

    for item in the_list:
        print(f"{x + 1}) {item[0:len(item)-5]}")
        x += 1

    if incorrect_version_files > 0:
        print(
            f"\nPlease note that {incorrect_version_files} files were found that could not be opened.")

    fail_count = 0

    while True:
        choice = input("\n")
        if choice.isnumeric():
            # user's choice is 1 indexed
            file_index = int(choice) - 1

            if file_index > -1 and file_index < len(the_list):
                break

        fail_count += 1

        if fail_count > 3:
            print("User did not choose a valid file, aborting load.")
            return False

    filename = the_list[file_index]
    f = open(filename, "r")
    saved_string = f.read()

    print("\n\n") # the game is getting loaded, so we need some space to distance ourselves from the menu

    return parse_and_restore_save_file(saved_string)


# handle the in game menu
def do_in_game_menu():
    display_in_game_menu()

    saved = False  # did we already save the game?
    # nifty little thing that lets us quit the menu if the player messes up three times.
    invalid_counter = 0

    while True:
        # what did the user say to making a save game if they hit exit, needs to be reset
        backup_save_choice = ""
        user_choice = input("Select your option (R to redisplay): ")

        # Save the game
        if user_choice.lower() == "a":
            invalid_counter = 0
            saved = save_game(True)

        # load the game
        elif user_choice.lower() == "b":
            invalid_counter = 0

            if not saved:
                print("")
                backup_save_choice = input(
                    "Would you like to save before loading? (Y/N) ")
                if backup_save_choice.lower() == "y" or backup_save_choice.lower() == "yes":
                    saved = save_game(True)
                    if not saved:
                        print("Aborted load due to save failure. (not supported yet)")
                        # save function will have its own warning message.
                        continue

            success = load_game()

            if success:
                go_to_gameplay()
                break
            else:
                while True:
                    retry_try = input("Try another file? (Y if yes)")
                    if not retry_try.lower() == "y":
                        break

        # options screen -- lol, What options???
        elif user_choice.lower() == "c":
            invalid_counter = 0
            do_options_menu()
            display_in_game_menu()

        # display some tips...
        elif user_choice.lower() == "d":
            do_help_blurb()

        # End the Current game
        elif user_choice.lower() == "e":
            invalid_counter = 0

            if not saved:
                backup_save_choice = input(
                    "Would you like to save before exiting? Y/N ")

                if (backup_save_choice.lower() == "y" or backup_save_choice.lower() == "yes"):
                    saved = save_game(True)

                    if not saved:
                        print(
                            "Aborted game ending, due to save failure. (Not Supported)")
                        # save function will have its own warning message.
                        continue

            reset_game()
            go_to_main_menu()  # back to the regular game menu
            break

        # Quit Program
        elif user_choice.lower() == "f":
            if not saved:
                backup_save_choice = input(
                    "Would you like to save before quitting? Y/N ")

                if backup_save_choice.lower() == "y" or backup_save_choice.lower() == "yes":
                    saved = save_game(True)
                    if not saved:
                        print("Aborted game ending, due to save failure.")
                        # save function will have its own warning message.
                        continue
            exit_game()
            break

        # Exit in-game menu
        elif user_choice.lower() == "g":
            invalid_counter = 0
            go_to_gameplay()
            break

        # what are the options again?
        elif user_choice.lower() == "r":
            invalid_counter = 0
            display_in_game_menu()  # remember, redisplay
            # just conitnue as there's nothing else to do here.

        # User put something invalid or cat sat on keyboard
        else:
            invalid_counter += 1

            if invalid_counter > 2:
                invalid_counter = 0  # remove when other code is in, it's just here to stop erroring
                # autosave?
                save_game(False)
                go_to_gameplay()
            else:
                print("Invalid choice, please try again.")


# display the options menu options.  Because of enable/disable, each option will need logic attached
def display_options_menu():
    print("")
    print("Options:")
    print("")
    global autosave_enabled

    if autosave_enabled:
        print("Autosave is on")
        print("\tA) Disable autosave")
    else:
        print("Autosave is off")
        print("\tA) Enable autosave")
    print("")
    print("B) Go Back")
    print("")


# hanle options menu selection
def do_options_menu():
    invalid_counter = 0
    global autosave_enabled

    while True:
        display_options_menu()
        user_choice = input("Choice: ")

        if user_choice.lower() == "a":
            invalid_counter = 0
            autosave_enabled = (not autosave_enabled)

            if (autosave_enabled):
                print("")
                print("Autosave enabled")

            else:
                print("")
                print("Autosave disabled")

        elif user_choice.lower() == "b":
            break

        else:
            invalid_counter += 1

            if invalid_counter > 2:
                print("Too many invalid choices, exiting options menu")
                break
            else:
                print("Invalid choice, please try again.")


def display_main_menu():
    global version_string

    print("\n\n\n\n\n\n\n\n")
    print("\t\t///ESCAPE ROOM\\\\\\")
    print(f"\n\tA) New Game\n\tB) Load Game\n\tC) Options\n\tD) Tips\n\tE) Credits\n\tF) Quit\n\n\nBeta Version {version_string}\n")


def display_credits():
    print("\n\n")
    print("\t\t\t///ESCAPE ROOM\\\\\\")
    print("")
    print("\n\nConcept, Programming, and Writing by John A Fernandez, aka Singularitus")
    print(f"\nThis is a Beta release, version {version_string}")
    print("If you enjoyed this game and want to support the developer go to:\npaypal.me/singularitus")
    input("\n\nPress Enter...")


def do_help_blurb():
    print("\n\nMost menus will have a letter or number to select an object or menu item to interact with. But, unlike many adventure games, your character will be able to figure out if an item is usable in specific situations by themself.")
    choice = input("\n\nWould you like further hints (Y/N)")
    if choice.lower() == "y":
        print("\n\nAnd if you feel like you've tried everything.  Why not try everything again?")
        input("\nPress enter...")
    



def do_main_menu():

    while True:
        display_main_menu()

        user_choice = input("Select your option: ")

        if user_choice.lower() == "a":
            reset_game()  # in case they played an instance previously
            go_to_new_game()
            break

        elif user_choice.lower() == "b":
            success = load_game()

            if success:
                go_to_gameplay()
                break

        elif user_choice.lower() == "c":
            do_options_menu()
        
        elif user_choice.lower() == "d":
            do_help_blurb()

        elif user_choice.lower() == "e":
            display_credits()

        elif user_choice.lower() == "f":
            exit_game()
            break


def do_initial_gameplay_description():
    print("")
    print("")
    print("A cacophonos klaxon awakens you!")
    print("")
    print("Disoriented, you are greeted by unfamiliar surroundings.")
    print("As far as you can tell, you have never been in this room before.")
    print("In shock, you try to understand what's happening, but you only take in one detail:")
    print("the only door to this room has no doorknob - You are trapped.")
    print("")
    input("Press Enter...")
    print("")
    print(f"A voice thunders through the speakers, \"All personnel evacuate immediately. Reactor leak! {STARTING_GAME_TIME} minutes to lethal radiation dose!\"")
    print("The voice repeats itself unendingly, and you realize it's a recorded message.")
    print("You bring your arm up to look at a watch you don't recognize and mark how much time you have to escape....")
    print("")
    input("Press Enter To Begin...")
    print("")
    print("")


global interactive_objects
interactive_objects = []


# Have this here just in case I need to initialize other things, too
def init():
    reset_game()


# reset and reinitialize the game state
def reset_game():
    global game_time

    game_data_initialized = True

    game_time = STARTING_GAME_TIME

    interactive_objects.clear()

    # set up the broken doonknob
    interactive_objects.append(interactive_object())
    interactive_objects[-1].name = "Broken Door"
    # print("Doing " + interactive_objects[-1].name)
    interactive_objects[-1].selector = "B"
    interactive_objects[-1].number_of_levels = 2
    interactive_objects[-1].keys.append("Doorknob")
    interactive_objects[-1].keys.append("\t")  # I'm a hacker, I know
    interactive_objects[-1].messages.append(
        "You examine the door closely. There are no hinges on this side and no significant gaps.\nDespite the missing doorknob, you cannot push the other side of the doorknob out.\nEven with tools, there's no way to access the opening mechanism.")
    interactive_objects[-1].messages.append(
        "The doorknob clicks in place!")
    interactive_objects[-1].messages.append(
        "You try to turn the doorknob, but the door is locked!")
    interactive_objects[-1].messages.append(
        "You open the door and exit the room!")
    interactive_objects[-1].enabled = True
    interactive_objects[-1].selector_changes_to = "B"
    interactive_objects[-1].changes_to = "Door"
    interactive_objects[-1].change_level = 1

    # set up the chest
    interactive_objects.append(interactive_object())
    interactive_objects[-1].name = "Chest"
    # print("Doing " + interactive_objects[-1].name)
    interactive_objects[-1].selector = "C"
    interactive_objects[-1].number_of_levels = 2
    interactive_objects[-1].keys.append("")
    interactive_objects[-1].messages.append("")
    interactive_objects[-1].messages.append(
        "You go for the chest and are happy to find it unlocked. But you end up disappointed, since it's empty.")
    interactive_objects[-1].messages.append("")
    interactive_objects[-1].messages.append(
        "You decide to also look under and behind the chest. Behind it is a keypad!")
    interactive_objects[-1].messages.append(
        "A third search of the chest and the area around it yields nothing.")
    interactive_objects[-1].rewards.append("")
    interactive_objects[-1].rewards.append("Keypad")
    interactive_objects[-1].enabled = True
    interactive_objects[-1].self_disables = True

    # set up the dresser parent object
    interactive_objects.append(interactive_object())
    interactive_objects[-1].name = "Dresser"
    # print("Doing " + interactive_objects[-1].name)
    interactive_objects[-1].selector = "D"
    interactive_objects[-1].number_of_levels = 1
    interactive_objects[-1].keys.append("")
    interactive_objects[-1].messages.append("")
    interactive_objects[-1].messages.append(
        "You see three drawers in the dresser.  Nothing has been placed on top of it.")
    interactive_objects[-1].rewards.append("")
    interactive_objects[-1].enabled = True
    interactive_objects[-1].enables.append([])
    interactive_objects[-1].enables[-1].append("Drawer 1")
    interactive_objects[-1].enables[-1].append("Drawer 2")
    interactive_objects[-1].enables[-1].append("Drawer 3")
    interactive_objects[-1].self_disables = True

    # set up drawer 1
    interactive_objects.append(interactive_object())
    interactive_objects[-1].name = "Drawer 1"
    # print("Doing " + interactive_objects[-1].name)
    interactive_objects[-1].selector = "1"
    interactive_objects[-1].number_of_levels = 2
    interactive_objects[-1].keys.append("")
    interactive_objects[-1].messages.append("")
    interactive_objects[-1].messages.append(
        "This drawer contains a journal. You open its pages, hoping to find something useful.  It contains entry after entry saying,\n\n\t\"Don't believe the message! Don't open the door!\"")
    interactive_objects[-1].messages.append(
        "You consider the journal you found in the first drawer.  Could all this just be some kind of game?")
    interactive_objects[-1].messages.append(
        "You consider the journal you found in the first drawer.  Could all this just be some kind of game?")
    interactive_objects[-1].messages.append(
        "You consider the journal you found in the first drawer.  Could all this just be some kind of game?")
    interactive_objects[-1].keys.append("")
    interactive_objects[-1].enabled = False

    # set up drawer 2
    interactive_objects.append(interactive_object())
    interactive_objects[-1].name = "Drawer 2"
    # print("Doing " + interactive_objects[-1].name)
    interactive_objects[-1].selector = "2"
    interactive_objects[-1].number_of_levels = 1
    interactive_objects[-1].messages.append(
        "This drawer contains a false bottom that you cannot seem to remove. Finally, you notice a key hole.")
    interactive_objects[-1].messages.append(
        "You place the key in the lock. It turns, and below the false bottom, you find a sheet of paper with a six digit code on it.")
    interactive_objects[-1].messages.append(
        "Searching through the second drawer again does not lead to any new discoveries.")
    interactive_objects[-1].keys.append("Key")
    interactive_objects[-1].rewards.append("Code")
    interactive_objects[-1].enabled = False

    # set up drawer 3
    interactive_objects.append(interactive_object())
    interactive_objects[-1].name = "Drawer 3"
    # print("Doing " + interactive_objects[-1].name)
    interactive_objects[-1].selector = "3"
    interactive_objects[-1].number_of_levels = 1
    interactive_objects[-1].keys.append("")
    interactive_objects[-1].messages.append("")
    interactive_objects[-1].messages.append(
        "You find a key in the third drawer! What could it be for?")
    interactive_objects[-1].messages.append(
        "A second search through this drawer yeilds nothing.")
    interactive_objects[-1].keys.append("")
    interactive_objects[-1].rewards.append("Key")
    interactive_objects[-1].enabled = False

    # set up the ceiling fan
    interactive_objects.append(interactive_object())
    interactive_objects[-1].name = "Fan"
    # print("Doing " + interactive_objects[-1].name)
    interactive_objects[-1].selector = "F"
    interactive_objects[-1].number_of_levels = 2
    interactive_objects[-1].keys.append("Step Ladder")
    interactive_objects[-1].keys.append("Screwdriver")
    interactive_objects[-1].messages.append(
        "You see a ceiling fan but you can't reach it.")
    interactive_objects[-1].messages.append(
        "With the step ladder you are able to reach the ceiling fan.\nIts stationary blades do not have anything placed on top.")
    interactive_objects[-1].messages.append(
        "You climb back up to the fan, but you cannot remove the cover by hand.")
    interactive_objects[-1].messages.append(
        "Opening the cover with the screwdriver, miraculously, you find the doorknob and can now use it to exit the room!")
    interactive_objects[-1].rewards.append("")
    interactive_objects[-1].rewards.append("Doorknob")
    interactive_objects[-1].enabled = True
    interactive_objects[-1].self_disables = True

    # set up the hole in
    interactive_objects.append(interactive_object())
    interactive_objects[-1].name = "Hole in the Wall"
    # print("Doing " + interactive_objects[-1].name)
    interactive_objects[-1].selector = "H"
    interactive_objects[-1].number_of_levels = 2
    interactive_objects[-1].messages.append(
        "Closely examining the hole in the wall, you find it has a wire ending in a usb port.")
    interactive_objects[-1].messages.append(
        "You connect the keypad's USB cord into the port in the hole. Then you place the keypad in the wall. It fits snugly, and a green light turns on -- Now that is progress!")
    interactive_objects[-1].messages.append(
        "You move to press the numbers on the keypad, but you don't know what keys to press.")
    interactive_objects[-1].messages.append(
        "You key the code into the keypad, and a lock clicks on the door!  Now you just need to open the door!")
    interactive_objects[-1].messages.append("")
    interactive_objects[-1].keys.append("Keypad")
    interactive_objects[-1].keys.append("Code")
    interactive_objects[-1].rewards.append("")
    # nothing to see here... no hacks or anything
    interactive_objects[-1].rewards.append("\t")
    interactive_objects[-1].enabled = True
    interactive_objects[-1].self_disables = True
    interactive_objects[-1].selector_changes_to = "K"
    interactive_objects[-1].changes_to = "Keypad"
    interactive_objects[-1].change_level = 1

    # set up the lamp
    interactive_objects.append(interactive_object())
    interactive_objects[-1].name = "Lamp"
    # print("Doing " + interactive_objects[-1].name)
    interactive_objects[-1].selector = "L"
    interactive_objects[-1].number_of_levels = 2
    interactive_objects[-1].keys.append("")
    interactive_objects[-1].messages.append("")
    interactive_objects[-1].messages.append(
        "In one of the corners is a lamp. You examine it and find nothing around it or stuck onto it. You even look in the light socket.")
    interactive_objects[-1].messages.append("")
    interactive_objects[-1].messages.append(
        "You decide to take a closer look, and it occurs to you to lift the lamp up to look under the base. You are excited to see a screwdriver hidden there!")
    interactive_objects[-1].messages.append(
        "You look at the lamp again, considering another search, but you realize there's no other place for an object to be hidden within it.")
    interactive_objects[-1].rewards.append("")
    interactive_objects[-1].rewards.append("Screwdriver")
    interactive_objects[-1].enabled = True
    interactive_objects[-1].self_disables = True

    # set up the step ladder
    interactive_objects.append(interactive_object())
    interactive_objects[-1].name = "Step Ladder"
    # print("Doing " + interactive_objects[-1].name)
    interactive_objects[-1].selector = "S"
    interactive_objects[-1].number_of_levels = 1
    interactive_objects[-1].keys.append("")
    interactive_objects[-1].messages.append("")
    interactive_objects[-1].messages.append(
        "You see a step ladder in the corner and realize that you can use it to reach the ceiling.")
    interactive_objects[-1].keys.append("")
    interactive_objects[-1].rewards.append("Step Ladder")
    interactive_objects[-1].enabled = True
    interactive_objects[-1].self_disables = True

    # set up the tv
    interactive_objects.append(interactive_object())
    interactive_objects[-1].name = "TV"
    # print("Doing " + interactive_objects[-1].name)
    interactive_objects[-1].selector = "T"
    interactive_objects[-1].number_of_levels = 1
    interactive_objects[-1].keys.append("Screwdriver")
    interactive_objects[-1].messages.append(
        "You examine a television in the corner of the room. It will not turn on.")
    interactive_objects[-1].messages.append(
        "You open the tv with the screwdriver with a little effort, but you do not see anything usable inside.")
    interactive_objects[-1].rewards.append("")
    interactive_objects[-1].enabled = True
    interactive_objects[-1].self_disables = True


def evaluate_victory_condition():
    global interactive_objects
    global end_game_object
    global loss_counter

    for thing in interactive_objects:
        if end_game_object == thing.name and thing.current_level == thing.number_of_levels:
            loss_count += 1
            return True

    return False


def evaluate_loss_condition():
    global game_time
    global loss_counter

    if game_time <= 0:
        loss_counter += 1
        return True
    else:
        return False


def manage_iteractable_use(i):
    global interactive_objects

    do_autosave = False

    print("\n")  # need some breaking room
    if interactive_objects[i].current_level < interactive_objects[i].number_of_levels:
        # print("True 1")
        # if the key is in hand
        if interactive_objects[i].keys.__len__() < 1 or interactive_objects[i].keys.__len__() <= interactive_objects[i].current_level or (interactive_objects[i].keys.__len__() > interactive_objects[i].current_level and (interactive_objects[i].keys[interactive_objects[i].current_level] in inventory or interactive_objects[i].keys[interactive_objects[i].current_level] == "")):
            # print("True 2")

            # if we have a valid message
            if interactive_objects[i].messages.__len__() > interactive_objects[i].current_level * 2 and interactive_objects[i].messages[interactive_objects[i].current_level * 2 + 1] != "":
                # print("True 3")

                print(
                    interactive_objects[i].messages[interactive_objects[i].current_level * 2 + 1])
            else:
                # print("False 3")

                print("WOKKA! Missing success message. Current level is " +
                      str(interactive_objects[i].current_level))

            # if we have a valid reward
            if interactive_objects[i].rewards.__len__() > interactive_objects[i].current_level and interactive_objects[i].rewards[interactive_objects[i].current_level] != "":
                # print("True 4")
                inventory.append(
                    interactive_objects[i].rewards[interactive_objects[i].current_level])
                do_autosave = True
            else:
                pass
                # print("False 4")

            if interactive_objects[i].enables.__len__() > interactive_objects[i].current_level and interactive_objects[i].enables[interactive_objects[i].current_level].__len__() > 0:
                # print("True 5")

                toggle_object(
                    interactive_objects[i].enables[interactive_objects[i].current_level])
            else:
                pass
                # print("False 5")

            # advance the player to the next level
            interactive_objects[i].current_level += 1
            do_autosave = True

        else:
            # print("false 3")
            if interactive_objects[i].messages.__len__() > interactive_objects[i].current_level * 2 - 1 and interactive_objects[i].messages[(interactive_objects[i].current_level - 1) * 2] != "":
                # print("true 6")
                print(
                    interactive_objects[i].messages[interactive_objects[i].current_level * 2])
            else:
                # print("false 6")
                print(
                    f"WOKKA! Missing failure message. Current level is {interactive_objects[i].current_level}")
    else:
        # print("false 1")
        print(interactive_objects[i].messages[-1])

    # if this objects name changes, then change its name
    if interactive_objects[i].change_level != -1 and interactive_objects[i].change_level <= interactive_objects[i].current_level:
        # print("True 7")
        interactive_objects[i].name = interactive_objects[i].changes_to
        interactive_objects[i].selector = interactive_objects[i].selector_changes_to
        do_autosave = True
    else:
        # print("False 7")
        pass

    # if we don't want this object to exist anymore, take it off the list.
    if interactive_objects[i].current_level == interactive_objects[i].number_of_levels and interactive_objects[i].self_disables:
        # print("True 8")
        interactive_objects[i].enabled = False
        do_autosave = True
    else:
        # print("False 8")
        pass

    global autosave_enabled

    if do_autosave and autosave_enabled:
        save_game(False)

    input("\nPress Enter to Continue... \n")


def toggle_object(list_of_things):
    global interactive_objects

    AssertionError(type(list_of_things) == list)

    for thing in list_of_things:
        for interactive_thing in interactive_objects:
            if thing == interactive_thing.name:
                interactive_thing.enabled = True


def select_the_object(string):
    global interactive_objects

    if type(string) == str:
        for i in range(0, interactive_objects.__len__(), 1):
            if interactive_objects[i].enabled and interactive_objects[i].selector.lower() == string.lower():
                return i

    return -1


def get_interactive_object(name):
    global interactive_objects
    for x in range(0, len(interactive_objects), 1):
        if name == interactive_objects[x].name:
            return x

    return -1


def list_interactible_objects():
    global interactive_objects
    print("You see the following things to examine:\n")
    for thing in interactive_objects:
        if thing.enabled == True:
            print("\t" + thing.selector + ") " + thing.name)


def list_alternate_choice():
    global interactive_objects
    drawer = get_interactive_object("Drawer 1")

    if drawer < 0 or drawer > len(interactive_objects):
        print("WOKKA! MISSING Object.  If you're the player, you're screwed!")
        return

    # has the journal been fully explored?
    if interactive_objects[drawer].current_level == interactive_objects[drawer].number_of_levels:
        print("\n\tJ) Consider the journal")


def list_inventory_objects():
    if inventory.__len__() > 0:
        print("\nYou can use the following objects:")
        result = "\t"

        for thing in inventory:
            # empty list or the shameful, dirty hack
            # if result != "":
            if result != "\t" and thing != "\t":
                result += ", "
                result += thing
            elif thing != "\t":
                result += thing

        # slice off the trailing comma and space
        # if (len(result) > 1 and result[-2] == ","):
        #    result = result[0:len(result) - 3]

        print(result)


def escape_game_messages():
    print("As you cross the door's threshold, you open the door and see another person, just like you, frantically looking through a room identical to the one you just escaped.\n\nHe mirrors the shocked look you give him, and as the klaxon and recorded message stop, a voice declares\n\n\t\"I guess you'll just have to try again.\"")
    print("\nSuddenly, you black out.")
    input("\nPress enter ...")


def lose_game_messages():
    print("Your time is up. You experienec a thrill of horror and cry out in frustration!\n\nAs you wait for death, the klaxon and recorded message end.  Another voice declares, \n\n\t\"I guess you'll just have to try again.\"\n\nA look of complete confusion just manages to cross your face as you black out.")
    input("\nPress enter ...")


def do_rejection_loop():
    global game_time

    print("\nYou sit and think about your situation.  You still have no memory of how you got here. You can remember your name, past and relationships until the last time you fell asleep...")
    print("\nYou know there is something off.  It feels as if someone has set all this up.  Items being scattered across a room so that you have to figure out how to escape does not make sense.")
    input("\nPress enter...")
    print("\nThe entries in the journal were hastily written, as if the writer knew they had almost no time. But if all this is real, then you need to get out of here as soon as possible.")
    print("\nIn a rush you decide to...")
    while True:
        choice = input(
            "\n\tA) Continue your attempts to get through the door.\n\tB) Yell at the ceiling that you aren't going to play this game anymore!\n")

        if choice.lower() == "a":
            return False
        else:
            break

    print("\nYou sit down on the ground and cross your arms.\n\n\t\"You can forget it.  I'm not playing anymore.\"\n")
    print("You say this with a steady voice, and you fight hard to keep fear from marking your features.\n")
    print("Nothing happens.")

    total_wait_time = 1

    while total_wait_time < 7 and game_time > 5:
        choice2 = input("\nKeep waiting? (Y/N)")

        if (choice2.lower() == "y"):
            game_time -= 1
            total_wait_time += 1
            print(
                f"\nYou wait for 1 more minute... {game_time} minutes until lethal dose.")
        elif (choice2.lower() == "n"):
            return False
        else:
            print(f"In your indecisiveness, another minute passes. {game_time} minutes until lethal dose")

    print(f"\n\nThe klaxon and recorded voice stop playing.  A new voice speaks.\n\n\"Well, it looks like you figured it out. Now we can finally end this experiment.  It took you {loss_counter + 1} tries to figure it out. But you're free to go.\"")
    print("\nThe room is flooded with sunlight as one of the walls retracts into the ground. And a car - your car is waiting with its door open, your phone ready to used in its holder.\n\n\tThis time, you are truly free...")
    input("\n...")

    reset_game()
    return True


def do_gameplay(new_game):
    global inventory
    global game_time

    if new_game:
        do_initial_gameplay_description()

    exit_state = False

    while True:

        game_time -= 1

        if evaluate_victory_condition():
            escape_game_messages()
            go_to_main_menu()
            break

        if evaluate_loss_condition():
            lose_game_messages()
            go_to_main_menu()
            break

        while True:
            list_interactible_objects()
            list_alternate_choice()
            list_inventory_objects()
            gameplay_choice = input(
                f"\n{game_time} minutes to lethal dose...What do you want to try?\n\nM) In-game menu\n")

            if gameplay_choice.lower() == "m":
                go_to_in_game_menu()
                game_time += 1  # slight hack to enable us to exit to the in-game menu
                exit_state = True
                break
            elif gameplay_choice.lower() == "j":
                if do_rejection_loop():
                    go_to_main_menu()
                    exit_state = True
                    break
            else:
                i = select_the_object(gameplay_choice)

                if (i < 0):
                    print(
                        "You get confused -- The radiation must be getting to you. You resolve to be more deliberate.")
                    continue

                manage_iteractable_use(i)

            break

        if exit_state == True:
            break


def mini_game_state_machine():

    global last_game_state
    last_game_state = GAME_START_STATE
    global next_game_state
    next_game_state = MAIN_MENU_STATE

    while True:
        AssertionError(next_game_state !=
                       GAME_START_STATE and next_game_state < 5)

        if next_game_state == MAIN_MENU_STATE:
            if last_game_state == GAME_START_STATE:
                init()
            do_main_menu()

        elif next_game_state == NEW_GAME_STATE:
            do_gameplay(True)

        elif next_game_state == GAMEPLAY_STATE:
            do_gameplay(False)

        elif next_game_state == GAME_MENU_STATE:
            do_in_game_menu()

        elif next_game_state == EXIT_GAME_STATE:
            break

        last_game_state = next_game_state


# run the game
mini_game_state_machine()
