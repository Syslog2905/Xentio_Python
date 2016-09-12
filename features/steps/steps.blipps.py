from behave import *
from behave_base_lib.selenium_basic_helpers import *
import time
from selenium.webdriver.common.action_chains import ActionChains


HTML_BUTTON = """button"""

#trigger blipp creation tools modal
CREATE_A_BLIPP = """blipp-create-choice-btn>a>div>p"""

#Blipp creation buttons

CREATE_BESPOKE_BUTTON = """.bespoke-blippbasic a"""
CREATE_BUILDER_BUTTON = """.blippbuilder-flash a"""
CREATE_BLIPPDESIGNER = """.blippbuilder-javascript a"""
CREATE_BLIPPJS = """.bespoke-javascript a"""
CREATE_ONE_BLIPP_TOOL = """[class="btn btn-default btn-create ng-scope"]"""


#In the case that the user only has permissions to create blipps for a unique tool then the selector changes
CREATE_BUILDER_ONLY_BUTTON = """.blippbuilder-flash"""
CREATE_BLIPPDESIGNER_ONLY_BUTTON = """.blippbuilder-javascript"""
CREATE_BLIPPJS_ONLY_BUTTON = """.bespoke-javascript"""
CREATE_BESPOKE_ONLY_BUTTON = """.bespoke-blippbasic"""


CREATE_BLIPP_DEFAULT_BUTTON = """.btn-default"""

CREATE_BUILDER_BUTTON_NORMAL_USER = """div[ng-controller="BlippNewBlippBtnCtrl"] button"""
CREATE_BUILDER_BUTTON_IN_DROPDOWN = """.open [ng-controller="BlippNewBlippBtnCtrl"] button"""

CHANGE_BLIPP_NAME_LINK = """div:nth-child(3) > h5:nth-child(1) > a:nth-child(1)""" #div.image:nth-child(2) > div:nth-child(1) > div:nth-child(3) > h5:nth-child(1) > a:nth-child(1)
INPUT_BLIPP_NAME= """#id_blippName"""
INPUT_BLIPP_FILE_ZIP="""div.well:nth-child(1) > input:nth-child(1)"""
INPUT_BLIPP_TEST_CODE=""".input-md"""
INPUT_BLIPP_MARKER_IMG=""".well > input:nth-child(1)"""

INPUT_OPTION_CHOOSE_COUNTRY="""div.radio:nth-child(3) > label:nth-child(1) > span:nth-child(2)"""  #"""input[id="scope-in"]"""
INPUT_COUNTRY_CHOOSER=""".ui-select-search"""

BLIPP_CARDS="""[ng-if="blipp.isCoreBlipp || blipp.isBlippVersion"]"""
BLIPP_CARD_STATUS = '.blipp-status'
BLIPP_VIEW_BTN = """.title a"""

INPUT_OPTION_MAKE_LIVE= """label.ng-scope > span:nth-child(2)""" #"""input[value="live"]"""
INPUT_BLIPP_NAME = """#id_blippName"""

# MODAL BUTTONS
BTN_NEXT = """.modal-footer .btn-primary"""
BTN_CANCEL = """.modal-footer .btn-primary""" #.modal-footer > button:nth-child(1)
BTN_CLOSE = ".close"
BTN_TEST_BLIPP = """[ng-click="createBespokeBlipp()"]"""#button.btn:nth-child(3) / .modal-footer .btn-primary
BTN_PUBLISH = """[ng-click="createBespokeBlipp()"]"""#button.btn:nth-child(3) / .modal-footer .btn-primary
BTN_CREATE = """.modal-footer .btn-primary"""
BTN_UPLOAD_BLIPP = """.drop-target""" #""".btn-primary"""
#BTN_CREATE = """button.ng-binding"""

BACK_FROM_BB = """.inline-block.back-button""" #""".fa-3"""
BUILDER_CHOOSER = """.blipp-builder-content"""
CREATE_BLIPP_DIALOG = """.modal"""
TOOLBAR_DIV = """div.row:nth-child(3)"""
CHECK_INTERVAL_SECONDS = 0.01

