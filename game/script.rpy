# Вы можете расположить сценарий своей игры в этом файле.

# Глобальные настройки
define debug = True
define config.menu_include_disabled = debug
define config.rollback_enabled = debug
define config.default_afm_enable = debug
define quick_menu = False
default preferences.afm_enable = True
default preferences.afm_after_click = False
default preferences.afm_time = 7.0

define config.has_autosave = True
define config.autosave_on_choice = False
define config.autosave_on_quit = False
define config.autosave_frequency = None
define config.keymap['quick_save'] = []
define config.keymap['quick_load'] = []

# Флаги квестов
define beggar_flag_help = False

# Стили текста
style dream_style:
    font "fonts/dream.ttf"
    size 32
    color "#8f12c5"

style check_style:
    font "fonts/check.ttf"
    size 32
    color "#1ae9db"

# Настраиваем внешний вид текста (размер, цвет, шрифт)
style death_style:
    font "fonts/dream.ttf"
    xalign 0.5
    size 60
    color "#ffffff"
    outlines [ (2, "#000000", 0, 0) ] # Черный контур, чтобы текст читался на любом фоне

init:
    transform slow_shaking:
        # 1-й цикл: плавно опускаемся и темнеем за 0.5 сек
        linear 1.0 yoffset 15 matrixcolor BrightnessMatrix(-0.5)
        linear 1.0 yoffset -15 matrixcolor BrightnessMatrix(0.0)
        
        # 2-й цикл
        linear 1.0 yoffset 15 matrixcolor BrightnessMatrix(-0.5)
        linear 1.0 yoffset -15 matrixcolor BrightnessMatrix(0.0)

        # Финал: возвращаем экран в центр за 0.5 сек
        linear 0.5 yoffset 0 matrixcolor BrightnessMatrix(0.0)

# Определение Python типов и функций
init python:
    import enum

    class STATE(enum.Enum):
        HEALTHY = "Здоров"
        INJURED = "Ранен"
        GRAVELY = "Умирает"
        DEAD = "Мертв"

    class PROF(enum.Enum):
        DOCTOR = "Доктор"
        MONK = "Монах"

    class Hero:
        def __init__(self, name, prof, state, humanity, will, aspect, control, dream, ord_rel, cult_rel, image, color):
            self.name = name
            self.prof = prof
            self.state = state
            self.humanity = humanity
            self.will = will
            self.aspect = aspect
            self.control = control
            self.ord_rel = ord_rel
            self.cult_rel = cult_rel
            self.image = image
            self.color = color
            self.dream = dream

    def delete_all_saves():
        for slot in renpy.list_saved_games(fast=True):
            renpy.unlink_save(slot)

    def passive_check(stat, min_value, text, altText, addDream):
        if(stat) >= min_value:
            renpy.sound.play("audio/fx/dream_fx.mp3") 

    def add_stat(hero_object, stat_name, value):
        # Получаем текущее значение свойства
        current_value = getattr(hero_object, stat_name)
        # Записываем новое измененное значение
        setattr(hero_object, stat_name, current_value + value)
        # Воспроизводим звук
        renpy.sound.play("audio/fx/pass_fx.mp3")

    def check_dream(min_value, text):
        if hero.dream > min_value:
            # Начинаем отображение сна
            renpy.transition(fade)
            renpy.sound.play("audio/fx/dream_fx.mp3") 
            
            # Трясем экран
            renpy.show("black", layer="bottom") 
            renpy.layer_at_list([slow_shaking], layer='master')
            renpy.say(None, f"{{=dream_style}}{text}{{/=dream_style}}", interact=True)
            renpy.layer_at_list([], layer='master')
            renpy.hide("black", layer="master")
            
            # Завершаем отображение сна
            renpy.transition(fade)

# Персонажи
define beggar = Character('Нищий', color="#7c9703")
define stefan = Character('Отец Стефан', color="#b02d2d")
define cultist = Character('Культист', color="#6a4001")
            
