import random
import time
import re
import urlparse
from behave import *
from selenium.webdriver.common.action_chains import ActionChains

SIDEBAR_GROUPS_LINK = '[href="/dashboard/groups"]'
SIDEBAR_APPROVALS = '[href="/dashboard/approvals"]'
GROUPS_HEADER_ELEMENT = '.panel-heading h1'
GROUP_FILTER = '[class="form-control ng-isolate-scope"]'  # First tools is fixed dummy.
CREATE_NEW_GROUP_BUTTON = """[ng-click="addGroup()"]>i"""
TABLE_FIRST_ROW = '#content .panel-body table tbody tr td:first-child'
GROUP_FORM = 'form[name="groupForm"]'
GROUP_NAME_INPUT = '#id_group_name'
COUNTRY_DROPDOWN = '[name="country"] .btn'
FIRST_OPTION = '.ui-select-choices-row'
GROUP_TYPE_DROPDOWN = '[name="type"] .btn'
#MODAL_LOGIN_SUBMIT_BUTTON = '.modal-footer .btn-primary:not([disabled])'
MODAL_LOGIN_SUBMIT_BUTTON = """.modal-footer [type="submit"]"""
EDIT_GROUP_BUTTON = '[ng-click="editGroup()"]>i'
MODAL_EDIT_GROUP_WINDOW = "h3.modal-title.ng-binding"
PERMISSIONS_CELL = '[ng-controller="GroupLicenseTypeCtrl"] td + td'
TABLE_HEADER_SORT_BY_ID = 'thead + thead [st-sort="Id"]'
NEW_USER_BUTTON_TOOLBAR = """[ng-click="actions.addUser()"]"""
FIRST_NAME_FIELD = '#id_first_name'
LAST_NAME_FIELD = '#id_last_name'
EMAIL_FIELD = '#id_email'
USER_SUCCESS_MESSAGE = '.gritter-success'
USER_TABLE_ROW = '[ng-repeat="user in filteredUsers"]'
GENERIC_MODAL = '.modal'
CONFIRM_BUTTON = '.modal [ng-click="yes()"]'
LOADER = """.spinner"""
CREATION_TOOLS_CHECKBOXES = """[class="checkbox ng-scope"]"""
MORE_OPTIONS_BTN = """.dropdown-toggle[tooltip="More options"]"""
MORE_OPTIONS = '.dropdown.open>ul.dropdown-menu.dropdown-menu-right'
GROUPS_TABLE = """tr[ng-repeat="group in filteredGroups"]"""
USERS_ROLES = """a.ng-binding"""
APPLIED_ROLES = """[ng-repeat="role in user.Roles track by $index"]"""
DROPDOWN_SUBMIT = """.btn.btn-primary"""
BLIPP_APPROVE_CHECKBOX = '[class="ng-scope ng-binding"]'
USER_DROPDOWN = """a[data-toggle="dropdown"]"""
GROUP_NAME_TITLE = '[for="id_group_name"]'
GROUP_TYPE_TITLE = '[mark-error="type"]'
COUNTRY_TITLE = '[mark-error="country"]'
LICENSE_START_TITLE = '[for="id_license_start"]'
ACCOUNT_MANAGER_TITLE = '[mark-error="account_manager"]'
GROUP_TYPE_SELECTOR = '.table.table.table-bordered.group-table.m-b-0 tbody tr:nth-child(4) td:nth-child(2)'

def select_group(context, group_name):
    context.execute_steps(u"""when filtering by {filter}""".format(filter=group_name))
    time.sleep(1)
    groups = context.browser.find_elements_by_css_selector(GROUPS_TABLE)
    for group in groups:
        #if group.text == re.search("(group_name)", group.text):
        if group_name in group.text:
            print("lets click on ", group_name)
            group.click()
        else:
            assert False, "Group {group} not found in {results}".format(group=group_name, results=groups)

