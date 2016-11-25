import os
import time
import urlparse
from behave import *
from selenium_basic_helpers import *
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CHECK_INTERVAL_SECONDS = 0.01


#############################
#### BASIC HELPER METHODS####
#############################



#################################################
#### SUBSTEPS (FOR BASIC ACTIONS)################
#################################################
# Valid identifiers: 'css_selector, id', 'name' and 'class_name'


#****************
# WHEN STEPS
#****************

#Valid formats for screenshot: base64, file
@when('take screenshot as {output_format} and show description {text}')
def step(context, output_format, text):
    if not os.path.exists("snapshots"):
        os.makedirs("snapshots")
    if output_format == "base64":
        captured_img = context.browser.get_screenshot_as_base64()
        if os.path.isfile("snapshots/snapshots_report.html"):
            with open("snapshots/snapshots_report.html", "a") as snapshot_file:
                snapshot_file.write("""<br>"""+ text +"""<br><img src="data:image/png;base64,"""+captured_img+"""" />""")
        else:
            with open("snapshots/snapshots_report.html", "w") as snapshot_file:
                snapshot_file.write("""<br>"""+ text +"""<br><img src="data:image/png;base64,"""+captured_img+"""" />""")

    if output_format == "file":
        captured_img = context.browser.get_screenshot_as_file("snapshots/" + str(time.time()) + text + ".png")
        if captured_img == False:
            raise Exception("ERROR: cannot take snapshot...")

@when('opening the url {url}')
def step(context, url):
    context.browser.get(urlparse.urljoin(context.config.userdata.get('target_env'), url))

@when('I refresh the page')
def step(context):
    context.browser.refresh()

@when('I scroll down element {element_selector} {times} times')
def step(context, element_selector, times):
    element = find_element(context, element_selector, 'css_selector')
    try:
        action = ActionChains(context.browser)
        action.move_to_element(element).perform()
        element.click()
        for _ in range(times):
            element.send_keys(Keys.SPACE)
            time.sleep(0.1)
    except Exception as e:
        raise Exception('Error scrolling down web element')

@when('hover on element {element} identified by {identifier}')
def step(context, element, identifier):
    element = find_element(context, element, identifier)
    hov = ActionChains(context.browser).move_to_element(element)
    hov.perform()

@when('back to the previous page')
def step(context):
    context.browser.back()

@when('fill input field {field_name}, identified by {identifier} with the value {value}')
def steps(context, field_name, identifier, value, timeout = 5.0):
    input_field = find_element(context, field_name, identifier)
    input_field.clear()
    input_field.send_keys(value)
    while timeout > 0:
        if input_field.get_attribute('value') == value:
            return
        time.sleep(CHECK_INTERVAL_SECONDS)
        timeout -= CHECK_INTERVAL_SECONDS

@when('fill select field {field_name}, identified by {identifier} with the value {value}')
def steps(context, field_name, identifier, value):
    select_field = Select(find_element(context, field_name, identifier))
    select_field.select_by_visible_text(value)

@when('click on button {button_name} identified by {identifier}')
def step(context, button_name, identifier):
    button = find_element(context, button_name, identifier)
    button.click()

@when('click in {section} identified by {identifier}')
def step(context, section, identifier):
    element = find_element(context, section, identifier)
    scroll_element_into_view(context.browser, element)
    element.click()

@when('move to element {element}, identified by {identifier}')
def step(context, element, identifier):
    element = find_element(context, element, identifier)
    actions = ActionChains(context.browser)
    actions.move_to_element(element)
    actions.perform()

@when('select option {option} in combobox {element}, identified by {identifier}')
def step(context, option, element, identifier):
    element = find_element(context, element, identifier)
    select = Select(element)
    select.select_by_visible_text(option)

# Shortcuts:
@when('hovering {selector}')
def step(context, selector):
    element = find_element(context, selector, 'css_selector')
    hover = ActionChains(context.browser).move_to_element(element)
    hover.perform()

@when('clicking {selector}')
def step(context, selector):
    element = find_element(context, selector, 'css_selector')
    element.click()

@when('click in link with text {text}')
def step(context, text):
    wait = WebDriverWait(context.browser, 10)
    if context.config.userdata.get('browser_name') == "ie":
        link = find_element(context, ".text > div:nth-child(1) > a:nth-child(2)", 'css_selector')
    else:
        link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, text)))
    if context.config.userdata.get('browser_name') == "chrome" or context.config.userdata.get('browser_name') == "ie":
        context.browser.execute_script("arguments[0].click();", link)
    else:
        link.click()

