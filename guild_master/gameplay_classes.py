# Note from the programmer.  -- I ran into some limitations in Python and I'm going to switch to another language.


from game_math import FLOAT_MAX, FLOAT_MIN, INT_MAX, INT_MIN
from game_time import time_has_elapsed



# ==== universe constants ====
CURRENCY_NAME = "Dollars" # but whut about mai credits??

# ==== Guild constants ====
IFF_FRIEND = 0
IFF_FRIENDLY = 1
IFF_NUTRAL = 2
IFF_SUSPISCIOUS = 3
IFF_ENEMY = 4

# ==== fleet constants ====
FLEET_STATE_UNSET = 0
FLEET_STATE_DOCKED = 1
FLEET_STATE_DEPARTING_STATION = 2
FLEET_STATE_DEPARTING_PLANET = 3
FLEET_STATE_SYSTEM_TRANSIT = 4
FLEET_STATE_INTERSYSTEM_TRANSIT = 5
FLEET_STATE_SYSTEM_PATROL = 6
FLEET_STATE_PLANET_PATROL = 7
FLEET_STATE_STATION_PATROL = 8
FLEET_STATE_COMBAT = 9
FLEET_STATE_CAPTURING = 10
FLEET_STATE_RETREAT = 11
FLEET_STATE_DISABLED = 12
FLEET_STATE_SURRENDERED = 13
FLEET_STATE_DESTROYED = 14
FLEET_STATE_PLANETARY_ORBIT = 15

# ==== ship constants =====
SUBSYSTEM_TYPES = ("Engine", "Subspace Drive", 
"Manuvering Thrusters", 
"Computer Main", "Aux Computer", 
"Atmosphere Regulation", "Water Reclamation", 
"Comms Receiver Dish", "Comms Transmitter", 
"Fission Reactor", "Fusion Reactor",
"Cooling", 
"Dorsal PDC", "Ventral PDC", "Aft PDC", "Stern PDC", "Port PDC", "Starboard PDC", 
"Dorsal APC", "Ventral APC", "Aft APC", "Stern APC", "Port APC", "Starboard APC",
"Dorsal ASM", "Ventral ASM", "Aft ASM", "Stern ASM", "Port ASM", "Starboard ASM")

WEAPON_SYSTEM_MIN = 12
WEAPON_SYSTEM_MAX = 29

WEAPON_TYPES = ("Amor Piercing Cannon", "Point Defense Cannon", "Anti Spacecraft Missile", "APC", "PDC", "ASM")

    
class Ship():
    def __init__(self, s_class, min_crew, crew_count, subsystems, passengers, max_volume, volume, mass, base_mass, frate, force, turn_force):
        self.ship_class = s_class		    # what type of ship is this? Can only be set on init.
        self.crew_minimum = min_crew		# int, just how much crew before this ship starts to have malfunctions in flight because of crew strain.
        self.crew_count = crew_count		# how many crew are on duty.
        self.subsystems = subsystems		# what subsystems are in use, dict type as key, HP number
        self.passengers = passengers		# should be a dict, destination key, passenger count number
        self.cargo_max_volume = max_volume	# the max volume of cargo
        self.cargo_current_volume = volume	# how much of the cargo volume is taken
        self.current_mass = mass		    # how much mass this ship has in total.
        self.base_mass = base_mass		    # if everything was removed, how much mass this ship should have.
        self.frate = frate			        # dict, type key, amount number, frate == freight
        self.max_engine_force = force       # how much actual force can this engine put out
        self.max_manuver_force = turn_force# how much actual force can the manuvering thrusters actually put out.

        # intrinsic instance variables

        # is this guy armed?
        if len(self.subsystems) < 1:
            self.armed = False
        else:
            for x in self.subsystems:
                if x >= WEAPON_SYSTEM_MIN and x <= WEAPON_SYSTEM_MAX:
                    self.armed = (True,)
                    break
                else:
                    self.armed = (False,)

        self.max_accel = self.max_engine_force / self.current_mass
        self.max_manuverability = self.max_manuver_force / self.current_mass
        self.in_combat = False

    def find_close_fleet(self, address):
        print("Yes, please implement find close fleet")
        return

        
    # crew methods
    def has_sufficient_crew(self):
        print("Unimplemented function run. has_sufficient_crew")


    # frate methods
    def add_frate(self, type, amount):
        print("Unimplemented function run. Add frate")
        return

    def get_frate_list(self):
        print("Unimplemented function run. get frate list")
        return

    def remove_frate(self, type_amount):
        print("Unimplemented function run. remove frate")
        return


    # passenger methods
    def add_passengers(self, amount):
        print("Unimplemented function run. add passengers")
        return
    
    def remove_passengers(self, amount):
        print("Unimplemented function run. remove_passengers")


    # cargo volume and mass calculations
    def recalculate_cargo_volume(self, amount):
        print("Unimplemented function run. recalculate_cargo_volume")

    def recalculate_ship_mass(self, amount):
        print("Unimplemented function run. recaulculate_ship_mass")


    # subsystem methods
    def damage_subsystem(self, subsystem, amount):
        print("Unimplemented function run. damage subsystem")
        return

    def repair_subsystem(self, subsystem, amount):
        print("Unimplemented function run.")
        return
       

