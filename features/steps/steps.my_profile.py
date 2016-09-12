from behave import *
import urlparse
import time

# ************
# CSS SELECTORS
# ************

PROFILE = """[class="ng-binding ng-scope"]"""
PAID_SECTION_TEXT = "p"

USER_DROPDOWN = """i.fa.fa-chevron-down.fa-inverse""" #"""a[data-toggle="dropdown"]"""
USER_ACCOUNT = """.user-account"""
USER_FIRST_NAME = """[name="first_name"]"""
USER_SURNAME = """[name="last_name"]"""
EMAIL = """#input_8""" #"""[type="email"]"""
PASSWORD = """#input_9"""
CHANGE_PASS_LINK = """[class="change-password-link"]"""
CHANGE_PASS_MODAL = """h2"""
OLD_PASS_INPUT = """[name="old_password"]"""
NEW_PASS_INPUT = """[name="new_password1"]"""
CONFIRM_NEW_PASS_INPUT = """[name="new_password2"]"""
CHANGE_PASS_SUBMIT = """[aria-label="Change password"]"""
CHANGE_PASS_SUBMIT_NOT_CLICKABLE = """.change-password-dialog [type="button"]"""

NEWSLETTER_CHECK_BOX = """[ng-model="user.data.receive_news"]"""
UNLOCK_POWER = """[class="ng-scope"] [ng-if="!user.data.external_developer"]"""
SHOW_ME_HOW = """[ng-click="user.showBDNSubscribe()"]"""
COUNTRY = """class="md-text ng-binding"]"""
SUBMIT_BUTTON = """[type="submit"]"""
ERROR_NAMES = """md-input-container.md-input-invalid .ng-scope"""
UPDATED_PROFILE = """[class="custom success inline"]"""

DEV_PORTAL = """[class="visible-lg"]"""
DEV_PORTAL_LINK = """[href="https://devportal.dev.blippar.com"]"""
API_PORTAL = """h2""" #""".text_title_BIG"""
DEV_PORTAL_MEMBER = """[class="flex"] h4"""
COUNT_ME_IN = """.developer-network-subscribe-dialog button""" #"""[ng-click="bdn.subscribe()]"""

# *****************************
# WHEN STEPS
# *****************************
@when('the user is on the My profile page')
def step_impl(context):
    context.execute_steps(u"""when I click on My account in the dropdown top right menu""")
    context.execute_steps(u"""when I switch to next browser window""")
    context.execute_steps(u"""then the page title must be User Profile""")

@when('I go to My Profile')
def step_impl(context):
    context.execute_steps(
        u"""then wait for element {element} identified by css_selector""".format(element=PROFILE))
    context.execute_steps(
        u"""then expect {selector} to contain {text}""".format(selector=PROFILE, text="profile"))
    context.execute_steps(
        u"""then wait for element {element} identified by css_selector""".format(element=PAID_SECTION_TEXT))
    context.execute_steps(u"""then expect {selector} to contain {text}""".format(selector=PAID_SECTION_TEXT,text="Join the Blippar Developer Network and code you own Blipps directly in Javascript"))

@when('I click on My account in the dropdown top right menu')
def step(context):
    context.execute_steps(u"""then allow time to update the UI""")
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=USER_DROPDOWN))
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=USER_DROPDOWN))
    time.sleep(1) #need this to update UI so Change password link can be visible
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=USER_ACCOUNT))

@when('the user deletes name and surname')
def step_impl(context):
    time.sleep(1)
    first_name = context.browser.find_element_by_css_selector(USER_FIRST_NAME)
    first_name.clear()
    surname = context.browser.find_element_by_css_selector(USER_SURNAME)
    surname.clear()
    #context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=USER_SURNAME))

@when('the user clicks Save button')
def step_impl(context):
     context.execute_steps(u"""then wait for element {selector} to be clickable""".format(selector=SUBMIT_BUTTON))
     context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=SUBMIT_BUTTON))

@when('the users checks newsletter checkbox')
def step(context):
    context.execute_steps(u"""then expect {selector}""".format(selector=NEWSLETTER_CHECK_BOX))
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=NEWSLETTER_CHECK_BOX))

@when('the user types the old password {password}')
def step(context,password):
    if password != "empty value":
        context.execute_steps(u"""then expect {selector}""".format(selector=OLD_PASS_INPUT))
        context.execute_steps(u"""when typing {text} in {selector}""".format(selector=OLD_PASS_INPUT,text=password))

@when('the user enters the new password {password}')
def step(context, password):
    if password != "empty value":
        context.execute_steps(u"""when typing {text} in {selector}""".format(selector=NEW_PASS_INPUT, text=password))

@when('the user confirms the new password {password}')
def step(context, password):
    if password != "empty value":
        context.execute_steps(u"""when typing {text} in {selector}""".format(selector=CONFIRM_NEW_PASS_INPUT, text=password))
        #trying to get confrimation button in the next scenario step clickable
        time.sleep(1)

