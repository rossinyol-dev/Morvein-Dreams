# Кровавое мигание
transform blood_flash:
    # Задаем начальную прозрачность без привязки к событиям
    alpha 1.0 
    # Бесконечный цикл мигания
    block:
        linear 1.0 alpha 0.3  # За полсекунды затухает до 30%
        linear 1.0 alpha 1.0  # За полсекунды возвращается к 100%
        repeat

# Медленная тряска экрана с затемнением
transform slow_shaking:
    linear 3.0 yoffset 15 matrixcolor BrightnessMatrix(-0.5)
    linear 3.0 yoffset -15 matrixcolor BrightnessMatrix(0.0)

    repeat

# Ховер элементов инвентаря
transform inventory_hover_effect:
    # Состояние по умолчанию (обычная яркость)
    on idle:
        ease 0.15 matrixcolor BrightnessMatrix(0.0)
    
    # Состояние при наведении (делаем картинку на 25% ярче)
    on hover:
        ease 0.15 matrixcolor BrightnessMatrix(0.25)

# Пульсирование элементов интерфейса
transform gui_pulse:
    zoom 1.0
    alpha 1.0
    
    ease 0.7 zoom 1.1 alpha 0.8
    ease 0.7 zoom 1.0 alpha 1.0
    repeat

# Фейд из черного
transform fade_in_from_black(delay=3.0):
    alpha 0.0
    linear delay alpha 1.0

# Дрожащие буквы
transform dream_letter_shake:
    subpixel True
    xoffset 0
    yoffset 0
    linear 0.04 xoffset 1 yoffset -1
    linear 0.04 xoffset -1 yoffset 1
    linear 0.04 xoffset 0 yoffset 0
    repeat

# Тень вокруг персонажа
transform dream_shadow:
    matrixcolor TintMatrix("#c011c0")
    alpha 0.6
    zoom 1.02

    block:
        linear 3 zoom 1.02 alpha 0.6
        linear 3 zoom 1.03 alpha 0.8
        repeat

# Фейдаут фона в черное
transform smooth_fade_out:
    alpha 0.0
    linear 3.0 alpha 1.0