def action_on_checkbox(checkbox, action):
    input_element = checkbox.find_element_by_css_selector('input')
    checkbox_selected = input_element.is_selected()
    if action == 'enable':
        if checkbox_selected == False:  #IF DISABLED CLICK ON THE ELEMENT
            input_element.click()
            return
        else:
            print('Checkbox already enabled, doing nothing')
            return
    elif action == 'disable':
        if checkbox_selected == True:  #IF ENABLED CLICK ON THE ELEMENT
            input_element.click()
            return
        else:
            print('Checkbox already disabled, doing nothing')
            return
    else:
        assert False, "Error specify a valid action (enable, disable)"
    assert False, "Error, the checkbox couldn't be {action}".format(action=action)

def open_more_options(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=MORE_OPTIONS_BTN))
    el = context.browser.find_element_by_css_selector(MORE_OPTIONS_BTN)
    action = ActionChains(context.browser)
    action.move_to_element(el).click().perform()

def get_more_options_settings(context):
    try:
        context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=MORE_OPTIONS))
    except:
        open_more_options(context)
    group_more_options = context.browser.find_element_by_css_selector(MORE_OPTIONS).text
    print("Group ops", group_more_options)#.split("\n"))
    if group_more_options:
        return group_more_options.split("\n")
    else:
        assert False, "Couldn't get group options"

def get_active_roles(context):
    roles_in_table=context.browser.find_elements_by_css_selector(APPLIED_ROLES)
    active_roles=[str(role.text.strip(",").strip()) for role in roles_in_table]
    print("Active user roles: ", active_roles)
    return active_roles

def is_user_creator_role(context):
    creation_tools_roles=['Blippbuilder (Classic) User', 'Blippbuilder (New) User', 'Custom (JavaScript) User']
    active_roles=get_active_roles(context)
    creator_roles_in_table=[x for x in active_roles if x in creation_tools_roles]
    print("creator_roles_in_table", creator_roles_in_table)
    return creator_roles_in_table


def revoke_access(context):
    roles_to_revoke = len(is_user_creator_role(context))
    print("Roles to revoke", roles_to_revoke)
    while roles_to_revoke > 0 :
        open_more_options(context)
        more_settings = get_more_options_settings(context)
        print("More settings", more_settings)
        for s in more_settings:
            if s.startswith(u'Revoke'):
                print("Found it", s)
                element = context.browser.find_element_by_link_text(s)
                action = ActionChains(context.browser)
                action.move_to_element(element).click().perform()
                time.sleep(1)
                print("Active roles after click", get_active_roles(context))
                open_more_options(context)
            else:
                print("No need to Revoke this access", s)
        roles_to_revoke -= 1
    else:
        print("This user dont have creation tool access")

def toggle_group_access_more_options(context, action, option):
    open_more_options(context)
    group_more_options = get_more_options_settings(context)
    group_more_options=[x.upper() for x in group_more_options]
    option_string = (option + " access").upper()
    print("Group options", group_more_options)
    if option_string.upper().endswith("BLIPPBUILDER (CLASSIC) ACCESS"):
        element = """[roles="[tools.BLIPPBUILDER_FLASH.UserRole.Key]"]"""
    elif option_string.upper().endswith("BLIPPBUILDER (NEW) ACCESS"):
        element = """[roles="[tools.BLIPPBUILDER_JAVASCRIPT.UserRole.Key]"]"""
    elif option_string.upper().endswith("CUSTOM (JAVASCRIPT) ACCESS"):
        element = """[roles="[tools.BESPOKE_JAVASCRIPT.UserRole.Key]"]"""
    elif option_string.upper().endswith("DEVELOPER (NETWORK & CUSTOM JS) ACCESS"):
        element = """[roles="[roles.DEVELOPER_NETWORK_ROLE.Key, roles.BESPOKE_JAVASCRIPT_ROLE.Key]"]"""
    elif option_string.upper() in "DISABLE USER":
        element = """[ng-click="actions.remove([user])"]"""
#TODO add other options
    else:
        assert False, "Please provide correct options! {option}".format(option=option_string)
    el=context.browser.find_elements_by_css_selector(element)
    el=el[0]
    roles = len(is_user_creator_role(context))
    if el.text.startswith(action):
        el.click()
        time.sleep(1)
        after_action_roles = len(is_user_creator_role(context))
        if action == "Add":
            assert roles + 1 == after_action_roles
        elif action == "Revoke":
            assert roles -1 == after_action_roles
        else:
            print("Is your action correct?")
        print("Changed access", el.text)
        time.sleep(1)
    else:
        print("No need to change this access", el.text)

