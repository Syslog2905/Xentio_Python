from behave import *
from behave_base_lib.selenium_basic_helpers import *
import time


#***********
#SELECTORS
#***********

CUSTOMJS_BTN= "blipp-create-bespoke-javascript-btn.ng-isolate-scope>a"
CUSTOMJS_CODEBASE_UPLOAD = "blipp-create-bespoke-javascript-btn.ng-isolate-scope>a"
BLIPPDESIGN_NEWTOOL = ".inline-block.p-10.blipp-choice.blipp-choice-highlight.blippbuilder-javascript.ng-scope>div>header>p"
CREATE_MARKER_MODAL=".ReactModal__Content.ReactModal__Content--after-open>div"
MARKER_FIRST_ID=""".mootstrap>div>div>div>div>div>div>div>div>div>div"""
UPLOAD_MARKER="""div[style='display: flex;'] > div:nth-child(2)"""
CANCEL_UPLOAD_MARKER="""div[style='display: flex;'] > div:nth-child(1)"""
UPLOAD_JSBLIPP_MODAL=".ReactModal__Content.ReactModal__Content--after-open.centered-modal"
BLIPPJS_SAVE_TESTCODE=""".mootstrap>div>div[style~='flex-end;']> div:nth-child(1)"""
BLIPPJS_MAKEITLIVE=""".mootstrap>div>div[style~='flex-end;']> div:nth-child(2)"""
BLIPPJS_ENTER_TESTCODE="""input[type="text"]"""
BLIPPJS_GLOBAL="#global"
BLIPPJS_LOCAL="#choose"
BLIPPJS_COUNTRY_SELECTION=".Select-control"
BLIPPJS_COUNTRY_SELECTION_MENU=".Select-menu"
BLIPPJS_COUNTRY_SELECTION_OPTION=".Select-option"
BLIPPJS_PUBLISH=""".mootstrap>div>div[style~='flex-end;']> div:nth-child(2)"""
BLIPPJS_PUBLISH_CANCEL=""".mootstrap>div>div[style~='flex-end;']> div:nth-child(1)"""
BLIPPJS_CREATION=".image-info.effect1"
BLIPPJS_TESTCODE=".break-word.ng-binding.ng-scope"
BLIPPJS_PUBLISH_DONE=""".mootstrap>div>div[style~='flex-end;']> div:nth-child(1)"""
BLIPPJS_DETAIL_PUBLISH="""[label="Publish"]"""
BLIPPJS_DETAIL_UNPUBLISH="""[ng-controller="BlippVersionUnpublishBtnCtrl"]"""
BLIPPJS_DETAIL_COUNTRIES=".break-word.ng-binding.ng-scope"
BLIPPJS_NEWVERSION_MODAL="div.ReactModal__Content.ReactModal__Content--after-open"
BLIPPJS_STATUS="li.ng-scope:nth-child(1)>div>div>p>span"
BLIPPJS_NEWVERSION_BUTTON="""[class="row tools ng-scope"]>form>blipp-create-bespoke-javascript-version-btn>button.btn.btn-blippar"""
BLIPPJS_MAKERMANAGER_CLOSE_BTN=""".material-icons"""

# *****************************
# HELPER METHODS
# *****************************

def get_testcode_jsblipp(context):
    global testcode
    testcode = context.browser.find_element_by_css_selector(BLIPPJS_ENTER_TESTCODE).get_attribute("value")
    print("Testcode     :",testcode)

#************
#* WHEN STEPS
#************

@when('I click on the JS blipp {text} link')
def step(context,text):
    context.execute_steps(u"""then the text {text} is present in the element {element} identified by css_selector""".format(element=CUSTOMJS_CODEBASE_UPLOAD, text=text))
    context.execute_steps(u"""when clicking {selector}""".format(selector=CUSTOMJS_CODEBASE_UPLOAD))

@when ('I upload file {value} from folder {upload}')
def step(context,value,upload):
    image_path = os.path.join(os.getcwd(), upload, value)
    input_field = find_element(context,"""input[type="file"]""",'css_selector')
    input_field.clear()
    input_field.send_keys(image_path)

@when('I click on the upload marker link')
def step(context):
    context.execute_steps(u"""when clicking {selector}""".format(selector=UPLOAD_MARKER))

@when('I click save JSblipp with testcode')
def step(context):
    get_testcode_jsblipp(context)
    context.execute_steps(u"""when clicking {selector}""".format(selector=BLIPPJS_SAVE_TESTCODE))
    time.sleep(2)

