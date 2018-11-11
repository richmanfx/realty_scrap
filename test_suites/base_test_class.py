# -*- coding: utf-8 -*-

""" Базовый класс для всех Helper классов """

import os
import sys
import time
import allure
import inspect
import datetime
from urllib.error import URLError
from importlib import import_module
from logbook import Logger, StreamHandler

from selene import browser
from selene.support import by
from selene.elements import SeleneElement
from selene.support.jquery_style_selectors import s, ss

from selenium import webdriver
from selenium.webdriver.support import wait
from selenium.webdriver.common.by import By
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import WebDriverException, NoSuchElementException, StaleElementReferenceException, \
    NoSuchFrameException, TimeoutException

from test_suites import config_file


def fix_decorator_for__stale_element_reference_exception(function_to_decorate):
    """
    Декоратор для исправления возникновения исключения 'StaleElementReferenceException' - три попытки (пока) применить
        :param function_to_decorate: Обёртываемая функция
        :return: Сама декорирующая функция
    """

    def wrapped():
        try:
            function_to_decorate()  # Первый раз
        except StaleElementReferenceException:
            time.sleep(config_file.WAIT_TIMEOUT)
            try:
                function_to_decorate()  # Второй раз
            except StaleElementReferenceException:
                time.sleep(config_file.WAIT_TIMEOUT)
                function_to_decorate()  # Третий раз

    return wrapped


