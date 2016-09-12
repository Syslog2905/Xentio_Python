import ast
import re
import requests
import json
import ssl
import os
import urlparse
import time
import urllib2
from requests_toolbelt import SSLAdapter
from environment import * #USERS, LOCATIONS, INTERACTION_USERS

VERIFY_SSL_CERT = True

# *****************************
# HELPER METHODS
# *****************************

def erase_last_response(context):
    context.config.userdata['last_response'] = ""

def set_api_response(context, response):
    context.config.userdata['last_response'] = response

def get_last_response(context):
    return context.config.userdata['last_response']

def get_method(context, url, user_role, check_response_code = True):
    erase_last_response(context)
    get_bearer_token(context,user_role)
    #update_token(context, user_role)
    s = requests.Session()
    s.headers = context.config.userdata.get("bake_api_token")
    s.mount(url, SSLAdapter(ssl.PROTOCOL_TLSv1))
    response = s.get(url, verify=VERIFY_SSL_CERT)
    set_api_response(context, response)
    if check_response_code:
        assert response.status_code == 200, "Error, status code is {code}, expected 200. The error is {error}".format(code=response.status_code, error=response.text)
    print('Response code: '+str(response.status_code))

def post_method(context, url, user_role, payload, check_response_code = True, files = None, custom_headers = None):
    erase_last_response(context)
    get_bearer_token(context,user_role)
    #update_token(context, user_role)
    s = requests.Session()
    s.headers = context.config.userdata.get("bake_api_token")
    if custom_headers != None:
        custom_headers = ast.literal_eval(custom_headers)
        for key, value in dict(custom_headers).iteritems():
            s.headers[key] = value
    print(s.headers)
    s.mount(url, SSLAdapter(ssl.PROTOCOL_TLSv1))
    print('Running POST: '+url, "By role:", user_role)
    if files:
        response = s.post(url, data=payload, files=files, verify=VERIFY_SSL_CERT)
    else:
        response = s.post(url, data=payload, verify=VERIFY_SSL_CERT)
    set_api_response(context, response)
    if check_response_code:
        assert response.status_code == 200 or response.status_code == 201, "Error, status code is {code}, expected 200 or 201. The error is {error}".format(code=response.status_code, error=response.text)
    print('Response code: '+str(response.status_code))

def patch_method(context, url, payload, check_response_code=True, user_role = 'blippar_admin'):
    erase_last_response(context)
    get_bearer_token(context,user_role)
    #update_token(context, user_role)
    s = requests.Session()
    s.headers = context.config.userdata.get("bake_api_token")
    s.mount(url, SSLAdapter(ssl.PROTOCOL_TLSv1))
    print('Running PATCH: '+url, "By role:", user_role)
    print('Using payload: '+str(payload))
    response = s.patch(url, data=payload, verify=VERIFY_SSL_CERT)
    set_api_response(context, response)
    if check_response_code:
        assert response.status_code == 200 or response.status_code == 201, "Error, status code is {code}, expected 200 or 201. The error is {error}".format(code=response.status_code, error=response.text)
    print('Response code: '+str(response.status_code))

def delete_method(context, url, user_role, check_response_code = True ):
    erase_last_response(context)
    get_bearer_token(context,user_role)
    #update_token(context, user_role)
    s = requests.Session()
    s.headers = context.config.userdata.get("bake_api_token")
    s.mount(url, SSLAdapter(ssl.PROTOCOL_TLSv1))
    response = s.delete(url, verify=VERIFY_SSL_CERT)
    set_api_response(context, response)
    print('Running DELETE: '+url, "By role:", user_role)
    if check_response_code:
        assert response.status_code == 204 or response.status_code == 200, "Error, status code is {code}, expected 200 or 204. The error is {error}".format(code=response.status_code,  error=response.text)
    else:
        #case of error 403
        if user_role in USERS.keys() and user_role != 'blippar_admin' and response.status_code == 403:
            print("Skip resp. check on if user is not admin and code is 403")
            return response.status_code
    print('Response code from delete: '+str(response.status_code))