DELETE_BLIPP_CONFIRMATION_DIALOG = """.modal-dialog"""
DELETE_BLIPP_CONFIRMATION_BUTTON = """.btn-primary"""
DUPLICATE_BLIPP_BUTTON = '[label="Duplicate"]'
CONFIRM_DUPLICATE_BLIPP_BUTTON = """.btn-primary"""
UPLOADING_DUPLICATE_BLIPP_BUTTON = """.btn-primary"""
CHANGE_BLIPP_MARKER = """.drop-target"""
ZIP_ICON = """.fa-file-zip-o.f-s-60"""

#****************
#* HELPER METHODS
#****************

def get_blipp_cards(context):
    blipp_cards = context.browser.find_elements_by_css_selector(BLIPP_CARDS)
    return blipp_cards
    print("blipp_cards", blipp_cards)

def get_blipp_card_name(blipp):
    time.sleep(1)
    return blipp.find_element_by_css_selector("h3").text

def get_blipp_card_status(blipp):
    return blipp.find_element_by_css_selector(BLIPP_CARD_STATUS).text

#DEPRECATED
def get_blipp_card_view_btn(blipp):
    return blipp.find_element_by_css_selector(BLIPP_VIEW_BTN)

def get_blipp_links(context):
    return context.browser.find_elements_by_css_selector(BLIPP_VIEW_BTN)

def click_on_blipp(context, blipp_name):
    blipps = get_blipp_links(context)
    for blipp in blipps:
        if blipp.text.lower() == blipp_name.lower():
            action = ActionChains(context.browser)
            action.move_to_element(blipp).click().perform()
            context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element="""[ng-show="::blipp.Id"]"""))
            return
    assert False, "Error, blipp with name {blipp_name} not found".format(blipp_name=blipp_name)

def get_blipp_card(context, name):
    blipp_cards = get_blipp_cards(context)
    for blipp in blipp_cards:
        if get_blipp_card_name(blipp) == name:
            return blipp
            print("get_blipp_card_name(blipp) ", get_blipp_card_name(blipp))
    # assert False, "ERROR: Can't find blipp"
    return None

def select_blipp_more_options(context, blipp_name, option):
    menu_items = ["Test", "View stats", "Version history", "Publish", "Unpublish", "Duplicate", "Move", "Delete"]
    if option in menu_items:
        choice_label_el = """li[label="{label}"] [ng-if="btn.label"]""".format(label=option)
        print(choice_label_el)
        card = get_blipp_card(context, blipp_name)
        if card != None:
            elements_list = card.find_elements_by_css_selector("*")
            more_options_button_element = ""
            for i in elements_list:
                if i.get_attribute("tooltip") == "More options":
                    i.click()
                    break
            time.sleep(1)

            card = get_blipp_card(context, blipp_name)
            card_items = card.find_elements_by_css_selector("*")
            for item in card_items:
                if str(item.text).lower() == str(option).lower():
                    print("Lets click on", str(item.text).lower())
                    item.click()
                    break
                else:
                    print("Couldn't find blipp More options")

    else:
        assert False, "Option {opt} not available in {menu_items}".format(opt=option, menu_items=menu_items)


def check_blipp_link_existence(context, link_selector):
    try:
        context.browser.find_element_by_css_selector(link_selector)
        return True
    except:
        return False

def get_permission_value(permissions, service):
    for permission in permissions:
        if permission.get('Action') == service:
            if permission.get('Permission') == 1:
                return True
            else:
                return False
    print("Service {service} not in permissions".format(service=service))
    return False

