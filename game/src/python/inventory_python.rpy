init python:
    class InvItem(object):
        def __init__(self, item_id, title, icon, description, count):
            self.id = item_id
            self.title = title
            self.icon = icon
            self.description = description
            self.count = count
    
    def inventory_item_click(item):
        if item.id == "order_history_2":
            use_order_history()
        if item.id == "potion_energy":
            use_potion_energy(item)
            remove_one_item()

    def remove_one_item(item):
        renpy.hide_screen("inventory_overlay")
        renpy.hide_screen("item_description")
        if item.count > 0:
            item.count -= 1

    def use_order_history():
        # if any(item.id == "unknown_seal" for item in inventory_items):
        #     return

        inventory_items.append(InvItem(
            "unknown_seal", 
            "Неизвестная печать",
            "images/misc/trillian_seal.png",
            "Неизвестная печать, оброненная незнакомцев в архивах Ордена",
            1
        ))

    def use_potion_energy(item):
        if item.count > 0:
            if hero.aspect > 0:
                hero.aspect -= 1
