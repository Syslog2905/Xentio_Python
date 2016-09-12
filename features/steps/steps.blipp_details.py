from behave import *
import re
from behave_base_lib.selenium_basic_helpers import *
from more_itertools import unique_everseen # http://stackoverflow.com/a/19279812/2194433
from selenium.webdriver.common.action_chains import ActionChains


VERSIONS_SELECTOR = """.timeline"""
LATEST_VERSION =  """[ng-repeat="version in blipp.Versions | orderBy: '-Id'"]""" #""".timeline > li:nth-child(1)"""
VERSION_STATUS = """.timeline-header .label"""
DELETE_VERSION_CONFIRMATION_DIALOG = """.modal-title"""
DELETE_VERSION_CONFIRMATION_BUTTON = """.btn-primary"""

UNPUBLISH_CONFIRMATION_DIALOG = """.btn-primary""" #""".modal-dialog"""
UNPUBLISH_CONFIRMATION_BUTTON = """.pull-left > button:nth-child(3)"""  #""".btn-blippar.ng-scope"""
BLIPP_STATUS = """[class="image-caption ng-binding"]"""
PUBLISH_CONFIRMATION_DIALOG = """#myModalLabel"""
PUBLISH_CONFIRMATION_BUTTON = """.btn-primary"""
CHANGE_COUNTRY_BUTTON = """.break-word > a:nth-child(2)"""
MORE_BLIPP_BUTTON = """button[data-toggle="dropdown"][tooltip="More options"]"""
MOVE_BLIPP_BUTTON = """li[label="Move"]"""
PUBLISH_BUTTON = """li[label="Publish"]>button"""
MAKE_BLIPP_LIVE_BUTTON = """div.form-group:nth-child(2) > label:nth-child(1)"""
ALL_COUNTRIES_RADIO_BUTTON = """div.radio:nth-child(2) > label:nth-child(1)"""
CHOOSE_COUNTRIES_RADIO_BUTTON = """div.radio:nth-child(3) > label:nth-child(1)"""
MOVE_BLIPP_MODAL_WINDOW = """#myModalLabel"""
MOVE_BLIPP_TO_CAMPAIGN = """select.form-control"""
SUBMIT_BUTTON = """#submit"""
TEXT_WHEN_NO_BLIPPS = """[class="status text-muted"] > p:nth-child(2)"""
INPUT_COUNTRY_CHOOSER=""".ui-select-search"""
DATE_CREATED = """.date.ng-binding"""
TIME_CREATED = """.time.ng-binding"""
BARCODE_ID = """small.col-md-12.ng-binding"""
EDITABLE_BLIPP_NAME = """.editable-wrapper"""

ALL_MARKERS = """h2.name"""
LEFT_MARKER_ARROW = """span.glyphicon.glyphicon-chevron-left"""
CLOSE_ALL_MARKERS = """button.btn.btn-primary.col-md-1"""

DETECTMODE = """span.label.marker-settings"""
PUBLISHED_VERSIONS = 'a.status-live'
UNPUBLISHED_VERSIONS = 'a.status-unpublished'

VERSION_STATUSES = {
    'GENERATING': 'generating'
}

MAX_ATTEMPTS = 10


def get_latest_version(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=LATEST_VERSION))
    return context.browser.find_element_by_css_selector(LATEST_VERSION)

def check_versions(context, type):
    if type == "live":
        selector = PUBLISHED_VERSIONS
    elif type == "unpublished":
        selector = UNPUBLISHED_VERSIONS
    else:
        assert False, "Error: enter version type (live, unpublished)"

    versions = context.browser.find_elements_by_css_selector(selector)
    for version in versions:
         version.click()

#************
#* WHEN STEPS
#************

@when('I remove the latest version of the blipp')
def step(context):
    elements = get_latest_version(context).find_elements_by_css_selector("*")
    more_options_button = None
    remove_button = None
    for element in elements:
        if element.get_attribute("tooltip") == "More options":
            more_options_button = element
        if element.get_attribute("class") == "fa fa-trash-o":
            remove_button = element
        if more_options_button != None and remove_button != None:
            break
    more_options_button.click()
    remove_button.click()
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=DELETE_VERSION_CONFIRMATION_DIALOG))
    context.execute_steps(u"""when click on button {submit_button} identified by css_selector""".format(submit_button=DELETE_VERSION_CONFIRMATION_BUTTON))
    context.execute_steps(u"""then expect {selector} to disappear""".format(selector=DELETE_VERSION_CONFIRMATION_DIALOG))
    time.sleep(1)

@when('I unpublish the latest version of the blipp')
def step(context):
    elements = get_latest_version(context).find_elements_by_css_selector("*")
    for element in elements:
         if element.get_attribute("class") == "fa fa-cloud-download":
            element.click()
            break
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=UNPUBLISH_CONFIRMATION_DIALOG))
    context.execute_steps(u"""when click on button {submit_button} identified by css_selector""".format(submit_button=UNPUBLISH_CONFIRMATION_DIALOG))
    context.execute_steps(u"""then expect {selector} to disappear within 20 seconds""".format(selector=UNPUBLISH_CONFIRMATION_DIALOG))


@when('I select campaign {campaign} from dropdown (UI)')
def step(context, campaign):
    retries = 2
    while retries > 0:
        all_campaign = Select(context.browser.find_element_by_css_selector(MOVE_BLIPP_TO_CAMPAIGN))
        all_campaign.select_by_visible_text(campaign)
        assert len(all_campaign.options) > 1
        retries -= 1
        print("waiting for campaign to move the blipp in")
    time.sleep(1)

