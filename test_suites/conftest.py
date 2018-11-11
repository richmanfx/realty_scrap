# -*- coding: utf-8 -*-
""" Хуки всякие """

import allure

from test_suites.base_test_class import BaseTestClass


def pytest_exception_interact(node):
    """ Выполняется при падении любого теста """

    BaseTestClass.log.debug(f"Work '{BaseTestClass.get_method_name()}'")
    driver = node.instance.drv

    # Прикрепить скриншот после падения теста
    message = f"Скриншот после падения теста '{node.name}'"
    allure.attach(driver.get_screenshot_as_png(), message, allure.attachment_type.PNG)
