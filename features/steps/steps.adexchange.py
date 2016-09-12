import time
from behave import *
from behave_base_lib.selenium_basic_helpers import *


# **************
# CSS SELECTORS
# **************
AD_TABLE = """tr[ng-repeat="ad in ads"]"""
AD_OBJECTS = """tr.ad"""
AD_BLIPP_MARKER = """td.ad-blipp-marker a"""
AD_BLIPP_NAME = """td.ad-blipp-name h4"""
AD_VIEWS = """td.ad-views h4"""
AD_CLICKS = """td.ad-clicks h4"""
AD_STATUS_BUTTON = """button.btn[ng-click]"""
AD_ONLINE_STATUS_BUTTON = """button.btn[ng-click="unpublish()""" #"""[ng-show="ad.IsOnline"]"""
AD_OFFLINE_STATUS_BUTTON = """button.btn[ng-click="publish()"]"""
REGION_TEXT = """tr.ad:nth-child(2) > td:nth-child(2) > p:nth-child(2)"""

AD_LINKS = """a""" #Running find_elements_by_css_selector on this selector from an ad object
                   # will return a list with pos : 0=link to edit, 1=mailto request status.
SCREEN_TITLE = """h1"""
CANCEL_BUTTON = """[href="/dashboard/adexchange/my-ads"]"""

CREATE_FORM_AD_TITLE_INPUT = """#ad_title""" # """[name="ad_title"]"""
CREATE_FORM_WEBSITE_INPUT = """#ad_website_url"""
CREATE_FORM_DESCRIPTION_INPUT = """#ad_description"""
CREATE_FORM_SAVE_AND_PUBLISH_BUTTON = """button#btn-save-and-publish"""
CREATE_FORM_SAVE_BUTTON = """button#btn-save"""
CREATE_FORM_CANCEL_BUTTON = """[href="/dashbodard/ads"]"""

MY_CAMPAIGNS = """[href="/dashboard/campaigns/mine"]"""
MANAGE_ADS_SCREEN = """.col-md-8"""
MANAGE_ADVERTISEMENTS = """[href="/dashboard/adexchange/my-ads"]""" #"""span.ng-binding"""
LOADING_TEXT = """ad-list-table.ng-isolate-scope > div:nth-child(1)"""
NEW_AD_BUTTON = """a.btn:nth-child(1)"""
CREATE_NEW_AD_TEXT = """.input-group > label:nth-child(1)"""
AD_SEARCH_KEYWORD = """#ad_search_term"""
AD_OBJECT_NAME = """h4.media-heading.ng-binding"""

CREATED_AD_NAME = """h4.ng-binding"""
AD_OBJECT_CHECKBOX = """span.styled-input.styled-checkbox"""
CREATE_AD_BUTTON = """button.btn-primary:nth-child(2)"""  #"""[href="/dashboard/adexchange/my-ads/create"]"""
AD_OBJECT_IMAGE = """figure.media-object.rounded-corner.marker-shadow"""
NO_ADS_FOUND_TEXT = """.blipp-search-results > div:nth-child(1)"""

HIDDEN_UPLOAD_AD_IMAGE = """input[type="file"]"""
UPLOADED_IMAGE = """figure.drop-zone-innards"""
WORLDWIDE_RADIO_BUTTON = """input[type="radio"][id="target-global"]"""
COUNTRY_RADIO_BUTTON = """input[type="radio"][id="target-in"]"""

WEBSITE_URL_ERROR = """[ng-messages="adForm.ad_website_url.$error"]"""
IMAGE_UPLOAD_ERROR = """[for="adForm.file.$error"]"""
EDIT_AD_LINK = """tr.ad:nth-child(3) > td:nth-child(2) > p:nth-child(3) > a:nth-child(1)"""


# ***************
# HELPER METHODS
# ***************
def get_ad_objects(context):
    objects = context.browser.find_elements_by_css_selector(AD_OBJECTS)
    return objects

def get_ad_title(context, ad):
    ad_title = context.browser.find_element_by_css_selector(AD_BLIPP_NAME).text
    return ad_title

