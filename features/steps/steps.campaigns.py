from behave import *
import time
import urlparse
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

# ************
# CSS SELECTORS
# ************

CAMPAIGNS_CARDS = """.gallery-campaigns .image"""
CAMPAIGN_NAME = """.title"""

CAMPAIGNS_CARDS_LINKS_LOCATOR = """div.col-md-12 h5.title"""
CAMPAIGNS_CARDS_LOCATOR = """div.col-md-12 div.image.col-md-3.ng-scope"""
NO_CAMPAIGNS_YET_ELEMENT = """.status > p:nth-child(1)"""

MORE_OPTIONS_CAMPAIGN = """.text-right .btn.btn-blippar.btn-sm"""
DELETE_CAMPAIGN_BUTTON_FROM_BAR = """.tools + .tools > div:nth-child(3) > div:nth-child(1) > button:nth-child(2)"""
#DELETE_CAMPAIGN_BUTTON_FROM_BAR = """[class="btn btn-blippar ng-scope"] [ng-controller="CampaignDeleteBtnCtrl"]"""
DELETE_CAMPAIGN_DIALOG = """.modal-body"""

CREATE_CAMPAIGN_BUTTON = """.btn-primary"""
CREATE_NEW_CAMPAIGN_DIALOG_TITLE = """#myModalLabel"""
SHARE_CAMPAIGN_DIALOG = """#myModalLabel"""
CAMPAIGN_NAME_INPUT = """#id_campaignName"""
#DELETE_CAMPAIGN_BUTTON = """.tools + .tools > div:nth-child(3) > div:nth-child(1) > button:nth-child(2)"""
DELETE_CAMPAIGN_CONFIRMATION_DIALOG = """.modal-title"""
DELETE_CAMPAIGN_CONFIRMATION_BUTTON = """.btn-primary"""
SHARE_CAMPAIGN_INPUT = """.ui-select-search"""

#REMOVE_ALL_USERS_SHARING = """.p-t-10 > a:nth-child(2)"""
REMOVE_ALL_USERS_SHARING = """a[ng-click="removeAll()"""
SHARE_CAMPAIGN_SUBMIT = """#submit"""
#NEW_CAMPAIGN_BUTTON_ALL_CAMPAIGNS = """div.row:nth-child(2) > div:nth-child(2) > button:nth-child(1)"""
#If we have already created campaigns the button NEW_CAMPAIGN_BUTTON_ALL_CAMPAIGNS is not """.btn-default""" anymore.

CAMPAIGN_ID_COLUMN = """th.tablesort-sortable:nth-child(2)"""
CAMPAIGN_NAME_COLUMN = """th.tablesort-sortable:nth-child(3)"""
CREATED_BY_COLUMN = """th.tablesort-sortable:nth-child(4)"""
CREATED_ON_COLUMN = """th.tablesort-sortable:nth-child(5)"""

CAMPAIGN_FILTER_BOX = """input.form-control"""
CAMPAIGN_TABLE_BODY = """.table > tbody:nth-child(2)"""
CAMPAIGN_NAME_BOX = """.editable-wrapper"""
CAMPAIGN_NAME_BOX_EDITABLE = """input[type="text"]"""
CAMPAIGN_EDIT_CONFIRM_BUTTON = """.editable-buttons > button:nth-child(1)"""
CAMPAIGN_LINKS = """.col-md-10.col-xs-10.p-l-5 > h3:nth-child(1)"""

CREATE_BLIPP_BTN = """.blipp-create-wrapper"""
# *****************************
# HELPER METHODS
# *****************************

#Return a dictionary with the groups using the id as key (slow if there are many groups in the table!)
def get_campaigns_from_table_view(context):
    campaigns = {}
    table = context.browser.find_element_by_css_selector(CAMPAIGN_TABLE_BODY)
    for tr in table.find_elements_by_tag_name('tr'):
        id = None
        values = []
        for td in tr.find_elements_by_tag_name('td'):
            if id == None:
                id = td.text
            else:
                values.append(td.text)
        campaigns[id] = values
    if campaigns.has_key(''): #Remove empty keys
        del campaigns['']
    return campaigns

#Returns a list of card elements
def get_campaigns_cards(context):
    if len(context.browser.find_elements_by_css_selector(NO_CAMPAIGNS_YET_ELEMENT)) == 0:
        try:
            campaigns_cards_list = context.browser.find_elements_by_css_selector(CAMPAIGNS_CARDS)
            if campaigns_cards_list:
                return campaigns_cards_list
        except:
            print("lets sleep on waiting for campaign_cards")
            time.sleep(2)
            campaigns_cards_list = context.browser.find_elements_by_css_selector(CAMPAIGNS_CARDS)
            return campaigns_cards_list
    else:
        print("No campaigns yet???")
        return None


def check_campaign_existence(context, name):
    campaign_list = get_campaign_names_from_grid(context)
    if campaign_list and name in campaign_list:
        return True
    else:
        return False

#Returns a list of elements inside of a specific card
def get_elements_from_card(card_element):
    element_list = card_element.find_elements_by_css_selector("*")
    return element_list

