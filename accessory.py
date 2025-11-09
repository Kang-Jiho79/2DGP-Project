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

class HealthNecklace(Accessory):
    def __init__(self):
        super().__init__("Health Necklace", "health", 10)

    def equip(self, player):
        player.max_hp += self.effect_value
        player.hp += self.effect_value

    def unequip(self, player):
        player.max_hp -= self.effect_value
        if player.hp > player.max_hp:
            player.hp = player.max_hp

class StaminaNecklace(Accessory):
    def __init__(self):
        super().__init__("Stamina Necklace", "Stamina", 10)

    def equip(self, player):
        player.max_stamina += self.effect_value
        player.stamina += self.effect_value

    def unequip(self, player):
        player.max_stamina -= self.effect_value
        if player.stamina > player.max_stamina:
            player.stamina = player.max_stamina

class AttackNecklace(Accessory):
    def __init__(self):
        super().__init__("Attack Necklace", "attack", 2)

    def equip(self, player):
        player.damage += self.effect_value

    def unequip(self, player):
        player.damage -= self.effect_value