define mercy_desc = [
    "Чужая боль тебя не трогает.",
    "Иногда ты готов помогать другим — если это тебе выгодно.",
    "Ты часто испытываешь сострадание к окружающим.",
    "Чужая судьба для тебя почти так же важна, как собственная.",
    "Ради других ты готов жертвовать собственным благополучием.",
]

define reason_desc = [
    "Тебе заметны только очевидные детали.",
    "Ты умеешь делать выводы из доступных фактов.",
    "Ты видишь закономерности там, где другие видят случайности.",
    "Немногое способно улизнуть от твоего взгляда.",
    "Ты способен распутать самый сложный клубок фактов.",
]

define aspect_desc = [
    "Мир кажется тебе абсолютно привычным и познаваемым.",
    "Иногда тебе кажется, что мир обретает незнакомые очертания.",
    "Ты чувствуешь присутствие чего-то иного.",
    "Что-то по ту сторону начинает говорить с тобой."
    "Граница между сном и явью становится едва отличимой.",
]

define control_desc = [
    "Ты способен держать себя в руках только в критических ситуациях.",
    "Эмоции нередко берут верх над твоим рассудком.",
    "Ты сохраняешь ясность мысли под давлением.",
    "Даже сильные потрясения едва способны вывести тебя из равновесия.",
    "Твой разум остаётся непоколебим перед лицом ужаса.",
]

define aspect_colors = [
    "#150b19", 
    "#55026b", 
    "#8301ab",
    "#a600dd",
    "#cc00ff",
]

define mercy_colors = [
    "#654320",
    "#884c19",
    "#b66417",
    "#cd6e16",
    "#ff7b00",
]

define reason_colors = [
    "#0f0f5a",
    "#190c7d",
    "#1808ad",
    "#2919bb",
    "#1900ff",
]

define control_colors = [
    "#175009",
    "#2a7615",
    "#2aa21a",
    "#42c811ff",
    "#44ff00ff",
]

init python:
    import enum
    import pygame_sdl2 as pygame
    import random
    import re
    import time
    import warnings

    class STATE(enum.Enum):
        HEALTHY = "Здоров"
        INJURED = "Ранен"
        GRAVELY = "Умирает"
        DEAD = "Мертв"

    class PROF(enum.Enum):
        DOCTOR = "Доктор"
        MONK = "Монах"

    class Hero:
        def __init__(self, name, full_name, prof, state, mercy, reason, aspect, control, ord_rel, cult_rel, image, portrait, color, is_debuffed = False):
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
            self.is_debuffed = is_debuffed

    def add_stat(hero_object, stat_name, value):
        if (getattr(hero_object, stat_name) < 10):
            renpy.sound.play("audio/fx/fx_stat_buff.mp3") 
            current_value = getattr(hero_object, stat_name)
            setattr(hero_object, stat_name, current_value + value)


    def reduce_stat(hero_object, stat_name, value):
        if (getattr(hero_object, stat_name) > 0):
            renpy.sound.play("audio/fx/fx_stat_debuff.mp3") 
            current_value = getattr(hero_object, stat_name)
            setattr(hero_object, stat_name, current_value - value)
    
    def reduce_aspect(hero):
        reduce_stat(hero, "aspect", 1)

    def debuff_phys_stats(hero):
        if (not hero.is_debuffed):
            reduce_stat(hero, "reason", 2)
            reduce_stat(hero, "control", 2)
        hero.is_debuffed = True

    def set_hero_state(hero, state):
        hero.state = state

        if state in (STATE.INJURED, STATE.GRAVELY):
            debuff_phys_stats(hero)
        elif state == STATE.HEALTHY:
            heal_phys_debuff(hero)

    def heal_phys_debuff(hero):
        if (hero.is_debuffed):
            add_stat(hero, "reason", 2)
            add_stat(hero, "control", 2)
        hero.is_debuffed = False

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

    def hero_state_desc(state):
        descriptions = {
            STATE.HEALTHY: "Ты полностью здоров.",
            STATE.INJURED: "Ты ранен. Каждое действие дается тебе тяжелее.",
            STATE.GRAVELY: "Ты умираешь. Времени почти не осталось.",
            STATE.DEAD: "Ты мертв.",
        }

        return descriptions.get(state, getattr(state, "value", str(state)))

    # def buy_item(item_id, price):

    