def get_ad_titles(context, ad_title):
    ads_table = context.browser.find_elements_by_css_selector(AD_TABLE)
    for ad in ads_table:
        if ad.text.startswith(ad_title):
            return ad

def get_ad_views(ad):
    return ad.find_element_by_css_selector(AD_VIEWS).text

def get_ad_clicks(ad):
    ad_info = ad.find_elements_by_css_selector(AD_CLICKS)
    return ad_info[2]

def click_in_blipp_marker(ad):
    ad.find_element_by_css_selector(AD_BLIPP_MARKER).click()

def get_ad_from_title(context, title):
    ads = get_ad_objects(context)
    for ad in ads:
        ad_title = get_ad_title(context, ad)
        if ad_title == title:
           return ad
           assert True
        else:
            assert False, "The ad with the title {title} does not exists".format(title=title)

def click_in_ad_element(context, ad_title, element):
    ad = get_ad_from_title(context, ad_title)
    if ad != None:
        ad.find_element_by_css_selector(element).click()
    else:
        assert False, "The ad with the title {title} does not exist".format(title=ad_title)

### Object (blipp) methods
def get_blipp_objects(context):
    time.sleep(0.5)
    blipps = context.browser.find_elements_by_css_selector(AD_OBJECT_NAME)
    return blipps

def get_blipp_title(context, title):
    blipp_titles = get_blipp_objects(context)
    for blipp in blipp_titles:
       # print("blipp text", blipp.text)
        if blipp.text == title:
            return blipp

# *****************************
# GIVEN STEPS
# *****************************
@Given("The user {user_name} with password {password} is at the manage ads screen")
def step(context, user_name, password):
    context.execute_steps(u"""when I login with user {user_name} and password {password}""".format(user_name=user_name, password=password))
    context.execute_steps(u"""when The user is at the manage ads screen with text Manage Advertisements""")

@Given("The {user_name} with password {password} is viewing the 'Create new Ad form'")
def step(context, user_name, password):
    context.execute_steps(u"""when I login with user {user_name} and password {password}""".format(user_name=user_name, password=password))
    context.execute_steps(u"""when The user is at the manage ads screen with text Manage Advertisements""")
    context.execute_steps(u"""when I click button New Advertisement""")
    context.execute_steps(u"""then The screen CREATE AN ADVERTISEMENT is opened""")
    context.execute_steps(u"""when I set the value bench in the search screen""")
    context.execute_steps(u"""then The blipp bench with title bench is shown""")
    context.execute_steps(u"""when I select the blipp by the checkbox""")
    context.execute_steps(u"""when I scroll down element with title bench 1 times and confirm ad creation""")


# *****************************
# WHEN STEPS
# *****************************

@when('The user is at the manage ads screen with text {text}')
def step(context,text):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=MY_CAMPAIGNS))
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element= MANAGE_ADVERTISEMENTS))
    context.execute_steps(u"""then the text {text} is present in the element {element} identified by css_selector""".format(element=MANAGE_ADVERTISEMENTS, text=text))

@when('I click button New Advertisement')
def step(context):
     context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=NEW_AD_BUTTON))
     context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element= NEW_AD_BUTTON))

@when('I set the value {search_val} in the search screen')
def step(context, search_val):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=AD_SEARCH_KEYWORD))
    context.execute_steps(u"""when fill input field {element}, identified by css_selector with the value {value}""".format(element=AD_SEARCH_KEYWORD, value=search_val)) #NB
    context.execute_steps(u"""when send key {key} to {selector}""".format(key="enter", selector=AD_SEARCH_KEYWORD))

@when("the value {domain} is entered in input field 'Website you want to link to'")
def step(context, domain):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=CREATE_FORM_WEBSITE_INPUT))
    context.execute_steps(u"""when fill input field {element}, identified by css_selector with the value {value}""".format(element=CREATE_FORM_WEBSITE_INPUT, value=domain))

@when("the blipp image is displayed")
def step(context):
     context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=AD_OBJECT_IMAGE))

@when('I select the blipp by the checkbox')
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=AD_OBJECT_CHECKBOX))
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element= AD_OBJECT_CHECKBOX))