Ship_Classes = {"taco example" : Ship("taco example", 5, 0, {SUBSYSTEM_TYPES[0]: 10}, 0, 100, 10, 15, 5, {})}


class Fleet():
    def __init__(self, owner, address, x, y, current_des, flight_plan, ships, docked, dry_docked):
        self.state = FLEET_STATE_UNSET
        self.state_time_target = 0
        self.owner = owner                      # which guild owns this fleet
        self.current_destination = current_des  # where is the fleet currently heading
        self.address = address
        self.velocity = [x, y]
        self.flight_plan = flight_plan          # what is the planned out route for this fleet
        self.ships = ships                      # what ships are in this fleet
        self.docked = docked                    # is this fleet docked?
        self.dry_docked = dry_docked            # is this fleet dry docked?

        # intrinsic instance variables
        self.max_accel = FLOAT_MAX
        self.max_manuverability = FLOAT_MAX
        self.armed_mass = 0.0                   # how much of this fleet is armed
        self.frate_mass = 0.0                # how much of this fleet is unarmed
        self.in_cpombat = False

        if len(self.ships) > 0:
            for ship in self.ships:
                # the fleet can only accelerate as fast as its slowest ship.
                if ship.max_accel < self.max_accel:
                    self.max_accel = ship.max_accel
                if ship.max_manuverability < self.max_manuverability:
                    self.max_manuverability = ship.max_manuverability
                
                if ship.armed:
                    self.armed_mass += ship.mass
                else:
                    self.frate_mass += ship.mass

    def task_is_complete(self, state):
        if self.state == FLEET_STATE_UNSET:
            self.what_am_i_doing()
            return True
        
        elif self.state == FLEET_STATE_DOCKED:
            if len(self.flight_plan) < 1:
                return False
            else:
                self.what_am_i_doing()

        elif self.state == FLEET_STATE_DEPARTING_STATION:
            if time_has_elapsed(self.state_time_target)


        elif self.state == FLEET_STATE_DEPARTING_PLANET:

        elif self.state == FLEET_STATE_SYSTEM_TRANSIT:

        elif self.state == FLEET_STATE_INTERSYSTEM_TRANSIT:

        elif self.state == FLEET_STATE_SYSTEM_PATROL:

        elif self.state == FLEET_STATE_PLANET_PATROL:

        elif self.state == FLEET_STATE_STATION_PATROL:

        elif self.state == FLEET_STATE_COMBAT:

        elif self.state == FLEET_STATE_CAPTURING:

        elif self.state == FLEET_STATE_RETREAT:

        elif self.state == FLEET_STATE_DISABLED:

        elif self.state == FLEET_STATE_SURRENDERED:

        elif self.state == FLEET_STATE_DESTROYED:

        elif self.state == FLEET_STATE_PLANETARY_ORBIT:

        else:
            print("task_is_complete has a bad state.")
            self.what_am_i_doing()
            return True

    def turn(self):

            
        if is_on_course(self.address, self.velocity, self.current_destination):
        
        else:
            calculate_orbital_math

        # this will check that there are any fleets to interact with
        close_fleets = find_close_fleets(self, self.address)

        if len(close_fleets) > 0:
            # this is going to be a function to evaluate just how much friendly and enemy presence
            iff_pair = evaluate_iff_standing(close_fleets)  
        
            if iff_pair[1] > 0 and iff_pair[0] < iff_pair[1] > 
        

        
        

