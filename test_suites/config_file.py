# -*- coding: utf-8 -*-
""" Конфигурационный файл """

# Поддерживаемые браузеры - раскомментировать один!
BROWSER = 'chrome'
# BROWSER = 'firefox'

# Размер окна браузера, например, (1024, 768)
# Если закомментировать, то будет максимальный размер окна
# BROWSER_SIZE = (1920, 1200)
# BROWSER_SIZE = (1920, 1080)
# BROWSER_SIZE = (1400, 1050)

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