class BaseTestClass(object):
    """ Базовый класс для всех Helper классов """

    @staticmethod
    def get_method_name() -> str:
        """ Возвращает имя текущего метода """
        return inspect.stack()[1][3]

    ####################################################################################################################
    # Инициализация логирования
    StreamHandler(sys.stdout, level=config_file.DEBUG_LEVEL).push_application()
    log = Logger("Logbook")

    ####################################################################################################################
    # Инициализация Webdriver соответствующего браузеру, указанному в конфиг-файле. Для Selenium-Grid.
    drv = None

    # Chrome
    if config_file.BROWSER.lower() == "chrome":
        try:
            drv = webdriver.Remote("http://selenium_hub:4444/wd/hub", DesiredCapabilities.CHROME)
        except URLError:
            allure.attach("Нужно прописать в hosts: 127.0.0.1   selenium_hub", "Причина падения теста")
            assert False

    # Отключить автоматическую инициализацию вебдрайвера в Selene и использовать собственный экземпляр драйвера:
    browser.set_driver(drv)

    # C изменёнными размерами окна браузера
    try:
        width = config_file.BROWSER_SIZE[0]
        height = config_file.BROWSER_SIZE[1]
    except AttributeError:
        try:
            # Если не указаны размеры окна в конфигурационном файле, то на весь экран
            drv.maximize_window()
        except WebDriverException:
            drv.set_window_size(1000, 700)  # В нескольких версиях Вебдрайвера был косяк и на весь экран не работало
    else:
        drv.set_window_size(width, height)

    # Неявное ожидание для AJAX
    drv.implicitly_wait(config_file.IMPLICITLY_WAIT_TIMEOUT)  # в секундах

    ####################################################################################################################
    @staticmethod
    def teardown_module() -> None:
        """ Выход из браузера """
        browser.quit()

    ####################################################################################################################
    def screen_shot(self, message: str) -> None:
        """
        Сделать скриншот в формате PNG и прикрепить его к Аллюре отчёту
            :param message: Сообщение в Аллюре отчёт
        """
        self.log.debug(f"Work '{self.get_method_name()}'")
        time.sleep(config_file.WAIT_TIMEOUT)
        base64_png_file = self.drv.get_screenshot_as_png()
        allure.attach(base64_png_file, message, allure.attachment_type.PNG)

    ####################################################################################################################
    def attach_json(self, message: str, json_data: str) -> None:
        """
        Прикрепить данные JSON к Аллюре отчёту
            :param message: Сообщение в Аллюре отчёт
            :param json_data: Строка с JSON
        """
        self.log.debug(f"Work '{self.get_method_name()}'")
        allure.attach(json_data, message, allure.attachment_type.JSON)

    ####################################################################################################################
    @allure.step("Открыть страницу сайта")
    def open_site(self, site_name: str) -> None:
        """
        Открыть страницу сайта
            :param site_name: URL страницы сайта, например, http://testing.turd:7777/
        """
        self.log.debug(f"Work '{self.get_method_name()}'")
        self.drv.get(site_name)  # Ловить эксцепшн не нужно!

    ####################################################################################################################
    @allure.step("Проверить отображение страницы входа в приложение")
    def check_login_page_show(self) -> None:
        """ Проверить отображение страницы входа в приложение """
        self.log.debug(f"Work '{self.get_method_name()}'")
        check_locator = "button[type='submit']"  # Кнопка ввода
        try:
            self.flash(s(by.css(check_locator))).is_displayed()
            self.screen_shot("Страница входа в приложение удачно открылась")
        except NoSuchElementException:
            self.screen_shot("Страница входа в приложение не открылась")
            assert False

    ####################################################################################################################
    def flash(self, element: SeleneElement, flash_quantity=config_file.FLASH_QUANTITY) -> SeleneElement:
        """
        Алиас для метода 'highlight'
            :param element: SeleneElement
            :param flash_quantity: Необязательный параметр - количество миганий
            :return element SeleneElement для каскадирования
        """
        # self.log.debug(f"Work '{get_method_name()}'")
        return self.highlight(element, flash_quantity=flash_quantity)

    ####################################################################################################################
    def highlight(self, element: SeleneElement, flash_quantity=config_file.FLASH_QUANTITY) -> SeleneElement:
        """
        Подсветка кликаемого элемента на WEB-странице для SeleneElement
            :param element: SeleneElement
            :param flash_quantity: Необязательный параметр - количество миганий
            :return element SeleneElement для каскадирования
        """
        # self.log.debug(f"Work '{get_method_name()}'")
        if config_file.FLASH_ALLOWED:

            def apply_style(style):

                @fix_decorator_for__stale_element_reference_exception
                def wrap_1():
                    self.drv.execute_script("arguments[0].setAttribute('style', arguments[1]);", native_element, style)

                wrap_1()

            native_element = element.get_actual_webelement()  # Натуральный элемент Selenium-а, не Selene!!!

            # Сохранение оригинального стиля
            @fix_decorator_for__stale_element_reference_exception
            def wrap_2():
                return native_element.get_attribute('style')

            original_style = wrap_2()
            # Конец Сохранения оригинального стиля

            while flash_quantity > 0:
                time.sleep(config_file.FLASH_PERIOD)
                # apply_style("background: yellow; border: 2px solid red;")     # От добавления рамки - разъезжается
                apply_style("background: red;")

                time.sleep(config_file.FLASH_PERIOD)
                apply_style(original_style)

                flash_quantity = flash_quantity - 1

        return element

    ####################################################################################################################
    def highlight_native_web_element(self, element) -> None:
        """
        Подсветка кликаемого элемента на WEB-странице для Вебэлемента Selenium
            :param element: Selenium Web Element
        """
        self.log.debug(f"Work '{self.get_method_name()}'")
        if config_file.FLASH_ALLOWED:
            def apply_style(style):
                self.drv.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, style)

            flash_quantity = config_file.FLASH_QUANTITY  # Количество миганий

            # Сохранение оригинального стиля
            original_style = element.get_attribute('style')

            while flash_quantity > 0:
                time.sleep(config_file.FLASH_PERIOD)
                # apply_style("background: yellow; border: 2px solid red;")     # От добавления рамки - разъезжается
                apply_style("background: red;")

                time.sleep(config_file.FLASH_PERIOD)
                apply_style(original_style)

                flash_quantity = flash_quantity - 1

    ####################################################################################################################
    def open_left_bar(self) -> None:
        """ Открыть левую панель с параметрами, если она закрыта """
        self.log.debug(f"Work '{self.get_method_name()}'")
        left_bar_xpath = "//div[@id='mySidenav']"
        left_opener_xpath = "//div[@id='leftSideButton']"
        self.open_bar(left_bar_xpath, left_opener_xpath)

    ####################################################################################################################
    def open_right_bar(self) -> None:
        """ Открыть правую панель с уведомлениями и историей, если она закрыта """
        self.log.debug(f"Work '{self.get_method_name()}'")
        right_bar_xpath = "//div[@id='mySidenav2']"
        right_opener_xpath = "//div[@id='rightSideButton']"
        self.open_bar(right_bar_xpath, right_opener_xpath)

    ####################################################################################################################
    def open_bar(self, bar_xpath: str, opener_xpath: str) -> None:
        """
        Открыть выдвигающуюся панель
            :param bar_xpath: Xpath панели
            :param opener_xpath: Xpath элемента открывания панели
        """
        self.log.debug(f"Work '{self.get_method_name()}'")
        # Если панель закрыта, то открыть
        if "width: 0px;" in s(by.xpath(bar_xpath)).get_attribute("style"):
            self.shading_disappearing()  # Затемнение
            self.highlight(s(by.xpath(opener_xpath)))
            s(by.xpath(opener_xpath)).click()
        # Проверить, что панель открылась
        assert "width: 0px;" not in s(by.xpath(bar_xpath)).get_attribute("style")

    ####################################################################################################################
    def shading_disappearing(self) -> None:
        """ Ожидание исчезновения затемнения """
        self.log.debug(f"Work '{self.get_method_name()}'")
        rent_button_xpath = "//a[contains(@title,'Аренда, безвозмездное пользование, доверительное управление " \
                            "имуществом, иные договоры, предусматривающие передачу прав владения и пользования в " \
                            "отношении государственного и муниципального имущества')]"

        wait.WebDriverWait(self.drv, config_file.IMPLICITLY_WAIT_TIMEOUT) \
            .until(ec.element_to_be_clickable((By.XPATH, rent_button_xpath)))

        self.log.debug("The shading was gone")

    ####################################################################################################################
    def shading_disappearing_in_frame(self) -> None:
        # TODO: Пока не реализовано!!!
        """ Ожидание пропадания затемнения во фрейме """
        self.log.debug(f"Work '{self.get_method_name()}'")
        shading_xpath = "//div[@id='BlockLoaderPanel' and contains(@style, 'display')]"
        wait.WebDriverWait(self.drv, config_file.IMPLICITLY_WAIT_TIMEOUT) \
            .until(ec.invisibility_of_element_located((By.XPATH, shading_xpath)))

    ####################################################################################################################
    def alert_accept(self, page) -> None:
        """
        Подтверждение в небраузерном алерт-е
            :param page: Page Object
        """
        self.log.debug(f"Work '{self.get_method_name()}'")
        ok_button_xpath = "//button[@id='alertify-ok']"

        # Иначе всплывающего окна не видно
        self.drv.switch_to.default_content()  # Вернуться из фреймов
        page.switch_to_page_frame()  # Снова переключиться на фрейм

        # Дождаться ПОЯВЛЕНИЯ всплывшего окна
        wait.WebDriverWait(self.drv, config_file.IMPLICITLY_WAIT_TIMEOUT) \
            .until(ec.element_to_be_clickable((By.XPATH, ok_button_xpath)))

        self.highlight(s(by.xpath(ok_button_xpath))).click()

        # Дождаться ПРОПАДАНИЯ всплывшего окна
        wait.WebDriverWait(self.drv, config_file.IMPLICITLY_WAIT_TIMEOUT) \
            .until_not(ec.element_to_be_clickable((By.XPATH, ok_button_xpath)))

    ####################################################################################################################
    def js_click(self, selene_element: SeleneElement) -> None:
        """
        Замена клика в Selenium, который не работает во фремах с 'padding' (workaround)
            :param selene_element: Selene Element
        """
        self.log.debug(f"Work '{self.get_method_name()}'")
        self.highlight(selene_element)  # Подсветка мигающая
        native_element = selene_element.get_actual_webelement()  # Вычленить из SeleneElement элемент Selenium
        self.drv.execute_script("arguments[0].click();", native_element)  # Клик через скрипт

    ####################################################################################################################
    def switch_to_frame_with_adaptive_waiting(self, frame_xpath: str, wait_time: int = 60) -> None:
        """
        Переключение на фрейм с адаптивным временем ожидания
            :param frame_xpath: Xpath фрейма
            :param wait_time: Время ожидания появления фрейма
        """
        self.log.debug(f"Work '{self.get_method_name()}': wait_time = {wait_time}")
        begin_ticks = time.time()
        end_ticks = begin_ticks + wait_time

        step = 0
        while True:
            step = step + 1

            # Поиск элемента фрейма и переключение на фрейм
            try:
                frame_element = self.drv.find_element_by_xpath(frame_xpath)
                self.drv.switch_to.frame(frame_element)
            except NoSuchFrameException:
                tenfold_wait_timeout = config_file.WAIT_TIMEOUT / 10  # Для сокращения числа шагов ожидания
                time.sleep(tenfold_wait_timeout)
            else:
                break

            # Выход по превышению wait_time
            current_ticks = time.time()
            if current_ticks > end_ticks:
                break

    ####################################################################################################################
    @allure.step("Закрыть все открытые фреймы")
    def close_frames(self, wait_time: int = 60) -> None:
        """
        Закрыть все 'iframes' путём нажатия крестика в закладке
            :param wait_time: Время ожидания в секундах
        """

        self.log.debug(f"Work '{self.get_method_name()}'. Wait time: {wait_time} seconds.")

        close_frame_xpath = "//div[@id='mainTabs']//div[@class='close-button']"

        frames_count_for_close = 10  # Бывали зацикливания какие-то в Webdriver
        while frames_count_for_close > 0:

            crosses_closing_frames = ss(by.xpath(close_frame_xpath))
            frames_count = crosses_closing_frames.size()
            self.log.debug(f"Opened frames: {frames_count} ")
            if frames_count > 0:

                # Обработка долгого автоматического обновления фрейма
                self.check_show_control_with_adaptive_waiting(close_frame_xpath, wait_time)

                self.highlight(crosses_closing_frames[0])

                try:
                    crosses_closing_frames[0].click()
                except WebDriverException:
                    self.log.debug(f"Cross click error - wait {config_file.WAIT_TIMEOUT} second")
                    time.sleep(config_file.WAIT_TIMEOUT)
                    crosses_closing_frames[0].click()

                frames_count_for_close -= 1
            else:
                break

    ####################################################################################################################
    def check_show_control_with_adaptive_waiting(
            self, control_xpath: str, wait_time: int, frame_element: str = "") -> bool:
        """
        Проверить отображение контрола на странице по Xpath, с адаптивным временем ожидания
            :param control_xpath: Xpath проверяемого элемента
            :param wait_time: Время ожидания появления тега в секундах
            :param frame_element: Вэбэлемент фрейма
            :return: True - если тег присутствует, иначе - False
        """
        self.log.debug(f"Work '{self.get_method_name()}'. "
                       f"Xpath: {control_xpath}. "
                       f"Maximum wait time: {wait_time} seconds.")
        exist_flag = False

        begin_ticks = time.time()
        end_ticks = begin_ticks + wait_time

        step = 0
        while True:

            step = step + 1

            if frame_element != "":
                # Выйти из фреймов
                self.drv.switch_to.default_content()

                # Переключиться на фрейм
                self.drv.switch_to.frame(frame_element)

            # Проверить отображение контрола на странице
            if self.check_show_control(control_xpath):
                exist_flag = True
                if exist_flag:
                    # Дождаться отсутствия затенения
                    self.shading_disappearing()
                break

            # Выход по превышению wait_time
            current_ticks = time.time()
            if current_ticks > end_ticks:
                self.log.debug(f"Timeout conversion exit: ~{wait_time} sec.")
                break

            time.sleep(config_file.WAIT_TIMEOUT)
            self.log.debug(f"step: {step}")

        return exist_flag

    ####################################################################################################################
    def check_show_control(self, check_xpath: str) -> bool:
        """
        Проверить отображение контрола на странице по Xpath
            :param check_xpath: Xpath проверяемого элемента
            :return: True - если тег присутствует , иначе - False
        """
        self.log.debug(f"Work '{self.get_method_name()}'")
        try:
            # Дождаться неявно видимости элемента
            self.log.debug(
                f"Implicitly expect in 'check_show_control'."
                f" Maximum wait time: {config_file.IMPLICITLY_WAIT_TIMEOUT} seconds."
            )
            wait.WebDriverWait(self.drv, config_file.IMPLICITLY_WAIT_TIMEOUT) \
                .until(ec.visibility_of_element_located((By.XPATH, check_xpath)))
        except (NoSuchElementException, TimeoutException):
            result = False
        else:
            result = True
        self.log.debug(f"Result 'check_show_control' for xpath {check_xpath}: '{result}'")
        return result

    ####################################################################################################################
    def quit_from_frame_and_close_frames(self) -> None:
        """
        Выйти из фрейма и закрыть все фреймы
        """

        self.log.debug(f"Work '{self.get_method_name()}'")

        # Вернуться из фреймов
        self.drv.switch_to.default_content()

        # Закрыть все iframes, если они открыты
        self.close_frames(wait_time=config_file.WAIT_TIMEOUT)

    ####################################################################################################################
    def current_date_time_output(self) -> None:
        """
        Выводит текущую дату и время в аллюре отчёт
        """
        self.log.debug(f"Work '{self.get_method_name()}'")
        current_date_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
        self.log.debug(f"Start test time: {current_date_time}")
        allure.attach(f"{current_date_time}", f"Время старта теста: {current_date_time}")

    ####################################################################################################################
    def get_user_language(self, profile_page) -> str:
        """ Возвращает язык пользователя из профиля """
        self.log.debug(f"Work '{self.get_method_name()}'")

        # Переключиться на фрейм
        profile_page.switch_to_page_frame()

        language_label_xpath = "//label[@for='language']"
        self.flash(s(by.xpath(language_label_xpath)))

        language_xpath = language_label_xpath + "/following-sibling::select/option[@selected='selected']"
        user_language = s(by.xpath(language_xpath)).text

        self.log.debug(f"User language: '{user_language}'")
        allure.attach(f"{user_language}", f"User language: {user_language}")

        return user_language

    def check_words(self, user_language: str, labels_dict: dict, label_type: str) -> None:
        """
        Проверяет слова на соответствие словарю, соответствующему языку пользователя
            :param user_language: Язык пользователя, например 'French'
            :param labels_dict: Словарь со словами
            :param label_type: Тип лейбла (tag, menu и т.п.)
        """
        self.log.debug(f"Work '{self.get_method_name()}'")

        status = False

        if label_type == "tag":
            label_type_insertion = "теге"
        elif label_type == "menu":
            label_type_insertion = "пункте меню"
        else:
            self.log.debug("Error: 'label_type' not defined!")

        try:
            language_dictionary = import_module(f"dictionaries.{user_language}")
        except ModuleNotFoundError:
            self.log.debug(f"No module named '{user_language}'")
            allure.attach(f"{user_language}", f"Не обнаружен словарь с языком '{user_language}'")
            assert False

        for tag in labels_dict:
            for label in labels_dict[tag]:
                labels_words = label\
                    .replace("/", " ").replace("\\", " ").replace("\n", " ").replace(" - ", " ").replace(" & ", " ") \
                    .replace("\"", "").replace("(", "").replace(")", "").replace(",", "")\
                    .replace("0", "").replace("1", "").replace("2", "").replace("3", "").replace("4", "") \
                    .replace("5", "").replace("6", "").replace("7", "").replace("8", "").replace("9", "") \
                    .split(" ")
                for word in labels_words:
                    # Проверить наличие слова в словаре
                    if word.lower() not in language_dictionary.word_tuple:
                        status = True
                        self.log.debug(f"Word '{word}' not found in language dictionary '{user_language}' "
                                       f"in {label_type_insertion} '{tag}'")
                        allure.attach(f"{word}", f"Нет слова '{word}' в словаре '{user_language}' "
                                      f"в {label_type_insertion} '{tag}'")

        if status:
            # Есть слова, не входящие в словарь
            assert False
        else:
            # Все слова удовлетворяют словарю
            if label_type != "menu":
                self.screen_shot(f"Скриншот: Все слова страницы удовлетворяют словарю языка '{user_language}'")

    def read_language(self) -> str:
        """ Считать язык из файла """
        self.log.debug(f"Work '{self.get_method_name()}'")

        with open("dictionaries" + os.path.sep + "auto_recognized_language.txt", "r", encoding="utf-8") as file:
            user_language = file.read()
            return user_language

    def labels_collect(self, actual_tags: list = None) -> dict:
        """
        Собирает и возвращает лейблы
            :param actual_tags: Список актуальных тегов, присутствующих на странице
            :return labels_dict: Словарь с лейблами в разрезе тегов
        """
        self.log.debug(f"Work '{self.get_method_name()}'")

        labels_dict = {}

        # Если актуальный список тегов для страницы не задан, то использовать дефолтный список
        if not actual_tags:
            actual_tags = self.interest_tags

        # Собираем лейблы в тексте тегов ("title" и "div" - особые)
        for tag in actual_tags:
            key = f"{tag}"
            if tag == "title":
                # для "title"
                self.log.debug(f"Adding to labels dict label 'title'")
                title_value = self.drv.title
                labels_dict[key] = [title_value]
                if title_value == "":
                    self.log.debug("Title not present on the page!")
                    allure.attach("Oops!", "Отсутствует TITLE на странице!")

            else:
                if tag == "div":
                    # для "div"
                    # tag_xpath = f"//{tag}[string()]"
                    tag_xpath = f"//{tag}"
                    # labels_dict[key] = self.get_div_label_list(tag_xpath)
                    labels_dict[key] = self.get_label_list(tag_xpath)
                else:
                    # для всех остальных тегов
                    # tag_xpath = f"//{tag}[text()]"
                    tag_xpath = f"//{tag}"
                    labels_dict[key] = self.get_label_list(tag_xpath)

        # Собираем лейблы в атрибутах "input"
        if "input" in actual_tags:
            input_attributes_list = [
                "placeholder",
                "value",
            ]
            for attr in input_attributes_list:
                key = f"input_{attr}"
                labels_dict[key] = self.get_inputs_attr_list(attr)

        # Собираем лейблы в атрибутах "button"
        if "button" in actual_tags:
            button_attributes_list = [
                "title",
            ]
            for attr in button_attributes_list:
                key = f"button_{attr}"
                labels_dict[key] = self.get_button_attr_list(attr)

        self.log.debug(f"labels_dict: {labels_dict}")
        return labels_dict

    def get_div_label_list(self, tag_xpath: str) -> list:
        """
        Возвращает список лейблов (текст) в теге "div"
            :param tag_xpath: Xpath тега
            :return label_list: Список лейблов
        """
        self.log.debug(f"Work '{self.get_method_name()}' with tag_xpath '{tag_xpath}'")

        label_list = []
        tag_div_elements = ss(by.xpath(tag_xpath))

        self.log.debug(f"Tag_div_elements: {tag_div_elements}")

        for label in tag_div_elements:
            # label.text
            self.log.debug(f"Div label element: {label}")

        return label_list

    def get_label_list(self, tag_xpath: str) -> list:
        """
        Возвращает список лейблов в заданном теге.
            :param tag_xpath: Xpath тега
            :return label_list: Список лейблов в тегах
        """
        self.log.debug(f"Work '{self.get_method_name()}' with tag_xpath '{tag_xpath}'")

        label_list = []
        tag_elements = ss(by.xpath(tag_xpath))

        self.log.debug(f"Size tag_elements: {tag_elements.size()}")

        for label in tag_elements:
            try:
                if label.is_displayed():
                    label_text = label.text
                    if label_text != "":
                        label_list.append(label_text)
            except TimeoutException as ex:
                # self.log.debug(f"Exception: Label with xpath '{tag_xpath}' not found")
                self.log.debug(f"Exception: '{ex}'")

        self.log.debug(f"Size label_list: {len(label_list)}")
        return label_list

    def get_inputs_attr_list(self, attr: str) -> list:
        """
        Возвращает список значений заданных атрибутов в тегах "input"
            :return attr_value_list: Список значений атрибутов
        """
        self.log.debug(f"Work '{self.get_method_name()}'. Attribute: '{attr}'")

        attr_value_list = []
        input_xpath = f"//input[@{attr} and @name!='csrfmiddlewaretoken']"
        input_elements = ss(by.xpath(input_xpath))

        for element in input_elements:
            attr_value_list.append(element.get_attribute(f"{attr}"))

        return attr_value_list

    def get_button_attr_list(self, attr: str) -> list:
        """
        Возвращает список значений заданных атрибутов в тегах "button"
            :return attr_value_list: Список значений атрибутов
        """
        self.log.debug(f"Work '{self.get_method_name()}'. Attribute: '{attr}'")

        attr_value_list = []
        button_xpath = f"//button[@{attr}]"
        button_elements = ss(by.xpath(button_xpath))

        for element in button_elements:
            attr_value_list.append(element.get_attribute(f"{attr}"))

        return attr_value_list

    @allure.step("Проверка лейблов по словарю языка '{1}'")
    def check_labels(self, user_language: str, labels_dict: dict) -> None:
        """
        Проверяет лейблы на соответствие словарю, соответствующему языку пользователя
            :param user_language: Язык пользователя
            :param labels_dict: Словарь с лейблами в разрезе тегов
        """
        self.log.debug(f"Work '{self.get_method_name()}'")

        self.check_words(user_language, labels_dict, "tag")  # Надписи в различных тегах

    def get_tags(self) -> list:
        """
        Определить наличие тегов на странице
            :return: Список присутствующих тегов
        """
        self.log.debug(f"Work '{self.get_method_name()}'")
        tags_list = []

        page_source = self.drv.page_source

        for tag in self.interest_tags:
            # self.log.debug(f"Tag in 'self.interest_tags': '{tag}'")
            if tag in page_source:
                # self.log.debug(f"Tag in 'page_source': '{tag}'")
                tags_list.append(tag)

        # "title" искать всегда - не факт (фреймы), на прогоне
        if "title" not in tags_list:
            tags_list.append("title")

        self.log.debug(f"List of actual tags on the page: {tags_list}")
        return tags_list