# Картинки фонов
image morvein_start = im.Scale("bg/morvein_start.png", 1920, 1080)
image morvein_streets = im.Scale("bg/morvein_streets.png", 1920, 1080)
image temple_inside = im.Scale("bg/temple_inside.png", 1920, 1080)
image temple_outside = im.Scale("bg/temple_outside.png", 1920, 1080)
image temple_interrogation_room = im.Scale("bg/temple_interrogation_room.png", 1920, 1200)
image temple_hospital = im.Scale("bg/temple_hospital.png", 1920, 1200)
image morvein_from_temple = im.Scale("bg/morvein_from_temple.png", 1920, 1200)

# Картинки персонажей
image stefan default = Transform("images/chars/stefan_default.png", zoom=0.6)
image beggar default = Transform("images/chars/beggar_default.png", zoom=0.6)
image cultist default = Transform("images/chars/cultist_default.png", xzoom=0.65, yzoom=0.7)
image sleepwalkers default = Transform("images/chars/sleepwalkers.png", xzoom=0.65, yzoom=0.7)

# Кровавое мигание
transform blood_flash:
    # Задаем начальную прозрачность без привязки к событиям
    alpha 1.0 
    # Бесконечный цикл мигания
    block:
        linear 1.0 alpha 0.3  # За полсекунды затухает до 30%
        linear 1.0 alpha 1.0  # За полсекунды возвращается к 100%
        repeat

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
        add "images/misc/state_gravely.png" matrixcolor SaturationMatrix(1.5) * BrightnessMatrix(-0.3) at blood_flash
        timer 10.0 action [SetField(hero, "state", STATE.DEAD), Jump("hero_died")]

# Сценарий
label start:
    $ quick_menu = debug
    $ _skipping = debug
    $ _game_menu_screen = None
    $ preferences.afm_enable = not debug
    $ preferences.afm_time = 10.0

    scene morvein_start
    with fade

    play music "audio/main_theme.m4a"

    "Дождь шел уже шестой день подряд.
    Морвейн всегда пах одинаково: мокрым камнем, 
    свечным воском и затхлой водой из старых каналов."

    "Горожане давно перестали замечать этот запах. Как и многое другое."

    "Ночные колокола.
    Людей, засыпающих прямо посреди разговора.
    Детей, которые по утрам рассказывают о местах, где никогда не были."

    "В Морвейне привыкли не задавать лишних вопросов. Особенно ночью."

    "Но ты оказался здесь не случайно.
    У каждого,
    кто приезжает в Морвейн,
    есть своя причина.
    Своя история."
    "И свои сны."

    with fade
    call screen char_choice()
    $ result = _return
    with fade

    # Обрабатываем выбор героя
    if result == "choice_1":
        $ hero = Hero("Мильтон", PROF.MONK, STATE.HEALTHY, 0, 2, 5, 5, 3, 3, 0, "images/chars/hero_milton_idle.png", "#f00")
        
        show screen char_stats

        "Когда-то ты уже жил в Морвейне.
        Годы спустя ты почти убедил себя,
        что детские молитвы,
        доносящиеся из-под собора,
        были лишь кошмаром.
        Но прошлой ночью ты снова услышал их во сне."

    elif result == "choice_2":
        $ hero = Hero("Фальк", PROF.DOCTOR, STATE.HEALTHY, 4, 4, 2, 2, 0, 0, 0, "images/chars/hero_falk_idle.png", "#593ed0")

        show screen char_stats

        "Первого пациента привели к тебе четыре дня назад.
        Мальчик не просыпался двое суток.
        Во сне он неустанно повторял одно слово на неизвестном языке."
        "Через день он исчез из палаты."

    show screen blood_overlay(hero)

    "Морвейн никогда не засыпал.
    По крайней мере,
    не так, как другие города."
    "Даже глубокой ночью
    в переулках горел свет.
    Люди ходили быстро,
    редко смотрели друг другу в глаза
    и всегда запирали двери до наступления темноты."

    "Над городом возвышался собор Ордена.
    Звон его колоколов определял жизнь Морвейна: когда работать, когда молиться, когда оставаться дома."
    "Говорили, что монахи могут распознать лунатика еще до того, как тот впервые заговорит во сне."

    "Под улицами Морвейна тянулись старые катакомбы.
    Некоторые тоннели давно обрушились.
    Некоторые — исчезли с карт Ордена."

    "Люди перешептывались между собой,
    что из этих катакомб по ночам можно услышать тяжелые шаги
    там, где уже много лет никого не было."

    "За северными воротами начинался лес, сырой и слишком тихий."
    "Дети иногда уходили туда во сне. И не всегда возвращались назад."

    "По разговорам людей становилось очевидным, что сон все сильнее проникает в Морвейн.
    И нынешний настоятель Ордена просил твоей помощи."

    menu:
        "Отправиться в собор":
            jump morvein_streets