# Load groups overview
@when("navigating to Groups & Users")
def step_impl(context):
    try:
        context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=USER_DROPDOWN))
        context.execute_steps(u"""when click on button {element} identified by css_selector""".format(element=USER_DROPDOWN))
        context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=SIDEBAR_GROUPS_LINK))
        context.execute_steps(u"""when clicking {selector}""".format(selector=SIDEBAR_GROUPS_LINK))
        context.execute_steps(u"""then expect {selector} to disappear within 30 seconds""".format(selector=LOADER))
    except:
        print("We have exception here: ", context.browser.title)


@then("the Groups overview is loaded")
def step_impl(context):
    context.execute_steps(
        u"""The screen Groups & users is opened""")

@then("I wait for the filter to become visible")
def step_impl(context):
    context.execute_steps(u"""then wait for {selector}""".format(selector=GROUP_FILTER))


@when("filtering by {group_id}")
def step_impl(context, group_id):
    context.execute_steps(u"""when typing {value} in {selector}""".format(value=group_id, selector=GROUP_FILTER))
    time.sleep(1)

@when("I select the group {group_name}")
def step(context, group_name):
    select_group(context, group_name)

@when("I open the group {group_name} for edition")
def step(context, group_name):
    select_group(context, group_name)
    context.execute_steps(u"""when click in link with text {text}""".format(text="Group Info"))
    context.execute_steps(u"""when clicking {selector}""".format(selector=EDIT_GROUP_BUTTON))

@when("I open the group shown")
def step(context):
    context.execute_steps(u"""when click in link with text {text}""".format(text="Group Info"))

@when('I revoke access to all tools for user {user}')
def step(context, user):
    context.execute_steps(u"""when filtering by {filter}""".format(filter=user))
    #get_active_roles(context)
    #open_more_options(context)
    #get_more_options_settings(context)
    revoke_access(context)

@then('I check that the user has all tools revoked')
def step(context):
    assert True, len(is_user_creator_role(context)) == 0

@when("I {action} access to {creation_tool} on group or user level")
def step(context, action, creation_tool):
    toggle_group_access_more_options(context, action, creation_tool)
    get_active_roles(context)

@then("the first result is a group with ID {group_id}")
def step_impl(context, group_id):
    time.sleep(1)
    #context.execute_steps(u"""then allow 1s to update the UI""")
    context.execute_steps(
        u"""then expect {selector} to contain {group_id}""".format(selector=TABLE_FIRST_ROW, group_id=group_id))

@when("I click on Approvals on the left sidebar")
def step_impl(context):
    context.execute_steps(u"""when clicking {selector}""".format(selector=SIDEBAR_APPROVALS))


# Creating a group
@when("I click on the New Group button")
def step_impl(context):
    context.execute_steps(u"""when clicking {selector}""".format(selector=CREATE_NEW_GROUP_BUTTON))

@then("the create new group modal is visible")
def step_impl(context):
    context.execute_steps(u"""then wait for {selector}""".format(selector=GROUP_FORM))

@when("filling out the new group form with the group name {group_name}")
def step_impl(context, group_name):
    context.execute_steps(u"""when typing {value} in {selector}""".format(value=group_name, selector=GROUP_NAME_INPUT))
    # Country
    context.execute_steps(u"""when clicking {selector}""".format(value=group_name, selector=COUNTRY_DROPDOWN))
    context.execute_steps(u"""when clicking {selector}""".format(value=group_name, selector=FIRST_OPTION))
    # Group type
    context.execute_steps(u"""when clicking {selector}""".format(value=group_name, selector=GROUP_TYPE_DROPDOWN))
    context.execute_steps(u"""when clicking {selector}""".format(value=group_name, selector=FIRST_OPTION))

@then("the submit button is clickable")
def step_impl(context):
    #context.execute_steps(u"""then wait for {selector}""".format(selector=MODAL_LOGIN_SUBMIT_BUTTON))
    context.execute_steps(u"""then wait for element {selector} to be clickable""".format(selector=MODAL_LOGIN_SUBMIT_BUTTON))


