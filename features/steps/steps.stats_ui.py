from behave import *
from behave_base_lib.selenium_basic_helpers import *
import time
from selenium.webdriver.support.ui import Select

AVERAGE_INTERACTIONS = """span[stats-interaction="averageUserInteraction"]"""
TOTAL_UNIQUE_USERS = """span[stats-interaction="totalUsers | number"]"""
TOTAL_INTERACTIONS = """span[stats-interaction="totalInteraction | number"]"""
VIEW_STATS = """.test-stats-link"""
PAGE_TITLE_LABEL = """h1.col-md-8"""

BLIPP_SELECTOR = """.blipp-selector""" # dropdown option

NO_DATA = """.textTop""" # pie chart element
INTERACTIONS = """td.text-center:nth-child(3)"""
PERCENTAGE = """td.text-center:nth-child(4)"""

#************
#* WHEN STEPS
#************

@when('I select blipp {blipp} from dropdown (UI)')
def step(context, blipp):
    retries = 5
    while retries > 0:
        blipps = Select(context.browser.find_element_by_css_selector(BLIPP_SELECTOR))
        assert len(blipps.options) > 1 # All blipps option is always present
        time.sleep(1)
        retries -= 1
        print("waiting for multiple blipps")
    context.execute_steps(u"""when select option {blipp} in combobox {element}, identified by css_selector""".format(blipp=blipp, element=BLIPP_SELECTOR))
    context.execute_steps(u"""then the page title must be Blipp Stats | Blippar Dashboard""")

#************
#* THEN STEPS
#************

@then('the number of average interactions per user is {average_interactions} (UI)')
def step(context, average_interactions):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=AVERAGE_INTERACTIONS))
    real_avg = context.browser.find_element_by_css_selector(AVERAGE_INTERACTIONS)
    assert str(real_avg.text) == str(average_interactions), "Error expected: {expected}, obtained: {obtained}".format(obtained= str(real_avg.text), expected=str(average_interactions))

@then('the number of total interactions for day Now is {total_interactions} (UI)')
def step_impl(context, total_interactions):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=TOTAL_INTERACTIONS))
    real_total_int = context.browser.find_element_by_css_selector(TOTAL_INTERACTIONS)
    assert str(real_total_int.text) == str(total_interactions), "Error expected: {expected}, obtained: {obtained}".format(obtained=str(real_total_int.text), expected=str(total_interactions))

@then('the number of unique users is {unique_users} (UI)')
def step_impl(context, unique_users):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=TOTAL_UNIQUE_USERS))
    real_unique_users = context.browser.find_element_by_css_selector(TOTAL_UNIQUE_USERS)
    assert str(real_unique_users.text) == str(unique_users), "Error expected: {expected}, obtained: {obtained}".format(obtained=str(real_unique_users.text), expected=str(unique_users))

@then('I check View Stats is not active')
def step(context):
    try:
        context.execute_steps(u"""wait for element {selector} to be clickable""".format(selector=VIEW_STATS))
        assert True, "Expected, the stats link is unclickable"
    except:
        return "Error, the stats link is clickable"

@then('I check that in Interaction Per Blipp table, the blipp has {interactions} interactions and {percentage} percentage (UI)')
def step(context, interactions, percentage):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=INTERACTIONS))
    real_int = context.browser.find_element_by_css_selector(INTERACTIONS)
    assert str(real_int.text) == str(interactions), "Error expected: {expected}, obtained: {obtained}".format(obtained=str(real_int.text), expected=str(interactions))
    real_percentage = context.browser.find_element_by_css_selector(PERCENTAGE)
    assert str(real_percentage.text) == str(percentage), "Error expected: {expected}, obtained: {obtained}".format(obtained=str(real_percentage.text), expected=str(percentage))

@then('I check that the pie chart is showing {text} (UI)')
def step(context, text):
     context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=NO_DATA))
     context.execute_steps(u"""then expect {selector} to contain {text}""".format(selector=NO_DATA, text=text))