label morvein_streets:
    scene morvein_streets
    with fade

    "Чем глубже ты заходишь в город, тем больше удушливое чувство всеобщего страха проникает в тебя."
    "Люди стараются не задерживаться на улицах. Некоторые, заметив твой взгляд, сразу опускают голову."

    "У перекрестка ты замечаешь человека, неподвижно стоящего под дождем с закрытыми глазами."
    "Словно почуяв твое присутствие издалека, он начинает медленно идти в твою сторону."
    "Ты ускоряешь шаг и переходишь на соседнюю улицу, продолжая двигаться вперед."

    with fade
    
    "Из приоткрытого окна доносится приглушенный спор."
    "— Нужно было отвести мальчика в собор раньше, он почти не просыпается...
    \n— Замолчи!"
    "Голоса резко стихают, когда ты проходишь мимо."

    with fade

    "Впереди снова звучит колокол, на этот раз ближе. Гул медленно прокатывается по улицам Морвейна, 
    и тебе кажется, будто город на мгновение замирает, прислушиваясь к нему."

    "Двое прохожих торопливо проходят мимо тебя"
    "— Говорят, этой ночью снова видели культистов у катакомб..."
    "Остаток фразы тонет в шуме дождя."

    "Дойдя до конца очередной тесной улицы, ты видишь как впереди сквозь туман проступают темные шпили собора." 

    jump temple_outside   

label temple_outside:
    scene temple_outside
    with fade

    "Собор Ордена возвышается над Морвейном,
    словно исполинский часовой.
    Его башни теряются в тумане,
    а дождь стекают по черному камню,
    будто собор никогда не высыхает полностью."

    "На фасаде нет ни ликов святых,
    ни привычных символов веры - 
    только фигуры с закрытыми глазами и опущенными головами.
    Кажется, будто так они прислушиваются ко всему происходящему вокруг."

    "Главные ворота настолько высоки,
    что человек рядом с ними кажется ребенком.
    Тяжелые створки покрывают резные узоры,
    напоминающие не то волны, не то человеческие веки."

    "Говорили,
    что монахи Ордена почти не спят.
    Что под собором находятся старые залы,
    куда не допускают даже послушников."

    "И что иногда,
    если долго стоять у стен в полной тишине,
    можно услышать пение,
    доносящееся откуда-то снизу."

    "Когда ты подходишь к храму ближе,
    колокола над городом снова начинают тревожно звучать.
    словно предупреждая Морвейн о чьем-то прибытии."

    "У стены собора сидит сгорбленный калека,
    укрывшись рваным плащом от дождя.
    Одна его нога заканчивается ниже колена,
    а пальцы дрожат так сильно,
    будто он никак не может согреться.
    Перед ним лежит деревянная чаша,
    почти пустая."

    "Когда ты проходишь мимо, то он обращает на тебя свой полуслепой взгляд, устремленный куда-то вдаль."

    show beggar default at center
    with dissolve

    if hero.prof == PROF.MONK:
        "Заметив на твоих одеждах знаки Ордена, попрошайка с почтительным ужасом отходит в сторону, пропуская тебя к дверям собора."
    else:
        beggar "Они снова поют сегодня ночью..."
        beggar "Значит, кто-то опять не проснется..."
        beggar "Опять..."
        
        menu:
            "Бросить монетку":
                "Поравнявшись с ним, ты кидаешь несчастному монетку в его почти пустую чашу. Взгляд нищего на секунду становится осмысленным, и он благодарно кивает."
                $ add_stat(hero, "humanity", 1)
                $ beggar_flag_help = True
            "Пройти мимо":
                "Ты проходишь мимо, решив, что перед тобой очередной безумец, сломленный Морвейном."

    "Оставив калеку за спиной, ты входишь в едва приоткрытые двери собора."

    stop music fadeout 3.0

    jump temple_inside

