style vscrollbar:
    xsize 32
    ysize 500
    ypos 150
    xpos 30
    base_bar Frame("misc/scroll.png", 8, 256)
    thumb Frame("misc/thumb.png", 8, 64)
    unscrollable "hide"

# Экран инвентаря
screen inventory_overlay():
    # Делаем экран модальным, чтобы КЛИКИ МИМО инвентаря НЕ листали диалог,
    # пока игрок смотрит вещи. Закрыть можно будет строго по крестику.
    modal True
    zorder 100

    add Solid("#000000AA")

    fixed:
        align (0.5, 0.5)
        xysize (1080, 1080)

        add "images/misc/inventory_inside.png"

        viewport:
            xpos 225
            ypos 175
            xysize (700, 750)

            mousewheel True
            draggable True
            scrollbars "vertical"
            yinitial 0.0

            vpgrid:
                cols 3
                spacing 20

                for i, inv_item in enumerate(inventory_items):
                    if inv_item.count >= 0:

                        $ col = i % 3
                        $ row = i // 3

                        $ item_x = 225 + col * 220
                        $ item_y = 120 + row * 220

                        button at inventory_hover_effect:
                            xysize (200, 250)
                            background None

                            hovered Show("item_description", item=inv_item, item_x=item_x, item_y=item_y)
                            unhovered Hide("item_description")
                            action Function(inventory_item_click, inv_item)

                            fixed:
                                xysize (200, 200)

                                add Transform(inv_item.icon, zoom=0.14):
                                    align (0.5, 0.5)

                                text "[inv_item.title] (x[inv_item.count])":
                                    xalign 0.5
                                    ypos 150
                                    text_align 0.5
                                    xmaximum 200
                                    font "fonts/char.ttf"
                                    size 24
                                    color "#000000"
                                    outlines [(1, "#475544", 0, 0)]
        imagebutton:
            align (0.91, 0.102)

            idle Transform(
                "images/misc/cross.png",
                zoom=0.24,
                alpha=0.8
            )
            hover Transform(
                "images/misc/cross.png",
                zoom=0.24,
                alpha=1.0
            )

            action Hide("inventory_overlay")
            
    key "K_ESCAPE" action Hide("inventory_overlay")

# Описание предметов
screen item_description(item, item_x, item_y):
    zorder 200

    frame:
        background "#000000DD"

        xpos item_x + 420
        ypos item_y + 210
        padding (20, 20)

        vbox:
            spacing 10

            text item.title:
                font "fonts/char.ttf"
                size 30
                color "#b4531c"

            text item.description:
                font "fonts/char.ttf"
                size 30
                color "#e6d2aa"
                xmaximum 360
