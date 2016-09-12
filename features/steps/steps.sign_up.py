import time
import urlparse
import datetime
import sys

from behave_base_lib.selenium_basic_helpers import *
from gmail_client import gmail_client
from behave import *
from environment import EMAIL_ACCOUNT, OAUTH_URL

TITLE_TEXT = """md-card-header h1"""
SUBTITLE_TEXT = """md-card-header h2"""
SCREEN_CAPTION_TEXT = """.md-title"""
FORGOT_PASS_CAPTION = """p.ng-scope"""
USER_FIRST_NAME = """[name="first_name"]"""
USER_SURNAME = """[name="last_name"]"""

PASSWORD_FORGOTTEN_LINK = """[class="md-caption form-alternative"] [href="/password/reset"]"""
BASIC_SIGN_UP_LINK = """[href="/signup/basic"]""" #"""[ng-href="/signup/basic"]"""
LOGIN_URL = """md-card-footer a"""
GOOGLE_ACCOUNTS_URL =  """https://accounts.google.com/ServiceLogin?service=mail&passive=true&rm=false&continue=https://mail.google.com/mail/&ss=1&scc=1&ltmpl=default&ltmplcache=2&emr=1&osid=1"""

SIGN_UP_EMAIL = """[name="email"]"""
EMAIL = """[type="email"]"""
PASSWORD = """[name="password1"]""" #"""[type="password"]"""
LOGIN_PASSWORD = """[name="password"]"""
OLD_PASSWORD = """[name="old_password"]"""
CURRENT_PASSWORD = """#input_0"""
CONFIRM_PASSWORD = """[name="password2"]"""
NEWSLETTER_CHECK_BOX = """[ng-model="account.registration.receive_news"]"""
CHECK_BOX = """[name="agree_toc"]""" #"""[ng-model="account.registration.agree_toc"]"""

LOGIN_SUBMIT_BUTTON = """button.md-primary"""
TERMS_CHECKBOX_ERROR = """div.ng-scope:nth-child(1)"""
EMAIL_ERROR = """.md-input-message-animation"""
SEND_BUTTON = """.md-primary"""
ALREADY_REGISTERED_EMAIL = """[ng-message="email_registered"]"""
LOGIN_FORM = """[name="login.form"]"""
SUBMIT_BUTTON = """[type=submit]"""
CONFIRMATION_TEXT = """md-card-content"""
LOGOUT_LINK = """a[ng-click="logout()"]"""
USER_DROPDOWN = """a[data-toggle="dropdown"]"""
LOGOUT_BUTTON = """button[ng-click="logout.logout()"]"""
STAY_LOGGED_IN_BUTTON = """button[ng-click="logout.stayLoggedIn()"]"""


LINK_TERMS_CONDITIONS = """[ng-click="legal.openTermsModal($event)"]"""
LINK_PRIVACY = """a[ng-click="legal.openPrivacyModal($event)"]"""
LINK = """a.ng-scope"""
MODAL_CAPTION = """h2.ng-binding.ng-scope"""
MODAL_WINDOW = """p.ng-scope:nth-child(1)"""

COUNTRY_SELECTOR = """[role="listbox"]"""
RESEND_EMAIL_BUTTON = """[ng-click="confirmation.resend()"]"""
RESET_FORM = """.md-subhead"""# """[name="reset.form"]"""
COUNTRY_OPTIONS_LIST = """md-option.ng-scope"""
ERROR = """[type="error"]"""
ERROR_EMAIL = """[class="md-input-messages-animation ng-active"]"""
INLINE_ERROR = """[class="ng-scope md-input-messages-animation ng-active"]"""

DROPDOWN_CURRENT_PASS_INPUT = """[name="old_password"]"""
DROPDOWN_NEW_PASS_INPUT = """[name="new_password1"]""" #"""[ng-model="form.new_password1"]"""
DROPDOWN_CONFIRM_PASS_INPUT = """[name="new_password2"]""" #"""[ng-model="form.new_password2"]"""
GET_STARTED_LINK = """.md-primary"""
CHANGE_PASS_SUBMIT = """[aria-label="Change password"]"""

MOVE_EMAILS_FROM_SPAM = True


