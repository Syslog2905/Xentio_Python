import time
from behave import *
import urlparse
from environment import *
from behave_base_lib.selenium_basic_helpers import *
import sys

CARD_NUMBER_INPUT = """[stripe-field="number"]"""
CVC_NUMBER_INPUT = """[stripe-field="cvc"]"""
SUBMIT_BUTTON = """button[type="submit"]"""  # NEXT and UPGRADE btns
STRIPE_CHECKOUT_FORM_TITLE = """.stripe-checkout-form h1"""
EXPIRATION_MONTH_COMBOBOX = """md-select[stripe-field="exp_month"]"""
MONTH_SELECTOR_LIST = """[ng-repeat="month in ::stripeData.months"]"""
EXPIRATION_YEAR_COMBOBOX = """md-select[stripe-field="exp_year"]"""
YEAR_SELECTOR_LIST = """[ng-repeat="year in ::stripeData.years"]"""
CARD_HOLDER_NAME_INPUT = """#id_name"""
COUNTRY_COMBOBOX = """[ng-model="account.registration.country"]"""
BUSINESS_USE = """[ng-model="payment.data.metadata.is_company"]"""
COMPANY_COUNTRY = """[ng-model="payment.data.address_country"]"""
COMPANY_COUNTRY_LISTBOX = """[ng-repeat="country in ::payment.countries"]"""
COMPANY_NAME_INPUT = """[ng-model="payment.data.metadata.company_name"]"""
VAT_NUMBER_INPUT = """[name="vat_number"]"""
STREET_ADDRESS_INPUT = """[stripe-field="address_line1"]"""
POSTAL_CODE_INPUT = """[stripe-field="address_zip"]"""
CITY_INPUT = """[stripe-field="address_city"]"""
STATE_INPUT = """[stripe-field="address_state"]"""
CREDIT_CARD_DETAILS_SECTION = """[ng-init="card = review.stripe.card"]"""
BILLING_DETAILS_SECTION = """[ng-init="meta = review.payment.metadata"]"""
ORDER_SUMMARY_SECTION = """div>table[ng-if="review.order"]"""

# *****************************
# HELPER METHODS
# *****************************

def find_value_in_section(context, selector, value, retries=3):
    #there is a real mess with what behave pro plugin encodes the text,
    #so do not copy paste currencies into specs!
    reload(sys)
    sys.setdefaultencoding("utf8")
    time.sleep(1)
    while retries > 0:
        details_elements = context.browser.find_elements_by_css_selector(selector)
        if details_elements != []:
            break
        else:
            retries -= 1
            time.sleep(1)
    #pound sign, eur, dollar US$â50.00
    value = value.replace(u'\xc2', "").replace(u'\u20ac', '€')#.replace(u'\xe2\x80\x88', ' ')
    #remove punctional space char
    #space after pound sign in the is actually punctuation space, not the typical space
    #Frontend note:sometimes the currency sign is so big that it touches the first digit of the price
    details_elements = [d.text.decode('utf-8').replace(u'\u2008', ' ').lower() for d in details_elements]
    print("list: ", details_elements)
    print('value lower:', value.lower(), type(value))
    if value.lower() in details_elements[0]:
        return True
    else:
        print("details text: ", details_elements)
        return False

# *****************************
# GIVEN STEPS
# *****************************


# *****************************
# WHEN STEPS
# *****************************

@when("I enter {card_number} in card number field")
def step(context, card_number):
    context.execute_steps(u"""when fill input field {selector}, identified by css_selector with the value {value}""".format(selector=CARD_NUMBER_INPUT, value=card_number))

@when("I set {cvc_number} in security code field")
def step(context, cvc_number):
    context.execute_steps(u"""when fill input field {selector}, identified by css_selector with the value {value}""".format(selector=CVC_NUMBER_INPUT, value=cvc_number))

