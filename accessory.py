class Accessory:
    def __init__(self, name, effect_type, effect_value):
        self.name = name
        self.effect_type = effect_type
        self.effect_value = effect_value
        self.equipped = False

    def equip(self, player):
        pass

    def unequip(self, player):
        pass