def get_user_email_from_last_email_received(email=EMAIL_ACCOUNT.get('email'), password=EMAIL_ACCOUNT.get('password')):
    if MOVE_EMAILS_FROM_SPAM:
        move_emails_from_spam(email, password)
    gm = gmail_client(email, password)
    email = gm.get_last_email()
    user_email = gm.get_user_email_from_email_body(email)
    gm.close_session()
    return user_email

def get_activation_link_from_last_email_received(email=EMAIL_ACCOUNT.get('email'), password=EMAIL_ACCOUNT.get('password')):
    if MOVE_EMAILS_FROM_SPAM:
        move_emails_from_spam(email, password)
    gm = gmail_client(email, password)
    email = gm.get_last_email()
    activation_link = gm.get_activation_link_from_email_body(email)
    gm.close_session()
    return activation_link

def get_reset_link_from_last_email_received(email=EMAIL_ACCOUNT.get('email'), password=EMAIL_ACCOUNT.get('password')):
    if MOVE_EMAILS_FROM_SPAM:
        move_emails_from_spam(email, password)
    gm = gmail_client(email, password)
    email = gm.get_last_email()
    activation_link = gm.get_reset_password_link_from_email_body(email)
    gm.close_session()
    return activation_link

def delete_emails_from_account(email=EMAIL_ACCOUNT.get('email'), password=EMAIL_ACCOUNT.get('password')):
    gm = gmail_client(email, password, mailbox='inbox')
    gm.delete_all_emails()
    gm.close_session()
    #Also delete spam folder
    gm = gmail_client(email, password, mailbox='[Gmail]/Spam')
    gm.delete_all_emails()
    gm.close_session()

def generate_email_alias(base_email):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    first_part = base_email.split("@")[0]
    domain = base_email.split("@")[1]
    address = "{first_part}+{timestamp}@{domain}".format(first_part=first_part, timestamp=timestamp, domain=domain)
    print("Email address generated: "+address)
    return address

def generate_new_password():
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    return "newpassword"+str(timestamp)

def move_emails_from_spam(email=EMAIL_ACCOUNT.get('email'), password=EMAIL_ACCOUNT.get('password')):
    gm = gmail_client(email, password, mailbox='[Gmail]/Spam')
    gm.move_all_emails('inbox')
    gm.close_session()


# *****************************
# GIVEN STEPS
# *****************************
@Given("the user is on the login page")
def step(context):
    context.execute_steps(u"""when The user opens the login page""")

@Given("the user has chosen a '{signup_type}' account")
def step(context, signup_type):
    if signup_type.lower() in ["free", "paid"]:
        context.execute_steps(u"""when I delete all browser cookies""")
        context.execute_steps(u"""when I logout""")
        url = urlparse.urljoin(OAUTH_URL, "/signup/{signup_type}".format(signup_type=signup_type.lower()))
        context.execute_steps(u"""when opening the url {element}""".format(element=url))
    else:
        assert False, "Choice {type} not free or paid as it should be".format(type=signup_type)

@Given('the user is on the Reset password page')
def step(context):
    context.execute_steps(u"""when opening the url {logout}""".format(logout=urlparse.urljoin(context.config.userdata['accounts_url'], "logout")))#the logout link for OAuth2
    context.execute_steps(u"""when I delete all browser cookies""")
    context.execute_steps(u"""when opening the url {element}""".format(element=context.config.userdata['accounts_url']))
    context.execute_steps(u"""when clicking {element}""".format(element=PASSWORD_FORGOTTEN_LINK))
    #context.execute_steps(u"""Then screen {screen} is opened""".format(screen=SCREEN_CAPTION_TEXT))

@Given('the user is on the Change password page')
def step(context):
    context.execute_steps(u"""when opening the url {login}""".format(login=urlparse.urljoin(context.config.userdata['accounts_url'], "user/change-password")))

#This given step is a shortcut created to keep running signup tests while the option is disabled for the
#first release that only includes login + password reset
@Given('the user is on the sign up for free page')
def step(context):
    context.execute_steps(u"""When I logout""")
    context.execute_steps(u"""when opening the url {login}""".format(login=urlparse.urljoin(context.config.userdata['accounts_url'], "signup/basic")))