def get_card_by_name(context, card_name, retries=3):
    if check_campaign_existence(context, card_name):
        campaigns_card_list = get_campaigns_cards(context)
        if campaigns_card_list:
            while retries > 0:
                for card in campaigns_card_list:
                    elements_list = get_elements_from_card(card)
                    for element in elements_list:
                        if element.text.lower() == card_name.lower():
                            return card
                    time.sleep(0.5)
                retries -= 1
            return None
        else:
            print("You dont have any campaigns?")
            return None
    else:
        return None

def get_campaign_card_link(card):
    campaigns_card_link = card.find_element_by_css_selector("a.custom-link.ng-binding")
    return campaigns_card_link

def get_campaign_names_from_grid(context, retries=5):
    names = []
    while retries > 0:
        if len(context.browser.find_elements_by_css_selector(NO_CAMPAIGNS_YET_ELEMENT)) == 0:
            try:
                el = context.browser.find_elements_by_css_selector(CAMPAIGN_NAME)
                if el:
                    for e in el:
                        names.append(e.text)
                    print("Campaign names from grid: ", names)
                    return names
            except:
                time.sleep(1)
                print("retrying on campaign_names_from_grid", retries)
                retries -= 1
        else:
            print("No campaigns yet???")
            return None
    else:
        assert False, "Couldn't get campaign names"



def is_text_present(source, text):
    return text in source


def select_campaign_more_options(context, campaign_name, option):
    #Test option is a bit complicated and we use xpath selector for it
    menu_items = ["Test", "View Stats", "Share", "Delete"]
    if option in menu_items:
        if option == "Test":
            choice_label_el = '//span[text()=" Test "]'
        elif option == "View Stats":
            choice_label_el = """li[ng-controller="CampaignStatsBtnCtrl"]>button"""
        else:
            # Delete and Share
            choice_label_el = """li[ng-controller="Campaign{label}BtnCtrl"]""".format(label=option)
        print(choice_label_el)
        card = get_card_by_name(context, campaign_name)
        print("Card elements", card.text)
        if card != None:
            elements_list = card.find_elements_by_css_selector("*")
            more_options_button_element = ""
            for i in elements_list:
                if i.get_attribute("tooltip") == "More options":
                    i.click()
                    break
            time.sleep(1)
            card_items=get_elements_from_card(card)
            for item in card_items:
                if str(item.text).lower() == str(option).lower():
                    print("Lets click on",str(item.text).lower())
                    item.click()
                    break
                    # wait = WebDriverWait(context.browser, 5)
                    # if option == "Test":
                    #     element = wait.until(EC.element_to_be_clickable(((By.XPATH, choice_label_el))))
                    # else:
                    #     element = wait.until(EC.element_to_be_clickable(((By.CSS_SELECTOR, choice_label_el))))
                    #     element.click()
    else:
        assert False, "Option {opt} not available in {menu_items}".format(opt=option, menu_items=menu_items)

# *****************************
# WHEN STEPS
# *****************************

@when('I create the campaign with the name {name}')
def step(context, name):
    context.execute_steps(u"""then allow time to update the UI""")
    #can't use the link_text selector because it's != on screen w/o campaigns vs when we have existing campaigns
    context.browser.find_element_by_css_selector('[ng-controller="CampaignNewBtnCtrl"]').click()
    context.execute_steps(u"""then allow time to update the UI""")
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=CREATE_NEW_CAMPAIGN_DIALOG_TITLE))
    context.execute_steps(u"""when fill input field {field}, identified by css_selector with the value {value}""".format(field=CAMPAIGN_NAME_INPUT, value=name))
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=CREATE_CAMPAIGN_BUTTON))
    context.execute_steps(u"""then wait for element {selector} to be clickable""".format(selector=CREATE_CAMPAIGN_BUTTON))
    context.execute_steps(u"""when click on button {submit_button} identified by css_selector""".format(submit_button=CREATE_CAMPAIGN_BUTTON))
    context.execute_steps(u"""then expect {selector} to disappear""".format(selector=CREATE_NEW_CAMPAIGN_DIALOG_TITLE))
    context.execute_steps(u"""then allow time to update the UI""")

@when('I open the campaign with the name {name}')
def step(context, name):
    campaign_links = context.browser.find_elements_by_css_selector(CAMPAIGN_LINKS)
    for campaign_link in campaign_links:
        if campaign_link.text.strip().lower() == name.lower():
            action = ActionChains(context.browser)
            action.move_to_element(campaign_link).click().perform()
            time.sleep(1)
            #wait for campaign id element
            context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=CREATE_BLIPP_BTN))
            return
    assert False, "Campaign with name {name} not found".format(name=name)

