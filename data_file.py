# Импорт необходимых библиотек
import gspread
import os

# Получение абсолютного пути к текущему файлу
path = os.path.abspath(os.path.dirname(__file__))
print(path)

# Инициализация глобальных словарей
main_dict = {}
text_dict = {}
stat_cat_dict = {}
stat_markets_dict = {}


# Функция для обновления данных из Google Sheets
def regenerate():
    global main_dict, text_dict, stat_cat_dict, stat_markets_dict

    # Авторизация в Google Sheets
    gc = gspread.service_account(filename="midyear-cursor-379909-cc15f63beea0.json")

    # Открытие таблицы по URL
    sht2 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1FhYGE5IODqbtXSfQGBs0BGUaUJYAWBGAC2SRWqYzf6M')

    # Получение данных из первого листа
    worksheet = sht2.sheet1
    main_list = worksheet.get_all_values()

    # Очистка словарей
    main_dict = {}
    text_dict = {}
    stat_cat_dict = {}
    stat_markets_dict = {}

    # Обработка каждой строки данных
    for el in main_list[1:]:
        # Добавление категории в main_dict
        if el[0] not in main_dict.get(el[8], []):
            main_dict.setdefault(el[8], []).append(el[0])

        # Формирование текста акции
        text = f"Название: {el[0]}\nСкидка: {el[3]}\nСсылка: {el[4]}\nДействует до: {el[5]}\nРегион: {el[6]}\nУсловия акции: {el[7]}\nПромокод ниже⬇️ "

        # Добавление текста акции и промокода в text_dict
        text_dict.setdefault(el[0], []).extend([text, el[2]])

        # Инициализация статистики посещений для каждой категории и магазина
        for k, v in main_dict.items():
            stat_cat_dict.setdefault(k, [])
            for x in v:
                stat_markets_dict.setdefault(x, [])


# Вызов функции для обновления данных
regenerate()
