define aspect_colors = [
    "#eda5ff", # 0-2
    "#da52ff", # 3-4
    "#cc26ff", # 5-6
    "#c310ff", # 7-8
    "#cc00ff", # 9-10
]

define mercy_colors = [
    "#7A6A45",
    "#9A8050",
    "#C9A96A",
    "#E0C27A",
    "#F2D98A",
]

define reason_colors = [
    "#4E6475",
    "#63839B",
    "#7FA7C9",
    "#9BC4E6",
    "#B8DFFF",
]

define control_colors = [
    "#2f372d",
    "#265619",
    "#2a831e",
    "#42a31fff",
    "#44ff00ff",
]

define GREEK_MAP = {
    "а": "α",
    "е": "ε",
    "з": "ζ",
    "и": "ι",
    "к": "κ",
    "м": "μ",
    "н": "η",
    "о": "ο",
    "р": "ρ",
    "с": "ς",
    "т": "τ",
    "у": "υ",
    "ф": "φ",
    "х": "χ",

    "А": "Α",
    "Е": "Ε",
    "З": "Ζ",
    "И": "Ι",
    "К": "Κ",
    "М": "Μ",
    "Н": "Η",
    "О": "Ο",
    "Р": "Ρ",
    "С": "Σ",
    "Т": "Τ",
    "У": "Υ",
    "Ф": "Φ",
    "Х": "Χ",
}

define mercy_desc = [
    "Чужая боль тебя не трогает.",
    "Иногда ты готов помогать другим — если это тебе выгодно.",
    "Ты остро переживаешь чужие страдания.",
    "Ради других ты готов жертвовать собственным благополучием.",
    "Чужая судьба для тебя почти так же важна, как собственная."
]

define reason_desc = [
    "Ты всё чаще упускаешь важные детали.",
    "Ты замечаешь больше, чем большинство людей.",
    "Ты начинаешь видеть закономерности там, где другие видят случайности.",
    "Немногие способны скрыть что-либо от твоего взгляда.",
    "Ты видишь связи, недоступные большинству людей."
]

define aspect_desc = [
    "Сны проходят мимо тебя, не оставляя следа.",
    "Иногда тебе кажется, что мир говорит с тобой.",
    "Сны оставляют след даже после пробуждения.",
    "Граница между сном и явью становится тоньше.",
    "Что-то по ту сторону начинает замечать тебя в ответ."
]

define control_desc = [
    "Эмоции всё чаще берут верх над рассудком.",
    "Ты ещё способен держать себя в руках.",
    "Даже под давлением ты сохраняешь ясность мысли.",
    "Твой разум остаётся непоколебим даже перед лицом ужаса.",
    "Ты полностью владеешь собой и своими страхами."
]