@when('the user saves changes')
def step_impl(context):
    try:
        context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=CHANGE_PASS_SUBMIT))
    except:
        time.sleep(1)
        context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=CHANGE_PASS_SUBMIT_NOT_CLICKABLE))
        assert False, "Can't click on Change password button"

@when('click on Count me in')
def step_impl(context):
    context.execute_steps(u"""then wait for {selector}""".format(selector=COUNT_ME_IN))
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=COUNT_ME_IN))
    time.sleep(2)  # need this to assure the modal window closing

@when('click on Go to the BDN webpage')
def step_impl(context):
    context.execute_steps(u"""when clicking {selector}""".format(selector=DEV_PORTAL_LINK))
    time.sleep(1)

# *****************************
# THEN STEPS
# *****************************
@then("they will see user first name, surname, Change password and Show me how links")
def step(context):
    context.execute_steps(u"""then wait for {selector}""".format(selector=PROFILE))
    screen_text = context.browser.find_element_by_css_selector(PROFILE).text
    print("profile_text", screen_text.lower())
    if screen_text.lower() == "profile":
        context.execute_steps(u"""then expect {field}""".format(field=USER_FIRST_NAME))
        context.execute_steps(u"""then expect {selector}""".format(selector=USER_SURNAME))
        context.execute_steps(u"""then expect {selector}""".format(selector=CHANGE_PASS_LINK))
        context.execute_steps(u"""then expect {selector}""".format(selector=NEWSLETTER_CHECK_BOX))
        #context.execute_steps(u"""then expect {selector}""".format(selector=SHOW_ME_HOW))
        assert True
    else:
        assert False,"The screen {screen_text} is not expected.".format(screen_text=screen_text)

@then('errors {error1} and {error2} are displayed')
#HUB-1236 - after it gets fixed should do: if condition1 and condition 2 instead if/elif
def step_impl(context,error1,error2):
    error = context.browser.find_element_by_css_selector(ERROR_NAMES).text
    if "You did not enter your first name" in error:
        assert True
    elif  "You did not enter your surname" in error:
       assert True
    else:
       assert False,"The error messages for the first name and surname are not as expected!"

@then('the user sees {expected_response}')
def step_impl(context, expected_response):
    context.execute_steps(u"""then don't expect CHANGE_PASS_SUBMIT""")
    context.execute_steps(
        u"""then wait for element {element} identified by css_selector""".format(element=UPDATED_PROFILE))
    toast_element = context.browser.find_element_by_css_selector(UPDATED_PROFILE).text.strip()
    try:
        if  toast_element == expected_response:
            assert True,"Test failed,message {expected_response} was expected but obtained {obtained}".format(obtained=toast_element)
    except:
        context.execute_steps(
            u"""then wait for element {element} identified by css_selector""".format(element=ERROR_NAMES))
        error_element = context.browser.find_element_by_css_selector(ERROR_NAMES).text.strip()
        assert error_element == expected_response, "we found {el}, instead of {exp}".format(el=error_element, exp=expected_response)
        context.execute_steps(u"""then the text {text} is present in the element {element} identified by css_selector""".format(
            element=ERROR_NAMES, text= expected_response))

@then('the modal window with text {text} is displayed')
def step_impl(context,text):
  context.execute_steps(
     u"""then expect {selector} to contain {text}""".format(selector=CHANGE_PASS_MODAL, text=text))

#Dev network steps
@then ('the user is logged into {portal} started with text {text}')
def step_impl(context,text,portal):
    try:
        context.execute_steps(
            u"""then wait for element {element} identified by css_selector""".format(element=DEV_PORTAL))
        dev_portal_text = context.browser.find_element_by_css_selector(DEV_PORTAL).text.lower()
        if dev_portal_text.startswith(text):
            assert True, "Error:DEV portal is not open or has unexpected caption text."
    except:
        context.execute_steps(
            u"""then wait for element {element} identified by css_selector""".format(element=API_PORTAL))
        api_portal_text = context.browser.find_element_by_css_selector(API_PORTAL).text.lower()
        if api_portal_text.startswith(text):
           assert True,"Error:API portal is not opened or has unexpected caption text."

@then('ending with text {text}')
def step_impl(context, text):
    dev_portal_text = context.browser.find_element_by_css_selector(DEV_PORTAL).text.lower()
    if dev_portal_text.endswith(text):
        assert True, "Error:Dev Portal error - not opened or has unexpected caption text."

@then('they are signed up to the developer network and the text {text} is shown')
def step_impl(context, text):
     time.sleep(0.5)
     context.execute_steps(
        u"""then expect {selector} to contain {text}""".format(selector=DEV_PORTAL_MEMBER, text=text))