@when('uploading {image} to {selector}')
def step(context, image, selector):
    element = find_element(context, selector, 'css_selector')
    image_path = os.path.join(os.getcwd(), 'images', image)
    if context.config.userdata.get('browser_name') == "ie":
        fix_ie_script = "function fixie(){document.querySelector(\"" + selector  +  "\").style.opacity=1;}" + "fixie();"
        context.browser.execute_script(fix_ie_script)
    element.send_keys(image_path)

@when('upload the video {video} to {selector}')
def step(context, video, selector):
    element = find_element(context, selector, 'css_selector')
    video_path = os.path.join(os.getcwd(), 'videos', video)
    if context.config.userdata.get('browser_name') == "ie":
        fix_ie_script = "function fixie(){document.querySelector(\"" + selector  +  "\").style.opacity=1;}" + "fixie();"
        context.browser.execute_script(fix_ie_script)
    element.send_keys(video_path)

@when('upload the zip {zip_file} to {selector}')
def step(context, zip_file, selector):
    fix_ie_script = \
        "function fixie(){ " \
            "var el = document.querySelector(\"" + selector + "\");" \
            "el.style='';" \
        "}" + "fixie();"
    context.browser.execute_script(fix_ie_script)
    wait_for_element_to_appear(context, selector, float(5))
    element = find_element(context, selector, 'css_selector')
    zip_path = os.path.join(os.getcwd(), 'assets/zip', zip_file)
    element.send_keys(zip_path)

@when('upload the marker {img_file} to {selector}')
def step(context, img_file, selector):
    fix_ie_script = \
        "function fixie(){ " \
            "var el = document.querySelector(\"" + selector + "\");" \
            "el.style='';" \
        "}" + "fixie();"
    context.browser.execute_script(fix_ie_script)
    wait_for_element_to_appear(context, selector, float(5))
    element = find_element(context, selector, 'css_selector')
    zip_path = os.path.join(os.getcwd(), 'assets/img', img_file)
    element.send_keys(zip_path)

#options: up, down, left, right, enter
@when('send key {key} to {selector}')
def step(context, key, selector):
    element = find_element(context, selector, 'css_selector')
    if key == "up":
        element.send_keys(Keys.ARROW_UP)
    if key == "down":
        element.send_keys(Keys.ARROW_DOWN)
    if key == "left":
        element.send_keys(Keys.ARROW_LEFT)
    if key == "right":
        element.send_keys(Keys.ARROW_RIGHT)
    if key == "enter":
        element.send_keys(Keys.ENTER)
    else:
        element.send_keys(key)

@when('typing {value} in {selector}')
def steps(context, selector, value):
    element = find_element(context, selector, 'css_selector')
    if not element.is_displayed():
        assert False, "cannot type {value} in {selector}, element not displayed".format(**locals())
    element.clear()
    element.send_keys(value)

@when('selecting {option} in {selector}')
def step(context, option, selector):
    select = Select(find_element(context, selector, 'css_selector'))
    select.select_by_visible_text(option)

@when('drag element {source_element} into {target_element}')
def step(context, source_element, target_element):
    source = find_element(context, source_element, 'css_selector')
    target = find_element(context, target_element, 'css_selector')
    actionchains = ActionChains(context.browser)
    ele = actionchains.drag_and_drop(source, target)
    ele.perform()

@when('drag element {source_element} to positions x {x} and y {y}')
def step(context, source_element, x, y):
    source = find_element(context, source_element, 'css_selector')
    actionchains = ActionChains(context.browser)
    ele = actionchains.drag_and_drop_by_offset(source, int(x), int(y))
    ele.perform()

@when('make element {element_css_selector} visible')
def step(context, element_css_selector):
    element = find_element(context, element_css_selector, 'css_selector')
    js = "arguments[0].style.height='auto'; arguments[0].style.visibility='visible';";
    context.browser.execute_script(js, element)

#****************
# THEN STEPS
#****************

@then("wait for element {element} identified by {identifier}")
def step(context, element, identifier, timeout=10):
    find_element(context, element, identifier)

@then("check that the element {element} disappears, identified by {identifier}")
def step(context, element, identifier):
    wait_for_element_to_disappear(context, element, identifier)

@then("the page contains the text {expected}")
def step(context, expected):
    pass

@then("the page title must be {expected}")
def step(context, expected):
    assert context.browser.title == expected, "Error: Page title expected: {expected}, obtained: {obtained}".format(expected=expected, obtained=context.browser.title)