def check_blipp_creation_buttons(context):
    blipp_builder_ui = check_blipp_link_existence(context, CREATE_BUILDER_BUTTON)
    if blipp_builder_ui == False: #In each case I verify the case that the button is the only one (selector changes)
        blipp_builder_ui = check_blipp_link_existence(context, CREATE_BUILDER_ONLY_BUTTON)
    blipp_designer_ui = check_blipp_link_existence(context, CREATE_BLIPPDESIGNER)
    if blipp_designer_ui == False:
        blipp_designer_ui = check_blipp_link_existence(context, CREATE_BLIPPDESIGNER_ONLY_BUTTON)
    blipp_js_ui = check_blipp_link_existence(context, CREATE_BLIPPJS)
    if blipp_js_ui == False:
        blipp_js_ui = check_blipp_link_existence(context, CREATE_BLIPPJS_ONLY_BUTTON)
    bespoke_ui = check_blipp_link_existence(context, CREATE_BESPOKE_BUTTON)
    if bespoke_ui == False:
        bespoke_ui = check_blipp_link_existence(context, CREATE_BESPOKE_ONLY_BUTTON)
    return {'blipp_builder_ui': blipp_builder_ui,
            'blipp_designer_ui': blipp_designer_ui,
            'blipp_js_ui': blipp_js_ui,
            'bespoke_ui': bespoke_ui}

#************
#* WHEN STEPS
#************


@when('I click on Create a blipp button')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=CREATE_A_BLIPP))
    context.execute_steps(u"""when clicking {btn}""".format(btn=CREATE_A_BLIPP))

@when('I click on Create Bespoke blipp button')
def step(context):
    context.execute_steps(u"""when click in link with text Upload to Blippbasic""")
    # context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=CREATE_BESPOKE_ONLY_BUTTON))
    # context.execute_steps(u"""when click on button {button} identified by css_selector""".format(button=CREATE_BESPOKE_ONLY_BUTTON))

@when('I click on Create BlippBuilder blipp button')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=CREATE_BUILDER_ONLY_BUTTON))
    context.execute_steps(u"""then wait for element {selector} to be clickable""".format(selector=CREATE_BUILDER_ONLY_BUTTON))
    context.execute_steps(u"""when clicking {button}""".format(button=CREATE_BUILDER_ONLY_BUTTON))

@when('I click on Create Blipp default button')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=CREATE_BLIPP_DEFAULT_BUTTON))
    context.execute_steps(u"""then wait for element {selector} to be clickable""".format(selector=CREATE_BLIPP_DEFAULT_BUTTON))
    context.execute_steps(u"""when clicking {button}""".format(button=CREATE_BLIPP_DEFAULT_BUTTON))

@when('I click on Create BlippBuilder new creation tool blipp button')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=CREATE_BLIPPDESIGNER))
    context.execute_steps(u"""then wait for element {selector} to be clickable""".format(selector=CREATE_BLIPPDESIGNER))
    context.execute_steps(u"""when clicking {button}""".format(button=CREATE_BLIPPDESIGNER))

@when('I click on Create code based blipp button')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=CREATE_BLIPPJS))
    context.execute_steps(u"""then wait for element {selector} to be clickable""".format(selector=CREATE_BLIPPJS))
    context.execute_steps(u"""when clicking {button}""".format(button=CREATE_BLIPPJS))

#Had to implement this step because the selectors for normal user are different.
@when('I click on Create BlippBuilder blipp button as a normal user')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=CREATE_BUILDER_BUTTON_NORMAL_USER))
    context.execute_steps(u"""when clicking {button}""".format(button=CREATE_BUILDER_BUTTON_NORMAL_USER))


@when('Creating my blipp I give it the name {blipp_name}')
def step(context, blipp_name):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=INPUT_BLIPP_NAME))
    context.execute_steps(u"""when fill input field {field_name}, identified by css_selector with the value {value}""".format(field_name=INPUT_BLIPP_NAME, value=blipp_name))
    input = context.browser.find_element_by_css_selector(INPUT_BLIPP_NAME)
    assert input.get_attribute('value') == blipp_name, "Error blipp name is not correct " + blipp_name + " but we have " +input.get_attribute('value')

@when('Creating my blipp I enter the test code {test_code}')
def step(context, test_code):
    context.execute_steps(u"""when fill input field {field_name}, identified by css_selector with the value {value}""".format(field_name=INPUT_BLIPP_TEST_CODE, value=test_code))

@when('Creating my blipp I select Make your blipp live: global')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=INPUT_OPTION_MAKE_LIVE))
    el = context.browser.find_element_by_css_selector(INPUT_OPTION_MAKE_LIVE)
    action = ActionChains(context.browser)
    action.move_to_element(el).perform()
    el.click()


