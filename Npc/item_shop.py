from pico2d import *
from accessory import *
from sound_manager import SoundManager

class ItemShop:
    def __init__(self, player):
        self.player = player
        self.image = load_image('resource/npc/item_npc_ui.png')
        self.items = [
            {'rect': (500, 490, 730, 580), 'name': 'Health Potion', 'price': 50},
            {'rect': (500, 300, 730, 400), 'name': 'Health Necklace', 'price': 100},
            {'rect': (500, 100, 730, 230), 'name': 'Stamina Necklace', 'price': 100},
            {'rect': (760, 490, 1000, 580), 'name': 'Attack Necklace', 'price': 150},
            {'rect': (760, 300, 1000, 400), 'name': 'Parring assistant Necklace', 'price': 200},
            {'rect': (760, 100, 1000, 230), 'name': 'Parring Damage Necklace', 'price': 250}
        ]
        self.sound = SoundManager()
        try:
            self.sound.load_sfx("resource/sound/buy.mp3", 'buy_sound')
        except Exception:
            pass

    def draw(self):
        self.image.clip_composite_draw(0, 0, 1472, 704, 0, '', 640, 360, 800, 600)

    def update(self):
        pass

    def handle_click(self, x, y):
        for item in self.items:
            left, bottom, right, top = item['rect']
            if left <= x <= right and bottom <= y <= top:
                if self.player.gold >= item['price']:
                    self.add_item(self.player, item)
                    print(f"Purchased {item['name']} for {item['price']} gold.")
                    try:
                        self.sound.play_sfx('buy_sound', volume=0.5)
                    except Exception:
                        pass
                else:
                    print("Not enough gold to purchase this item.")
                return

    def add_item(self, player, item):
        if player.gold >= item['price']:

            if item.get('name') == 'Health Potion':
                if player.hp + 5 <= player.max_hp:
                    player.hp += 5
                else:
                    player.hp = player.max_hp
            elif player.accessory_count < 2:
                if item.get('name') == 'Health Necklace':
                    player.equip_accessory(HealthNecklace())
                elif item.get('name') == 'Stamina Necklace':
                    player.equip_accessory(StaminaNecklace())
                elif item.get('name') == 'Attack Necklace':
                    player.equip_accessory(AttackNecklace())
                elif item.get('name') == 'Parring assistant Necklace':
                    player.equip_accessory(ParringAssistantNecklace())
                elif item.get('name') == 'Parring Damage Necklace':
                    player.equip_accessory(ParringDamageNecklace())
            else:
                print("Cannot equip more than 2 accessories.")
                return
            player.gold -= item['price']