# Определение Python типов и функций
init python:
    import enum
    import pygame_sdl2 as pygame
    import random
    import re
    import time

    config.layers = [ "background", "master", "transient", "screens", "overlay" ]

    class STATE(enum.Enum):
        HEALTHY = "Здоров"
        INJURED = "Ранен"
        GRAVELY = "Умирает"
        DEAD = "Мертв"

    class PROF(enum.Enum):
        DOCTOR = "Доктор"
        MONK = "Монах"

    class Hero:
        def __init__(self, name, full_name, prof, state, mercy, reason, aspect, control, ord_rel, cult_rel, image, portrait, color):
            self.name = name
            self.full_name = full_name
            self.prof = prof
            self.state = state
            self.mercy = mercy
            self.reason = reason
            self.aspect = aspect
            self.control = control
            self.ord_rel = ord_rel
            self.cult_rel = cult_rel
            self.image = image
            self.portrait = portrait
            self.color = color

    class Note(object):
        def __init__(self, note_id, title, text=""):
            self.id = note_id
            self.title = title
            self.text = text

    class InvItem(object):
        def __init__(self, item_id, title, icon, description, count):
            self.id = item_id
            self.title = title
            self.icon = icon
            self.description = description
            self.count = count

    # Настройки игры
    def delete_all_saves():
        for slot in renpy.list_saved_games(fast=True):
            renpy.unlink_save(slot)

    def pause_music():
        global saved_music_pos, saved_music_file

        saved_music_pos = renpy.music.get_pos("music")
        saved_music_file = renpy.music.get_playing("music")

        renpy.music.stop(channel="music", fadeout=1.0)

    def resume_music():
        if saved_music_file:
            renpy.music.play(
                saved_music_file,
                channel="music",
                loop=True,
                synchro_start=saved_music_pos,
                fadein=1.0
            )

    # Логические функци
    def passive_check(stat, min_value, text, altText, addDream):
        if(stat) >= min_value:
            renpy.sound.play("audio/fx/dream_fx.mp3") 

    def add_stat(hero_object, stat_name, value):
        current_value = getattr(hero_object, stat_name)
        setattr(hero_object, stat_name, current_value + value)
        renpy.sound.play("audio/fx/pass_fx.mp3")

    def debuff_stats(hero):
        isDebuffed: True
        hero.mercy -= 1
        hero.reason -= 1
        hero.aspect -= 1
        hero.control -= 1
    
    def heal_debuff(hero):
        if (isDebuffed):
            hero.mercy += 1
            hero.reason += 1
            hero.aspect += 1
            hero.control += 1
    
    def reduce_dream(hero):
        hero.aspect =- 1

    # Эффекты
    def start_dream_effect():
        pause_music()
        renpy.sound.play("audio/fx/horror_bell.mp3")
        renpy.music.play(
            "audio/dream_theme.mp3",
            fadein=2.0
        )
        renpy.show("black", layer="background")
        renpy.layer_at_list([slow_shaking], layer="master")

    def stop_dream_effect():
        renpy.layer_at_list([], layer="master")
        renpy.music.stop(fadeout=2.0)
        resume_music()

    def check_dream(min_value, text):
        if hero.aspect > min_value:
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

    def hard_fade(scene_name, delay=3.0, texts = None):
        renpy.stop_skipping()

        renpy.hide_screen("say")
        renpy.hide_screen("quick_menu")
        renpy.hide_screen("gui")

        renpy.scene(layer="screens")
        renpy.scene(layer="overlay")

        renpy.scene(layer="master")
        renpy.show("black", layer="master")
        renpy.with_statement(None)

        if texts:
            renpy.say(None, texts)

        renpy.pause(0.5, hard=True)

        renpy.show(scene_name, layer="master", at_list=[fade_in_from_black(delay)])
        renpy.pause(delay, hard=True)
            

    dream_active = True

    def dreamify(text):
        if hero_selected:
            parts = re.split(r'(\{.*?\})', text)
            result = []
            chance = 0.2 + (hero.aspect - 3) * 0.1

            for part in parts:
                if part.startswith("{") and part.endswith("}"):
                    result.append(part)
                    continue

                transformed = []

                for char in part:
                    if char in GREEK_MAP and random.random() < chance:
                        transformed.append(
                            "{color=#9b59ff}{i}" +
                            "{shader=jitter:u__jitter=1.0,1.0}" +
                            GREEK_MAP[char] +
                            "{/shader}" +
                            "{/i}{/color}"
                        )
                    else:
                        transformed.append(char)

                result.append("".join(transformed))

            return "".join(result)
        else:
            return text

    def dream_char(image_name, pos=None, z=10, transition=dissolve):
        if pos is None:
            pos = []

        low_dream_level=3

        if hero.aspect >= low_dream_level:
            renpy.show(
                image_name,
                tag=image_name.split()[0] + "_shadow",
                at_list=pos + [dream_shadow],
                zorder=z - 1
            )

        renpy.show(
            image_name,
            at_list=pos,
            zorder=z
        )

        renpy.transition(transition)

    def hide_dream_char(image_name, transition=dissolve):
        # Получаем тег персонажа (первое слово в названии)
        tag_name = image_name.split()[0]
        
        # Скрываем тень персонажа
        renpy.hide(tag_name + "_shadow")
        
        # Скрываем самого персонажа
        renpy.hide(tag_name)
        
        # Применяем эффект перехода
        renpy.transition(transition)


    old_say = renpy.say

    def dream_say(who, what, *args, **kwargs):
        if dream_active:
            what = dreamify(what)

        return old_say(who, what, *args, **kwargs)

    renpy.say = dream_say

    dream_alpha = 0.8
    def dream_scene_dynamic(st, at, image_name):
        global dream_alpha

        dream_alpha += random.uniform(-0.05, 0.05)
        dream_alpha = max(0.4, min(0.6, dream_alpha))

        d = Composite(
            (1920, 1080),
            (0, 0), renpy.displayable(image_name),
            (0, 0), Transform(
                renpy.displayable(image_name + "_dream"),
                alpha=dream_alpha
            )
        )

        return d, 0.1

    def stat_desc(value, text_table, color_table):
        if value <= 2:
            idx = 0
        elif value <= 4:
            idx = 1
        elif value <= 6:
            idx = 2
        elif value <= 8:
            idx = 3
        else:
            idx = 4

        return "{color=%s}%s{/color}" % (color_table[idx], text_table[idx])

    # 1. Определяем функцию, которая будет собирать и выводить данные
    def debug_print_properties():
        # Проверяем, существует ли нужный объект в игре, чтобы избежать вылета
        if 'hero' in globals():
            obj = globals()['hero']
            
            # Печатаем в системную консоль/терминал (откуда запущен Ren'Py)
            print("\n=== DEBUG PROPERTIES ===")
            for k, v in vars(obj).items():
                print(f"{k}: {v}")
            print("========================\n")
            
            # Дублируем вывод в log.txt (на случай, если консоль закрыта)
            renpy.log(f"DEBUG: {vars(obj)}")
            
            # Опционально: показываем быстрое уведомление на экране игры
            renpy.notify("Свойства объекта hero напечатаны в консоль!")
        else:
            renpy.notify("Ошибка: Объект 'hero' еще не создан.")

    # 2. Регистрируем новое действие в системе клавиш Ren'Py
    # Назначаем комбинацию ctrl_K_d (Ctrl + D)
    config.underlay.append(renpy.Keymap(ctrl_K_d = debug_print_properties))