label temple_inside:
    scene temple_inside
    with fade

    play music "<from 52.0>audio/temple.mp3" fadein 3.0

    "Внутри собора почти темно. Высокие своды теряются где-то наверху, за дымом свечей и тенями."
    "Шаги звучат непривычно глухо, будто камень под ногами поглощает эхо."
    "Вдоль стен тянутся ряды деревянных скамей, на которых спят люди."

    "У алтаря ходят монахи в поизносившихся одеяниях. Некоторые молятся, некоторые будто прямо стоя, неподвижно склонив головы."

    "Двое монахов осторожно проводят через зал мальчика лет десяти. Ребенок идет босиком с закрытыми глазами, едва переставляя ноги."
    "Когда один из монахов берет его за плечо, мальчик никак не реагирует, словно находится где-то бесконечно далеко отсюда."
    "В дальнем конце зала ты замечаешь еще нескольких спящих детей, лежащих под темными покрывалами."

    "Чуть дальше ты видишь, как один молодой монах, несущий ведро воды, на мгновение останавливается посреди прохода."
    "Его взгляд становится пустым, а ведро выскальзывает из рук, с глухим стуком ударяясь о пол."
    "Лишь через несколько секунд он приходит в себя и поднимает упавшее ведро, избегая чужих взглядов."

    "Где-то в глубине собора слышится негромкое и монотонное пение. 
    Несколько голосов повторяют одну и ту же фразу снова и снова, словно убаюкивают ребенка."

    $ check_dream(1, "На одно короткое мгновение тебе кажется, будто пол под ногами едва заметно дрожит. Или даже дышит...")

    show stefan default at center
    with dissolve

    "Из темноты впереди появляется фигура монаха."
    "Высокий, болезненно бледный человек с глубоко запавшими глазами внимательно смотрит на тебя."

    stefan "Добро пожаловать в собор Ордена." 
    stefan "Я отец Стефан, его настоятель."
    stefan "Полагаю, вы уже видели, что происходит в городе?"

    menu:
        "Люди здесь боятся вас.":
            stefan "Страх — частая цена за порядок."
            $ hero.ord_rel -= 1
        "Да, люди напуганы. Без ваших усилий город охватила бы паника.":
            stefan "Делаем все, что в наших силах."
            $ hero.ord_rel += 1

    stefan "Мы лишь пытаемся удержать то, что еще можно удержать."

    stefan "Сегодня утром мы поймали одного из культистов у северных катакомб."
    stefan "Обычно они предпочитают смерть разговору. Но этот сам попросил привести его сюда."

    if hero.prof == PROF.MONK:
        stefan "Я как раз собирался допросить его лично. Если вы не против, продолжим наш разговор внизу."
        jump temple_interrogation_room
    else:
        stefan "Я как раз собирался допросить его лично. Подождите меня в храмовой лечебнице, и мы продолжим наш разговор. 
        Если хотите, то можете осмотреть больных."
        jump temple_hospital
        
