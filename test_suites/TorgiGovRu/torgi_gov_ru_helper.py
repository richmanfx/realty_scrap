# -*- coding: utf-8 -*-
""" Хелпер скрапа объектов недвижимости, сдающихся государством в аренду на сайте "torgi.gov.ru" """

import time
import pickle

from selene.api import *
# from selene.support import by
# from selene.support.jquery_style_selectors import s, ss

from selenium.webdriver.support.ui import Select

from test_suites import config_file
from test_suites.base_test_class import BaseTestClass


class TorgiGovRuHelper(BaseTestClass):
    """ Хелпер скрапа объектов недвижимости, сдающихся государством в аренду на сайте "torgi.gov.ru" """

    new_object_info = {}

    def come_in_ext_search(self) -> None:
        """ Войти в расширенный поиск """
        self.log.debug(f"Work '{self.get_method_name()}'")
        self.flash(s(by.xpath("//ins[@id='ext_search']"))).click()
        time.sleep(config_file.WAIT_TIMEOUT)  # Костылим, по другому не хочет

    def set_auction_type(self) -> None:
        """ Выбрать тип торгов """
        self.log.debug(f"Work '{self.get_method_name()}'")
        self.flash(s(by.xpath("//a/div/li[text()='В процессе подачи заявок']"))).click()

    def set_property_type(self) -> None:
        """ Указать тип имущества """
        self.log.debug(f"Work '{self.get_method_name()}'")

        img_xpath = "//td/label[text()='Тип имущества:']" \
                    "/../following-sibling::td[1]//table//tr/td/a[@title='Выбрать']/img"
        self.flash(s(by.xpath(img_xpath))).click()

        check_box_path = "//td/span[text()='Помещение']/preceding-sibling::input"
        self.flash(s(by.xpath(check_box_path))).click()

        button_xpath = "//ins[text()='Выбрать']"
        self.flash(s(by.xpath(button_xpath))).click()

        time.sleep(config_file.WAIT_TIMEOUT)  # Костылим, по другому не хочет

    def set_contract_type(self) -> None:
        """ Указать вид договора """
        self.log.debug(f"Work '{self.get_method_name()}'")

        img_xpath = "//td/label[text()='Вид договора:']" \
                    "/../following-sibling::td[1]//table//tr/td/a[@title='Выбрать']/img"
        self.flash(s(by.xpath(img_xpath))).click()

        check_box_path = "//td/span[text()='Договор аренды']/preceding-sibling::input"
        self.flash(s(by.xpath(check_box_path))).click()

        button_xpath = "//ins[text()='Выбрать']"
        self.flash(s(by.xpath(button_xpath))).click()

        time.sleep(config_file.WAIT_TIMEOUT)  # Костылим, по другому не хочет

    def set_country(self) -> None:
        """ Выбрать страну """
        self.log.debug(f"Work '{self.get_method_name()}'")

        label_select_country_xpath = "//label[text()='Страна размещения:']"
        select_country_xpath = "//select[@name='extended:country']"
        self.flash(s(by.xpath(label_select_country_xpath)))
        select = Select(s(by.xpath(select_country_xpath)))
        select.select_by_visible_text("РОССИЯ")

    def set_property_location(self) -> None:
        """ Указать местоположение имущества """
        self.log.debug(f"Work '{self.get_method_name()}'")

        time.sleep(config_file.WAIT_TIMEOUT)  # Костылим, по другому не хочет

        img_xpath = "//td/label[text()='Местоположение:']" \
                    "/../following-sibling::td[1]//table//tr/td/a[@title='Выбрать']/img"
        self.flash(s(by.xpath(img_xpath))).click()

        # Субъект РФ
        label_xpath = "//label[text()='Субъект РФ:']"
        field_xpath = "//input[@name='container1:level1']"
        self.flash(s(by.xpath(label_xpath)))

        value = "Москва (г)"
        s(by.xpath(field_xpath)).set_value(value)

        button_xpath = "//ins[text()='Выбрать']"
        self.flash(s(by.xpath(button_xpath))).click()

        time.sleep(config_file.WAIT_TIMEOUT)  # Костылим, по другому не хочет

    def set_object_area_range(self) -> None:
        """ Указать диапазон площади объекта """
        self.log.debug(f"Work '{self.get_method_name()}'")

        time.sleep(config_file.WAIT_TIMEOUT)  # Костылим, по другому не хочет

        min_label_xpath = "//label[text()='Площадь (м²) с:']"
        min_field_xpath = "//input[@name='extended:areaMeters:stringAreaMetersFrom']"
        self.flash(s(by.xpath(min_label_xpath)))
        s(by.xpath(min_field_xpath)).set_value(config_file.OBJECT_MIN_AREA)

        max_label_xpath = "//label[text()='Площадь (м²) с:']/../following-sibling::td/label[text()='по:']"
        max_field_xpath = "//input[@name='extended:areaMeters:stringAreaMetersTo']"
        self.flash(s(by.xpath(max_label_xpath)))
        s(by.xpath(max_field_xpath)).set_value(config_file.OBJECT_MAX_AREA)

    def set_rental_period(self) -> None:
        """ Указать минимальный срок аренды """
        self.log.debug(f"Work '{self.get_method_name()}'")

        label_xpath = "//label[text()='Срок аренды (мес.) с:']"
        field_xpath = "//input[@name='extended:propertyExtended:stringRentFrom']"
        self.flash(s(by.xpath(label_xpath)))
        s(by.xpath(field_xpath)).set_value(config_file.MIN_RENTAL_PERIOD * 12)

    def search_button_click(self) -> None:
        """ Кликнуть на кнопке поиска """
        self.log.debug(f"Work '{self.get_method_name()}'")

        button_xpath = "//ins[@id='lot_search']"
        self.flash(s(by.xpath(button_xpath))).click()

    def objects_wait(self) -> None:
        """ Дождаться отображения объектов """
        self.log.debug(f"Work '{self.get_method_name()}'")

        xpath = "//h2/span[contains(text(),'найдено лотов')]"
        self.flash(s(by.xpath(xpath))).is_displayed()

        time.sleep(config_file.WAIT_TIMEOUT)        # Для завершения поиска и

    def get_objects_quantity(self) -> int:
        """ Определить количество найденных объектов """
        self.log.debug(f"Work '{self.get_method_name()}'")

        xpath = "//h2/span[contains(text(),'найдено лотов')]"
        label_text = self.flash(s(by.xpath(xpath))).text
        objects_quantity = label_text.split(" ")[-1]

        return objects_quantity

    def object_info_collect(self, all_object_info: dict) -> None:
        """ Собирает информацию по объектам на всех страницах """
        self.log.debug(f"Work '{self.get_method_name()}'")

        # Собрать на текущей странице
        object_info = self.one_page_object_info_collect()

        # Добавить к основному словарю
        self.new_object_info = self.merge_two_dicts(all_object_info, object_info)

        # Есть ли следующая страница
        next_page_xpath = "//a[@title='Перейти на одну страницу вперед']"
        next_page_links = ss(by.xpath(next_page_xpath))
        if next_page_links.size() < 1:   # Условие выхода из рекурсии
            # Выходим
            # self.log.debug("Выход из рекурсии")
            return
        else:
            # Перейти на следующую страницу
            self.go_to_next_page()
            self.object_info_collect(self.new_object_info)      # Рекурсия

    def go_to_next_page(self):
        """ Пагинация """
        self.log.debug(f"Work '{self.get_method_name()}'")

        next_page_xpath = "//a[@title='Перейти на одну страницу вперед']"
        next_page_link = s(by.xpath(next_page_xpath))
        self.flash(next_page_link)
        next_page_link.click()
        time.sleep(config_file.WAIT_TIMEOUT)

    @staticmethod
    def merge_two_dicts(dict_1: dict, dict_2: dict) -> dict:
        """ Объединить два словаря """
        sum_dict = dict_1.copy()
        sum_dict.update(dict_2)
        return sum_dict

    def one_page_object_info_collect(self) -> dict:
        """ Собирает информацию по объектам на одной странице """
        self.log.debug(f"Work '{self.get_method_name()}'")

        object_info = {}

        real_obj_xpath = "//div[@class='scrollx']/table//tr[contains(@class,'datarow')]"
        real_objects = ss(by.xpath(real_obj_xpath))
        real_objects_on_page_count = real_objects.size()

        # Номера извещений объектов
        notice_numbers_xpath = real_obj_xpath + "/td[3]/span/span[1]"
        objects_notice_numbers = ss(by.xpath(notice_numbers_xpath))

        # Площадь объектов
        area_xpath = real_obj_xpath + "/td[3]/span/span[4]"
        objects_areas = ss(by.xpath(area_xpath))

        # Стоимость аренды в месяц
        rent_xpath = real_obj_xpath + "/td[7]/span"
        objects_month_rents = ss(by.xpath(rent_xpath))

        # Срок аренды
        rent_periods_xpath = real_obj_xpath + "/td[6]/span/span[2]"
        objects_rent_periods = ss(by.xpath(rent_periods_xpath))

        # Ссылка для просмотра
        link_xpath = real_obj_xpath + "/td[1]//a[@title='Просмотр']"
        objects_links = ss(by.xpath(link_xpath))

        # Информацию в словарь
        for index in range(real_objects_on_page_count):
            object_info[objects_notice_numbers[index].text] = [
                float(objects_areas[index].text.replace(" м²", "")),
                float(objects_month_rents[index].text.replace(" ", "").replace(",", ".").replace("руб.", "")),
                objects_links[index].get_attribute("href"),
                int(objects_rent_periods[index].text.replace(" лет", "")),
            ]

        return object_info

    def to_file_save(self, info_to_save: dict) -> None:
        """ Сохранить информацио в файл """
        self.log.debug(f"Work '{self.get_method_name()}'")