@when('Creating my blipp I select Make your blipp live: choose countries')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=INPUT_OPTION_MAKE_LIVE))
    el = context.browser.find_element_by_css_selector(INPUT_OPTION_MAKE_LIVE)
    action = ActionChains(context.browser)
    action.move_to_element(el).perform()
    el.click()
    choose_countries = context.browser.find_element_by_css_selector(INPUT_OPTION_CHOOSE_COUNTRY)
    action.move_to_element(choose_countries).click().perform()


@when('I choose {country_code} as the country')
def step(context, country_code):
    context.execute_steps(u"""when fill input field {field_name}, identified by css_selector with the value {country_code}""".format(field_name=INPUT_COUNTRY_CHOOSER, country_code=country_code))
    context.execute_steps(u"""when send key {key} to {selector}""".format(key="enter", selector=INPUT_COUNTRY_CHOOSER))

@when('Creating my blipp I upload the marker {img_file}')
# The image file should be in ../BlipparRepoBake/features/assets/img.
def step(context, img_file):
    context.execute_steps(u"""when upload the marker {img_file} to {selector}""".format(selector=INPUT_BLIPP_MARKER_IMG, img_file=img_file))
    context.execute_steps(u"""then wait for element {selector} to be clickable""".format(selector=BTN_CREATE))
    context.execute_steps(u"""when clicking {button}""".format(button=BTN_CREATE))
    context.execute_steps(u"""then expect {selector} to disappear""".format(selector=BTN_CREATE))

@when('Duplicating my blipp I upload the marker {img_file}')
# The image file should be in ../BlipparRepoBake/features/assets/img.
def step(context, img_file):
    context.execute_steps(u"""when upload the marker {img_file} to {selector}""".format(selector=INPUT_BLIPP_MARKER_IMG, img_file=img_file))
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=UPLOADING_DUPLICATE_BLIPP_BUTTON))
    context.execute_steps(u"""then wait for element {selector} to be clickable""".format(selector=UPLOADING_DUPLICATE_BLIPP_BUTTON))
    context.execute_steps(u"""when clicking {button}""".format(button=UPLOADING_DUPLICATE_BLIPP_BUTTON))
    context.execute_steps(u"""then expect {selector} to disappear""".format(selector=UPLOADING_DUPLICATE_BLIPP_BUTTON))


@when('I click in back button from blippbuilder')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=BACK_FROM_BB))
    context.execute_steps(u"""when clicking {button}""".format(button=BACK_FROM_BB))
    time.sleep(3)

@when('Creating my blipp I upload the zip {zip_file}')
def step(context, zip_file):
    context.execute_steps(u"""when upload the zip {zip_file} to {selector}""".format(selector=INPUT_BLIPP_FILE_ZIP, zip_file=zip_file))
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=ZIP_ICON))

@when('I click on next')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=BTN_NEXT))
    context.execute_steps(u"""when clicking {button}""".format(button=BTN_NEXT))
    context.execute_steps(u"""then expect {selector} to disappear within 20 seconds""".format(selector=BTN_NEXT))

@when('I click on test blipp')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=BTN_TEST_BLIPP))
    context.execute_steps(u"""then wait for element {selector} to be clickable""".format(selector=BTN_TEST_BLIPP))
    context.execute_steps(u"""when clicking {button}""".format(button=BTN_TEST_BLIPP))
    context.execute_steps(u"""then expect {selector} to disappear""".format(selector=BTN_TEST_BLIPP))

@when('I click on publish blipp')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=BTN_PUBLISH))
    context.execute_steps(u"""when clicking {button}""".format(button=BTN_PUBLISH))
    try:
        context.execute_steps(u"""then expect {selector} to disappear within 30 seconds""".format(selector=CREATE_BLIPP_DIALOG))
    except:
        assert False, "Probably Publish Blipp have not worked!"