@when("I click on the modal submit button")
def step_impl(context):
    context.execute_steps(u"""when clicking {selector}""".format(selector=MODAL_LOGIN_SUBMIT_BUTTON))
    context.execute_steps(u"""then expect {selector} to disappear""".format(selector=MODAL_LOGIN_SUBMIT_BUTTON))

@then("a group is created with the group name {group_name}")
def step_impl(context, group_name):
    context.execute_steps(u"""then wait for {selector}""".format(selector='.gritter-title'))


# Updating a group
@when("navigating to the last group")
def step_impl(context):
    context.execute_steps(u"""when navigating to Groups & Users""")
    context.execute_steps(u"""when clicking {selector}""".format(selector=TABLE_HEADER_SORT_BY_ID))
    context.execute_steps(u"""when clicking {selector}""".format(selector=TABLE_FIRST_ROW))


@when("I click on the edit group button")
def step_impl(context):
    context.execute_steps(u"""when click in link with text {text}""".format(text="Group Info"))
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=EDIT_GROUP_BUTTON))
    context.execute_steps(u"""when clicking {selector}""".format(selector=EDIT_GROUP_BUTTON))


@then("the edit group modal is visible")
def step_impl(context):
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element=GROUP_FORM))


@when("I click on the edit group form submit button")
def step_impl(context):
    context.execute_steps(u"""when clicking {selector}""".format(selector=MODAL_LOGIN_SUBMIT_BUTTON))


@then("the group is renamed to {group_name}")
def step_impl(context, group_name):
     context.execute_steps(u"""then I expect a success message""")
     selector = context.browser.find_element_by_css_selector(GROUP_NAME_SELECTOR).text
     assert selector == group_name, "Error: obtained value {value} doesn't match expected value {group_name}".format(value=selector, group_name=group_name)


@then(u'the group is updated')
def step_impl(context):
    context.execute_steps(u"""then expect {selector} to disappear""".format(selector=MODAL_EDIT_GROUP_WINDOW))

# Creating a user
@when("I click on the users tab")
def step_impl(context):
    time.sleep(2)
    context.execute_steps(u"""when click in link with text {text}""".format(text="Users"))


@when("I click on the new user button in the toolbar")
def step_impl(context):
    context.execute_steps(u"""when clicking {selector}""".format(selector=NEW_USER_BUTTON_TOOLBAR))


@when("I create a new user trying any of the buttons")
def step(context):
    context.execute_steps(u"""when click in link with text {text}""".format(text="Users"))
    try:
        context.execute_steps(u"""when I click on the new user button""")
    except:
        context.execute_steps(u"""when I click on the new user button in the toolbar""")


@then("the create new user modal is visible")
def step_impl(context):
    context.execute_steps(u"""then wait for {selector}""".format(selector='h3.modal-title'))


@when("filling out the new user form with first name {firstname} and last name {lastname}")
def step_impl(context, firstname, lastname):
    email = 'someuser+group_admin_auto_{randy}@blippar.com'.format(randy=random.random())
    context.execute_steps(
        u"""when typing {firstname} in {selector}""".format(selector=FIRST_NAME_FIELD, firstname=firstname))
    context.execute_steps(
        u"""when typing {lastname} in {selector}""".format(selector=LAST_NAME_FIELD, lastname=lastname))
    context.execute_steps(u"""when typing {email} in {selector}""".format(selector=EMAIL_FIELD, email=email))


@when("creating a user with first name {firstname} and last name {lastname} and email from global var {global_var}")
def step(context, firstname, lastname, global_var):
    email = context.config.userdata[global_var]
    context.execute_steps(
        u"""when typing {firstname} in {selector}""".format(selector=FIRST_NAME_FIELD, firstname=firstname))
    context.execute_steps(
        u"""when typing {lastname} in {selector}""".format(selector=LAST_NAME_FIELD, lastname=lastname))
    context.execute_steps(u"""when typing {email} in {selector}""".format(selector=EMAIL_FIELD, email=email))


