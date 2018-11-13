# -*- coding: utf-8 -*-
""" Хелпер скрапа объектов недвижимости, сдающихся государством в аренду на сайте "torgi.gov.ru" """

import os
import time
import pickle

from selene.api import *
# from selene.support import by
# from selene.support.jquery_style_selectors import s, ss

from selenium.webdriver.support.ui import Select

from jinja2 import Template, FileSystemLoader, Environment

from test_suites import config_file
from test_suites.base_test_class import BaseTestClass


class TorgiGovRuHelper(BaseTestClass):
    """ Хелпер скрапа объектов недвижимости, сдающихся государством в аренду на сайте "torgi.gov.ru" """

    new_object_info = {}
    file_name = "test_suites/TorgiGovRu/torgi_gov_ru.pkl"

    def come_in_ext_search(self) -> None:
        """ Войти в расширенный поиск """
        self.log.debug(f"Work '{self.get_method_name()}'")
        self.flash(s(by.xpath("//ins[@id='ext_search']"))).click()
        time.sleep(2 * config_file.WAIT_TIMEOUT)  # Костылим, по другому не хочет

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

        check_box_path = f"//td/span[text()='{config_file.PROPERTY_TYPE}']/preceding-sibling::input"
        self.flash(s(by.xpath(check_box_path))).click()

        button_xpath = "//ins[text()='Выбрать']"
        self.flash(s(by.xpath(button_xpath))).click()

        time.sleep(2 * config_file.WAIT_TIMEOUT)  # Костылим, по другому не хочет

    def set_contract_type(self) -> None:
        """ Указать вид договора """
        self.log.debug(f"Work '{self.get_method_name()}'")

        img_xpath = "//td/label[text()='Вид договора:']" \
                    "/../following-sibling::td[1]//table//tr/td/a[@title='Выбрать']/img"
        self.flash(s(by.xpath(img_xpath))).click()

        check_box_path = f"//td/span[text()='{config_file.CONTRACT_TYPE}']/preceding-sibling::input"
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
        select.select_by_visible_text(f"{config_file.COUNTRY}")

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

        s(by.xpath(field_xpath)).set_value(config_file.PROPERTY_LOCATION)

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
                int(objects_rent_periods[index].text.replace(" лет", "")),
                objects_links[index].get_attribute("href"),

            ]

        return object_info

    def to_file_save(self, info_to_save: dict) -> None:
        """ Сохранить информацию в файл """
        self.log.debug(f"Work '{self.get_method_name()}'. Filename: {self.file_name}")

        output_file = open(self.file_name, "wb")
        pickle.dump(info_to_save, output_file)
        output_file.close()

    def from_file_load(self) -> dict:
        """ Считать информацию из файла """
        self.log.debug(f"Work '{self.get_method_name()}'. Filename: {self.file_name}")

        input_file = open(self.file_name, 'rb')
        info_from_file = pickle.load(input_file)
        input_file.close()

        return info_from_file

    @property
    def payback_calculation(self) -> list:
        """ Рассчитать коэффициент окупаемости для каждого объекта """
        self.log.debug(f"Work '{self.get_method_name()}'")

        big_realty_dict = {}        # Большой словарь с параметрами объектов для отчёта

        for real_obj in self.new_object_info:

            building_area = self.new_object_info[real_obj][0]                   # Площадь объекта, кв.м.
            rent_rights_cost = 12 * self.new_object_info[real_obj][1]           # Стоимости права аренды, руб в год
            rent_time = self.new_object_info[real_obj][2]                       # Срок аренды, лет

            # Страховка всей площади за год, руб
            year_all_area_insurance = self.get_insurance(building_area)

            # Стоимость отопления в месяц, руб
            month_heating = config_file.HEATING * building_area

            # Обслуживание ЖЭКом в месяц, руб
            month_housing_office = config_file.HOUSING_OFFICE * building_area

            # Доход от аренды в месяц
            month_rental_income = building_area * config_file.AVERAGE_RENTAL

            # Выплаты за аренду в месяц
            month_rental_payout = self.new_object_info[real_obj][1]

            # Расходы в месяц
            month_payout = \
                month_rental_payout + \
                month_heating + \
                month_housing_office + \
                config_file.ACCOUNTING_SERVICE + \
                (config_file.CONTRACT_REGISTRATION + config_file.RUNNING_COST) / rent_time / 12

            # Доход в год с учётом несдаваемых месяцев
            year_rental_income = month_rental_income * config_file.PROFIT_MONTHS

            # Коэффициент доходности
            profit_margin = (year_rental_income - (month_payout * 12) + year_all_area_insurance) / \
                            (config_file.CONTRACT_REGISTRATION + config_file.RUNNING_COST)

            # Безубыточность сдачи, руб/кв.м. в месяц
            loss_free_rent = ((month_payout * 12) / 10) / building_area

            # Собрать большой словарь с параметрами объектов для отчёта
            big_realty_dict[real_obj] = {
                "Коэффициент доходности": int(f"{profit_margin:.0f}"),
                "Площадь": f"{building_area:.1f}",
                "Безубыточная сдача, руб/кв.м. в месяц": f"{loss_free_rent:.2f}",
                "Выплаты ренты в год": f"{rent_rights_cost:.2f}",
                "Страховка за год": f"{year_all_area_insurance:.2f}",
                "Выплаты ренты в месяц": f"{month_rental_payout:.2f}",
                "Расходы в месяц": f"{month_payout:.2f}",
                "Стоимость отопления в месяц": f"{month_heating:.2f}",
                "Обслуживание ЖЭКом в месяц": f"{month_housing_office:.2f}",
                "Доход в год": f"{year_rental_income:.2f}",
                "Доход в месяц": f"{month_rental_income:.2f}",
            }

        # Отсортировать большой словарь по коэффициенту доходности
        sort_field_name = "Коэффициент доходности"
        sorted_big_realty_list = sorted(big_realty_dict.items(), key=lambda x: x[1][sort_field_name], reverse=True)

        return sorted_big_realty_list

    def get_insurance(self, building_area: float) -> float:
        """ Расчёт Страховки всей площади за год """
        # self.log.debug(f"Work '{self.get_method_name()}'")

        if 0 < building_area < 100:
            year_all_area_insurance = config_file.YEARLY_INSURANCE[100]
        elif 100 <= building_area < 300:
            year_all_area_insurance = config_file.YEARLY_INSURANCE[300]
        elif 300 <= building_area < 500:
            year_all_area_insurance = config_file.YEARLY_INSURANCE[500]
        elif 500 <= building_area < 1000:
            year_all_area_insurance = config_file.YEARLY_INSURANCE[1000]
        elif 1000 <= building_area:
            year_all_area_insurance = config_file.YEARLY_INSURANCE[99999999]
        else:
            self.log.debug(f"Неудачная площадь: '{building_area}' кв.м. поэтому и неудачная сумма годовой страховки")
            assert False

        return year_all_area_insurance

    def html_report_create(self, realty_list: list) -> None:
        """ Создать отчёт в формате HTML """
        self.log.debug(f"Work '{self.get_method_name()}'")

        # Темлейт "jinja2"
        project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        template_dir = project_dir + os.path.sep + "templates"
        env = Environment(loader=FileSystemLoader(template_dir))
        html_template = env.get_template("realty_table.tpl")

        # Преобразовать данные для темплейта
        realty_list_for_template = self.convert_real_dict_to_list(realty_list)

        # Получить заголовки столбцов таблицы из данных
        realty_list_titles = self.get_table_titles(realty_list)

        # Записать html файл
        with open(template_dir + os.path.sep + "index.html", "w", encoding='utf-8') as html_file:
            html_file.write(html_template.render(
                table_titles=realty_list_titles,
                realty_objects_array=realty_list_for_template,
            ))

    def convert_real_dict_to_list(self, in_list: list) -> list:
        """ Преобразовать список со словарями данных объекта в список для темплейта """
        self.log.debug(f"Work '{self.get_method_name()}'")

        out_list = []
        for real_obj in in_list:

            real_list = [
                real_obj[0],
                real_obj[1]["Коэффициент доходности"],
                real_obj[1]["Площадь"],
                real_obj[1]["Безубыточная сдача, руб/кв.м. в месяц"],
                real_obj[1]["Выплаты ренты в год"],
                real_obj[1]["Страховка за год"],
                real_obj[1]["Выплаты ренты в месяц"],
                real_obj[1]["Расходы в месяц"],
                real_obj[1]["Стоимость отопления в месяц"],
                real_obj[1]["Обслуживание ЖЭКом в месяц"],
                real_obj[1]["Доход в год"],
                real_obj[1]["Доход в месяц"],
            ]

            out_list.append(real_list)

        return out_list

    def get_table_titles(self, in_list: list) -> list:
        """ Получить заголовки столбцов таблицы из данных """
        self.log.debug(f"Work '{self.get_method_name()}'")

        title_list = in_list[0][1].keys()

        return title_list
