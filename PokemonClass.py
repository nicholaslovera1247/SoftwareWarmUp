class Pokemon:
    def __init__(self,id,name,type,HP,stage = None):
        self.id = id
        self.name = name
        self.type = type
        self.HP = HP
        self.stage = stage

    def __str__(self):
        return (f"ID: {self.id} \n"
                f"Name: {self.name} \n"
                f"Type: {self.type} \n"
                f"HP: {self.HP} \n"
                f"Stage: {self.stage}")
