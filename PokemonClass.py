class Pokemon:
    def __init__(self,id,name,type,HP,stage = None):
        self.id = id
        self.name = name
        self.type = type
        self.HP = HP
        self.stage = stage

    @staticmethod
    def from_dict(dict):
        return Pokemon(dict['index'], dict['name'], dict['type'], dict['hp'], 
                      dict['stage'] if 'stage' in dict.keys() else None)

    def __str__(self):
        return (f"ID: {self.id} \n"
                f"Name: {self.name.title()} \n"
                f"Type: {self.type.title()} \n"
                f"HP: {self.HP} \n"
                f"Stage: {self.stage} \n"
                "-----------------------")