@Given('the user with name {name} and surname {surname} fills the form accordingly')
def step(context, name, surname):
    context.execute_steps(u"""when the user signs up with name {name} and surname {surname}""".format(name=name, surname=surname))
    context.execute_steps(u"""when the user types email gergana.ivanova@blippar.com and password gerg456ivan""")
    context.execute_steps(u"""when the user checks terms checkbox""")
    context.execute_steps(u"""then the newsletter checkbox is selected by default""")

@Given('the user with email {email} and password {password} is logged in')
def steps(context, email, password):
    context.execute_steps(u"""When I logout""")
    context.execute_steps(u"""when fill input field {field}, identified by css_selector with the value {name}""".format(name=email, field=SIGN_UP_EMAIL))
    context.execute_steps(u"""when fill input field {field}, identified by css_selector with the value {name}""".format(name=password, field=LOGIN_PASSWORD))
    context.execute_steps(u"""when clicking {selector}""".format(selector=LOGIN_SUBMIT_BUTTON))
    #TODO: check login steps to verify that the user is logged in after the new auth is merged. Find a sync mechanism there instead of putting this sleep.
    time.sleep(1)

@Given('The testing account does not contain any emails')
def steps(context):
    context.execute_steps(u"""when All emails are deleted from test account""")

# *****************************
# WHEN STEPS
# *****************************

@when("All emails are deleted from test account")
def step(context):
    delete_emails_from_account()

@when("The user opens the login page")
def step(context):
    context.execute_steps(u"""When I logout""")
    context.execute_steps(u"""when opening the url {url}""".format(url=context.config.userdata['target_env']))

@when("the user signs up with name {name} and surname {surname}")
def step(context, name, surname):
    context.execute_steps(u"""then expect {field}""".format(field=USER_FIRST_NAME))
    context.execute_steps(u"""when fill input field {field}, identified by css_selector with the value {name}""".format(name=name, field=USER_FIRST_NAME))
    context.execute_steps(u"""then expect {field}""".format(field=USER_SURNAME))
    context.execute_steps(u"""when fill input field {field}, identified by css_selector with the value {name}""".format(name=surname, field=USER_SURNAME))

#If the value is empty value means that we want to force an empty value for that field.
@when('the user types email {email} and password {password}') # this step is ONLY for login page as password selectors are different for login and signup
def step(context, email, password):
    if email != "empty value":
        context.execute_steps(u"""then expect {selector}""".format(selector=SIGN_UP_EMAIL))
        context.execute_steps(u"""when typing {email} in {field}""".format(email=email, field=SIGN_UP_EMAIL))
        context.execute_steps(u"""when send key {key} to {selector}""".format(key="enter", selector=SIGN_UP_EMAIL))
    if password != "empty value":
        context.execute_steps(u"""then expect {selector}""".format(selector=LOGIN_PASSWORD))
        context.execute_steps(u"""when typing {password} in {field}""".format(password=password, field=LOGIN_PASSWORD))
        context.execute_steps(u"""when send key {key} to {selector}""".format(key="enter", selector=LOGIN_PASSWORD))

@when('the user logins using the email from global {var_name} and the password {password}')
def step(context, var_name, password):
    context.execute_steps(u"""when fill input field {field}, identified by css_selector with the value {name}""".format(name=context.config.userdata[var_name],field=SIGN_UP_EMAIL))
    context.execute_steps(u"""when fill input field {field}, identified by css_selector with the value {name}""".format(name=password,field=LOGIN_PASSWORD))
    context.execute_steps(u"""when clicking {selector}""".format(selector=LOGIN_SUBMIT_BUTTON))

@when('the user logins using the email {email} and the password from global var {var_name}')
def step(context, var_name, email):
    context.execute_steps(u"""when fill input field {field}, identified by css_selector with the value {name}""".format(name=email, field=SIGN_UP_EMAIL))
    context.execute_steps(u"""when fill input field {field}, identified by css_selector with the value {name}""".format(name=context.config.userdata[var_name],field=LOGIN_PASSWORD))
    context.execute_steps(u"""when clicking {selector}""".format(selector=LOGIN_SUBMIT_BUTTON))

@When('the terms & conditions checkbox is displayed')
def step(context):
    context.execute_steps(u"""then expect {selector}""".format(selector=CHECK_BOX))