@then("the login error message appears saying {error_message}")
def step(context, expected):
    pass

@then("check that the combo button {combo_button} is selected")
def step(context, combo_button):
    if combo_button.is_selected():
        assert True
    else:
        assert False

@then("check that the element {selector} is not present")
def step(context, selector):
    try:
        element = find_element(context, selector, 'css_selector', timeout=1.0)
        assert False, "Error, the element is present, it is expected to be not present"
    except:
        assert True

@then("the text {text} is present in the element {element} identified by {identifier}")
def step(context, text, element, identifier):
    elem = find_element(context, element, identifier)
    assert elem.text == text, "Error: expected value is {exp}, but the actual value is {actual}".format(exp=text, actual=elem.text)

@then("the input field {input_field_element} contains the value {value} identified by {identifier}")
def step(context, input_field_element, value, identifier):
    elem = find_element(context, input_field_element, identifier)
    elem_value = elem.get_attribute("value")
    assert elem_value == value, "ERROR: Expected input {selector} to contain '{text}', but contains '{elem_text}'".format(selector=input_field_element, text=value, elem_text=elem_value)

@then("check that the element {element} is displayed, identified by {identifier}")
def step(context, element, identifier):
    elem = find_element(context, element, identifier)
    if elem.is_displayed():
        assert True
    if not elem.is_displayed():
        assert False, "The element is not displayed"

@then("wait until the element {element} is displayed, identified by {identifier}")
def step(context, element, identifier, timeout=5):
    elem = find_element(context, element, identifier)
    while timeout > 0:
        if elem.is_displayed():
            assert True
            return
        time.sleep(1)
        timeout -= 1
    assert False, "The element is not displayed"

@then("expect {selector} to contain {text}")
def step(context, selector, text):
    element = find_element(context, selector, 'css_selector')
    # lower(): when text is uppercased with CSS, it will return uppercase.
    assert text.lower() in element.text.lower(), "Expected {selector} to contain '{text}', but contains '{elem_text}'".format(text=text, selector=selector, elem_text=element.text)

@then("expect {selector} to have the value {text}")
def step(context, selector, text):
    element = find_element(context, selector, 'css_selector')
    assert text in element.get_attribute('value'), "Expected input {selector} to have the value '{text}', but has value '{elem_text}'".format(text=text, selector=selector, elem_text=element.get_attribute('value'))

@then("expect {selector} to disappear within {timeout} seconds")
def step(context, selector, timeout):
    wait_for_element_to_disappear(context, selector, 'css_selector', timeout=float(timeout))

@then("expect {selector} to disappear")
def step(context, selector):
    wait_for_element_to_disappear(context, selector, 'css_selector')

@then("allow time to update the UI")
def step(context):
    time.sleep(CHECK_INTERVAL_SECONDS)

@then("allow {time_seconds}s to update the UI")
def step(context, time_seconds):
    time.sleep(float(time_seconds))

@then("wait up to {timeout} seconds for {selector}")
def step(context, timeout, selector):
    wait_for_element_to_appear(context, selector, float(timeout))

@then("expect {selector} to have {option} selected")
def step(context, selector, option):
    element = find_element(context, selector, 'css_selector')
    select = Select(element)
    assert select.first_selected_option.text == option, \
        "Expected {option} to be selected, but {actual_option} was selected instead".format(
            option=option, actual_option=select.first_selected_option.text)

@then("wait for element {selector} to be clickable")
def step(context, selector):
    wait = WebDriverWait(context.browser, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))

@then("check that the combobox element {selector} selected value is {value}")
def step(context, selector, value):
    selected_option = Select(find_element(context, selector, 'css_selector')).first_selected_option.text
    if value == selected_option:
        assert True
    else:
        assert False, "Error, the option selected is '{observed}', expected '{obtained}'".format(observed=selected_option, obtained=value)

# These should be at the end of the file to prevent conflicts.
@then("expect {selector}")
def step(context, selector):
    element = find_element(context, selector, 'css_selector')
    assert element.is_displayed(), "Expected element {selector} isn't displayed".format(selector=selector)

@then("don't expect {selector}")
def step(context, selector):
    try:
        find_element(context, selector, 'css_selector', timeout=0).is_displayed()
    except (ElementNotVisibleException, NoSuchElementException):
        assert True
    else:
        assert False, "Element {selector} should not be displayed".format(selector=selector)

@then("wait for {selector}")
def step(context, selector, timeout=5):
    wait_for_element_to_appear(context, selector, 5.0)