@when('I scroll down element with title {text} {times} times and confirm ad creation')
def step(context, text, times):
    #context.execute_steps(u"""when I scroll down element {element_selector} {times} times""".format(element_selector=AD_OBJECT_NAME, times=times))
    context.execute_steps(u"""then expect {element_selector} to contain {text}""".format(element_selector=AD_OBJECT_NAME, text=text))
    #provided that the first ad object is chosen as the scroll down still fails
    context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element= CREATE_AD_BUTTON))

@When("I click in Cancel button in 'Create and ad screen'")
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=CANCEL_BUTTON))
    context.execute_steps(u"""when click on button {submit_button} identified by css_selector""".format(submit_button=CANCEL_BUTTON))

@When("I find the ad with the title {title}")
def step(context, title):
    context.execute_steps(u"""then wait until the element {title} is displayed, identified by css_selector""".format(title=CREATED_AD_NAME))
    ad = get_ad_titles(context,title)
    if ad.text.startswith(title):
       assert True
    else:
        assert False, "No ad with this title {title} found.".format(title=title)

@When("I edit the ad with the title {title}" )
def step(context, title):
    ad = get_ad_titles(context,title)
    action = ActionChains(context.browser)
    action.move_to_element(ad).click().perform()
    ad.find_element_by_link_text('Edit').click()

@when('I change {title} ad status to Offline')
def step(context,title):
    context.execute_steps(u"""then wait until the element {title} is displayed, identified by css_selector""".format(title=CREATED_AD_NAME))
    ad = get_ad_titles(context,title)
    action = ActionChains(context.browser)
    action.move_to_element(ad)
    time.sleep(1)
    #context.execute_steps(u"""when make element {css_selector} visible""".format(css_selector=AD_ONLINE_STATUS_BUTTON))
    ad.find_element_by_css_selector(AD_STATUS_BUTTON).click()

@when('I change {title} ad status to Online')
def step(context,title):
    context.execute_steps(u"""then wait until the element {title} is displayed, identified by css_selector""".format(title=CREATED_AD_NAME))
    ad = get_ad_titles(context,title)
    action = ActionChains(context.browser)
    action.move_to_element(ad)
    #time.sleep(2)
    ad.find_element_by_css_selector(AD_OFFLINE_STATUS_BUTTON).click()
    #ad.find_element_by_css_selector(AD_STATUS_BUTTON).click() - this button does not work for offline ad so that I implemented Change Status in 2 distict steps


@When("I upload the image {img_file} to verify it meets the requirements")
# The image file should be in ../features/assets/img.
def step(context, img_file):
    #removing assertion step for upload here in order to get the error message
    context.execute_steps(u"""when ng uploading {img_file} to {selector}""".format(selector=HIDDEN_UPLOAD_AD_IMAGE, img_file=img_file))
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=UPLOADED_IMAGE))

@When("I upload the image {img_file} to the ad")
# The image file should be in ../features/assets/img.
def step(context, img_file):
    context.execute_steps(u"""when ng uploading {img_file} to {selector}""".format(selector=HIDDEN_UPLOAD_AD_IMAGE, img_file=img_file))
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=UPLOADED_IMAGE))
    context.execute_steps(u"""then wait until the element {element} is displayed, identified by {identifier}""".format(element=UPLOADED_IMAGE,identifier='css_selector'))