@when('the user types email {email}, password {password1} and reenter password {password2}')
def step(context, email, password1, password2):
    if email != "empty value":
        context.execute_steps(u"""then expect {selector}""".format(selector=SIGN_UP_EMAIL))
        context.execute_steps(u"""when typing {email} in {field}""".format(email=email, field=SIGN_UP_EMAIL))
        context.execute_steps(u"""when send key {key} to {selector}""".format(key="enter", selector=SIGN_UP_EMAIL))
    if password1 != "empty value":
        context.execute_steps(u"""then expect {selector}""".format(selector=PASSWORD))
        context.execute_steps(u"""when typing {password} in {field}""".format(password=password1, field=PASSWORD))
        context.execute_steps(u"""when send key {key} to {selector}""".format(key="enter", selector=PASSWORD))
    if password2 != "empty value":
        context.execute_steps(u"""then expect {selector}""".format(selector=CONFIRM_PASSWORD))
        context.execute_steps(u"""when typing {password} in {field}""".format(password=password2, field=CONFIRM_PASSWORD))
        context.execute_steps(u"""when send key {key} to {selector}""".format(key="enter",selector=CONFIRM_PASSWORD))

@when('a new email alias is generated using the base account {account} and stored in the global variable {var_name}')
def step(context, account, var_name):
    context.config.userdata[var_name]=generate_email_alias(account)

@when('the user types the email from global {var_name} in email field and sets the password {password}')
def step(context, var_name, password):
    context.execute_steps(u"""then expect {selector}""".format(selector=SIGN_UP_EMAIL))
    context.execute_steps(u"""when typing {email} in {field}""".format(email=context.config.userdata[var_name], field=SIGN_UP_EMAIL))
    context.execute_steps(u"""then expect {selector}""".format(selector=PASSWORD))
    context.execute_steps(u"""when typing {password} in {field}""".format(field=PASSWORD, password=password))
    context.execute_steps(u"""then expect {selector}""".format(selector=CONFIRM_PASSWORD))
    context.execute_steps(u"""when typing {password} in {field}""".format(field=CONFIRM_PASSWORD, password=password))

@when('the user types the email from global {var_name} in email field')
def step(context, var_name):
    context.execute_steps(u"""then expect {selector}""".format(selector=SIGN_UP_EMAIL))
    context.execute_steps(u"""when typing {email} in {field}""".format(email=context.config.userdata[var_name], field=SIGN_UP_EMAIL))

@when('the user selects the country {country}')
def step(context, country):
    context.execute_steps(u"""then expect {selector}""".format(selector=COUNTRY_SELECTOR))
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=COUNTRY_SELECTOR))
    options = find_elements(context, COUNTRY_OPTIONS_LIST, 'css_selector')
    for option in options:
        if option.text == country:
            option.click()
        else:
            pass

@when('the user clicks the reset password link')
def step(context):
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=PASSWORD_FORGOTTEN_LINK))

@when('the newsletter subscription checkbox is displayed')
def step(context):
    context.execute_steps(u"""then wait for element {selector} identified by css_selector""".format(selector=NEWSLETTER_CHECK_BOX))

@When('the users checks newsletter subscription checkbox')
def step(context):
    context.execute_steps(u"""then expect {selector}""".format(selector=NEWSLETTER_CHECK_BOX))
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=NEWSLETTER_CHECK_BOX))

@When('the user checks terms checkbox')
def step(context):
    context.execute_steps(u"""then expect {selector}""".format(selector=CHECK_BOX))
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element= CHECK_BOX))

@when('the user deselects the terms & conditions checkbox')
def step(context):
    context.execute_steps(u"""then expect {title}""".format(title=TITLE_TEXT))
    check_box = context.browser.find_element_by_css_selector(CHECK_BOX)
    if "ng-invalid-required" in check_box.get_attribute("class"):# unchecked state
        check_box.click()
        if "ng-valid-required" in check_box.get_attribute("class"):  # checked state
            check_box.click()
            context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=LOGIN_SUBMIT_BUTTON))
    elif "ng-valid-required" in check_box.get_attribute("class"):
        check_box.click()
        if "ng-invalid-required" in check_box.get_attribute("class"):
            context.execute_steps(
            u"""when click on button {element} identified by css_selector""".format(element=LOGIN_SUBMIT_BUTTON))
    else:
        assert False,"The terms and condition checkbox is not checked so can't be deselected"

