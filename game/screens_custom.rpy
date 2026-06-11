default saved_music_pos = 0.0
default saved_music_file = None
define hovered_note = None
default hovered_inv_item = None
default journal_notes = [
    Note("main", "Задачи", "Здесь ты можешь записывать свои мысли."),
    Note("side", "Заметки", "Здесь можно хранить любую информацию, которая может пригодиться в будущем.")
]
default inventory_items = []
default isDebuffed = False
define long_fade = Fade(2.0, 0.5, 2.0)

# Основное меню
screen main_menu():
    tag menu

    # Добавление вашей картинки на фон
    add "images/bg/main_menu.png" xsize 1920 ysize 1080

    vbox:
        xpos 0.06
        ypos 0.4
        style_prefix "navigation"
        spacing 15
        
        # Заменяем сложную проверку на простую логику.
        if renpy.newest_slot(r"^\d.+"):
            textbutton _("Продолжить") action Continue(confirm=False)
        if renpy.list_saved_games(fast=True):
            textbutton _("Новая игра") action Confirm(
                _("Вы уверены? Это действие безвозвратно удалит ВСЕ текущие сохранения."), 
                yes=[Function(delete_all_saves), Start()]
            )
        else:
            textbutton _("Новая игра") action Start()
        textbutton _("Об игре") action ShowMenu("about")
        textbutton _("Выход") action Quit(confirm=not main_menu)

    fixed:
        style_prefix "main_menu"

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

# Модалка персонажа
screen char_stats():
    zorder 100 # Поверх остальных элементов (чтобы не перекрывался диалоговым окном)
    
    frame:
        xalign 0.02 # Отступ слева
        yalign 0.1 # Отступ сверху
        padding (20, 20, 20, 20) # Внутренние отступы рамки
        
        vbox:
            spacing 5 # Расстояние между строками
            text "{color=[hero.color]}[hero.name]{/color}":
                font "fonts/char.ttf"
                size 50
                xalign 0.5
            text "[hero.prof.value]":
                font "fonts/char.ttf"
                xalign 0.5
            if debug:
                text "Орден: [hero.ord_rel]"
                text "Культ: [hero.cult_rel]"
                text "Милосердие: [hero.humanity]"
                text "Разум: [hero.will]"
                text "Аспект: [hero.aspect]"
                text "Контроль: [hero.control]"
                text "Сон: [hero.dream]"
                text "Статус: [hero.state.value]"
            add [hero.image] zoom 0.25

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

# Оверлей ранения    
screen blood_overlay(hero_instance):    
    if hero_instance.state == STATE.INJURED:
        add "images/misc/state_gravely.png" alpha 0.5
    elif hero_instance.state == STATE.GRAVELY:
        $ debuff_stats(hero_instance)
        add "images/misc/state_gravely.png" matrixcolor SaturationMatrix(1.5) * BrightnessMatrix(-0.3) at blood_flash
        timer 10.0 action [SetField(hero, "state", STATE.DEAD), Jump("hero_died")]

# Кнопка инвентаря
screen inventory_button():
    modal False

    fixed:
        align (0.00, 0.6)
        xysize (320, 240)

        add Transform(
            "images/misc/inventory.png",
            zoom=0.27,
            alpha=1.0,
            matrixcolor=TintMatrix("#ff4800")
        ):
            align (0.5, 0.5)

        imagebutton:
            idle Transform("images/misc/inventory.png", zoom=0.25, alpha=0.9)
            hover Transform("images/misc/inventory.png", zoom=0.27, alpha=1.0)

            align (0.5, 0.5)
            action Show("inventory_overlay")

# Экран инвентаря
screen inventory_overlay():
    # Делаем экран модальным, чтобы КЛИКИ МИМО инвентаря НЕ листали диалог,
    # пока игрок смотрит вещи. Закрыть можно будет строго по крестику.
    modal True
    zorder 100

    add Solid("#000000AA")

    fixed:
        align (0.5, 0.5)
        xysize (1100, 1100)

        add "images/misc/inventory_inside.png"

        vpgrid:
            cols 4
            rows 4
            
            xpos 100
            ypos 80
            spacing 30
            
            for i, inv_item in enumerate(inventory_items):
                if inv_item.count > 0:
                    $ col = i % 4
                    $ row = i // 4

                    $ item_x = 100 + col * 230
                    $ item_y = 80 + row * 230

                    button at inventory_hover_effect:
                        xysize (200, 200)
                        background None

                        hovered Show("item_description", item=inv_item, item_x=item_x, item_y=item_y)
                        unhovered Hide("item_description")
                        action NullAction()

                        fixed:
                            xysize (200, 200)

                            add Transform(inv_item.icon, zoom=0.12):
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