@when('I publish the blipp with the name {blipp_name} globally (UI)')
def step(context, blipp_name):
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element= MAKE_BLIPP_LIVE_BUTTON))
    #All countries is selected by default
    #context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element= ALL_COUNTRIES_RADIO_BUTTON))
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=PUBLISH_CONFIRMATION_BUTTON))
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element= PUBLISH_CONFIRMATION_BUTTON))
    time.sleep(5)

@when('tap on All markers')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=ALL_MARKERS))
    action = ActionChains(context.browser)
    el = context.browser.find_element_by_css_selector(""".image-inner""")
    action.move_to_element(el).perform()
    time.sleep(0.5)
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=ALL_MARKERS))



#************
#* THEN STEPS
#************

@then('The Latest Version should have the status {status}')
def step(context, status):
    attempts = 0

    def _check_version_status(_context, _status, _attempts):
        _attempts += 1

        version = get_latest_version(_context)
        version_status = version.find_element_by_css_selector(VERSION_STATUS).text

        if version_status.lower() == status.lower():
            assert True
        elif _attempts >= MAX_ATTEMPTS:
            assert False, "ERROR: status is incorrect, should be " + _status
        elif version_status.lower() == VERSION_STATUSES['GENERATING']:
            context.browser.refresh()
            _check_version_status(_context, _status, _attempts)

    _check_version_status(context, status, attempts)

@then('The blipp must have {no_versions} versions')
def step(context, no_versions):
    elem = find_element(context, VERSIONS_SELECTOR, 'css_selector')
    versions = elem.find_elements_by_css_selector("li")
    counter = 0
    for version in versions:
        if version.get_attribute("ng-repeat") == "version in blipp.Versions | orderBy: '-Id'":
                counter += 1
    assert str(no_versions) == str(counter), "Error: The number of blipp versions is not correct. Expected:{expected}, Observed:{observed}".format(expected=no_versions, observed=counter)

@then('I click on Change Country blipp button')
def step(context):
    context.browser.find_element_by_link_text('Change country').click()

@then('I click on More option button on blipp {name} (UI)')
def step(context, name):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=MORE_BLIPP_BUTTON))
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=MORE_BLIPP_BUTTON))

@then('I click on Move button on blipp {name} (UI)')
def step(context, name):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=MOVE_BLIPP_BUTTON))
    context.browser.find_element_by_css_selector(MOVE_BLIPP_BUTTON).click()
    time.sleep(5)

@then('I wait to see modal dialog Move Blipp (UI)')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=MOVE_BLIPP_MODAL_WINDOW))

@then('I click button Submit (UI)')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=SUBMIT_BUTTON))
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=SUBMIT_BUTTON))
    time.sleep(3)

@then('I checked that in the campaign {campaign_name} there is no blipps available (UI)')
def step(context, campaign_name):
    context.browser.find_element_by_css_selector(TEXT_WHEN_NO_BLIPPS)

@then('I wait to see modal dialog Publish Your Blipp (UI)')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=PUBLISH_BUTTON))
    context.browser.find_elements_by_css_selector(PUBLISH_BUTTON)[1].click()
    context.browser.find_element_by_css_selector(PUBLISH_CONFIRMATION_DIALOG)

@then('I check that the status of the blipp {blipp_name} detail page is {status} (UI)')
def step(context, blipp_name, status):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=VERSION_STATUS))
    label = context.browser.find_element_by_css_selector(VERSION_STATUS)
    assert label.text.upper() == status.upper(), "ERROR: blipp status is " + label.text.upper() + " should be " +  status.upper()

@then('I check that the blipp {blipp_name} has date and time of creation (UI)')
def step(context, blipp_name):
    context.browser.find_element_by_css_selector(DATE_CREATED)
    context.browser.find_element_by_css_selector(TIME_CREATED)

@then('I can see Barcode numbers')
def step(context):
    barcodes = get_latest_version(context).find_elements_by_css_selector(BARCODE_ID)
    for barcode in barcodes:
        # this is the barcode example ID: 9002236311037
        re.match(r'ID:\s\d+', barcode.text)

@then('I can see duplicated Blipp name')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=EDITABLE_BLIPP_NAME))
    # this is to match the default duplicated name COPY OF [name of source blipp]
    actual_name = context.browser.find_element_by_css_selector(EDITABLE_BLIPP_NAME)
    assert re.match(r'COPY\sOF\s.*', actual_name.text), "ERROR: The duplicated blipp name does NOT contain COPY OF"

@then('go through all Bespoke markers to check them')
def step(context):
    #move to next marker
    context.browser.find_element_by_css_selector('.right.carousel-control').click()

@then('I check that blipp has DetectModes {modes}')
def step(context,modes):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=DETECTMODE))
    labels_list = context.browser.find_elements_by_css_selector(DETECTMODE)
    modes_list = modes.split(",")
    label_obtained_elements = []
    for element in labels_list:
        if element.text != "":
            label_obtained_elements.append(element.text)
    label_obtained_elements = list(unique_everseen(label_obtained_elements))
    assert modes_list == label_obtained_elements, "Error: the list of options is not the expected. Expected {expected}, obtained {obtained}".format(expected=modes_list, obtained=label_obtained_elements)
