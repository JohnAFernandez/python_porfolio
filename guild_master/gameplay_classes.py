
# ==== universe constants ====
CURRENCY_NAME = "Dollars" # but whut about mai credits??


# ==== ship constants =====
SUBSYSTEM_TYPES = ("Engine", "Subspace Drive", 
"Manuevering Thrusters", 
"Computer Main", "Aux Computer", 
"Atmosphere Regulation", "Water Reclamation", 
"Comms Receiver Dish", "Comms Transmitter", 
"Fission Reactor", "Fusion Reactor",
"Cooling", 
"Dorsal PDC", "Ventral PDC", "Aft PDC", "Stern PDC", "Port PDC", "Starboard PDC", 
"Dorsal APC", "Ventral APC", "Aft APC", "Stern APC", "Port APC", "Starboard APC",
"Dorsal ASM", "Ventral ASM", "Aft ASM", "Stern ASM", "Port ASM", "Starboard ASM")


WEAPON_TYPES = ("Amor Piercing Cannon", "Point Defense Cannon", "Anti Spacecraft Missile", "APC", "PDC", "ASM")

    
class ship():
    def __init__(self, s_class, min_crew, crew_count, subsystems, passengers, max_volume, volume, mass, base_mass, frate):
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
       

Ship_Classes = {"taco example" : ship("taco example", 5, 0, {SUBSYSTEM_TYPES[0]: 10}, 0, 100, 10, 15, 5, {})}


class fleet():
    def __init__(self, owner, current_des, flight_plan, ships, docked, dry_docked):
        self.owner = owner                      # which guild owns this fleet
        self.current_destination = current_des  # where is the fleet currently heading
        self.flight_plan = flight_plan          # what is the planned out route for this fleet
        self.ships = ships                      # what ships are in this fleet
        self.docked = docked                    # is this fleet docked?
        self.dry_docked = dry_docked            # is this fleet dry docked?
        

class module(): # a building or installtion module -- Only listing everything in an installation, or if owned by a guild on a world.
    def __init__(self, type, owner, address):
        self.type = type            # what type of module.
        self.owner = owner          # what guild or faction owns this
        self.address = address      # ID, what is this module's address?

Module_Types = {}


class stockpile(): # a stockpile of either material or finished good
    def __init__(self, owner, address, type, amount):
        self.owner = owner		# owner of this stockpile
        self.address = address		# an ID for its location
        self.type = type		# what type of material is this?
        self.amount = amount		# How much (Not mass, not weight, just purchasable units)

Stockpile_Types = {}


class material(): # basically a material's properties.
    def __init__(self, density, hours, necessary, con_type):
        self.density = density			# used for weight and capacity calculations
        self.man_hours = hours			# how many hours it takes to create something. used to figure out the essential value
        self.life_supporting = necessary	# if this runs out, will people start dying? Bool
        self.consumption_type = con_type	# how does this material get consumed by the population or industry, consumption type will inform how quickly people will die, if life supporting

Material_Types = {}


class inhabitable():
    def __init__(self, pop, producing, address, government, stockpiles, modules):
        self.population = pop               # the total population of this inhabitable
        self.producing_list = producing     # what this inhabitable is producing, name is key, amount is value
        self.address = address              # ID, where is this?
        self.governed_by = government       # who is running this thing?
        self.stockpiles = stockpiles        # what supplies does this inhabitable have
        self.modules = modules              # what modules have been built?


class installation(inhabitable):
    def __init__(self, pop, producing, address, government, stockpiles, modules):
        super().__init__(pop, producing, address, government, stockpiles, modules, type)
        type = type     # what type of installation?

Installation_Types = {}


class world(inhabitable):
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
    

world_Types = {}


class system():
    def __init__(self, star, worlds, fields, fleets):
        self.star = star                # what type of star do we have?
        self.worlds = worlds            # what worldS are in system? list.
        self.fields = fields            # what asteroid fields 
        self.fleets = fleets            # what fleets are in system?

System_Types = {}
Star_Types = {}

class guild():
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

# I need a way to define orbits.  We're going with cicular because you know, we've been making this way too complicated
Locations = [] # list of lists, where the index is tracked in each object, for quick access.  Then each sublist will list all objects at that location.
