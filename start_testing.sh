#!/bin/sh
#/bin/cp environment.xml results_for_allure/environment.xml

#######################################################################
# To display debug messages in the console, use "-s" switch for pytest.
#######################################################################

py.test --tb=short -v -l --alluredir results_for_allure --allure-features="1. TorgiGovRu"
#py.test --tb=short -v -l --alluredir results_for_allure --allure-features="1. Login"
#py.test --tb=short -v -l --alluredir results_for_allure --allure-features="2. TestMenuItems"
#py.test --tb=short -v -l --alluredir results_for_allure --allure-features="3. ProfilePage"

exit 0