@when('the user submits the newsletter form') #not sure if I need this anymore,should check
def step(context):
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=NEWSLETTER_CHECK_BOX))
    context.browser.Alert.accept() #dismiss()

@when("they click on the terms & conditions link")
def step(context):
    context.execute_steps(u"""then wait until the element {title} is displayed, identified by css_selector""".format(title=TITLE_TEXT))
    context.execute_steps(u"""when click in link with text terms and conditions""")

@when('the user clicks on the emailed link')
def step(context):
    context.execute_steps(u"""when opening the url {email_account}""".format(email_account = "http://gmail.com)"))#TBD
    #maybe I should think of some API step for login to user's email
    context.execute_steps(u"""Then The screen '{screen}' is opened""".format(screen=SCREEN_CAPTION_TEXT))

@when('the user clicks on the sign up for free link')
def step(context):
    context.execute_steps(u"""when click on button {link} identified by css_selector""".format(link=BASIC_SIGN_UP_LINK))

@when('the user submits the form')
def step(context):
    time.sleep(1)
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=LOGIN_SUBMIT_BUTTON))

@when('the activation link is obtained from the email received and it is opened')
def step(context):
    activation_url = get_activation_link_from_last_email_received()
    print("Email activation url", activation_url)
    if activation_url != None:
        context.execute_steps(u"""when opening the url {url}""".format(url=activation_url))
    else:
        assert False, "Test failed, no activation url found in email body"

@when('the activation link is obtained from the email, the token is modified and the link is opened')
def step(context):
    activation_url = get_activation_link_from_last_email_received()
    if activation_url != None:
        context.execute_steps(u"""when opening the url {url}""".format(url=activation_url+"aaa"))
    else:
        assert False, "Test failed, no activation url found in email body"

@when('the user activates the managed account setting password {password} and confirmation {confirmation_password}')
def step(context, password, confirmation_password):
    context.execute_steps(u"""when fill input field {field}, identified by css_selector with the value {value}""".format(value=password, field=PASSWORD))
    context.execute_steps(u"""when fill input field {field}, identified by css_selector with the value {value}""".format(value=confirmation_password, field=CONFIRM_PASSWORD))
    time.sleep(0.5)

@when('the logout option is selected in user dropdown menu')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=USER_DROPDOWN))
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=USER_DROPDOWN))
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=LOGOUT_LINK))
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=LOGOUT_LINK))

@when('the user clicks in LOGOUT button')
def step(context):
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=LOGOUT_BUTTON))

@when('the user clicks in STAY LOGGED IN button')
def step(context):
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=STAY_LOGGED_IN_BUTTON))

@when('the user clicks in RESEND EMAIL button')
def step(context):
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=RESEND_EMAIL_BUTTON))

@when('the user enter the email {email} in the reset password screen and clicks in send email button')
def step(context, email):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=SIGN_UP_EMAIL))
    context.execute_steps(u"""when fill input field {field}, identified by css_selector with the value {name}""".format(name=email,field=SIGN_UP_EMAIL))
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=LOGIN_SUBMIT_BUTTON))
    time.sleep(2)
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=LOGIN_SUBMIT_BUTTON))
    time.sleep(5) #ugly solution to give some more extra time to the mail to be sent.

@when('a new password is generated and stored in global variable {global_pass_var}')
def step(context, global_pass_var):
    context.config.userdata[global_pass_var]=generate_new_password()

@when('the reset password link is obtained from the last email and it is opened')
def step(context):
    time.sleep(5)
    reset_url = get_reset_link_from_last_email_received()
    if reset_url != None:
        context.execute_steps(u"""when opening the url {url}""".format(url=reset_url))
    else:
        assert False, "Test failed, no reset url found in email body"

@when('the reset password link is obtained from the last email, the token is changed and it is opened')
def step(context):
    reset_url = get_reset_link_from_last_email_received()
    if reset_url != None:
        context.execute_steps(u"""when opening the url {url}""".format(url=reset_url+"aaad"))
    else:
        assert False, "Test failed, no reset url found in email body"

