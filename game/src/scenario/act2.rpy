# Второй акт

label act_2_rykard_house:
    call show_act_title("АКТ II", "ЗОВ")

    $ hard_fade("trillian_drawing_room")

    $ dream_char("rykard default", [center])

    narrator "Героя встречает Рикард в особняке."
    rykard "Меня зовут Рикард фон Триллиан."
    rykard "Мой род был одним из старейших родов Морвейна еще до возвышения Ордена."
    rykard "Триллианы помнят город таким, каким он был до нынешних запретов, страхов и молчания."
    rykard "Я давно искал встречи с вами."
    rykard "У вас наверняка накопилась куча вопросов."
    rykard "Пройдемте в библиотеку. Там я смогу на них ответить."

    jump act_2_rykard_library

label act_2_rykard_library:
    $ hard_fade("trillian_library")

    $ dream_char("rykard default", [center])

    rykard "Под Морвейном спит древнее существо."
    rykard "Несколько сотен лет назад монахи не уничтожили его."
    rykard "Они просто усыпили его и с тех пор держат в этом состоянии."
    rykard "Я слышал странные слухи."
    rykard "Будто певцы Ордена в последнее время сменяются слишком часто."

    if has_inventory_item("choir_resonance_notes"):
        menu:
            "Показать Рикарду вырванные страницы о хоре":
                narrator "Герой показывает Рикарду вырванные страницы о хоре."
                rykard "Значит, черные слухи об Ордене подтвердились."
                rykard "Они действительно используют певцов, чтобы поддерживать сон существа."
            "Не показывать страницы":
                narrator "Герой не показывает Рикарду вырванные страницы о хоре."

    rykard "Раньше Морвейном управляли древние роды."
    rykard "Мы знали о существе под городом."
    rykard "И у нас получалось договариваться с ним."
    rykard "Так продолжалось, пока не случился кризис."

    if order_history_explored_flag:
        menu:
            "Показать страницу хроники о Триллианах":
                narrator "Герой вспоминает страницу хроники о Триллианах и их участии в жертвоприношениях."
                rykard "Да."
                rykard "В прошлом моего рода есть вещи, которыми невозможно гордиться."
                narrator "Рикард мрачнеет."
                rykard "Но это давно в прошлом."
                rykard "И я предлагаю вам убедиться в этом самому."

                jump act_2_rykard_altar
    else:
        rykard "Если вы сомневаетесь, я предлагаю пойти вместе в храм."
        rykard "Там вы сможете убедиться, что я говорю правду."
        rykard "Пойдемте в гостиную, обсудим там."

        jump act_2_path_choice

label act_2_rykard_altar:
    $ hard_fade("trillian_altar_grotto")

    $ dream_char("rykard default", [center])

    narrator "Герой видит алтарь."
    narrator "Алтарь выглядит заброшенным."
    rykard "Он не использовался уже несколько сотен лет."
    rykard "Все это давно осталось в прошлом."

    if hero.aspect >= 2:
        call dream_scene(
            [
                "Герой видит короткое видение.",
                "Рикард стоит перед алтарем с кинжалом в руке.",
                "Рикард пронзает кого-то кинжалом."
            ],
            "rykard horror",
            [],
            [],
            True)

        $ hard_fade("trillian_altar_grotto")

    narrator "Герой и Рикард возвращаются в гостиную."

    jump act_2_path_choice

label act_2_path_choice:
    $ hard_fade("trillian_drawing_room")

    narrator "Ты стоишь в гостиной."
    narrator "Пора сделать выбор."

    menu:
        "Отправиться в храм с Рикардом":
            jump act_2_rykard_ancient_temple
        "Сдать Рикарда Ордену":
            jump act_2_rykard_arrest

    jump act_2_path_choice

label act_2_rykard_arrest:
    $ hard_fade("trillian_drawing_room")

    narrator "Герой говорит Рикарду, что ему нужно немного подумать."
    narrator "Герой покидает особняк Триллианов."

    $ hard_fade("temple_council")

    $ dream_char("edmund default", [center])

    narrator "Герой возвращается в Совет и требует срочной аудиенции."
    narrator "Герой сообщает, что Рикард знает о существе под Морвейном."
    narrator "Герой сообщает, что Рикард собирался вести его к этому существу."
    narrator "Герой говорит, что намерения Рикарда неясны."
    narrator "Совет решает, что в текущем кризисе не может рисковать."
    narrator "Совет отправляет стражу за Рикардом."

    $ dream_char("rykard default", [center])

    narrator "Вскоре Рикарда приводят в зал Совета."
    narrator "Совет требует от Рикарда объяснений."
    narrator "Рикард говорит, что Орден боится не его, а правды."
    narrator "Совет приказывает задержать Рикарда до выяснения обстоятельств."

    jump act_2_rykard_interrogation

label act_2_rykard_interrogation:
    $ hard_fade("temple_interrogation_room")

    narrator "Рикарда уводят на допрос."
    narrator "Герой слышит начало допроса из-за двери."
    narrator "Совет требует от Рикарда рассказать путь к существу под Морвейном."
    narrator "Рикард отвечает, что Орден и так знает путь."
    narrator "За дверью раздается удар."
    narrator "Рикард говорит, что герой все равно узнает правду."
    narrator "Герой понимает, что теперь пойдет в храм вместе с Орденом."
    narrator "Герой понимает, что сомнения никуда не исчезли."

    jump act_2_order_ancient_temple

label act_2_rykard_ancient_temple:
    $ hard_fade("morvein_ancient_temple")

    $ dream_char("rykard default", [center])

    narrator "Ты идешь в храм с Рикардом."

    return

label act_2_order_ancient_temple:
    $ hard_fade("morvein_ancient_temple")

    $ dream_char("edmund default", [center])

    narrator "Ты идешь в храм с Орденом."

    return