label temple_interrogation_room:
    scene temple_interrogation_room
    with fade

    "Вы вдвоем спускаетесь в комнату для допроса. Тяжелая дверь со скрипом закрывается за вашей спиной."
    "В воздухе стоит тяжелый запах — смесь человеческого пота и запекшейся крови."
    "Каменные стены покрыты потемневшими символами Ордена, а единственный фонарь под потолком едва разгоняет темноту.
    В центре комнаты, прикованный к деревянному креслу цепями, сидит пленник."

    show cultist default at center
    with dissolve

    "Его голова с грязными волосами опущена, а губы едва заметно шевелятся, словно произнося немую молитву."
 
    menu:
        "Почему вы держите его в таком состоянии? Он сдался вам добровольно." if hero.humanity > 1:
            hide cultist
            show stefan default at center
            with dissolve
            stefan "Ты, видимо, не знаешь, на что они способны."
            $ add_stat(hero, "humanity", 1)
        "Что вы от него уже узнали?":
            hide cultist
            show stefan default at center
            with dissolve
            stefan "Он отказывается говорить."

    hide stefan
    show cultist default at center
    with dissolve

    "Пленник медленно поднимает голову. Его глаза останавливаются прямо на тебе, и он с усмешкой улыбается."
    cultist "Ты уже видел их?"

    menu:
        "..." if hero.dream > 0:
            cultist "Вижу, ты понимаешь, о чем я говорю."
            "Культист продолжает криво улыбаться."
        "О чем ты?" if hero.dream == 0:
            cultist "Значит, время еще не пришло. Скоро."
            "Культист продолжает криво улыбаться."

    cultist "Ты ведь слышал колокола, правда? Все всегда начинаются с колоколов."
    cultist "Они всегда звучат перед Приливом. "
    cultist "Главное — не отвечай, если услышишь свое имя."
    "Голос культиста становится серьезным."
    cultist "Ты уже наверняка обратил внимание на всех этих спящих наверху."
    cultist "Орден считает, что они могут их вылечить. Наивные болваны."

    hide cultist
    show stefan default at center
    with dissolve

    stefan "Довольно!"
    "Отец Стефан делает резкий шаг по направлению к узнику с поднятой рукой, явно намереваясь заставить его замолчать."
    "Неожиданно звуки хора наверху резко смолкают. В возникшей тишине слышно лишь нервное дыхание пленника и удары капель дождя о купол собора."
    "По лицу отца Стефана становится понятно, что такого прежде не происходило."
    stefan "Наверх, быстро!"

    jump awakening_temple

label temple_hospital:
    scene temple_hospital

    with fade

    "Пока отец Стефан медленно спускается по лестнице в комнату для допросов, один из служителей проводит тебя в храмовую лечебницу."

    "В самом помещении вдоль стен стоят наспех скроенные койки, занятые спящие людьми разного возраста. 
    Некоторые что-то тихо бормочут во сне, другие лежат совершенно неподвижно, словно погрузились в безвременный отдых."

    "Осматривая пациентов, ты быстро понимаешь, почему местные считают происходящее болезнью."
    "У многих наблюдаются одинаковые признаки: истощение, холодные исхудавшие руки с проступившими синими венами и темные круги под глазами."

    "Рядом с тобой несколько монахов ухаживают за детьми, которых болезнь поразила особенно сильно. 
    Один мальчик внезапно садится на кровати, произвонит несколько бессвязных слов и снова ложится, даже не проснувшись."

    "Сквозь открытый проем до тебя доносится пение хора. Оно сопровождало тебя все время с момента прибытия в собор и давно превратилось 
    в часть окружающего шума. Поэтому в какой-то момент ты даже не не понимаешь, что случилось." 
    
    "Лишь спустя несколько секунд приходит осознание: хор замолчал."

    "Над лечебницей мгновенно застывает напряжение. Через мгновение несколько спящих пациентов одновременно начинают садиться на своих койках."

    "Один за другим они встают на ноги, будто откликнувшись на беззвучный приказ. 
    Именно тогда из глубины собора доносятся первые встревоженные крики."

    jump awakening_temple