@when('ng uploading {image} to {selector}')
def step(context, image, selector):
    '''
    For Ads Excnahge we have a new plugin dealing with file uploads
    https://github.com/danialfarid/ng-file-upload
    Since it's doing some validations via Angular JS and the input element is hidden,
    We need some JS tricks:
    input[type=file] is the input field (Upload btn) and it's a child of an unvisible parent
    on the JS script we make the parent visible (to Selenium only) and setAttribute value to the filename
    Then Selenium can deal with it and we send the same filename via send_keys which validates the image and we can proceed
    TODO:
        make $('input[type=file]') a param going inside js var
    '''
    hidden_uploader_input = context.browser.find_element_by_css_selector(selector)
    image_path = os.path.join(os.getcwd(), 'images', image.lower())
    print(image_path)
    js_show_input = "$('input[type=file]').parent().removeAttr('style');"
    js_fill_value = "$('input[type=file]')[0].setAttribute('value','{val}');".format(val=image_path)
    js_get_value="""return $('input[type="file"]')[0].getAttribute("value")"""
    context.browser.execute_script(js_show_input)
    context.browser.execute_script(js_fill_value)
    assert image_path == context.browser.execute_script(js_get_value)
    if context.config.userdata.get('browser_name') == "ie":
        fix_ie_script = "function fixie(){document.querySelector(\"" + selector  +  "\").style.opacity=1;}" + "fixie();"
        context.browser.execute_script(fix_ie_script)
    hidden_uploader_input.send_keys(image_path)
    #We need to implement an assertion for uploading file in the browser cause now this steps passes only with some_file.jpg name even w/o having real .jpg file
    assert hidden_uploader_input.get_attribute('value') == image.lower() , "Error, expected {expected}, obtained: {obtained}".format(expected=image, obtained=hidden_uploader_input.get_attribute('value'))

@When("The form is filled with the website {website}")
def step(context, website):
    context.execute_steps(u"""when fill input field {field_name}, identified by css_selector with the value {website}""".format(field_name=CREATE_FORM_WEBSITE_INPUT,website=website))
    context.execute_steps(u"""when send key {key} to {selector}""".format(key="enter", selector=CREATE_FORM_WEBSITE_INPUT))

@When("The form is filled with the description {description} and title {title}")
def step(context, title, description):
    context.execute_steps(u"""when fill input field {element}, identified by css_selector with the value {title}""".format(element=CREATE_FORM_AD_TITLE_INPUT,title=title))
    context.execute_steps(u"""when send key {key} to {selector}""".format(key="enter", selector=CREATE_FORM_AD_TITLE_INPUT))
    context.execute_steps(u"""when fill input field {field_name}, identified by css_selector with the value {description}""".format(field_name=CREATE_FORM_DESCRIPTION_INPUT,description=description))
    context.execute_steps(u"""when send key {key} to {selector}""".format(key="enter", selector=CREATE_FORM_DESCRIPTION_INPUT))

@when("no search results for blipp objects are found")
def step(context):
    context.execute_steps(u"""then check that the element {selector} is not present""".format(selector=AD_OBJECT_IMAGE))

# ***************
# THEN STEPS
# ***************

@then("the response is {expected_response}")
def step(context, expected_response):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=WEBSITE_URL_ERROR))
    #urlstatus = find_element(context, WEBSITE_URL_ERROR,'css_selector')
    element =  context.browser.find_element_by_css_selector(WEBSITE_URL_ERROR).text
    if element == expected_response:
           assert True
           if  element == None:
            assert True, "The URL has correct format"
    else:
        empty_url_field =  context.browser.find_element_by_css_selector(CREATE_FORM_WEBSITE_INPUT).text
        if empty_url_field == "":
            assert True,"Please note:{expected_response}".format(expected_response=expected_response)
        else:
            assert False, "ERROR: Ops, unknown URL status"

@then("the error message {error} is shown")
def step(context, error):
    image_error =  context.browser.find_element_by_css_selector(IMAGE_UPLOAD_ERROR)
    if image_error.text.find(error):
        assert True
    else:
        assert False, "ERROR:No error message or unrecognized error."

@Then("The number of views of the ad with title {title} is {views}")
def step(context, title, views):
    ad = get_ad_from_title(title)
    if ad != None:
        if str(get_ad_views(ad)) == str(views):
            assert True
            return
    else:
        assert False, "The ad with the title {title} does not exists".format(title=title)

@Then("The number of clicks of the ad with title {title} is {clicks}")
def step(context, title, clicks):
    ad = get_ad_from_title(context, title, clicks)
    if ad != None:
        if str(get_ad_clicks(ad)) == str(clicks):
            assert True
            return
    else:
        assert False, "The ad with the title {title} does not exists".format(title=title)

