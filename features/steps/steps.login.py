import urlparse
import time
from behave import *
from more_itertools import unique_everseen # http://stackoverflow.com/a/19279812/2194433
from environment import *

# ************
# CSS SELECTORS
# ************

LOGIN_USER = """[name="email"]"""
LOGIN_PASSWORD = """[name="password"]"""
LOGIN_URL = """http://alpha-accounts.dev.blippar.com/login"""
USER_DROPDOWN = """i.fa.fa-chevron-down.fa-inverse"""
REMEMBER_ME_CHECKBOX = """[name="remember"]"""
SIGNME_IN_BUTTON = """button.md-button"""
LOGIN_SUBMIT_BUTTON = "button.btn.btn-primary"
USER_LOGGED = """.user-initials"""#""".navbar-user span"""
#SIDEBAR = """#sidebar"""
DROPDOWN_ITEMS = """.dropdown-menu.user-menu"""
USER_CREATOR = """.animate-if.ng-binding.ng-scope"""
CONTEXT_LOGIN_BUTTON = """[class="caret"]"""
CHANGE_PASS = """[ng-click="user.showChangePassword()"]""" #"""[ng-click="changePassword()"]"""
LOGOUT_DROPDOWN_BTN = """[ng-click="logout()"]"""
NEW_PASSWORD = """[ng-model="form.new_password1"]""" #"""[ng-model="form.password1"]"""
CONFIRM_PASSWORD = """[ng-model="form.new_password2"]""" #"""[ng-model="form.password2"]"""
ERROR_LOGIN = """[type="error"]"""
LOGOUT_CONFIRM = """button[ng-click="logout.logout()"]"""
PASSWORD_ERROR = """p.ng-active"""
CONTINUE_AFTER_RESET_PASS = """a.md-primary.md-raised.md-button"""
DROPDOWN_SUBMIT = """button.btn.btn-primary"""

# *****************************
# GIVEN STEPS
# *****************************

@Given("the user is on the accounts login page")
def step(context):
    context.execute_steps(u"""when opening the url {logout}""".format(logout=urlparse.urljoin(context.config.userdata['accounts_url'], "logout"))) #the logout link for OAuth2
    context.execute_steps(u"""when I delete all browser cookies""")
    context.execute_steps(u"""when opening the url {element}""".format(element=LOGIN_URL))

@Given("I am logged in as a {role} user")
def step(context, role):
    user = USERS[role]['email']
    password = USERS[role]['password']
    retries = 5
    while retries > 0:
        try:
            context.execute_steps(u"""When I login with user {user} and password {password}""".format(user=user, password=password))
            time.sleep(0.5)
            return
            #context.execute_steps(u"""then don't expect LOGIN_PASSWORD""")
        except:
            retries -= 1
            time.sleep(1)
    assert False, "Error could not login user"

# *****************************
# WHEN STEPS
# *****************************

@when('I login with user {user_name} and password {password}')
def step(context, user_name, password):
    context.execute_steps(u"""when I logout""") #Make sure that no user is logged in
    time.sleep(0.5)
    #context.execute_steps(u"""when opening the url {url}""".format(url=context.config.userdata.get('target_env')))
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=LOGIN_USER))
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=LOGIN_PASSWORD))
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=SIGNME_IN_BUTTON))
    context.execute_steps(u"""when fill input field {username_field}, identified by css_selector with the value {value}""".format(username_field=LOGIN_USER, value=user_name))
    context.execute_steps(u"""when fill input field {password_field}, identified by css_selector with the value {value}""".format(password_field=LOGIN_PASSWORD, value=password))
    context.execute_steps(u"""when click on button {LOGIN_SUBMIT_BUTTON} identified by css_selector""".format(LOGIN_SUBMIT_BUTTON=SIGNME_IN_BUTTON))
    time.sleep(3)
    context.execute_steps(u"""then don't expect LOGIN_PASSWORD""")

@when('I logout')
def step(context):
    context.execute_steps(u"""when opening the url {url}""".format(url=context.config.userdata.get('target_env')))
    if len(context.browser.find_elements_by_css_selector(USER_LOGGED)) > 0:
        context.execute_steps(u"""when click on button {button} identified by css_selector""".format(button=USER_LOGGED))
        context.execute_steps(u"""when click in link with text Log Out""")
        context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=LOGOUT_CONFIRM))
        context.execute_steps(u"""when click on button {btn} identified by css_selector""".format(btn=LOGOUT_CONFIRM))
    else:
        print("You should be out!")
    context.execute_steps(u"""then The user is logged out""")

