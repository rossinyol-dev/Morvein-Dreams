default inventory_items = []
default inventory_new_item_alert = False
default used_items = []

init python:
    class InvItem(object):
        def __init__(self, item_id, title, icon, description, count):
            self.id = item_id
            self.title = title
            self.icon = icon
            self.description = description
            self.count = count
    
    def add_inventory_item(item):
        inventory_items.append(item)
        renpy.store.inventory_new_item_alert = True

    def inventory_item_title(item):
        return renpy.translation.translate_string(item.title)

    def inventory_item_description(item):
        return renpy.translation.translate_string(item.description)

    def remove_item(item_id):
        for item in inventory_items:
            if item.id == item_id:
                inventory_items.remove(item)
                return

    def inventory_item_click(hero, item):
        if item.id == "order_history_1":
            use_order_history_first()
        if item.id == "order_history_2":
            use_order_history_second()
        if item.id == "girl_picture":
            use_girl_sketch()
        if item.id == "potion_energy":
            use_potion_energy(item)
            remove_one_item(item)
        if item.id == "potion_dream":
            use_potion_dream(item)
            remove_one_item(item)
        if item.id == "potion_hp":
            set_hero_state(hero, STATE.HEALTHY)
            remove_one_item(item)
        if item.id == "potion_poison":
            set_hero_state(hero, STATE.INJURED)
            remove_one_item(item)
        
    def remove_one_item(item):
        if item.count > 0:
            item.count -= 1

    def item_used(item_id):
        if item_id in store.used_items:
            return True
        else:
            store.used_items.append(item_id)
            return False

    def use_order_history_first():
        if not item_used("order_history_1"):
            texts = [
                "Ты изучаешь первый том хроники."
                "В разделе о древней истории Морвейна ты находишь список знатных семейств города и их гербы."
            ]
            renpy.call_in_new_context(
                "read_new_book", 
                texts,
                "images/misc/morvein_history_seals_2.png",
                True
            )

            renpy.store.order_history_explored_flag = True
        else:
            renpy.call_in_new_context("book_is_readed")

    def use_order_history_second():
        if not item_used("order_history_2"):
            texts = [
                "Ты изучаешь второй том хроники.",
                "Между страницами книги ты неожиданно находишь сложенный в несколько раз листок.",
                "На нем карандашом набросан портрет молодой обнаженной девушки.",
                "Интересно, кто оставил его здесь...",
                
            ]
            renpy.call_in_new_context(
                "read_new_book", 
                texts, 
                "images/misc/archivist_sketch_min.png"
            )

            add_inventory_item(InvItem(
                "girl_picture", 
                "Портрет девушки", 
                "images/misc/archivist_sketch_min.png", 
                "Карандашный портрет обнаженной девушки, найденный в книге.", 
                1
            ))
            
            renpy.store.girl_picture_found_flag = True
        else:
            renpy.call_in_new_context("book_is_readed")

    def use_girl_sketch():
        renpy.call_in_new_context(
            "read_new_book", 
            None, 
            "images/misc/archivist_sketch_min.png"
        )

    def use_potion_energy(item):
        if item.count > 0:
            renpy.store.inventory_tutorial_blink = False
            renpy.hide_screen("inventory_overlay")
            renpy.hide_screen("item_description")
            reduce_aspect(hero)
            renpy.call_in_new_context("potion_energy_relief")

    def use_potion_dream(item):
        if item.count > 0:
            add_aspect(hero)

    def get_inventory_item(item_id):
        for item in inventory_items:
            if item.id == item_id:
                return item
        return None

    def has_inventory_item(item_id):
        return get_inventory_item(item_id) is not None

    def get_gold_count():
        coins = get_inventory_item("coins")
        if coins:
            return coins.count
        return 0

    def remove_all_gold():
        coins = get_inventory_item("coins")
        if coins:
            coins.count = 0

    def add_or_stack_item(new_item):
        existing = get_inventory_item(new_item.id)

        if existing:
            existing.count += new_item.count
        else:
            inventory_items.append(new_item)

        renpy.store.inventory_new_item_alert = True

    def buy_shop_item(item_id, title, icon, description, price):
        coins = get_inventory_item("coins")

        if not coins or coins.count < price:
            return

        coins.count -= price

        add_or_stack_item(InvItem(
            item_id,
            title,
            icon,
            description,
            1
        ))
    

