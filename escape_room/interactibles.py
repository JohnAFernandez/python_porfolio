class interactive_object:
    def __init__(self):
        # tracker "flags", iow what has happened to this object already?
        # !! FIX ME! Second game has new name instead of old name....
        self.default_name = ""
        self.name = ""
        self.selector = ""
        # every level that has a reward, needs a level above it to receive the reward
        self.number_of_levels = 0
        self.current_level = 0  # do not manually assign

        self.keys = []  # object or objects required to open
        self.messages = []  # unopened, success,
        self.rewards = []  # what it gives when opened
        self.enables = []
        self.enabled = True
        self.self_disables = False
        # maybe this section would be better if we just replaced with another Interactible object
        self.changes_to = ""
        # but if I upgrade to using graphics, then I can use the same coordinates.
        self.selector_changes_to = ""
        # Also, this may end up introducing fewer bugs overall, since I don't have to make sure another object works.
        self.change_level = -1