@when('the user set the password {password} in field {password_field} in reset password screen')
def step(context, password, password_field):
    if password_field.lower() == "new password":
        selector = PASSWORD
    elif password_field.lower() == "retype new password":
        selector = CONFIRM_PASSWORD
    elif password_field.lower() == "enter your current password":
        selector = DROPDOWN_CURRENT_PASS_INPUT
    elif password_field.lower() == "choose a new password":
        selector = DROPDOWN_NEW_PASS_INPUT
    elif password_field.lower() == "confirm your new password":
        selector = DROPDOWN_CONFIRM_PASS_INPUT
    else:
        assert False, "Error: provide a valid password field name"
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=selector))
    context.execute_steps(u"""when fill input field {field}, identified by css_selector with the value {value}""".format(value=password, field=selector))

@when('the user set the password in the field {password_field} from the global variable {global_var}')
def step(context, password_field, global_var):
    context.execute_steps(u"""when the user set the password {password} in field {password_field} in reset password screen""".\
                          format(password=context.config.userdata[global_var], password_field=password_field))

@when('the user clicks in SET NEW PASSWORD button')
def step(context):
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=LOGIN_SUBMIT_BUTTON))
    context.execute_steps(u"""then wait up to 15 seconds for {selector}""".format(selector=RESET_FORM))
    #time.sleep(13)

#LOGIN steps
@when("clicks the 'Reset password' link")
def step(context):
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=PASSWORD_FORGOTTEN_LINK))

@when("click the change password button in Change password modal screen")
def step(context):
    time.sleep(1) #sleep needed
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=CHANGE_PASS_SUBMIT))
    time.sleep(2) #sleep needed

@when("clicks the 'Get Started' link")
def step(context):
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=GET_STARTED_LINK))

# *****************************
# THEN STEPS
# *****************************
@Then("The user is on the screen {screen}")
#I couldn't reuse login step from steps.screen_navigation.py directly because it uses different css selector PAGE_TITLE_LABEL = """h1.col-md-8"""
def step(context, screen):
    time.sleep(1)
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=SCREEN_CAPTION_TEXT))
    context.execute_steps(u"""then expect {selector} to contain {text}""".format(selector=SCREEN_CAPTION_TEXT, text=screen))

@then("the following fields are shown on the screen")
def step(context):
    screen_text = context.browser.find_element_by_css_selector(SCREEN_CAPTION_TEXT).text
    if screen_text.startswith("Create your account"):
        context.execute_steps(u"""then expect {field}""".format(field=USER_FIRST_NAME))
        context.execute_steps(u"""then expect {selector}""".format(selector=USER_SURNAME))
        context.execute_steps(u"""then expect {selector}""".format(selector=SIGN_UP_EMAIL))
        context.execute_steps(u"""then expect {selector}""".format(selector=PASSWORD))
        context.execute_steps(u"""then expect {selector}""".format(selector=CONFIRM_PASSWORD))
        context.execute_steps(u"""then expect {selector}""".format(selector=NEWSLETTER_CHECK_BOX))
        context.execute_steps(u"""then expect {selector}""".format(selector=CHECK_BOX))
        context.execute_steps(u"""then expect {selector}""".format(selector=LOGIN_SUBMIT_BUTTON))
        assert True
    elif screen_text.startswith("Log in to your Blippar account"):
        #this is the same for LOGIN and RESET screen, only the url is different
        context.execute_steps(u"""then expect {field}""".format(field=SIGN_UP_EMAIL))
        context.execute_steps(u"""then expect {selector}""".format(selector=LOGIN_PASSWORD))
       #context.execute_steps(u"""then expect {selector}""".format(selector=REMEMBER_CHECK_BOX)) - not available anymore, date 21/03/2016
        context.execute_steps(u"""then expect {selector}""".format(selector=PASSWORD_FORGOTTEN_LINK))
        context.execute_steps(u"""then expect {selector}""".format(selector=BASIC_SIGN_UP_LINK))
        context.execute_steps(u"""then expect {selector}""".format(selector=LOGIN_SUBMIT_BUTTON))
        assert True
    elif screen_text.startswith("Forgot your password?"):
        #this is Forgot password scenario
        context.execute_steps(u"""then expect {field}""".format(field=SIGN_UP_EMAIL))
        context.execute_steps(u"""then expect {selector}""".format(selector=LOGIN_SUBMIT_BUTTON))
        context.execute_steps(u"""then expect {selector}""".format(selector=BASIC_SIGN_UP_LINK))
        assert True
    elif screen_text.startswith("Change your password"):
        #this is Reset password scenario
        context.execute_steps(u"""then expect {field}""".format(field=CURRENT_PASSWORD))
        context.execute_steps(u"""then expect {selector}""".format(selector=PASSWORD))
        context.execute_steps(u"""then expect {selector}""".format(selector=CONFIRM_PASSWORD))
        context.execute_steps(u"""then expect {selector}""".format(selector=LOGIN_SUBMIT_BUTTON))
        assert True
    else:
        print("screen", screen_text)
        assert False,"Where am I? This screen is not expected."