label awakening_temple:
    scene temple_inside

    play music "<from 147.0>audio/epic_theme.m4a"

    if hero.prof == PROF.MONK:
        "Вы быстро поднимаетесь по лестнице обратно к главному залу.
        С каждой ступенькой чувство тревоги накатывает на вас все сильнее."

        "Навстречу вам выбегает молодой послушник, его белое лицо перекошено от страха:
        \n— Отец Стефан, мы не можем их остановить!"

        show sleepwalkers default at center
        with dissolve

        "Вы врываетесь в главный зал собора вместе настоятелем. 
        Ты видишь, как большинство прихожан в ужасе жмутся к стенам." 
        
        "В центре зала толпятся несколько десятков спящих, среди которых и прихожане, и монахи, и певцы хора.
        с закрытыми глазами они медленно идут вперед, не реагируя ни на что вокруг."

        hide sleepwalkers default
        show stefan default at center
        with dissolve
    else:
        show sleepwalkers default at center
        with dissolve

        "Вы врываеетесь в главный зал собора вместе в другими монахами.
        Ты видишь, как большинство прихожан в ужасе жмутся к стенам." 
        
        "В центре зала толпятся несколько десятков спящих, среди которых и прихожане, и монахи, и певцы хора.
        с закрытыми глазами они медленно идут вперед, не реагируя ни на что вокруг."

        "Ты слышишь, как в другом конце зала отец Стефан уже отдает приказы."

        hide sleepwalkers default
        show stefan default at center
        with dissolve

    stefan "Закройте двери! Не дайте им выйти в город!"

    hide stefan default
    show sleepwalkers default at center
    with dissolve

    "Один из монахов пытается остановить женщину в грязном белом платке, преградив ей путь, 
    но та буквально опрокидывает его, продолжая идти вперед."
    "Второй монах хватает за руку приведенного недавно мальчика,
    но тот вырывается с неожиданной силой и бредет по направлению к выходу, словно ведомый незримой силой."

    "Отец Стефан быстро отдает распоряжения, перебрасывая своих людей от одного прохода к другому."
    "По его лицу видно, что он пытается хоть как-то контролировать происходящее, 
    но лунатики продолжают возникать в разных частях собора и каждый раз обходят препятствия, будто заранее знают, где их встретят."

    "Несколько братьев опрокидывают тяжелые деревянные скамьи поперек центрального нефа, превратив их в подобие баррикады."
    "Однако лунатики не останавливаются — они медленно перелезают через препятствия или сворачивают в боковые проходы, 
    продолжая двигаться к выходу с пугающим упорством."

    "Ты видишь, что у главных ворот, несмотря на приказ отца Стефана, царит неразбериха."

    "Пока одни монахи пытаются закрыть тяжелые створки, другие выводят испуганных людей из давки, возникшей перед выходом."
    "Несколько прихожан в панике наваливаются на двери, стремясь покинуть собор, мешая монахам к ним пробиться."

    "К тому моменту, как братьям удается расчистить проход и взяться за створки, 
    большинство спящих уже оказывается на улице..."

    jump morvein_from_temple

label morvein_from_temple:
    scene morvein_from_temple 

    with fade

    hide sleepwalkers default
    with dissolve

    "Вы с отцом Стефаном выбегаете на широкую площадку перед собором и замираете."
    "Отсюда весь Морвейн лежит как на ладони: лабиринт тесных улиц, крыши, теряющиеся в тумане, и редкие огни в окнах."
    "По всему городу двигаются люди — десятки, а может быть, сотни фигур медленно выходят из домов, переулков и дворов, 
    сливаясь в длинные безмолвные потоки"

    show beggar default at center
    with dissolve

    "Перед вами неожиданно возникает нищий, которого вы видели перед входом в собор. 
    Он резко кидается на тебя с закрытыми глазами и зажатым в руке камнем."

    if beggar_flag_help:
        "В последний момент, словно на мнговение узнав тебя, калека в словно замешательстве останавливается. 
        И через пару секунд падает на землю без сознания."
    else:
        "Калека бросает в твою голову камень, после чего падает на землю без сознания."
        $ hero.state = STATE.INJURED

    hide beggar default
    with dissolve

    "Ты с ужасом понимаешь, что это первый раз, когда кто-то из спящих попытался напасть на человека."

    show stefan default at center
    with dissolve

    menu:
        "Что нам делать?":
            "Отец Стефан не отвечает. Его взгляд прикован к людям вдалеке."
            "По его остекленевшим глазам ты понимаешь: он впервые не знает, что происходит..."

    jump prologue_end

label prologue_end:
    hide screen blood_overlay
    hide screen char_stats

    scene black with fade 

    image tbc_message = Text("ПРОДОЛЖЕНИЕ СЛЕДУЕТ", style="death_style")

    show expression "images/misc/hourglass.png" at Transform(xalign=0.5, yanchor=0.5, ypos=0.40)
    show tbc_message at Transform(xalign=0.5, yanchor=0.5, ypos=0.80)

    $ renpy.take_screenshot()
    $ renpy.save("1-1", "Конец пролога")

    $ renpy.pause()

    jump act_1_start

label act_1_start:
    scene morvein_from_temple

    "..."

    return

label hero_died:
    image death_message = Text("ВАШ ПУТЬ ОКОНЧЕН", style="death_style")

    # Скрываем экран с кровью, так как персонаж уже мертв
    hide screen blood_overlay
    hide screen char_stats

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