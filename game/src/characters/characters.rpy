# Картинки персонажей
image stefan default = Transform("images/chars/stefan_default.png", zoom=0.7)
image stefan horror = Transform("images/chars/stefan_horror.png", zoom=0.7)
image beggar default = Transform("images/chars/beggar_default.png", zoom=0.7)
image cultist default = Transform("images/chars/cultist_default.png", xzoom=0.65, yzoom=0.7)
image sleepwalkers default = Transform("images/chars/sleepwalkers.png", zoom=0.7)
image mattias default = Transform("images/chars/mattias_default.png", zoom=0.7)
image edmund default = Transform("images/chars/edmund_default.png", zoom=0.7)
image cornelius default = Transform("images/chars/cornelius_default.png", zoom=0.7)
image agatha default = Transform("images/chars/agatha_default.png", zoom=0.7)
image rykard default = Transform("images/chars/rykard_default.png", zoom=0.7)
image boy horror = Transform("images/chars/boy_horror.png", zoom=0.7)
image girl horror = Transform("images/chars/girl_horror.png", zoom=0.7)

# Персонажи
define narrator = Character()
define thoughts = Character(
    what_italic=True
)
define dream = Character(
    None,
    what_font="fonts/dream.ttf",
    what_xalign=0.5,
    what_text_align=0.5,
    what_color="#9d0778",
    what_slow_cps=15
)
define horror = Character(
    None,
    what_font="fonts/dream.ttf",
    what_xalign=0.5,
    what_text_align=0.5,
    what_color="#f61111",
    what_slow_cps=15
)
define beggar = Character('Нищий', color="#7c9703")
define stefan = Character('Отец Стефан', color="#b02d2d")
define cultist = Character('Культист', color="#6a4001")
define mattias = Character('Брат Маттиас', color="#19e6db")
define edmund = Character('Брат Эдмунд', color="#0cb314")
define cornelius = Character('Брат Корнелиус', color="#981aca")
define agatha = Character('Агата', color="#eb049a")
define rykard = Character('Рикард фон Триллиан', color="#002b7c")