@then('the user is automatically subscribed to receive email updates from Blippar')
def step(context):
     #context.execute_steps(u"""then("the page contains the text {expected}").format(expected=expected)
    pass

@then('the checkbox is deselected by default')
def step(context):
    terms_check_box = context.browser.find_element_by_css_selector(CHECK_BOX)
    if terms_check_box.get_attribute("area-checked") == "false":
        assert True, "Error: The terms and conditions check box is selected by default."

@then('the newsletter checkbox is selected by default')
def step(context):
    newsletter_check_box = context.browser.find_element_by_css_selector(NEWSLETTER_CHECK_BOX)
    if newsletter_check_box.get_attribute("area-checked") == "true":
        assert True, "Error: The terms and conditions check box is selected by default."

@then(u"the response received is {expected_response}")
def step(context, expected_response):
    reload(sys)
    sys.setdefaultencoding("utf8")
    time.sleep(1)
    if expected_response == "No message":
        try:
            elem = context.browser.find_element_by_css_selector(INLINE_ERROR).text.strip()
            assert False, "Test failed, no error message was expected. Obtained {obtained}".format(obtained=elem.text)
        except:
            assert True
    else:
        context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=INLINE_ERROR))
        element = context.browser.find_element_by_css_selector(INLINE_ERROR).text.strip()
        element = element.decode('utf-8').replace(u'\u2019', "'") #unicode fun
        expected_response = expected_response.decode('utf-8').replace(u'\u2019', "'")
        assert element == expected_response, "we found {el}, instead of {exp}".format(el=element, exp=expected_response)

@then('terms checkbox error message is displayed')
def step(context):
    terms_error = context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=TERMS_CHECKBOX_ERROR))
    if terms_error == None:
        assert False,"No error message,please check what happens."
    else:
        assert True, "In order to create a Blippar account, you must agree to Blippar’s Terms and Conditions and Privacy Policy."

@then('type a new password {password} and submit it')
def step(context, password):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=PASSWORD))
    context.execute_steps(u"""when typing {password} in {field}""".format(field=PASSWORD))

@then('Next time the user goes to login,it happens without enter email and password')
def step(context):
    context.execute_steps(u"""Given the user is on the login page""")
    context.execute_steps(u"""Then The user is on the screen Log in to Blippar""")
    #TBD some more verification that the user is really logged

@then('an activation mail is sent for the account stored in {var_name}')
def step(context, var_name):
    email_account = context.config.userdata[var_name]
    time.sleep(5)
    retries = 5
    while retries > 0:
        last_email_user = get_user_email_from_last_email_received()
        if last_email_user == email_account:
            assert True
            return
        else:
            retries -= 1
            time.sleep(1)
    assert False, "Test failed, the activation email for account {account} was never received".format(account=email_account)

@then('the confirm your email screen is opened showing the email account stored in {var_name}')
def step(context, var_name):
    time.sleep(2)
    email_account = context.config.userdata[var_name]
    context.execute_steps(u"""when wait for the screen with the title selector {selector} to contain the title {title} up to {timeout} seconds""".\
        format(selector=SCREEN_CAPTION_TEXT, title="Confirm your email", timeout=3))
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=CONFIRMATION_TEXT))
    context.execute_steps(u"""then expect {selector} to contain {text}""".format(selector=CONFIRMATION_TEXT, text=email_account))

