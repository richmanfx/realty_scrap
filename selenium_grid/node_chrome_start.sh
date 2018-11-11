#!/bin/sh
java -Dwebdriver.chrome.driver=/home/zoer/PycharmProjects/realty_scrap/drivers/chromedriver -jar /home/zoer/PycharmProjects/realty_scrap/selenium_grid/selenium-server-standalone.jar -role webdriver -hub http://localhost:4444/grid/register -port 5558 -browser browserName=chrome