@when('I select month {month} and year {year} in expiration fields')
def step(context, month, year):
    context.execute_steps(u"""then expect {selector}""".format(selector=EXPIRATION_MONTH_COMBOBOX))
    context.execute_steps(u"""when clicking {element}""".format(element=EXPIRATION_MONTH_COMBOBOX))
    options = find_elements(context, MONTH_SELECTOR_LIST, 'css_selector')
    time.sleep(1)
    for option in options:
        if option.text == month:
            option.click()
            context.execute_steps(u"""then expect {selector} to disappear""".format(selector=MONTH_SELECTOR_LIST))
            break
        else:
            pass
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=EXPIRATION_YEAR_COMBOBOX))
    context.execute_steps(u"""when clicking {element}""".format(element=EXPIRATION_YEAR_COMBOBOX))
    options = find_elements(context, YEAR_SELECTOR_LIST, 'css_selector')
    time.sleep(1)
    for option in options:
        if option.text == year:
            option.click()
            context.execute_steps(u"""then expect {selector} to disappear""".format(selector=YEAR_SELECTOR_LIST))
            break
        else:
            pass
@when('I set the name {name} in card holder name field')
def step(context, name):
    context.execute_steps(u"""when fill input field {selector}, identified by css_selector with the value {value}""".format(selector=CARD_HOLDER_NAME_INPUT, value=name))

@when('I set country {country} for company')
def step(context, country):
    context.execute_steps(u"""when click in {element} identified by css_selector""".format(element=COMPANY_COUNTRY))
    options = find_elements(context, COMPANY_COUNTRY_LISTBOX, 'css_selector')
    time.sleep(1)
    for option in options:
        if option.text == country:
            option.click()
            context.execute_steps(u"""then expect {selector} to disappear""".format(selector=COMPANY_COUNTRY_LISTBOX))
            break
        else:
            pass

@when('I set {name} in company name field')
def step(context, name):
    context.execute_steps(u"""when fill input field {selector}, identified by css_selector with the value {value}""".format(selector=COMPANY_NAME_INPUT, value=name))

@when('I set {vat_no} in vat number field')
def step(context, vat_no):
    context.execute_steps(u"""when fill input field {selector}, identified by css_selector with the value {value}""".format(selector=VAT_NUMBER_INPUT, value=vat_no))

@when('I set {address} in street address field')
def step(context, address):
    context.execute_steps(u"""when fill input field {selector}, identified by css_selector with the value {value}""".format(selector=STREET_ADDRESS_INPUT, value=address))

@when('I set {postal_code} in postal code field')
def step(context, postal_code):
    context.execute_steps(u"""when fill input field {selector}, identified by css_selector with the value {value}""".format(selector=POSTAL_CODE_INPUT, value=postal_code))

@when('I set {city} in city field')
def step(context, city):
    context.execute_steps(u"""when fill input field {selector}, identified by css_selector with the value {value}""".format(selector=CITY_INPUT, value=city))


@when('I enable This is for business use checkbox')
def step(context):
    context.execute_steps(u"""when click in {section} identified by css_selector""".format(section=BUSINESS_USE))

@then('I can review payment details')

@when('I proceed') #NEXT and UPGRADE
def step(context):
    context.execute_steps(u"""when click in {section} identified by css_selector""".format(section=SUBMIT_BUTTON))
    time.sleep(2)

@then('the {field} with value {value} is present in {section}')
def step(context, value, field, section):
    if section.lower() == "order summary":
        selector = ORDER_SUMMARY_SECTION
    elif section.lower() == "billing details":
        selector = BILLING_DETAILS_SECTION
    elif section.lower() == "credit card":
        selector = CREDIT_CARD_DETAILS_SECTION
    else:
        assert False, "Error, wrong section entered for review and confirm step screen"
    value = value.decode('utf8')
    if find_value_in_section(context, selector, value):
        assert True
    else:
        assert False, "Test failed, {field} with value {value} not found in {section}".format(field=field, value=value, section=section)


@then('{locator} contains {text}')
def step(context, locator, text):
    if locator.lower() == "card number field":
        el = CARD_NUMBER_INPUT
    elif locator.lower() == "security code field":
        el = CVC_NUMBER_INPUT
    else:
        assert False, "Error, wrong input field entered for check"
    context.execute_steps(u"""then the input field {input_field_element} contains the value {value} identified by css_selector""".format(input_field_element = el, value=text))
