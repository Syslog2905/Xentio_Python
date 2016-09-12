import ast
import re
from api_helpers import *


#****************
# HELPER METHODS
#****************

#************
#GIVEN STEPS
#***********

@given("I clear the userdata")
def step(context):
    context.config.userdata.pop("ADITIONAL_HEADERS", None)
    context.config.userdata.pop("FILENAME", None)
    context.config.userdata.pop("PAYLOAD", None)

#****************
# WHEN STEPS
#****************
@when("I set payload {payload}")
def step(context, payload):
    if (payload.find(":{dynamic_id}"))!=-1:
        payload=payload.replace(":{dynamic_id}",str(blipp_campiagn_id))
    context.config.userdata['PAYLOAD'] = payload

@when("I set aditional header {header}")
def step(context, header):
    context.config.userdata['ADITIONAL_HEADERS'] = header

@when("I add file {filename} from folder {folder} and filetype {file_type}")
def step(context, filename, folder, file_type):
    files = [[file_type, [filename, open(os.path.join(os.getcwd(), folder, filename), 'rb')]]]
    context.config.userdata['FILENAME'] = files

@when("As {role} I run a {action} in the endpoint {endpoint} with base in var {base}")
def step(context, role, action, endpoint, base):
    base_url = context.config.userdata[base]
    if (endpoint.find(":{dynamic_id}"))!=-1:
        endpoint=endpoint.replace(":{dynamic_id}",str(blipp_campiagn_id))
        print(endpoint)
    print(base_url)
    url = urlparse.urljoin(base_url, endpoint)
    print(url)
    if action == "GET":
        get_method(context, url, user_role=role)
    elif action == "POST":

        if ('ADITIONAL_HEADERS' in context.config.userdata and 'PAYLOAD' in context.config.userdata):
            headers = context.config.userdata['ADITIONAL_HEADERS']
            post_method(context, url, role, json.dumps(ast.literal_eval(context.config.userdata['PAYLOAD'])),custom_headers=headers)

        elif ('FILENAME' in context.config.userdata and 'ADITIONAL_HEADERS' in context.config.userdata):
            headers = context.config.userdata['ADITIONAL_HEADERS']
            file = context.config.userdata['FILENAME']
            post_method(context, url, role, payload=None, files=file, custom_headers=headers)

        elif ('FILENAME' in context.config.userdata):
            file = context.config.userdata['FILENAME']
            post_method(context, url, role, payload=None,files=file )

        elif ('FILENAME' in context.config.userdata  and 'PAYLOAD' in context.config.userdata):
            file = context.config.userdata['FILENAME']
            post_method(context, url, role, json.dumps(ast.literal_eval(context.config.userdata['PAYLOAD'])),files=file )

        elif ('PAYLOAD' in context.config.userdata):
            print("PAYLOAD    :", context.config.userdata['PAYLOAD'])
            post_method(context, url, role, json.dumps(ast.literal_eval(context.config.userdata['PAYLOAD'])))

    elif action == "DELETE":
        delete_method(context, url, role)
    elif action == "PATCH":
        patch_method(context, url, role, json.dumps(context.config.userdata['PAYLOAD']))
    else:
        assert False, "Error, invalid action (GET,POST,DELETE or PATCH)"

#This is an adapter to the scenario : @when("As {role} I run a {action} in the endpoint {endpoint} with base in var {base}")
#The objective is to support the endpoint from a global variable
@When('As role {role} I run a {action} using endpoint stored in variable {variable} with base in {base}')
def step(context, role, action, variable, base):
    endpoint = context.config.userdata[variable]
    context.execute_steps(u"""when As {role} I run a {action} in the endpoint {endpoint} with base in var {base}""".\
                          format(role=role, action=action, endpoint=endpoint, base=base))

#The value in the endpoint string that is enclosed by {} will be replacer by the value in the global variable.
#eg. "/api/v1/user/{user_id}"
@When('I build the url for endpoint {endpoint} using variable in {variable} and I store it in {endpoint_variable}')
def step(context, endpoint, variable, endpoint_variable):
    value_in_var = context.config.userdata[variable]
    r = re.compile('{.*}')
    search = r.search(endpoint)
    if search:
        context.config.userdata[endpoint_variable] = endpoint.replace(search.group(0), str(value_in_var))
    else:
        assert False, "The endpoint should contain a parameter to replace inside {}. eg. {user_id}"


#****************
# THEN STEPS
#****************

@then("the status code of the response is {status_code}")
def step(context, status_code):
    assert status_code == get_last_response(context).status_code, "Test failed. Status code obtained {obtained}, expected {expected}".\
        format(expected=status_code, obtained=get_last_response(context).status_code)

#Searching using basic text search. See examples. Need more time to use a more elegant way using json.
@Then('the response contains the value {value}')
def step(context, value):
    response = get_last_response(context).text
    assert response.find(value) != -1, "Test failed, couldn't find value {value} in response. Response obtained {response}".\
    format(value=value, response=response)

@then("I get the {Id} from json object")
def step(context,Id):
    global blipp_campiagn_id
    blipp_campiagn_id=get_last_response(context).json().get(Id)
    print(blipp_campiagn_id)
