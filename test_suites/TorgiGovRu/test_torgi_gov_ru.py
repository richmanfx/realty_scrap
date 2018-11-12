# -*- coding: utf-8 -*-
"""
    Скрапинг объектов недвижимости, сдающихся государством в аренду на сайте "torgi.gov.ru"
"""
import allure
import pytest

from test_suites import config_file
from test_suites.TorgiGovRu.torgi_gov_ru_helper import TorgiGovRuHelper


class TestTorgiGovRu(TorgiGovRuHelper):

    def setup_method(self) -> None:
        """ Метод выполнится перед каждым тестовым методом класса """
        # Время старта теста в Allure отчёт
        self.current_date_time_output()

    def teardown_class(self) -> None:
        """ Метод выполнится после выполнения всех тестовых методов класса """
        # Закрыть браузер
        self.drv.quit()

    ####################################################################################################################
    # @pytest.skip
    @allure.feature("1. TorgiGovRu")
    @pytest.mark.run(order=101)
    @pytest.mark.dependency()
    @allure.step("Выставление фильтров поиска")
    def test_set_search_filters(self):
        """ Выставить фильтры поиска """

        # Открыть страницу сайта
        self.open_site(config_file.SITE_NAME)

        # Выбрать тип торгов
        # self.set_auction_type()

        # Войти в расширенный поиск
        self.come_in_ext_search()

        # Указать тип имущества
        self.set_property_type()

        # Указать вид договора
        self.set_contract_type()

        # Указать страну
        self.set_country()

        # Указать местоположение имущества
        self.set_property_location()

        # Указать диапазон площади объекта
        self.set_object_area_range()

        # Указать минимальный срок аренды
        self.set_rental_period()

        # Искать
        self.search_button_click()

        # Дождаться отображения объектов
        self.objects_wait()

    ####################################################################################################################
    # @pytest.skip
    @allure.feature("1. TorgiGovRu")
    @pytest.mark.run(order=102)
    @pytest.mark.dependency(depends=["test_set_search_filters"])
    @allure.step("Сбор информации об объектах")
    def test_collect_information_about_objects(self):
        """ Собрать информацию об объектах """

        # Определить количество найденных объектов
        objects_quantity = self.get_objects_quantity()
        self.log.debug(f"Количество найденных объектов: {objects_quantity}")

        # Собрать информацию об объектах
        self.object_info_collect({})
        self.log.debug(f"Колекция объектов: {self.new_object_info}")

