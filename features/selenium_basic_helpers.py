import os
import time
import urlparse
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#TODO: We should get this value from behave.ini
CHECK_INTERVAL_SECONDS = 0.01

def find_element(context, element, identifier, timeout=5.0):
    """
    Looks for a single web element in the page.
    :param context: the behave context variable.
    :param element: the element value to find.
    :param identifier: search by 'css_selector', 'id', 'name' or 'class_name'.
    :param timeout: optional parameter. Retries the search until n seconds (float).
    :return: selenium web element.
    """
    options = {
        'css_selector': context.browser.find_element_by_css_selector,
        'id': context.browser.find_element_by_id,
        'name': context.browser.find_element_by_name,
        'class_name': context.browser.find_element_by_class_name,
    }
    while timeout > 0:
        try:
            search_input = lambda: options[identifier](element)
            return search_input()
        except (ElementNotVisibleException, NoSuchElementException):
            time.sleep(CHECK_INTERVAL_SECONDS)
            timeout -= CHECK_INTERVAL_SECONDS
    search_input = lambda: options[identifier](element)
    return search_input()

def find_elements(context, selector, timeout=10):
    """
    Looks for a group of elements in the page.
    :param context: the behave context variable.
    :param selector: the css selector value to find.
    :param timeout: optional parameter. Retries the search until n seconds (float).
    :return: List of selenium web elements if found. If not elements found it will return an empty list.
    """
    while timeout > 0:
        elements = context.browser.find_elements_by_css_selector(selector)
        if elements != []:
            return elements
        else:
            time.sleep(1)
            timeout -= 1
    return []

def wait_for_element_to_appear(context, selector, timeout):
    """
    Wait the specified amount of time until the element appears.
    :param context: the behave context variable.
    :param selector: css_selector corresponding to the element.
    :param timeout: time to wait until the element appears.
    :return: Nothing, if the element does not appear in the specified time then an exception is raised.
    """
    element = find_element(context, selector, 'css_selector')
    while timeout > 0:
        if element.is_displayed():
            assert True
            return
        time.sleep(CHECK_INTERVAL_SECONDS)
        timeout -= CHECK_INTERVAL_SECONDS
    context.browser.refresh()
    raise Exception("The element {selector} is not displayed within {timeout} seconds".format(**locals()))

def wait_for_element_to_disappear(context, selector, identifier, timeout=10.0):
    """
    Wait n seconds until the specified element dissapears.
    :param context: the behave context variable.
    :param selector: the element value to find.
    :param identifier: search by 'css_selector', 'id', 'name' or 'class_name'.
    :param timeout: Optional. time to wait until the element dissapears.
    :return: True if the element dissapears. An exception is raised if the element does not dissapear.
    """
    print("locals:{l}").format(**locals())
    while timeout >= 0:
        print("Timeout while entering", timeout)
        try:
            element = find_element(context, selector, identifier, timeout=0.0)
            if not element.is_displayed():
                return True
            time.sleep(CHECK_INTERVAL_SECONDS)
            timeout -= CHECK_INTERVAL_SECONDS
            print("Timeout on try", timeout)
        except (ElementNotVisibleException, NoSuchElementException, StaleElementReferenceException):
            return True
    assert False, "The element {selector} has not dissapeared within {timeout} seconds".format(**locals())

def scroll_element_into_view(driver, element):
    """
    Scrolls to an element.
    :param driver: the behave context.
    :param element: the web element object.
    :return: nothing.
    """
    y = element.location['y']
    driver.execute_script('window.scrollTo(0, {0})'.format(y))

def take_snapshot(context, output_format, text):
    """
    Takes an snapshot. It will be stored in a html file if the format is base64 or in a separate png file. The output directory will be snapshots.
    :param context: The behave context.
    :param output:format (base64 will add it to html file, or file to create a png file)
    :param text:label for base64, part of the file name in the case of file
    """
    if not os.path.exists("snapshots"):
        os.makedirs("snapshots")
    if output_format == "base64":
        captured_img = context.browser.get_screenshot_as_base64()
        if os.path.isfile("snapshots/snapshots_report.html"):
            with open("snapshots/snapshots_report.html", "a") as snapshot_file:
                snapshot_file.write("""<br>"""+ text.encode('utf-8').strip('\u2019') +"""<br><img src="data:image/png;base64,"""+captured_img+"""" />""")
        else:
            with open("snapshots/snapshots_report.html", "w") as snapshot_file:
                snapshot_file.write("""<br>"""+ text.encode('utf-8').strip('\u2019')+"""<br><img src="data:image/png;base64,"""+captured_img+"""" />""")
    if output_format == "file":
        captured_img = context.browser.get_screenshot_as_file("snapshots/" + str(time.time()) + text + ".png")
        if captured_img == False:
            raise Exception("ERROR: cannot take snapshot...")
