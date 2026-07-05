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
                            action Function(inventory_item_click, hero, inv_item)

                            fixed:
                                xysize (200, 200)

                                add Transform(inv_item.icon, zoom=0.14):
                                    align (0.5, 0.5)

                                text "[inv_item.title] (x[inv_item.count])":
                                    yoffset 20
                                    xalign 0.5
                                    ypos 150
                                    text_align 0.5
                                    xmaximum 200
                                    font "fonts/char.ttf"
                                    size 23
                                    color "#000000"
                                    outlines [(1, "#475544", 0, 0)]
        imagebutton:
            align (0.903, 0.108)

            idle Transform(
                "images/misc/cross.png",
                zoom=0.2,
                alpha=0.8
            )
            hover Transform(
                "images/misc/cross.png",
                zoom=0.2,
                alpha=1.0
            )

            action [SetVariable("inventory_tutorial_blink", False), Hide("inventory_overlay")]
             
    key "K_ESCAPE" action [SetVariable("inventory_tutorial_blink", False), Hide("inventory_overlay"), Hide("item_description")]

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

# Превью предмета
screen fullscreen_item_preview(image_path):
    modal True
    zorder 200

    add Solid("#000000cc")

    add image_path:
        xalign 0.5
        yalign 0.5      
        fit "contain"
        xsize 1600
        ysize 900

    textbutton "Закрыть":
        text_font "fonts/char.ttf"
        xalign 0.5
        yalign 0.975
        action Return()

# Чтение книг
label read_new_book(texts = None, preview_image_path = None, action = None):
    hide screen inventory_overlay
    hide screen item_description

    if texts is None:
        $ texts = []

    python:
        for text in texts:
            renpy.say("narrator", text)

    if preview_image_path:
        call screen fullscreen_item_preview(preview_image_path)

    if action:
        call cut_book_page()
                
    return

label book_is_readed:
    hide screen inventory_overlay
    hide screen item_description

    narrator "Книга уже прочитана."

    return

label cut_book_page:
    menu:
        "Вырвать страницу из книги":
            narrator "Ты вырываешь страницу из книги — вдруг еще пригодится."
            $ add_inventory_item(InvItem(
                "morvein_history_torn", 
                "Страница хроники", 
                "images/misc/morvein_history_torn.png", 
                "Вырванная страница из хроники Морвейна, в которой рассказывается об истории рода Триллианов.", 
                1
            ))
        "Не вырывать":
            narrator "Ты решаешь не портить артефакт древности."