# Кнопка журнала
screen journal_button():
    modal False

    fixed:
        align (0.11, 0.6)
        xysize (320, 240)

        add Transform(
            "images/misc/journal.png",
            zoom=0.27,
            alpha=1.0,
            matrixcolor=TintMatrix("#ff4800")
        ):
            align (0.5, 0.5)

        imagebutton:
            idle Transform("images/misc/journal.png", zoom=0.25, alpha=0.9)
            hover Transform("images/misc/journal.png", zoom=0.28, alpha=1.0)

            align (0.5, 0.5)
            action Show("journal_overlay")

# Кнопка целебного зелья
screen potion_button:
    modal False

    fixed:
        align (0.11, 0.7)
        xysize (320, 240)

        add Transform(
            "images/misc/potion.png",
            zoom=0.27,
            alpha=1.0,
            matrixcolor=TintMatrix("#ff4800")
        ):
            align (0.5, 0.5)

        imagebutton:
            idle Transform("images/misc/potion.png", zoom=0.25, alpha=0.9)
            hover Transform("images/misc/potion.png", zoom=0.28, alpha=1.0)

            align (0.5, 0.5)
            action Show("potion_overlay")

# Журнал
screen journal_overlay():
    zorder 300
    modal True

    add Solid("#000000AA")

    fixed:
        align (0.5, 0.15)
        xysize (1200, 700)

        add "images/misc/notes.png"

        vbox:
            xpos 100
            ypos 130
            spacing 10

            text "Заметки":
                size 100
                color "#c30b0b88"
                font "fonts/char.ttf"
                outlines [(1, "#5a3c28", 0, 0)]

            for note in journal_notes:
                button:
                    xalign 0.15
                    yalign 0.5

                    background None

                    vbox:
                        text "◊ [note.title]":
                            font "fonts/char.ttf"
                            size (80 if hovered_note == note.id else 70)
                            color ("#d25a14bc" if hovered_note == note.id else "#2b1a10d0")
                            outlines [(1, "#82390f", 0, 0)]

                    action Show("note_editor", note=note)
                    hovered SetVariable("hovered_note", note.id)
                    unhovered SetVariable("hovered_note", None)

        textbutton "❌":
            xalign 1.0
            yalign 0.0
            xoffset -20
            yoffset 45
            text_color "#2b1a10"
            background None
            action Hide("journal_overlay")

# Редактирование заметки
screen note_editor(note):
    zorder 400
    modal True

    add Solid("#00000099")

    fixed:
        align (0.6, 0.26)
        xysize (1200, 700)

        add "images/misc/notes.png"

        vbox:
            xpos 100
            ypos 130
            spacing 25

            text "[note.title]":
                font "fonts/char.ttf"
                size 80
                color "#a12727"
                outlines [(1, "#5a3c28", 0, 0)]

            input:
                value FieldInputValue(note, "text")
                font "fonts/char.ttf"
                multiline True
                length 2000
                xysize (960, 420)
                color "#2b1a10"
                size 60
                outlines [(1, "#82390f", 0, 0)]

        textbutton "❌":
            xpos 980
            ypos 600
            text_size 30
            text_color "#2b1a10"
            background None
            action Hide("note_editor")
        
        key "K_ESCAPE" action Hide("note_editor")

# Эффект зелья
screen potion_overlay():
    on "show" action SetField(hero, "state", STATE.GRAVELY)

    # Таймер на 3 секунды, который сработает один раз
    timer 3.0 action [
        SetField(hero, "state", STATE.HEALTHY), # Возвращаем здоровье
        Hide("potion_overlay")                  # Прячем экран автоматически
    ]

# Модалка персонажа
screen rpg_overlay():
    zorder 100 # Поверх остальных элементов (чтобы не перекрывался диалоговым окном)
    
    add Solid("#00000000") 

    frame:
        background None

        xalign 0.98 # Отступ слева
        yalign 0.05 # Отступ сверху
        padding (20, 20, 20, 20) # Внутренние отступы рамки
        
        vbox:
            use journal_button
            use inventory_button
            use potion_button

# Экран смертиы
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

# GUI
screen gui:
    use blood_overlay(hero)
    use char_stats
    use rpg_overlay