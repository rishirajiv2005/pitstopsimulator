## WHEEL CLASS
## should have attributes of GPIO sensors numbers to tell the pi which sensors to check
## these attributes should be assigned in the constructor AKA __init__

class wheel:
    def __init__(self, name):
        self.name = name ## string, rear or front, just for reference purposes
        self.present = True
        self.locked = True
        self.new = False
    
    
    
    ## getter functions should take gpio sensors and return the relevant information
    ## for now they will just grab inputs from the command line    
    
    def set_present(self):
        self.present = bool(int(input(self.name + " wheel present (0: yes 1: no)? ")))

    def set_lock(self):
        self.locked = bool(int(input(self.name + " wheel locked (0: yes 1: no)? ")))

    def set_new(self):
        self.new = bool(int(input(self.name + " wheel new/old (0: yes 1: no)? ")))
        
    def validate(self):
        if (not self.present and self.locked):
            return False
        return True

## FUEL TANK CLASS

class fueltank:
    # name : name of the fuel tank
    # level : float representing % of fuel in tank
    # full : bool representing if the tank is full
    # probe_inserted : bool representing if the fuel probe is inserted
    
    def __init__(self, name):
        self.name = name
        self.level = 0.0
        self.full = False
        self.probe_inserted = False
        
    def set_level(self):
        self.level = float(input(self.name + " level (float 0 - 100)? "))
    
    def set_probe(self):
        self.probe_inserted = bool(int(input(self.name + " fuel probe inserted (0: yes 1: no)? "))) 
    