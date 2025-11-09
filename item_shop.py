from pico2d import *

class ItemShop:
    def __init__(self):
        self.image = load_image('resource/npc/item_npc_ui.png')
        self.items = [
            {'rect': (500, 490, 730, 580), 'name': 'Health Potion', 'price': 50},
            {'rect': (500, 300, 730, 400), 'name': 'Health Bracelet', 'price': 100},
            {'rect': (500, 100, 730, 230), 'name': 'Stamina Bracelet', 'price': 100},
            {'rect': (760, 490, 1000, 580), 'name': 'Attack Bracelet', 'price': 150},
            {'rect': (760, 300, 1000, 400), 'name': 'Parring assistant Bracelet', 'price': 200},
            {'rect': (760, 100, 1000, 230), 'name': 'Parring Damage Bracelet', 'price': 250}
        ]

    def draw(self):
        self.image.clip_composite_draw(0, 0, 1472, 704, 0, '', 640, 360, 800, 600)
        for item in self.items:
            left, bottom, right, top = item['rect']
            draw_rectangle(left, bottom, right, top)

    def update(self):
        pass