# @then('the user is redirected to the expected screen {screen}')
# def step(context, screen):
#     time.sleep(1)
#     context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=TITLE_TEXT))
#     screen_title = context.browser.find_element_by_css_selector(TITLE_TEXT).text.lower()
#     if screen_title.startswith("reset your password?"):
#         context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=ERROR))
#         context.execute_steps(u"""then expect {selector} to contain {text}""".format(selector=ERROR, text='Looks like the link has expired, submit a new request to reset your password.'))
#         assert True
#     elif screen_title.startswith("log in to your blippar account"):
#         context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=TITLE_TEXT))
#         context.execute_steps(u"""then expect {selector} to contain {text}""".format(selector=TITLE_TEXT, text=screen))
#     elif screen_title.startswith("confirm your email"):
#        #Need to check the second caption here, this time this is not of error type
#         context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=FORGOT_PASS_CAPTION))
#         screen_second_caption = context.browser.find_element_by_css_selector(FORGOT_PASS_CAPTION).text.lower() #change selector here and then click step should go below the check
#         context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=SEND_BUTTON))
#         if screen_second_caption.endswith("activated your account yet."):
#             pass
#             assert True
#         else:
#             print("screen_second_caption", screen_second_caption)
#             assert False, "Unexpected error. "
#             # context.execute_steps(u"""then expect {selector} to contain {text}""".format(selector=FORGOT_PASS_CAPTION, text='Looks like you haven’t activated your account yet.')) #TBD use regex to escape ',otherwise works
#     else:
#         print("screen_title", screen_title)
#         assert False, "Unexpected window or error."

@then('the user is redirected to the expected screen {screen}')
def step(context, screen):
    time.sleep(1)
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=TITLE_TEXT))
    screen_title = context.browser.find_element_by_css_selector(TITLE_TEXT).text.lower()
    if screen.lower() in screen_title.lower():
        assert True
    else:
        assert False, "User redirected to another screen or not redirected. Expected title {expected}, actual screen title {title}".format(expected=screen, title=screen_title)


@then('the logout confirmation message is opened')
def step(context):
    context.execute_steps(u"""when wait for the screen with the title selector {selector} to contain the title {title} up to {timeout} seconds""".\
        format(selector=TITLE_TEXT, title="Log out", timeout=3))

#TODO check if this can be used in other scenarios in hub, if so then move it to screen_navigation file
@then('{screen_title} screen is opened')
def step(context, screen_title):
    time.sleep(1)
    context.execute_steps(u"""when wait for the screen with the title selector {selector} to contain the title {title} up to {timeout} seconds""".\
        format(selector=SCREEN_CAPTION_TEXT, title=screen_title, timeout=10))
    print("screen_title", screen_title)

@then('the message in the login window is {message}') #this step takes all fields in the login form
def step(context, message):
    time.sleep(5)
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=LOGIN_FORM))
    context.execute_steps(u"""then expect {selector} to contain {text}""".format(selector=LOGIN_FORM, text=message))

@then('the message in the reset form is {message}')
def step(context, message):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=RESET_FORM))
    context.execute_steps(u"""then expect {selector} to contain {text}""".format(selector=RESET_FORM, text=message))

@then('the email field is present')
def step(context):
     context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=EMAIL))

@then('the submit button is present')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=LOGIN_SUBMIT_BUTTON))

@then('the link with the text {text} is present')
def step(context,text):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=LOGIN_URL))
    link_text = context.browser.find_element_by_css_selector(LOGIN_URL).text
    assert text.lower() in link_text.lower(), "Expected {link_text} to contain '{text}', but contains '{elem_text}'".format(text=text, link_text=link_text, elem_text=link_text)

@then('The user types the old password {password}')
def step(context, password):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=OLD_PASSWORD))
    context.execute_steps(u"""when typing {password} in {field}""".format(password=password, field=OLD_PASSWORD))

@then('the terms & conditions are opened in a new browser tab')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=TITLE_TEXT))
    modal_text = context.browser.find_element_by_css_selector(TITLE_TEXT)
    if modal_text.text.startswith("Terms and conditions"):
       assert True
    else:
        assert False, "Terms text is not according the requirements"

@then('a subtitle with text {text} is displayed')
def step(context,text):
    context.execute_steps(
        u"""then wait for element {element} identified by css_selector""".format(element=SUBTITLE_TEXT))
    context.execute_steps(
        u"""then expect {selector} to contain {text}""".format(selector=SUBTITLE_TEXT, text=text.strip(' ')))