class Module(): # a building or installtion module -- Only listing everything in an installation, or if owned by a guild on a world.
    def __init__(self, type, owner, address):
        self.type = type            # what type of module.
        self.owner = owner          # what guild or faction owns this
        self.address = address      # ID, what is this module's address?

Module_Types = {}


class Stockpile(): # a stockpile of either material or finished good
    def __init__(self, owner, address, type, amount):
        self.owner = owner		# owner of this stockpile
        self.address = address		# an ID for its location
        self.type = type		# what type of material is this?
        self.amount = amount		# How much (Not mass, not weight, just purchasable units)

Stockpile_Types = {}


class Material(): # basically a material's properties.
    def __init__(self, density, hours, necessary, con_type):
        self.density = density			# used for weight and capacity calculations
        self.man_hours = hours			# how many hours it takes to create something. used to figure out the essential value
        self.life_supporting = necessary	# if this runs out, will people start dying? Bool
        self.consumption_type = con_type	# how does this material get consumed by the population or industry, consumption type will inform how quickly people will die, if life supporting

Material_Types = {}


class Inhabitable():
    def __init__(self, pop, producing, address, government, stockpiles, modules):
        self.population = pop               # the total population of this inhabitable
        self.producing_list = producing     # what this inhabitable is producing, name is key, amount is value
        self.address = address              # ID, where is this?
        self.governed_by = government       # who is running this thing?
        self.stockpiles = stockpiles        # what supplies does this inhabitable have
        self.modules = modules              # what modules have been built?


class Installation(Inhabitable):
    def __init__(self, pop, producing, address, government, stockpiles, modules):
        super().__init__(pop, producing, address, government, stockpiles, modules, type)
        self.type = type     # what type of installation?

Installation_Types = {}


class World(Inhabitable):
    def __init__(self, pop, producing, address, government, stockpiles, modules, type, raw_materials, ecology):
        super().__init__(pop, producing, address, government, stockpiles, modules)
        self.type = type
        self.raw_materials = raw_materials  # what minerals is available on the world
        self.ecology_produces = ecology     # a list of things the local ecology produces
    
    # are there people down there?
    def is_colonized(self):
        return self.pop > 0
    
    # is the colony ready to be started?
    def is_colony_ready(self):
        print("Unimplemented Function Run is_colony_ready")
        return False 
    
    # the planet is in its natural state
    def is_pristine(self):
        return self.pop < 1 and len(self.modules) < 1 and len(self.stockpiles) < 1

    # time to eat metal
    def consume_raw_material(self, material, amount):
        remaining = self.raw_materials[material]

        if amount > remaining:
            self.raw_materials[material] = 0.0
            return remaining
        else: 
            self.raw_materials[material] = remaining - amount
            return amount
    
    # yeah, what am I doing here???
    def recycle_materials(self):
        print("Unimplemented Function Run, recycle materials.")
        return
    

World_Types = {}


class System():
    def __init__(self, star, worlds, fields, fleets):
        self.star = star                # what type of star do we have?
        self.worlds = worlds            # what worldS are in system? list.
        self.fields = fields            # what asteroid fields 
        self.fleets = fleets            # what fleets are in system?

System_Types = {}
Star_Types = {}

class Guild():
    def __init__(self, name, reputation, eth_rep, routes, fleets, installations, inventory, assets, employees):
        self.name = name                        # name of the guild
        self.reputation = reputation            # how well respected is this guild, whether good or ill?
        self.ethical_reputation = eth_rep       # has this faction acted like they are an ethical faction in the past?
        self.routes = routes                    # what routes are known to this guild
        self.fleets = fleets                    # what fleets are maintained by this guild
        self.installations = installations      # the installations owned by this guild.
        self.inventory = inventory              # what raw materials, completed materials are used in this guild.
        self.assets = assets                    # Currency, Inventory, Ships, etc.
        self.employees = employees              # A list of employees.  Not sure what to do with this yet.
        self.iffs = []                          # dictonary enemy as key, then

class Location():
    def __init__(self, system, orbit, orbital_direction, degrees):
        self.system = system
        self.orbit = orbit
        self.orbital_direction = orbital_direction
        self.orbit_angle = degrees
        

# I need a way to define orbits.  We're going with cicular because you know, we've been making this way too complicated
Locations = [] # dictionary where the index is tracked in each object, for quick access.  Then each sublist will list all objects at that location.

Fleets = []
Systems = []
Installations = []
Guilds = []