@then('The blipp {blipp} with title {title} is shown')
def step(context, blipp, title):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=CREATED_AD_NAME))
    adtitle = get_blipp_title(context, title)
    if adtitle != None and adtitle.text == title:
        assert True
        return
    else:
        assert False, "The blipp with the title {title} does not exists".format(title=title)

@then('{radio_button_label} radio button is selected')
def step(context, radio_button_label):
    if radio_button_label == "Available Worldwide":
        assert context.browser.find_element_by_css_selector(WORLDWIDE_RADIO_BUTTON).is_selected() == True
    elif radio_button_label == "Country specific":
        assert context.browser.find_element_by_css_selector(COUNTRY_RADIO_BUTTON).is_selected() == True
    else:
        assert False, "Ads radio btns are: Available Worldwide and Country specific"

@then('The user clicks on the {button} button')
def step(context, button):
      context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=CREATE_FORM_SAVE_AND_PUBLISH_BUTTON))
      #context.execute_steps(u"""then wait for element {element} to be clickable""".format(element=CREATE_FORM_SAVE_AND_PUBLISH_BUTTON))
      context.execute_steps(u"""when click on button {submit_button} identified by css_selector""".format(submit_button=CREATE_FORM_SAVE_AND_PUBLISH_BUTTON))
      #context.execute_steps(u"""then expect {selector} to disappear""".format(selector=CREATE_FORM_SAVE_AND_PUBLISH_BUTTON))

@then('The user clicks on the button {button}')
def step(context, button):
      context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=CREATE_FORM_SAVE_BUTTON))
      context.execute_steps(u"""then wait for element {element} to be clickable""".format(element=CREATE_FORM_SAVE_BUTTON))
      context.execute_steps(u"""when click on button {submit_button} identified by css_selector""".format(submit_button=CREATE_FORM_SAVE_BUTTON))
      context.execute_steps(u"""then expect {selector} to disappear""".format(selector=CREATE_FORM_SAVE_AND_PUBLISH_BUTTON))

@then('An Advertisement is created for each selected blipp')
def step(context):
    context.execute_steps(u"""then expect {selector} to disappear""".format(selector=CREATE_FORM_SAVE_AND_PUBLISH_BUTTON))

@then('I check that {title} ad has status {status}')
def step(context, status, title):
    context.execute_steps(u"""then wait until the element {title} is displayed, identified by css_selector""".format(title=CREATED_AD_NAME))
    ad = get_ad_titles(context,title)
    if ad.text.startswith(title):
            if ad.text.endswith(status):
                return ad
                assert True
            else:
                assert False, "ERROR: The ad has incorrect status"
    else:
            assert False, "ERROR: can't find this ad {ad}".format(ad=title)

@then("the data in the form is reset and the user is redirected back to the screen {screen}")
def step(context, screen):
    #context.execute_steps(u""""expect {selector} to disappear within 1 seconds""".format(element=WEBSITE_URL_INPUT))
    context.execute_steps(u"""then wait for element {screen} identified by css_selector""".format(screen=MANAGE_ADVERTISEMENTS))

@then("Save & Publish and Save buttons are disabled")
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=CANCEL_BUTTON))
    context.execute_steps(u"""then check that the element {selector} is not present""".format(selector=CREATE_FORM_SAVE_AND_PUBLISH_BUTTON))
    context.execute_steps(u"""then check that the element {selector} is not present""".format(selector=CREATE_FORM_SAVE_BUTTON))

@then("'Create Advertisement' button is disabled")
def step(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=CANCEL_BUTTON))
    context.execute_steps(u"""then check that the element {selector} is not present""".format(selector=CREATE_AD_BUTTON))

@then("a message is displayed {text}")
def step(context, text):
      context.execute_steps(u"""then expect {element_selector} to contain {text}""".format(element_selector=NO_ADS_FOUND_TEXT, text=text))

@then('the website is {url}')
def step(context, url):
    context.execute_steps(u"""then expect {element_selector} to contain {text}""".format(element_selector=AD_LINKS, url=url))

@then('the region is {region}')
def step(context, region):
    context.execute_steps(u"""then expect {element_selector} to contain {region}""".format(element_selector=REGION_TEXT, region=region))

