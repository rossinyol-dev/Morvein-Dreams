screen merchant_shop():
    modal True
    zorder 100

    add Solid("#000000AA")

    frame:
        align (0.5, 0.5)
        xysize (760, 640)
        background "#0b0b0bdd"
        padding (40, 35)

        vbox:
            spacing 24

            text "Лавка торговки":
                font "fonts/char.ttf"
                size 42
                color "#c8b28a"

            text "Золото: [get_gold_count()]":
                font "fonts/char.ttf"
                size 30
                color "#d6c49a"

            null height 10

            textbutton "Зелье исцеления — 40 золота":
                sensitive get_gold_count() >= 40
                action Function(
                    buy_shop_item,
                    "potion_hp",
                    "Зелье исцеления",
                    "images/misc/potion.png",
                    "Колба с мерцающей красной жидкостью внутри. Исцеляет даже самые тяжелые раны.",
                    40
                )

            textbutton "Зелье бодрости — 55 золота":
                sensitive get_gold_count() >= 55
                action Function(
                    buy_shop_item,
                    "potion_energy",
                    "Зелье бодрости",
                    "images/misc/potion_energy.png",
                    "Редкое зелье из черного вереска. Выпей — и кошмары отступят.",
                    55
                )

            textbutton "Яд — 75 золота":
                sensitive get_gold_count() >= 75
                action Function(
                    buy_shop_item,
                    "potion_poison",
                    "Яд",
                    "images/misc/potion_poison.png",
                    "Темная жидкость без запаха. Торговка не спрашивает, зачем он тебе.",
                    75
                )

            null height 20

            textbutton "Уйти":
                action Return()

    key "K_ESCAPE" action Return()