@when('I delete the campaign {campaign}')
def step(context, campaign):
    # this will delete only a single campaign, fix it later for the case when we have multiple!
    card = get_card_by_name(context, campaign)
    while card is not None:
        action = ActionChains(context.browser)
        action.move_to_element(card).perform()
        select_campaign_more_options(context, campaign, "Delete")
        context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=DELETE_CAMPAIGN_CONFIRMATION_DIALOG))
        context.execute_steps(u"""when click on button {submit_button} identified by css_selector""".format(submit_button=DELETE_CAMPAIGN_CONFIRMATION_BUTTON))
        context.execute_steps(u"""then expect {selector} to disappear""".format(selector=DELETE_CAMPAIGN_CONFIRMATION_DIALOG))
        time.sleep(2)
        card = get_card_by_name(context, campaign)
        #context.execute_steps(u"""when I navigate to My Projects""")
    else:
        print("No campaign to delete.")

@when("I delete all the campaigns")
def step(context):
    cards = get_campaigns_cards(context)
    campaigns_to_delete = False
    if cards != []:
        for card in cards:
            elements_list = get_elements_from_card(card)
            checkbox_element = None
            behave_campaign = None
            for element in elements_list:
                if element.get_attribute("type") == "checkbox":
                    checkbox_element = element
                if element.text.find("BEHAVE") != -1: #This is to select only campaigns with prefix BEHAVE to avoid accidents deleting others
                    behave_campaign = True
            if behave_campaign == True:
                checkbox_element.click()
                campaigns_to_delete = True
        if campaigns_to_delete:
            context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=DELETE_CAMPAIGN_BUTTON_FROM_BAR))
            context.execute_steps(u"""when click on button {submit_button} identified by css_selector""".format(submit_button=DELETE_CAMPAIGN_BUTTON_FROM_BAR))
            context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=DELETE_CAMPAIGN_CONFIRMATION_DIALOG))
            context.execute_steps(u"""when click on button {submit_button} identified by css_selector""".format(submit_button=DELETE_CAMPAIGN_CONFIRMATION_BUTTON))
            context.execute_steps(u"""then expect {selector} to disappear""".format(selector=DELETE_CAMPAIGN_CONFIRMATION_DIALOG))
            context.execute_steps(u"""when opening the url /dashboard/campaigns/mine""")
            time.sleep(0.3)
            for campaign_card in get_campaigns_cards(context):
                if campaign_card.text.find("BEHAVE") != -1:
                    assert get_campaigns_cards(context) == [], "Error: The campaigns were not deleted (Or there were other campaigns not named with BEHAVE prefix)"


@when('I share the campaign {campaign} to the user {user_email}')
def step(context, campaign, user_email):
    card = get_card_by_name(context, campaign)
    if card != None:
        action = ActionChains(context.browser)
        action.move_to_element(card).perform()
        select_campaign_more_options(context, campaign, "Share")
        context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=SHARE_CAMPAIGN_DIALOG))
        context.execute_steps(u"""then wait up to 30 seconds for {element}""".format(element=REMOVE_ALL_USERS_SHARING))
        context.execute_steps(u"""when I click in link {link} in share campaign modal""".format(link="Remove all users"))
        context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=SHARE_CAMPAIGN_INPUT))
        context.execute_steps(u"""when fill input field {field}, identified by css_selector with the value {value}""".format(field=SHARE_CAMPAIGN_INPUT, value=user_email))
        context.execute_steps(u"""when send key {key} to {selector}""".format(key="enter", selector=SHARE_CAMPAIGN_INPUT))
        context.execute_steps(u"""when I navigate to My Projects""")

@when('I click in link {link} in share campaign modal')
def step(context, link):
    options = context.browser.find_elements_by_css_selector("p.p-t-10 a")
    for option in options:
        if option.text.lower() == link.lower():
            retries = 3
            while retries > 0:
                try:
                    option.click()
                    return
                except:
                    retries -= 1
                    time.sleep(1)
    assert False, "Error: link {link} not found".format(link=link)


@when('I update the name of the campaign to {name}')
def step(context, name):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=CAMPAIGN_NAME_BOX))
    context.execute_steps(u"""when click on button {submit_button} identified by css_selector""".format(submit_button=CAMPAIGN_NAME_BOX))
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=CAMPAIGN_NAME_BOX_EDITABLE))
    context.execute_steps(u"""when fill input field {field}, identified by css_selector with the value {value}""".format(field=CAMPAIGN_NAME_BOX_EDITABLE, value=name+"\n"))

@when('I select {option} of the campaign {campaign}')
def step(context, option, campaign):
    card = get_card_by_name(context, campaign)
    action = ActionChains(context.browser)
    action.move_to_element(card).perform()
    select_campaign_more_options(context, campaign, option)

# *****************************
# THEN STEPS
# *****************************

@then('I check that there is a campaign card with the name {name}')
def step(context, name):
    context.execute_steps(u"""then allow time to update the UI""")
    assert check_campaign_existence(context, name) == True, "Error, the campaign {name} is not present".format(name=name)

@then('I check that there are not campaigns cards with the name {name}')
def step(context, name):
    context.execute_steps(u"""then allow time to update the UI""")
    assert check_campaign_existence(context, name) == False, "Error, the campaign {name} is present".format(name=name)

@then('no entries are visualized in the campaign table')
def step(context):
    campaigns = get_campaigns_cards(context)
    assert campaigns == {}, "Error, there are entries that matched the search, empty table expected."
