# -*- coding: utf-8 -*-
"""
    Скрапинг объектов недвижимости, сдающихся государством в аренду
"""
import allure
import pytest

from test_suites import config_file
from test_suites.base_test_class import BaseTestClass


class TestTorgiGovRu(BaseTestClass):

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
    # @pytest.mark.dependency()
    @allure.step("Доступность WEB приложения")
    def test_web_app_accessibility(self):
        """ Проверка доступности WEB приложения """
        # Открыть страницу сайта
        self.open_site(config_file.SITE_NAME)