@then("a user is created with first name {firstname} and last name {lastname}")
def step_impl(context, firstname, lastname):
    context.execute_steps(
    u"""then expect {selector} to disappear within 5 seconds""".format(selector=DROPDOWN_SUBMIT))
    context.execute_steps(u"""then wait for element {element} identified by css_selector""".format(element='.gritter-title'))
    rows = context.browser.find_elements_by_css_selector(USER_TABLE_ROW)
    for row in rows:
        try:
            context.execute_steps(u"""then expect {selector} to contain {firstname}""".format(selector=USER_TABLE_ROW,
                                                                                              firstname=firstname))
            context.execute_steps(
                u"""then expect {selector} to contain {lastname}""".format(selector=USER_TABLE_ROW, lastname=lastname))
            return
        except:
            pass
    assert False, "Test failed: couldn't find user with firstname {firstname} and lastname {lastname}" \
        .format(firstname=firstname, lastname=lastname)


@when("I click on the confirm button")
def step_impl(context):
    context.execute_steps(u"""when clicking {selector}""".format(selector=CONFIRM_BUTTON))

@then("all users are marked as deleted")
def step_impl(context):
    context.execute_steps(u"""then I expect a success message""")
    rows = context.browser.find_elements_by_css_selector(USER_TABLE_ROW)
    for row in rows:
        if 'DELETED' not in row.text.upper():
            assert False, "User not deleted"


@when("I set {checkbox_name} checkbox {status}")
def step(context, checkbox_name, status):
    checkboxes = context.browser.find_elements_by_css_selector(CREATION_TOOLS_CHECKBOXES)
    for checkbox in checkboxes:
         if checkbox.text == checkbox_name:
            if status == 'enabled':
                action_on_checkbox(checkbox, 'enable')
                return
            elif status == 'disabled':
                action_on_checkbox(checkbox, 'disable')
                return
            else:
                assert False, "Error, must provide enabled or disabled for creation tool checkbox"
    assert False, "Error, invalid checkbox name"

@when("I open the user page for blippar group") #hard coded url with a group number in it but it's not a problem cause we use it only once in 6-hub-groups-and-users.feature
def step(context):
    url = urlparse.urljoin(context.config.userdata['target_env'], "dashboard/group/7/users")
    context.execute_steps(u"""when opening the url {url}""".format(url=url))

@then("I wait up to {time} secs for the users to load")
def step(context, time):
    context.execute_steps(u"""then wait up to {timeout} seconds for {selector}""".format(timeout=time, selector=USER_TABLE_ROW))

#approve/disapprove the blipp
@then('admin sets checkbox blipp {blipp_name} {status}')
def step_impl(context, blipp_name, status):
    checkboxes = context.browser.find_elements_by_css_selector(BLIPP_APPROVE_CHECKBOX)
    for checkbox in checkboxes:
        print("checkbox.text", checkbox.text)
        if checkbox.text == blipp_name:
            if status == 'enabled':
                checkbox.click()
                return
            elif status == 'disabled':
                checkbox.click()
                return
            else:
                assert False, "Error, must provide enabled or disabled for blipp approval checkbox"
    assert False, "Error, invalid checkbox name"

@then('the following fields are displayed {group_name},{group_type},{country},{license_date},{account_manager}')
def step(context, group_name, group_type, country,license_date, account_manager):
    context.execute_steps(u"""then wait for {selector}""".format(selector=GROUP_NAME_TITLE))
    context.execute_steps(u"""then expect {selector} to contain {group_name}""".format(selector=GROUP_NAME_TITLE, group_name=group_name))
    context.execute_steps(u"""then expect {selector} to contain {group_type}""".format(selector=GROUP_TYPE_TITLE, group_type=group_type))
    context.execute_steps(u"""then expect {selector} to contain {country}""".format(selector=COUNTRY_TITLE, country=country))
    context.execute_steps(u"""then expect {selector} to contain {license_date}""".format(selector=LICENSE_START_TITLE, license_date=license_date))
    context.execute_steps(u"""then expect {selector} to contain {account_manager}""".format(selector=ACCOUNT_MANAGER_TITLE, account_manager=account_manager))

@then('the Group type field contains {group_type}')
def step(context, group_type):
    context.execute_steps(u"""then wait for {selector}""".format(selector=GROUP_TYPE_SELECTOR))
    context.execute_steps(u"""then expect {selector} to contain {group_type}""".format(selector=GROUP_TYPE_SELECTOR, group_type=group_type))
