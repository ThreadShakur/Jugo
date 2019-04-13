class ItemNotInFieldset(Exception):
    def __init__(self, field, model):
        self.field = field
        self.model = model
    
    def __str__(self):
        return f"Unknown field {self.field} in {self.model}"

class UsedReservedVariable(Exception):
    def __init__(self, var, model):
        self.var = var
        self.model = model
    
    def __str__(self):
        return f"Variable {self.var} in {self.model} is RESERVED, please use another one"