@when('I click on create blipp')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=CREATE_BLIPP_DIALOG))
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=BTN_CREATE))
    context.execute_steps(u"""when clicking {button}""".format(button=BTN_CREATE))
    context.execute_steps(u"""then expect {selector} to disappear""".format(selector=CREATE_BLIPP_DIALOG))

@when('I go to {blipp_menu_item} of {blipp_name} blipp')
def step(context, blipp_menu_item, blipp_name):
    context.execute_steps(u"""then expect {selector} to disappear within 10 seconds""".format(selector=""".gritter-title"""))
    select_blipp_more_options(context, blipp_name, blipp_menu_item)
    # try:
    #     context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=""".timeline"""))
    # except:
    #     print("Probably clicking on blipp card haven't worked!")

@when('I click on new version')
def step(context):
    time.sleep(2)
    context.execute_steps(u"""when clicking {el}""".format(el=""".create-version>i"""))

    # toolbar = find_element(context, TOOLBAR_DIV,'css_selector')
    # elements = toolbar.find_elements_by_css_selector("*")
    # time.sleep(1)
    # for element in elements:
    #     if element.get_attribute("class") == "btn btn-blippar ng-scope":
    #         element.click()
    #         break

@when('I delete the blipp {blipp}')
def step(context, blipp):
    card = get_blipp_card(context, blipp)
    while card != None:
        elements_list = card.find_elements_by_css_selector("*")
        more_options_button_element = ""
        delete_button_element = ""
        for i in elements_list:
            if i.get_attribute("tooltip") == "More options":
                more_options_button_element = i
            if i.get_attribute("label") == "Delete":
                delete_button_element = i

        assert type(more_options_button_element) != str, "Error: cannot find menu button in blipp card"
        assert type(delete_button_element) != str, "Error: cannot find delete button in blipp card"
        more_options_button_element.click()
        delete_button_element.click()
        context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=DELETE_BLIPP_CONFIRMATION_DIALOG))
        context.execute_steps(u"""when click on button {submit_button} identified by css_selector""".format(submit_button=DELETE_BLIPP_CONFIRMATION_BUTTON))
        context.execute_steps(u"""then expect {selector} to disappear""".format(selector=DELETE_BLIPP_CONFIRMATION_DIALOG))
        # context.execute_steps(u"""when I navigate to My Projects""")
        time.sleep(2)
        card = get_blipp_card(context, blipp)
    else:
        print("No blipps to delete.")

#************
#* THEN STEPS
#************

@then('I check that the blipp with the name {name} is created')
def step(context, name, timeout=10.0):
    #context.execute_steps(u"""then expect a success message""")
    while timeout >= 0:
        blipp = get_blipp_card(context, name)
        if blipp:
            return blipp
        time.sleep(CHECK_INTERVAL_SECONDS)
        timeout -= CHECK_INTERVAL_SECONDS
    assert False, "ERROR: Could not find blipp"

@then('I check that the blipp with the name {name} has the status {status}') #not used step
def step(context, name, status):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=BLIPP_CARD_STATUS))
    blipp = get_blipp_card(context, name)
    if blipp:
        blipp_status = get_blipp_card_status(blipp)
        if blipp_status == status:
            assert True
        else:
            assert False, "ERROR: blipp has incorrect status"
    else:
        assert False, "ERROR: can't find blipp"

@then('I check that the blipp with the name {name} is there (UI)')
def step(context, name):
    try:
        card = get_blipp_card(context, name)
        assert True, "The blipp  {name} is present"
    except:
        assert False, "ERROR: The blipp is NOT present"

@then('The BlippBuilder page has loaded')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=BUILDER_CHOOSER))

@then('I check that there are not blipp cards with the name {name}')
def step(context, name):
    try:
        card = get_blipp_card(context, name)
        assert False, "ERROR: The blipp is present"
    except:
        assert True

@then('I click on Duplicate button on the blipp (UI)')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=DUPLICATE_BLIPP_BUTTON))
    context.execute_steps(u"""then wait for element {selector} to be clickable""".format(selector=DUPLICATE_BLIPP_BUTTON))
    context.execute_steps(u"""when click on button {submit_button} identified by css_selector""".format(submit_button=DUPLICATE_BLIPP_BUTTON))