@when('I open Help from user menu')
def step(context):
    context.execute_steps(u"""when click on button {button} identified by css_selector""".format(button=USER_LOGGED))
    context.execute_steps(u"""when click in link with text Help & Support""")

@when('the user clicks Change password upper right dropdown')
def step(context):
    #context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=CONTEXT_LOGIN_BUTTON))
    #context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=CONTEXT_LOGIN_BUTTON))
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=USER_DROPDOWN))
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=USER_DROPDOWN))
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=CHANGE_PASS))

@when('the user clicks Logout upper right dropdown')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=CONTEXT_LOGIN_BUTTON))
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=CONTEXT_LOGIN_BUTTON))
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=LOGOUT_DROPDOWN_BTN))

@when('the user submits the reset password form from dropdown')
def step(context):
    time.sleep(1)
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=LOGIN_SUBMIT_BUTTON))

@when('the user clicks Continue button after resetting the password')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=CONTINUE_AFTER_RESET_PASS))
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=CONTINUE_AFTER_RESET_PASS))

@when('the user submits dropdown form')
def step(context):
    time.sleep(1)
    context.execute_steps(u"""then wait for element {selector} to be clickable""".format(selector=DROPDOWN_SUBMIT))
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=DROPDOWN_SUBMIT))
    time.sleep(1)

# *****************************
# THEN STEPS
# *****************************

@then('The user is logged out')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=LOGIN_USER))
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=LOGIN_PASSWORD))
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=SIGNME_IN_BUTTON))

@then('The user {user_name} is logged in')
def step(context, user_name):
    user_names = user_name.split()
    user_initials = ''.join(name [0].upper() for name in user_names)
    retries = 5
    while retries > 0:
        try:
            context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=USER_LOGGED))
            context.execute_steps(u"""then expect {selector} to contain {text}""".format(selector=USER_LOGGED, text=user_initials))
            assert True
            return
        except:
            time.sleep(1)
            retries -= 1
    assert False, "ERROR: The user was not logged in or the username is not displayed"

#options are in order comma separated
@then('The options in the side menu are {options}')
#todo rename the step to smthg like available user menus...
def step(context, options):
    options_list = options.split(",")
    context.execute_steps(u"""when click on button {button} identified by css_selector""".format(button=USER_LOGGED))
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=DROPDOWN_ITEMS))
    items_object = context.browser.find_element_by_css_selector(DROPDOWN_ITEMS).text
    items_elements_list = items_object.split('\n')
    obtained_elements = []
    for element in items_elements_list:
        if element != "":
            obtained_elements.append(element.strip())
    obtained_elements = list(unique_everseen(obtained_elements))

    assert set(options_list).issubset(set(obtained_elements)) == True, "Error: the list of options is not the expected. Expected {expected}, obtained {obtained}".format(expected=set(options_list), obtained=set(obtained_elements))
    #assert options_list in obtained_elements, "Error: the list of options is not the expected. Expected {expected}, obtained {obtained}".format(expected=options_list, obtained=obtained_elements)


@then('type a new password {password} and retype it')
def step(context, password):
    context.execute_steps(u"""then expect {selector}""".format(selector=NEW_PASSWORD))
    context.execute_steps(u"""when typing {password} in {field}""".format(password=password, field=NEW_PASSWORD))
    context.execute_steps(u"""then expect {selector}""".format(selector=CONFIRM_PASSWORD))
    context.execute_steps(u"""when typing {password} in {field}""".format(password=password, field=CONFIRM_PASSWORD))

@then('an error {error} is shown and the password is not changed')
def step(context, error):
    time.sleep(0.5)
    context.execute_steps(u"""then wait for element {selector} identified by css_selector""".format(selector=PASSWORD_ERROR))
    error_text = context.browser.find_element_by_css_selector(PASSWORD_ERROR).text
    assert error.lower() in error_text.lower(), "Expected the error to contain '{error}', but contains '{elem_text}'".format(error=error, text=error_text, elem_text=error_text)
