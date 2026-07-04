# Оверлей сна
screen dream_text_overlay(dream_text, display_time):
    # Создаем свою плашку без привязки к системным say_window
    frame:
        # Центрируем по горизонтали и опускаем вниз экрана (0.88 — стандартная высота для диалогов)
        xalign 0.5
        yalign 0.88
        
        # Размеры плашки (можете настроить под свой интерфейс)
        xminimum 800
        xmaximum 1200
        yminimum 150
        
        # Делаем плашку полупрозрачной черной (или укажите свой background)
        background Solid("#000000a0") 
        padding (20, 20)

        # Выводим сам текст строго по центру нашей плашки
        text dream_text:
            xalign 0.5
            yalign 0.5
            text_align 0.5

    # Таймер закрытия экрана
    timer display_time action Return()

# Модалка выбора персонажа
screen char_choice():
    modal True
    add "#00000080"

    # Переменная для отслеживания наведения (0 - никто, 1 - Мильтон, 2 - Фальк)
    default hovered_char = 0

    grid 2 1:
        xfill True
        yfill True
        spacing 0

        # --- ЛЕВАЯ ПОЛОВИНА (Мильтон) ---
        fixed:
            imagebutton:
                xsize 0.5         # Занимает ровно 50% ширины экрана
                ysize 1.0         # Занимает 100% высоты экрана
                auto "chars/hero_milton_%s.png"
                
                yoffset -80
                xoffset -80

                hovered SetScreenVariable("hovered_char", 1)
                unhovered SetScreenVariable("hovered_char", 0)
                action Return("choice_1")

            # Блок текста для Мильтона
            if hovered_char == 1:
                vbox:
                    align (0.5, 0.9)      # Центрируем весь блок внутри левой половины
                    # Ограничиваем ширину текста, чтобы он не упирался в края (минус отступы 50px с двух сторон)
                    # Если экран 1920x1080, то половина — это 960. Делаем блок шириной 860.
                    xsize 0.9             # Занимает 90% от ширины своей половины экрана
                    spacing 15            # Промежуток между элементами (заменяет пустую строку)

                    text "Мильтон":
                        xalign 0.5        # Имя строго по центру блока
                        size 40           # Крупный шрифт для имени
                        color "#fff"
                        outlines [ (2, "#000", 0, 0) ]

                    text "Бывший монах Ордена. Служил в храме Морвейна много лет, прежде чем покинуть его. Годы служения сделали его черствым к людским слабостям, а увиденные странности стали проникать в его сновидения.":
                        xalign 0.0        # Описание начинается слева
                        text_align 0.0    # Выравнивание строк длинного текста по левому краю
                        size 24           # Шрифт для описания чуть меньше
                        color "#e0e0e0"
                        outlines [ (2, "#000", 0, 0) ]

        # --- ПРАВАЯ ПОЛОВИНА (Фальк) ---
        fixed:
            imagebutton:
                xsize 0.5         # Занимает ровно 50% ширины экрана
                ysize 1.0         # Занимает 100% высоты экрана
                auto "chars/hero_falk_%s.png"
                
                hovered SetScreenVariable("hovered_char", 2)
                unhovered SetScreenVariable("hovered_char", 0)
                action Return("choice_2")

            # Блок текста для Фалька
            if hovered_char == 2:
                vbox:
                    align (0.5, 0.9)      # Центрируем весь блок внутри правой половины
                    xsize 0.9             # Занимает 90% от ширины своей половины экрана
                    spacing 15            # Промежуток между элементами (заменяет пустую строку)

                    text "Фальк":
                        xalign 0.5        # Имя строго по центру блока
                        size 40
                        color "#fff"
                        outlines [ (2, "#000", 0, 0) ]

                    text "Блестящий столичный лекарь. Попал в немилость из-за смерти влиятельного горожанина. Оказался в Морвейне совсем недавно, но уже заслужил уважение местных. Милосерден и крайне рационален, в происходящем в Морвейне пытается найти научное объяснение.":
                        xalign 0.0        # Описание начинается слева
                        text_align 0.0    # Выравнивание строк длинного текста по левому краю
                        size 24
                        color "#e0e0e0"
                        outlines [ (2, "#000", 0, 0) ]

# Экран смерти
label hero_died:
    image death_message = Text("ВАШ ПУТЬ ОКОНЧЕН", style="death_style")

    # Скрываем экран с кровью, так как персонаж уже мертв
    hide screen gui

    scene black with fade 
    
    $ renpy.music.queue([], channel='music', clear_queue=True)
    $ renpy.music.stop(channel='music', fadeout=3)
    $ renpy.pause(3, hard=True)

    # 2. Включаем звук смерти
    # Используем канал sound (для разовых эффектов), чтобы музыкальный канал оставался свободным
    play sound "audio/fx/death.mp3"

    # Показываем текст ниже картинки (xalign 0.5 отцентрирует по горизонтали)
    show expression "images/misc/state_dead.png" at Transform(xalign=0.5, yanchor=0.5, ypos=0.40)
    show death_message at Transform(xalign=0.5, yanchor=0.5, ypos=0.80)
    
    # Обязательно добавляем паузу, иначе игра сразу закроется!
    # Игрок увидит картинку с текстом и сможет нажать клик для выхода.
    $ renpy.pause()
    
    return