@then('I confirm Duplicating the blipp')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=CONFIRM_DUPLICATE_BLIPP_BUTTON))
    context.execute_steps(u"""when click on button {submit_button} identified by css_selector""".format(submit_button=CONFIRM_DUPLICATE_BLIPP_BUTTON))

@then('I write the name as {blipp_name} (UI)')
def step(context, blipp_name):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=INPUT_BLIPP_NAME))
    context.execute_steps(u"""when fill input field {blipp_name}, identified by css_selector with the value {value}""".format(blipp_name=INPUT_BLIPP_NAME, value=blipp_name))

@then('I cancel uploading')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=BTN_CANCEL))
    context.execute_steps(u"""when clicking {button}""".format(button=BTN_CANCEL))

@then('I close uploading')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=BTN_CLOSE))
    context.execute_steps(u"""when clicking {button}""".format(button=BTN_CLOSE))

@then('I click the link with blipp name {text}')
def step(context, text):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=CHANGE_BLIPP_NAME_LINK))
    context.execute_steps(u"""then expect {selector} to contain {text}""".format(selector=CHANGE_BLIPP_NAME_LINK, text=text))

@then('I check that the options for blipp creation are correct according to the permissions in {var}')
def step(context, var):
    permissions = context.config.userdata[var]

    #Get info from permissions
    blipp_builder_perm = get_permission_value(permissions, 'access_blippbuilder_flash_tool')
    blipp_designer_perm = get_permission_value(permissions, 'access_blippbuilder_javascript_tool')
    blipp_js_perm = get_permission_value(permissions, 'access_bespoke_javascript_flow')
    bespoke_perm = get_permission_value(permissions, 'access_bespoke_blippbasic_flow')

    #Get available buttons in UI
    blipp_creation_buttons = check_blipp_creation_buttons(context)
    blipp_builder_ui = blipp_creation_buttons.get('blipp_builder_ui')
    blipp_designer_ui = blipp_creation_buttons.get('blipp_designer_ui')
    blipp_js_ui = blipp_creation_buttons.get('blipp_js_ui')
    bespoke_ui = blipp_creation_buttons.get('bespoke_ui')

    #Look for differences, extract them and do the assert
    differences = []
    if blipp_builder_perm != blipp_builder_ui:
        differences.append("Blipp builder permission: {perm}, present in ui: {ui}".format(perm=blipp_builder_perm, ui=blipp_builder_ui))
    if blipp_designer_perm != blipp_designer_ui:
        differences.append("Blipp designer permission: {perm}, present in ui: {ui}".format(perm=blipp_designer_perm, ui=blipp_designer_ui))
    if blipp_js_perm != blipp_js_ui:
        differences.append("Blipp JS permission: {perm}, present in ui: {ui}".format(perm=blipp_js_perm, ui=blipp_js_ui))
    if bespoke_perm != bespoke_ui:
        differences.append("Bespoke blipp permission: {perm}, present in ui: {ui}".format(perm=bespoke_perm, ui=bespoke_ui))

    assert differences == [], str(differences)


@then("the options for blipp creations are {options}")
def step(context, options):
    options_list = options.split(",")
    blipp_creation_tools = []

    blipp_creation_buttons = check_blipp_creation_buttons(context)
    blipp_builder_ui = blipp_creation_buttons.get('blipp_builder_ui')
    blipp_designer_ui = blipp_creation_buttons.get('blipp_designer_ui')
    blipp_js_ui = blipp_creation_buttons.get('blipp_js_ui')
    bespoke_ui = blipp_creation_buttons.get('bespoke_ui')

    if blipp_builder_ui:
        blipp_creation_tools.append("bb_classic")
    if blipp_designer_ui:
        blipp_creation_tools.append("bb_new")
    if blipp_js_ui:
        blipp_creation_tools.append("js")
    if bespoke_ui:
        blipp_creation_tools.append("bespoke")

    assert sorted(options_list) == sorted(blipp_creation_tools), "Error: the list of options is not the expected. Expected {expected}, obtained {obtained}".format(expected=options_list, obtained=blipp_creation_tools)