@when('I select Make It Live')
def step(context):
    get_testcode_jsblipp(context)
    context.execute_steps(u"""when clicking {selector}""".format(selector=BLIPPJS_MAKEITLIVE))

@when('I cick on the cancel button')
def step(context):
    context.execute_steps(u"""when clicking {selector}""".format(selector=BLIPPJS_PUBLISH_CANCEL))

@when('I update the testcode {text}')
def step(context,text):
    context.execute_steps(u"""when fill input field {element}, identified by css_selector with the value {value}""".format(element=BLIPPJS_ENTER_TESTCODE, value=text))

@when('I cick on the publish button')
def step(context):
    context.execute_steps(u"""when clicking {selector}""".format(selector=BLIPPJS_PUBLISH))

@when('I cick on the new version button')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=BLIPPJS_DETAIL_PUBLISH))
    context.execute_steps(u"""when clicking {selector}""".format(selector=BLIPPJS_NEWVERSION_BUTTON))



@when('I cick cancel on the marker confirmation modal')
def step(context):
    context.execute_steps(u"""when clicking {selector}""".format(selector=CANCEL_UPLOAD_MARKER))

@when('I cick on the publish confirmation')
def step(context):
    context.execute_steps(u"""when clicking {selector}""".format(selector=BLIPPJS_PUBLISH_DONE))

@when('I select the country specific publish:{countries}')
def step(context,countries):
    country_list=countries.split( )
    context.execute_steps(u"""when clicking {selector}""".format(selector=BLIPPJS_LOCAL))
    for country in country_list:
        element = find_element(context, BLIPPJS_COUNTRY_SELECTION, 'css_selector')
        element.click()
        context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=BLIPPJS_COUNTRY_SELECTION_MENU))
        time.sleep(2)
        country_dropdown=context.browser.find_elements_by_css_selector(BLIPPJS_COUNTRY_SELECTION_OPTION)
        i=1
        for count_d in country_dropdown:
            xpath_val="html/body/div[4]/div/div/div/div[2]/div[3]/div/div[2]/div/div["+str(i)+"]"
            dropdown_text=context.browser.find_element_by_xpath(xpath_val).text
            if dropdown_text==country:
                context.browser.find_element_by_xpath(xpath_val).click()
                break
            i=i+1

@when('I cick on the publish in blipp detail')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=BLIPPJS_DETAIL_PUBLISH))
    context.execute_steps(u"""when clicking {selector}""".format(selector=BLIPPJS_DETAIL_PUBLISH))

@when('I cick on the publish close button')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=BLIPPJS_MAKERMANAGER_CLOSE_BTN))
    context.execute_steps(u"""when clicking {selector}""".format(selector=BLIPPJS_MAKERMANAGER_CLOSE_BTN))

#************
#* THEN STEPS
#************

@then('The create new modal open')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=CREATE_MARKER_MODAL))

@then('The marker {file} exist in the modal')
def step(context,file):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=MARKER_FIRST_ID))
    context.execute_steps(u"""then the text {text} is present in the element {element} identified by css_selector""".format(element=MARKER_FIRST_ID, text=file))

@then('The JS blipp modal open')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=UPLOAD_JSBLIPP_MODAL))

@then('The new version modal open')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=BLIPPJS_NEWVERSION_MODAL))


@then('The generate testcode {text} exist')
def step(context,text):
    code=text+" "+testcode
    context.execute_steps(u"""then the text {text} is present in the element {element} identified by css_selector""".format(element=BLIPPJS_TESTCODE, text=code))

@then ('The select {countries} should be displayed in blipp detail screen')
def step(context,countries):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=BLIPPJS_DETAIL_COUNTRIES))
    context.execute_steps(u"""then the text {text} is present in the element {element} identified by css_selector""".format(element=BLIPPJS_DETAIL_COUNTRIES, text=countries))

@then ('The publish blipp status should be change to unpublish')
def step(context):
    retries = 5
    while retries>0:
        try:
            context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=BLIPPJS_DETAIL_PUBLISH))
            return
        except:
            time.sleep(1)
            retries -= 1
        assert False, "Failure: the blipp is not unpublished"

@then ('The status of the bipp should be {status}')
def step(context,status):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=BLIPPJS_STATUS))
    context.execute_steps(u"""then the text {text} is present in the element {element} identified by css_selector""".format(element=BLIPPJS_STATUS, text=status))

