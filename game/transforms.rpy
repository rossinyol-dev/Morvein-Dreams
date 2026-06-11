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

transform inventory_hover_effect:
    # Состояние по умолчанию (обычная яркость)
    on idle:
        ease 0.15 matrixcolor BrightnessMatrix(0.0)
    
    # Состояние при наведении (делаем картинку на 25% ярче)
    on hover:
        ease 0.15 matrixcolor BrightnessMatrix(0.25)

transform gui_pulse:
    zoom 1.0
    alpha 1.0
    
    ease 0.7 zoom 1.1 alpha 0.8
    ease 0.7 zoom 1.0 alpha 1.0
    repeat