# Экран смерти
label to_be_continued:
    image tbc_message = Text("ПРОДОЛЖЕНИЕ СЛЕДУЕТ", style="death_style")

    # Скрываем экран с кровью, так как персонаж уже мертв
    hide screen gui

    scene black with fade 

    # Показываем текст ниже картинки (xalign 0.5 отцентрирует по горизонтали)
    show expression "images/misc/hourglass.png" at Transform(xalign=0.5, yanchor=0.5, ypos=0.40)
    show tbc_message at Transform(xalign=0.5, yanchor=0.5, ypos=0.80)
    
    # Обязательно добавляем паузу, иначе игра сразу закроется!
    # Игрок увидит картинку с текстом и сможет нажать клик для выхода.
    $ renpy.pause()
    
    return

# Сцена сна
label dream_scene(texts_start = [], horror_char = None, texts_horror = [], texts_end = [], show_gui_after = True):
    hide screen gui
    with fade

    $ renpy.show("black", zorder=-100)

    $ start_dream_effect()

    $ old_skip = preferences.skip_unseen
    $ preferences.skip_unseen = False

    python:
        for text in texts_start:
            dream(text)
            renpy.pause(2.0, hard=True)

    if texts_horror:
        if horror_char:
            show expression horror_char as horror_character
            with dissolve

        python:
            for text in texts_horror:
                horror(text)
                renpy.pause(2.0, hard=True)

    if texts_end:
        python:
            for text in texts_end:
                dream(text)
                renpy.pause(2.0, hard=True)

    hide horror_character
    with dissolve

    if show_gui_after:
        show screen gui(hero)
        with fade

    $ stop_dream_effect()

    $ preferences.skip_unseen = old_skip

    return

label tutorial_text:
    if tutorial_shown_flag:
        return

    scene black with fade
    show screen gui(hero)

    narrator "Добро пожаловать в Сны Морвейна!"
    narrator "Это нарративная игра с элементами визуальной новеллы и RPG в позднесредневековом стиле."
    narrator "В ней вам предстоит погрузиться в мир, где каждый выбор имеет подследствия, а ваши действия формируют судьбу героя и целого города."
    narrator "В правом верхнем углу находится иконка персонажа. Нажав на нее, вы увидите описание героя и его состояние."
    narrator "В инвентаре вы найдете предметы, которые помогут вам в путешествии. Некоторые из них можно использовать, а некоторые — изучить."
    narrator "Не ждите от игры привычных подсказок — здесь многое решает ваша внимательность и способность анализировать происходящее."
    narrator "Да пребудет с вами Сила!"

    $ tutorial_shown_flag = True

    return

transform act_title_fade:
    alpha 0.0
    yoffset 18
    ease 1.4 alpha 1.0 yoffset 0
    pause 1.4
    ease 1.0 alpha 0.0 yoffset -12

screen act_title_screen(act_title, act_subtitle=None, display_time=3.8):
    zorder 1000
    modal True

    add Solid("#000000")

    button:
        xfill True
        yfill True
        background None
        action Return()

    vbox at act_title_fade:
        xalign 0.5
        yalign 0.48
        spacing 28

        text act_title:
            xalign 0.5
            text_align 0.5
            font "fonts/char.ttf"
            size 72
            color "#d8c08a"
            outlines [(2, "#000000", 0, 0)]

        add Solid("#8b1f1f"):
            xalign 0.5
            xsize 420
            ysize 2

        if act_subtitle:
            text act_subtitle:
                xalign 0.5
                text_align 0.5
                font "fonts/char.ttf"
                size 34
                color "#d9d2c0"
                outlines [(2, "#000000", 0, 0)]

    timer display_time action Return()

label show_act_title(act_title, act_subtitle=None, display_time=3.8):
    hide screen gui
    call screen act_title_screen(act_title, act_subtitle, display_time)
    return

screen soft_vignette(fade_time=3.0):
    zorder 100
    add "images/effects/vignette_soft_1920x1080.png" at vignette_fade_in(fade_time)

screen soft_vignette_hide(fade_time=3.0):
    zorder 100
    add "images/effects/vignette_soft_1920x1080.png" at vignette_fade_out(fade_time)

label show_vignette(fade_time=3.0):
    show screen soft_vignette(fade_time)
    return

label hide_vignette(fade_time=3.0):
    hide screen soft_vignette
    show screen soft_vignette_hide(fade_time)
    $ renpy.pause(fade_time, hard=True)
    hide screen soft_vignette_hide
    return

screen cinematic_dialogue(text, show_time=4.0, fade_out_time=0.8, centered=False, italic=False):
    zorder 200
    modal True

    $ display_text = "{i}" + text + "{/i}" if italic else text

    key "dismiss" action NullAction()
    key "rollback" action NullAction()
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()

    window:
        style "window"
        at cinematic_dialogue_fade_in_out(show_time, fade_out_time)

        if centered:
            text display_text:
                style "say_dialogue"
                xalign 0.5
                text_align 0.5
        else:
            text display_text:
                style "say_dialogue"

    timer show_time action Return()

label cinematic_narrator(text, show_time=4.0, hide_time=2.0, centered=False, italic=False):
    $ fade_out_time = min(0.8, show_time)
    call screen cinematic_dialogue(text, show_time, fade_out_time, centered, italic)
    $ renpy.pause(hide_time, hard=True)
    return

transform cinematic_dialogue_fade_in_out(show_time=4.0, fade_out_time=0.8):
    alpha 0.0
    yoffset 24
    ease 0.8 alpha 1.0 yoffset 0
    pause max(0.0, show_time - 0.8 - fade_out_time)
    ease fade_out_time alpha 0.0 yoffset 24

transform vignette_fade_in(fade_time=3.0):
    alpha 0.0
    linear fade_time alpha 1.0

transform vignette_fade_out(fade_time=3.0):
    alpha 1.0
    linear fade_time alpha 0.0


