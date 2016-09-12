import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from behave import *

# ************
# CSS SELECTORS
# ************
MY_CAMPAIGNS = """[href="/dashboard/campaigns/mine"]"""
ALL_CAMPAIGNS = """[href="/dashboard/campaigns/all"]"""
MANAGE_ADS = """[href="/dashboard/adexchange/my-ads"]"""
CAMPAIGN_NAVIGATOR = """.campaign-nav>a"""

BACK_BUTTON=""".back-button"""
PAGE_TITLE_LABEL = """h1"""

MODAL_TITLE_LABEL = """.modal-title"""

MODAL_STEP_TITLE_NAME= """ol.bwizard-steps li.active:nth-child(1)"""
MODAL_STEP_TITLE_PUBLISH = """ol.bwizard-steps li.active:nth-child(2)"""
MODAL_STEP_BLIPP_ZIP = """ol.bwizard-steps li.active:nth-child(1)"""
LOADING_TEXT = """ad-list-table.ng-isolate-scope > div:nth-child(1)"""

HEADER_ROW = '.row.panel-heading'

# *****************************
# WHEN STEPS
# *****************************

@when('I switch to next browser window')
def step(context):
    context.browser.switch_to_window(context.browser.window_handles[-1])
    time.sleep(3)

@when('I go to Manage Ads')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=MANAGE_ADS))
    context.execute_steps(u"""when click on button {submit_button} identified by css_selector""".format(submit_button=MANAGE_ADS))
    context.execute_steps(u"""then expect {selector} to disappear within {timeout} seconds""".format(selector=LOADING_TEXT,timeout=10))

@when('I navigate to {campaign_selector}')
def step(context, campaign_selector):
    #My Projects/Group Projects/All Projects
    #we might end up 2 levels inside with back buttons MY projects-> Campaign->Blipp->Version history
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=""".navbar-brand"""))
    context.execute_steps(u"""when clicking {el}""".format(el=""".navbar-brand"""))
    context.execute_steps(u"""when clicking {el}""".format(el=CAMPAIGN_NAVIGATOR))
    context.execute_steps(u"""when click in link with text {link}""".format(link=campaign_selector))

@when('wait for the screen with the title selector {selector} to contain the title {title} up to {timeout} seconds')
def step(context, selector, title, timeout):
    retries = int(timeout)
    while retries > 0:
        try:
            context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=selector))
            context.execute_steps(u"""then expect {selector} to contain {text}""".format(selector=selector, text=title))
            break
        except:
            retries -= 1
            time.sleep(1)
    if retries == 0:
        assert False, "Test failed, screen title not match or the page was not loaded"

# *****************************
# THEN STEPS
# *****************************

@then('The screen {screen_title} is opened')
def step(context, screen_title):
    # try:
    #     find_element(context, CAMPAIGN_NAVIGATOR, css_selector, timeout=3.0)
    #     context.execute_steps(u"""then expect {selector} to contain {text}""".format(selector=CAMPAIGN_NAVIGATOR, text=screen_title.encode("utf-8")))
    # except:
    #     #context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=PAGE_TITLE_LABEL))
    context.execute_steps(u"""then expect {selector} to contain {text}""".format(selector=HEADER_ROW, text=screen_title.encode("utf-8")))


@then('The modal {modal_title} is opened')
def step(context, modal_title):
    #context.execute_steps(u"""then wait for {element}""".format(element=MODAL_TITLE_LABEL))
    context.execute_steps(u"""then allow time to update the UI""")
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=MODAL_TITLE_LABEL))
    #context.execute_steps(u"""then expect {selector} to contain {text}""".format(selector=MODAL_TITLE_LABEL, text=modal_title))
    time.sleep(3)
    retries = 3
    while retries > 0:
        try:
            context.execute_steps(u"""then the text {text} is present in the element {element} identified by css_selector""".format(element=MODAL_TITLE_LABEL, text=modal_title))
            break
        except:
            time.sleep(0.5)
            retries -= 1

@then('The modal step Publish is active')
def step(context):
    context.execute_steps(u"""then allow time to update the UI""")
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=MODAL_STEP_TITLE_PUBLISH))

@then('The modal step Name is active')
def step(context):
    context.execute_steps(u"""then allow time to update the UI""")
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=MODAL_STEP_TITLE_NAME))

@then('The modal step Blipp Zip is active')
def step(context):
    context.execute_steps(u"""then allow time to update the UI""")
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=MODAL_STEP_TITLE_NAME))
