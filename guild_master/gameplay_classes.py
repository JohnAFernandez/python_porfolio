CURRENCY_NAME = "Dollars"
UNIN" = ""

SUBSYSTEM_TYPES = ("Engine", "Subspace Drive", 
"Manuevering Thrusters", 
"Computer Main", "Aux Computer", 
"Atmosphere Regulation", "Water Reclamation", 
"Comms Receiver Dish", "Comms Transmitter", 
"Fission Reactor", "Fusion Reactor", 
"Dorsal PDC", "Ventral PDC", "Aft PDC", "Stern PDC", "Port PDC", "Starboard PDC", 
"Dorsal APC", "Ventral APC", "Aft APC", "Stern APC", "Port APC", "Starboard APC",
"Dorsal ASM", "Ventral ASM", "Aft ASM", "Stern ASM", "Port ASM", "Starboard ASM"


VALID_WEAPON = ("Amor Piercing", "Point Defense", "Anti Spacecraft Missile")


    
class ship():
    def __init__(self, s_class, min_crew, crew_count, subsystems, passengers, max_volume, volume, mass, base_mass, frate):
        self.ship_class = s_class		# what type of ship is this?
        self.crew_minimum = min_crew		# int, just how much crew before this ship starts to have malfunctions in flight because of crew strain.
        self.crew_count = crew_count		# how many crew are on duty.
        self.subsystems = subsystems		# what subsystems are in use, dict type as key, HP number
        self.passengers = passengers		# should be a dict, destination key, passenger count number
	self.cargo_max_volume = max_volume	# the max volume of cargo
        self.cargo_current_volume = volume	# how much of the cargo volume is taken
        self.current_mass = mass		# how much mass this ship has in total.
        self.base_mass = base_mass		# if everything was removed, how much mass this ship should have.
        self.frate = frate			# dict, type key, amount number

    def add_frate(self, type, amount):


    def get_frate_list(self):


    def remove_frate(self, type_amount):


    def add_passengers(self, amount):


    def damage_subsystem(self, subsystem, amount):


    def repair_subsystem(self, subsystem, amount):

       

Ship_Classes = {"taco example" : ship("taco example", 5, 0, {SUBSYSTEM_TYPES[0]: 10}, 0, 100, 10, 15, 5, {})

}


class fleet():
    def __init__(self, owner, current_route ):
        self.owner = owner
        self.current_route = []
        self.flight_plan = [] 	# 
        self.ships = []
        

class module(): # a building or installtion module -- Only listing everything in an installation, or if owned by a guild on a planet.
    def __init__(self, type, owner, address):
        self.type = type
        self.owner = owner
        self.address = address

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
    def __init__(self):
        self.population


class installation(inhabitable):
    def __init__(self):


class planet(inhabitable):
    def __init__(self):


class guild():
    def __init__(self):


Locations = []
    def __init__(self):
