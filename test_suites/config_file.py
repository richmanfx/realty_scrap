﻿# -*- coding: utf-8 -*-
""" Конфигурационный файл """

# Поддерживаемые браузеры - раскомментировать один!
BROWSER = 'chrome'
# BROWSER = 'firefox'

# Размер окна браузера, например, (1024, 768)
# Если закомментировать, то будет максимальный размер окна
# BROWSER_SIZE = (1920, 1200)
# BROWSER_SIZE = (1920, 1080)
BROWSER_SIZE = (1100, 1130)

# Сервер
SITE_NAME = 'https://torgi.gov.ru/lotSearch2.html'
USER_NAME = ''
USER_PASSWORD = ''
USER_LABEL = ''

IMPLICITLY_WAIT_TIMEOUT = 20    # Неявное ожидание, в секундах
WAIT_TIMEOUT = 3    # Явное ожидание, в секундах

# Подсветка элемента для визуальной отладки
FLASH_QUANTITY = 2     # Количество миганий
FLASH_PERIOD = 0.11    # Период мигания в секундах
FLASH_ALLOWED = True   # True - включить подсветку, False - выключить

# Уровень отладочных сообщений
DEBUG_LEVEL = 'DEBUG'

# Параметры объекта для выставления фильтров
OBJECT_MIN_AREA = 25    # Минимальная площадь объекта
OBJECT_MAX_AREA = 70    # Максимальная площадь объекта
MIN_RENTAL_PERIOD = 5   # Минимальный срок аренды, лет
PROPERTY_TYPE = "Помещение"             # Тип имущества
CONTRACT_TYPE = "Договор аренды"        # Вид договора
COUNTRY = "РОССИЯ"                      # Страна
PROPERTY_LOCATION = "Москва (г)"        # Местоположение имущества (город)

# Столбец, по которому сортировать
SORT_FIELD_NAME = "Коэффициент доходности"
# SORT_FIELD_NAME = "Доход в месяц"


########################################################################################################################
# Параметры для расчёта окупаемости

# Флаг для вывода на экран конфигурационных параметров (False или True)
CONFIG_PARAMETERS_PRINT = True

# Флаг для вывода на экран и дополнительных рассчитанных параметров (False или True)
OPTIONAL_CALCULATED_PARAMETERS_PRINT = True

AVERAGE_RENTAL = 1292.0         # Средняя стоимость аренды, руб. за кв.м. в мес.
PROFIT_MONTHS = 10              # Количество доходных месяцев в году
REPAIR = 300.0                  # Предварительный ремонт, рублей за кв.м.  (??? - уточнить)

# Разовые затраты
CONTRACT_REGISTRATION = 4000.0             # Стоимость регистрации договора, рублей
RUNNING_COST = 15000.0                      # Мелкие расходы на запуск объекта

# Ежегодные затраты
YEARLY_INSURANCE = {            # Стоимость годовой страховки (рубли) в Альфа-Страховании, зависит от площади в метрах
    100: 4000,
    300: 6000,
    500: 8000,
    1000: 12000,
    99999999: 20000,
}

# Ежемесячные затраты
HEATING = 22.43                 # Отопление, рублей за кв.м. в месяц
HOUSING_OFFICE = 27.14          # Обслуживание ЖЭКом, рублей за кв.м. в месяц
# MIN_INSURANCE = 30.0          # Минимальная страховка, рублей за кв.м. в месяц
ACCOUNTING_SERVICE = 2000.0     # Бухгалтерское обслуживание, рублей в месяц

REQUIRED_PROFIT_MARGIN = 25     # Требуемый (хороший) коэффициент доходности
