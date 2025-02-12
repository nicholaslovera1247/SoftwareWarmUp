"""Module that contains a Pokemon class"""

class Pokemon:
    """Represents a Pokemon from the Firebase database, 
    used for easily printing the output of queries"""

    def __init__(self, index, name, element, hp, stage = None):
        self.index = index
        self.name = name
        self.type = element
        self.hp = hp
        self.stage = stage

    @staticmethod
    def from_dict(param_dict):
        """Returns an instance of a Pokemon initialized from dictionary values"""

        return Pokemon(
            param_dict['index'], param_dict['name'], param_dict['type'], param_dict['hp'],
            param_dict['stage'] if 'stage' in param_dict.keys() else None)

    def __str__(self):
        return (f"ID: {self.index} \n"
                f"Name: {self.name.title()} \n"
                f"Type: {self.type.title()} \n"
                f"HP: {self.hp} \n"
                f"Stage: {self.stage} \n"
                "-----------------------")
