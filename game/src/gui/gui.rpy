
# Кнопка журнала
screen journal_button():
    modal False

    fixed:
        xysize (100, 100)

        add Transform(
            "images/misc/journal.png",
            zoom=0.20,
            alpha=1.0,
            matrixcolor=TintMatrix("#ff4800")
        ):
            align (0.5, 0.5)

        imagebutton:
            idle Transform("images/misc/journal.png", zoom=0.18, alpha=0.9)
            hover Transform("images/misc/journal.png", zoom=0.20, alpha=1.0)

            align (0.5, 0.5)
            # action Show("journal_overlay")
            action Show("journal_tbd_modal")

# TBD
screen journal_tbd_modal():
    modal True
    zorder 200

    button:
        background Solid("#000000AA")
        xfill True
        yfill True
        action Hide("journal_tbd_modal")

    frame:
        align (0.5, 0.5)
        background "#000000DD"
        padding (40, 30)

        text "Раздел в разработке":
            font "fonts/char.ttf"
            size 36
            color "#e6d2aa"

# Кнопка персонажа
screen char_button:
    modal False

    fixed:
        xysize (100, 100)

        add Transform(
            "images/misc/helmet.png",
            zoom=0.20,
            alpha=1.0,
            matrixcolor=TintMatrix("#ff4800")
        ):
            align (0.5, 0.5)

        imagebutton:
            idle Transform("images/misc/helmet.png", zoom=0.18, alpha=0.9)
            hover Transform("images/misc/helmet.png", zoom=0.20, alpha=1.0)

            align (0.5, 0.5)
            action Show("char_stats")

# Кнопка инвентаря
screen inventory_button():
    modal False

    fixed:
        xysize (100, 100)

        if inventory_new_item_alert or inventory_tutorial_blink or hero.state in (STATE.INJURED, STATE.GRAVELY):
            add Transform(
                "images/misc/inventory.png",
                zoom=0.22,
                matrixcolor=TintMatrix("#00ff08")
            ) at inventory_wound_blink:
                align (0.5, 0.5)
        else:
            add Transform(
                "images/misc/inventory.png",
                zoom=0.20,
                alpha=1.0,
                matrixcolor=TintMatrix("#ff4800")
            ) align (0.5, 0.5)


        imagebutton:
            idle Transform("images/misc/inventory.png", zoom=0.18, alpha=0.9)
            hover Transform("images/misc/inventory.png", zoom=0.20, alpha=1.0)

            align (0.5, 0.5)
            action [SetVariable("inventory_new_item_alert", False), Show("inventory_overlay")]
# HUD
screen hud():
    zorder 100 # Поверх остальных элементов (чтобы не перекрывался диалоговым окном)
    
    add Solid("#00000000") 

    frame:
        background None

        xalign 0.9 # Отступ слева
        yalign 0.05 # Отступ сверху
        
        hbox:
            spacing 100
            use char_button
            use inventory_button
            use journal_button

# GUI
screen gui:
    use blood_overlay(hero)
    use hud
