# -*- coding: utf-8 -*-
""" Базовый PageObject """

import time
import inspect

from test_suites import config_file
from test_suites.base_test_class import BaseTestClass


def get_method_name() -> str:
    """ Возвращает имя текущего метода """
    return inspect.stack()[1][3]


class BasePage(BaseTestClass):
    """
    Базовый класс BaseObject
        iframe_src_tag_part - часть значения тега "src" фрейма \n
        tab_name - имя закладки страницы \n
        page_title - заголовок страницы
    """

    def __init__(self, page_obj_init_list: list) -> None:
        """
        Конструктор
            :param page_obj_init_list: Список с параметрами инициализации класса
        """
        self.iframe_src_tag_part = page_obj_init_list[0]  # часть значения тега "src" фрейма
        self.tab_name = page_obj_init_list[1]  # имя закладки страницы
        self.page_title = page_obj_init_list[2]  # заголовок страницы

    def switch_to_page_frame(self) -> None:
        """
        Переключиться на фрейм справочника
        """
        self.log.debug(f"Work '{get_method_name()}': '{self.iframe_src_tag_part}'")
        frame_xpath = f"//iframe[contains(@src, '{self.iframe_src_tag_part}')]"

        wait_time = 60
        self.switch_to_frame_with_adaptive_waiting(frame_xpath, wait_time)
        time.sleep(config_file.WAIT_TIMEOUT)
