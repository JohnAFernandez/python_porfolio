
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
        self.frate = frate			        # dict, type key, amount number

    

    def add_frate(self, type, amount):
        print("Unimplemented function run.")
        return

    def get_frate_list(self):
        print("Unimplemented function run.")
        return

    def remove_frate(self, type_amount):
        print("Unimplemented function run.")
        return

    def add_passengers(self, amount):
        print("Unimplemented function run.")
        return

    def damage_subsystem(self, subsystem, amount):
        print("Unimplemented function run.")
        return

    def repair_subsystem(self, subsystem, amount):
        print("Unimplemented function run.")
        return
       

Ship_Classes = {"taco example" : ship("taco example", 5, 0, {SUBSYSTEM_TYPES[0]: 10}, 0, 100, 10, 15, 5, {})}


class fleet():
    def __init__(self, owner, current_des ):
        self.owner = owner                      # which guild owns this fleet
        self.current_destination = current_des  # where is the fleet currently heading
        self.flight_plan = []                   # what is the planned out route for this fleet
        self.ships = []                         # what ships are in this fleet
        

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
    def __init__(self, pop, producing, address, government, stockpiles, modules, raw_materials, ecology):
        super().__init__(pop, producing, address, government, stockpiles, modules)
        self.raw_materials = raw_materials  # what minerals is available on the world surface
        self.ecology_produces = ecology     # a list of things the local ecology produces
    
    def is_colonized(self):
        return self.pop > 0
    
    def is_colony_ready(self):
        print("Unimplemented Function Run")
        return False 
    
    def is_pristine(self):
        return self.pop < 1 and len(self.modules) < 1 and len(self.stockpiles) < 1

    def consume_raw_material(self, material, amount){

        return 
    }

world_Types = {}


class system():
    def __init__(self, star, worlds, fields, fleets):
        self.star = star                # what type of star do we have?
        self.worlds = worlds            # what worldS are in system? list.
        self.fields = fields            # what asteroid fields 
        self.fleets = fleets            # what fleets are in system?

System_Types = {}


class guild():
    def __init__(self, name, routes, fleets, installations, inventory, assets, employees):
        self.name = name
        self.routes = routes
        self.fleets = fleets 
        self.installations = installations
        self.inventory = inventory
        self.assets = assets
        self.employees = employees


Locations = []
