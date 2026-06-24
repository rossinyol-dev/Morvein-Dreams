# Модалка персонажа
screen char_stats():
    modal True
    zorder 100

    add Solid("#000000AA")

    fixed:
        align (0.5, 0.5)
        xysize (1920, 1080)

        add "images/misc/char_list.png"

        hbox:
            align (0.5, 0.5)
            spacing 200

            add hero.portrait:
                xoffset 75
                xysize (500, 750)

            vbox:
                yalign 0.5
                yoffset 50
                spacing 30
                xysize (900, 800)
                style_prefix "char_page_style"

                vbox:
                    spacing 20
                    yoffset 20

                    text "[hero.name]"
                    text "[hero.prof.value]"
                    text "[hero_state_desc(hero.state)]"

                vbox:
                    spacing 20
                    yoffset -50

                    text "[stat_desc(hero.mercy, mercy_desc, mercy_colors)]"
                    text "[stat_desc(hero.reason, reason_desc, reason_colors)]"
                    text "[stat_desc(hero.aspect, aspect_desc, aspect_colors)]"
                    text "[stat_desc(hero.control, control_desc, control_colors)]"

                    if debug:
                        text "М — ([hero.mercy]), Р — ([hero.reason])"
                        text "A — ([hero.aspect]), K — ([hero.control])"

        imagebutton:
            align (0.94, 0.105)

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

            action Hide("char_stats")

    key "K_ESCAPE" action Hide("char_stats")

# Оверлей ранения    
screen blood_overlay(hero_instance):    
    if hero_instance.state == STATE.INJURED:
        add "images/misc/state_gravely.png" alpha 0.5
    elif hero_instance.state == STATE.GRAVELY:
        add "images/misc/state_gravely.png" matrixcolor SaturationMatrix(1.5) * BrightnessMatrix(-0.3) at blood_flash
        timer 20.0 action [SetField(hero, "state", STATE.DEAD), Jump("hero_died")]