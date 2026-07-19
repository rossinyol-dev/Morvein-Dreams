# Экран глоссария
screen glossary_overlay():
    modal True
    zorder 100

    on "show" action Function(open_first_glossary_entry)

    add Solid("#000000AA")

    fixed:
        align (0.5, 0.5)
        xysize (1080, 1080)

        add "images/misc/glossary_inside.png"

        if glossary_entries:
            viewport:
                xpos 170
                ypos 230
                xysize (310, 670)

                mousewheel True
                draggable True
                scrollbars "vertical"
                yinitial 0.0

                vbox:
                    spacing 12

                    for entry in glossary_entries:
                        $ is_selected = entry.id == glossary_selected_entry_id
                        $ is_unread = entry.id not in glossary_read_entry_ids

                        button:
                            xysize (260, 72)
                            background Solid("#00000000")
                            hover_background Solid("#3a211644")
                            selected_background Solid("#6d351f44")
                            selected is_selected
                            action Function(open_glossary_entry, entry.id)

                            hbox:
                                spacing 10
                                yalign 0.5

                                if is_unread:
                                    text "•":
                                        font "fonts/char.ttf"
                                        size 32
                                        color "#b4531c"
                                        yalign 0.5
                                else:
                                    null width 18

                                text entry.title:
                                    font "fonts/char.ttf"
                                    size 30
                                    color ("#1f120d" if is_selected else "#000000")
                                    outlines [(1, "#8b6f3f", 0, 0)]
                                    xmaximum 215
                                    yalign 0.5

            $ selected_entry = get_glossary_entry(glossary_selected_entry_id)

            if selected_entry is not None:
                frame:
                    xpos 520
                    ypos 230
                    xysize (440, 670)
                    background Solid("#00000000")

                    viewport:
                        xfill True
                        yfill True
                        mousewheel True
                        draggable True

                        vbox:
                            spacing 24

                            text selected_entry.title:
                                font "fonts/char.ttf"
                                size 42
                                color "#2b1710"
                                outlines [(1, "#d0b27a", 0, 0)]

                            if selected_entry.sketch is not None:
                                add selected_entry.sketch:
                                    xalign 0.0
                                    fit "contain"
                                    xsize 240
                                    ysize 280

                            text selected_entry.text:
                                font "fonts/char.ttf"
                                size 30
                                color "#0f0b08"
                                line_spacing 6
                                xmaximum 420
        else:
            text "Записей пока нет.":
                align (0.5, 0.5)
                font "fonts/char.ttf"
                size 38
                color "#2b1710"

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

            action Hide("glossary_overlay")

    key "K_ESCAPE" action Hide("glossary_overlay")