def update_token(context, user_role, token_regexp='my_token=(.*?);'):
    erase_last_response(context)
    if user_role in USERS.keys():
        headers = {'User-Agent': 'Mozilla/5.0'}
        payload = {'email':USERS[user_role]['email'], 'password':USERS[user_role]['password']}
        print("Update token Payload:", payload)
        base_url = context.config.userdata['target_env']
        session = requests.Session()
        redirect_url = session.get(base_url, verify=VERIFY_SSL_CERT)
        retries = 3
        while retries > 0:
            response = session.post(redirect_url.url, headers=headers, data=payload, verify=VERIFY_SSL_CERT)
            raw_header = response.headers.get("set-cookie")
            if re.search('^ApiSession', raw_header):
                print("Found APISession in the cookie. Let's retry. Did you authorize this user on the TARGET_ENV?")
                retries -= 1
            else:
                break
        r = re.compile(token_regexp)
        search = r.search(raw_header)
        if search:
            token = search.group(1)
        else:
            assert False, "ERROR: Cannot extract token"
        context.config.userdata['bake_api_token'] = {'Authorization': token}
        print("Resulting API Token", context.config.userdata['bake_api_token'])
    else:
        assert False, "Error, wrong user role {role}. Valid roles are: {roles}".format(role=user_role,roles = USERS.keys())


def get_csrf_token(context, url=OAUTH_URL):
    url = urlparse.urljoin(url, "/login")
    r = requests.get(url)
    print("CSRF, headers Set-cookie", r.headers.get('Set-Cookie'))
    csrf_token = r.headers.get('Set-Cookie').split(';')[0].split('=')[1]
    print("csrftoken:", csrf_token)
    return csrf_token
 #  ['csrftoken=zDXo9ydS31EnCRBOhlBVhYzGUh88bUBB',
 # ' expires=Mon, 27-Feb-2017 13:00:53 GMT',
 # ' Max-Age=31449600',
 # ' Path=/']

def get_session_id(context, user_role, regexp='sessionid=\w+;'):
    url=urlparse.urljoin(OAUTH_URL, "/api/v1/login")
    payload = {'email':USERS[user_role]['email'],'password':USERS[user_role]['password'],\
               'csrftoken':get_csrf_token(context)}

    exp = re.compile(regexp)
    retries = 3
    while retries > 0:
        r=requests.post(url, data=payload)
        try:
            set_cookies = r.headers.get('Set-Cookie')
            search = exp.search(set_cookies)
            if search:
                token = search.group(0)
                sessionid = token.replace('sessionid=', "")
                print("sessionid: ", sessionid)
                return sessionid
        except:
            time.sleep(0.5)
            retries -= 1
    assert False, "Couldn't get session_id, Headers {h}".format(h=r.headers)

def get_bearer_token(context, user_role, token_regexp='access_token=\w+'):
    '''
    Wrapping up authentication on OAUTH2 Implicit Grant
    :param user_role:
    :param token_regexp: we gather this from a Location header. It was tricky becase there is a redirrection on this request
    :return: {'Authorization': 'Bearer tteDnkzjFhTxDicNir1Pn0gKFCxYGN'})
    '''
    erase_last_response(context)
    if user_role in USERS.keys():
        cookies={'sessionid': get_session_id(context,user_role)}
        url=urlparse.urljoin(OAUTH_URL,"/o/authorize/?client_id={id}&response_type=token"\
            .format(id=CLIENT_IDS[context.config.userdata['target_env']]))
        r=requests.head(url, cookies=cookies, verify=True, allow_redirects=True)
        u=r.history[0].headers['Location']
        # 'https://alpha-hub.dev.blippar.com/dashboard/#access_token=co0y0a19e72aUlcvLZF46rNzuzv7V3&token_type=Bearer&expires_in=36000&scope=read+everything+write'
        encoded_url=urllib2.url2pathname(u)
        print("Location URL:", encoded_url)
        exp = re.compile(token_regexp)
        search = exp.search(encoded_url)
        if search:
            token = search.group(0)
            # we receive 'access_token=co0y0a19e72aUlcvLZF46rNzuzv7V3'
            context.config.userdata['bake_api_token'] = {'Authorization': 'Bearer ' + token.replace('access_token=', "")}
            print("Resulting OAUTH Bearer Token", context.config.userdata['bake_api_token'])
        else:
            assert False, "ERROR: Cannot extract token"
    else:
        assert False, "Error, wrong user role {role}. Valid roles are: {roles}".format(role=user_role,roles = USERS.keys())
