
class TkToken:

    def __init__(self,typ,value):
        self.type = typ
        self.value = value
    
    def __repr__(self):
        return f"(type={self.type},value={self.value})"
