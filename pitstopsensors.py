## WHEEL CLASS
## should have attributes of GPIO sensors numbers to tell the pi which sensors to check
## these attributes should be assigned in the constructor AKA __init__

class wheel:
    def __init__(self, name):
        self.name = name ## string, rear or front, just for reference purposes
        present = True
        locked = True
        new = False
    
    
    
    ## getter functions should take gpio sensors and return the relevant information
    ## for now they will just grab inputs from the command line    
    
    def get_present(self):
        self.present = bool(int(input(self.name + " wheel present? ")))

    def get_lock(self):
        self.locked = bool(int(input(self.name + " wheel locked? ")))

    def get_new(self):
        self.new = bool(int(input(self.name + " wheel new? ")))
        
    def validate(self):
        if (not self.present and self.locked):
            return False
        return True

## FUEL TANK CLASS

class fueltank:
    def __init__(self):
        self.level = 0.0