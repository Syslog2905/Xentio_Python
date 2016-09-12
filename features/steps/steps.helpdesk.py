from behave import *

# ************
# CSS SELECTORS
# ************
LOGIN_USER = """[type="email"]"""
LOGIN_PASSWORD = """[ng-model="user.password"]"""
REMEMBER_ME_CHECKBOX = """[name="remember"]"""
SIGNME_IN_BUTTON = """[type="submit"]"""
USER_LOGGED = """[id="user-name"]"""
LOGOUT_CONFIRM = """button[ng-click="logout.logout()"]"""


@when('I switch to next tab')
def step(context):
    context.browser.switch_to_window(context.browser.window_handles[1]) #assuming new tab is at index 1

@when('I switch to the new tab')
def step(context):
    context.browser.switch_to_window(context.browser.window_handles[0]) #assuming new tab is at index 0

@when('I delete all browser cookies')
def step(context):
    context.browser.delete_all_cookies()

@when('I open {url} and login with user {user_name} and password {password}')
def step(context, url, user_name, password):
    '''
    I couldn't reuse login step from steps.login.py because it's opening target_env url
    '''
    context.execute_steps(u"""when opening the url {logout}""".format(logout="https://support.blippar.com/access/logout?return_to=https://support.blippar.com"))
    context.execute_steps(u"""when I delete all browser cookies""")
    context.execute_steps(u"""when opening the url {url}""".format(url=url))
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=LOGIN_USER))
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=LOGIN_PASSWORD))
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=SIGNME_IN_BUTTON))
    context.execute_steps(u"""when fill input field {username_field}, identified by css_selector with the value {value}""".format(username_field=LOGIN_USER, value=user_name))
    context.execute_steps(u"""when fill input field {password_field}, identified by css_selector with the value {value}""".format(password_field=LOGIN_PASSWORD, value=password))
    context.execute_steps(u"""when click on button {submit_button} identified by css_selector""".format(submit_button=SIGNME_IN_BUTTON))
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=USER_LOGGED))

@when(u'I logout from Zendesk')
def step(context):
    context.execute_steps(u"""when click on button {button} identified by css_selector""".format(button=USER_LOGGED))
    context.execute_steps(u"""when click in link with text Sign out""")
    context.execute_steps(u"""when click on button {btn} identified by css_selector""".format(btn=LOGOUT_CONFIRM))


@then(u'The user {user} is logged in Zendesk')
def step(context, user):
    context.execute_steps(u"""then expect {selector} to contain {text}""".format(selector=USER_LOGGED, text=user))
