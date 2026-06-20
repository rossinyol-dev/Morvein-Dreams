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
                spacing 30
                xysize (900, 800)
                style_prefix "char_page_style"

                vbox:
                    spacing 40
                    yoffset 20

                    text "{color=[hero.color]}[hero.name]{/color}"
                    text "[hero.prof.value]"
                    text "Состояние персонажа: [hero.state.value]"

                vbox:
                    spacing 20
                    yoffset -50

                    text "[stat_desc(hero.mercy, mercy_desc, mercy_colors)]"
                    text "[stat_desc(hero.reason, reason_desc, reason_colors)]"
                    text "[stat_desc(hero.aspect, aspect_desc, aspect_colors)]"
                    text "[stat_desc(hero.control, control_desc, control_colors)]"

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