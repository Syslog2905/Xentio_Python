from behave import *
from behave_base_lib.selenium_basic_helpers import *
import urlparse


# ************
# CSS SELECTORS
# ************
FIRST_ROW_NAME = '.table.table-bordered.table-hover.ng-scope tbody tr:nth-child(1) td:nth-child(3)'
USER_TAB = """.nav.nav-tabs>li>a[href$="users"]"""
OPTION_BTN='.btn.btn-sm.btn-blippar'
MENU_OPEN='ul.dropdown-menu.pull-right'
ACCESS_AU=""".ng-scope[ng-if$="AdvertiserUser:user:group.Users"]"""
MANAGE_AD='.ng-isolate-scope[name="Manage Advertisements"]'
MANAGE_AD_HEADER='.col-md-8'
NAV_GROUPUSER_7='/dashboard/group/7/users'

# *****************************
# WHEN STEPS
# *****************************


@when('I click on the first row of the table')
def step_impl(context):
    time.sleep(1)
    context.execute_steps(u"""when clicking {selector}""".format(selector=FIRST_ROW_NAME))

@when('I click on the more option menu')
def step_impl(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=FIRST_ROW_NAME))
    time.sleep(1)
    context.execute_steps(u"""when clicking {selector}""".format(selector=OPTION_BTN))

@when('I click on the Advertiser access sub menu')
def step_impl(context):
    context.execute_steps(u"""when clicking {selector}""".format(selector=ACCESS_AU))
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=OPTION_BTN))

#To access the hard coded url,to reduce the execution time.Step will be removed once Groups & Users performance issue fixed
@when('Navigate to the User link directly')
def step_impl(context):
    context.execute_steps(u"""when opening the url {url}""".format(url=urlparse.urljoin(context.config.userdata.get('target_env'), NAV_GROUPUSER_7)))

# *****************************
# THEN STEPS
# *****************************

@then('the {users} tab is visible')
def step_impl(context,users):
    context.execute_steps(u"""when clicking {selector}""".format(selector=USER_TAB))
    context.execute_steps(u"""then expect {selector} to contain {text}""".format(selector=USER_TAB,text=users))

@then('the {submenus} sub menu is visible')
def step_impl(context,submenus):
    context.execute_steps(u"""then expect {selector} to contain {text}""".format(selector=ACCESS_AU,text=submenus))

@then('User should have Manage Advertisements access')
def step_impl(context):
    context.execute_steps(u"""when clicking {selector}""".format(selector=MANAGE_AD))
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=MANAGE_AD_HEADER))


@then('User should not have Manage Advertisements access')
def step(context):
    try:
       find_element(context, MANAGE_AD, 'css_selector',timeout=0).is_displayed()
    except (ElementNotVisibleException, NoSuchElementException):
       assert True
    else:
        assert False,"ERROR: The Manage Advertisement Menu is present"










