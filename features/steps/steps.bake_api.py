from api_helpers import *

def get_stats_from_blipp(context,blipp_id, stat, date_from, date_to):
    #stat may be interactions, users, locations
   base_url = context.config.userdata['stats_api_url']
   if date_to == "Now":
        date_to = time.strftime("%Y-%m-%d %H:%M:%S")
   url = urlparse.urljoin(base_url, "/blipp/{blipp_id}/{stat}?datefrom={date_from}&dateto={date_to}".format(blipp_id=blipp_id, stat=stat, date_from=date_from, date_to=date_to))
   get_method(context, url, user_role="blippar_admin")
   return get_last_response(context).json()


def get_stats_from_campaign(context, campaign_id, stat, date_from, date_to):
   base_url = context.config.userdata['stats_api_url']
   if date_to == "Now":
        date_to = time.strftime("%Y-%m-%d")
   url = urlparse.urljoin(base_url, "/campaign/{campaign_id}/{stat}?datefrom={date_from}&dateto={date_to}".format(campaign_id=str(campaign_id[0]), stat=stat, date_from=date_from, date_to=date_to))
   print("URL", url)
   get_method(context, url, user_role="blippar_admin")
   return get_last_response(context).json()

def post_interaction(context, number_of_interactions, blipp_id, location="Amsterdam", user="user1", timestamp="Now", check_response_code=True, user_role = 'blippar_admin'):
    erase_last_response(context)
    url = urlparse.urljoin(context.config.userdata['stats_api_url'], "/post")
    get_bearer_token(context,user_role)
    s = requests.Session()
    s.headers = context.config.userdata.get("bake_api_token")
    s.mount(url, SSLAdapter(ssl.PROTOCOL_TLSv1))
    s.headers['X-Blippar-OSVersion'] = '19'
    s.headers['X-Blippar-EngineVersion'] = '15'
    s.headers['Accept-encoding'] = 'gzip'
    s.headers['X-Blippar-Gender'] = ' '
    s.headers['X-Blippar-DeviceType'] = 'android'
    s.headers['X-Blippar-SessionID'] = INTERACTION_USERS.get(user)
    s.headers['X-Blippar-Age'] = ' '
    s.headers['X-Blippar-Location-Accuracy'] = '49.0'
    s.headers['X-Blippar-Location'] = LOCATIONS.get(location)
    s.headers['X-Blippar-Device'] = 'motorolaXT1021'
    s.headers['X-Blippar-UniqueID'] = '3fc7573c-f06b-4dce-80ef-2787937f5d73'
    country = 'nl'
    if location in [ 'Mountain View', 'San Francisco', 'Los Angeles']:
        country = 'us'
    if location in [ 'New Delhi' , 'Mumbai' , 'Bangalore' , 'Chennai']:
        country = 'in'

    s.headers['X-Blippar-Region'] = country
    s.headers['X-Blippar-Database-Filter'] = 'debug'   #This value must not be set if an interaction want to be added in PROD env
    s.headers['X-Blippar-Geo-Region'] = 'ad'
    s.headers['X-Blippar-Action-Type'] = 'setProperty'
    s.headers['X-Blippar-Language'] = 'en'
    s.headers['Content-Type'] = 'application/x-www-form-urlencoded'
    s.headers['X-Blippar-AppVersion'] = '1.7.2.02'
    s.headers['User-Agent'] = 'Dalvik/1.6.0 (Linux; U; Android 4.4.4; XT1021 Build/KXC21.5-40)'
    s.headers['X-Blippar-Hash'] = ' fcb471503fc1c87cca0fb1008d26d754b50b15117c559b36b382494e2a5d2f1f'
    s.headers['X-Blippar-Token'] = 'da1ab1a2c34dda82890140bc0cff05aeed617030'

    blipp = get_blipp_full_data_from_id(context, blipp_id, user_role=user_role)
    cover_image_id = str(blipp.get('CoverImageId'))
    plist_id = str(blipp.get('LastPlistId'))

    if timestamp == "Now":
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    payload = {"analytics":{"items":[{"a":"40c95a1055", "id":"BLIPP", "m":"m"+cover_image_id, "metadata":"Scene default.onShow", "p":"p"+plist_id, "timestamp":timestamp}]}}

    for i in range(int(number_of_interactions)):
        response = s.post(url, json.dumps(payload), verify=VERIFY_SSL_CERT)
        set_api_response(context, response)
        if check_response_code:
            assert response.status_code == 200 or response.status_code == 201, "Error, status code is {code}, expected 200 or 201. The error is {error}".format(code=response.status_code, error=response.text)
        time.sleep(0.2) #some pause in running several requests

def get_blipp_id_from_name(context, blipp_name, campaign_id, user_role="blippar_admin"):
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/campaign/{campaign_id}/blipps?limit=0&metadata=0".format(campaign_id=str(campaign_id[0])))
    get_method(context, url, user_role)
    blipps = []
    response = get_last_response(context).json()
    if response != []:
        for blipp in response:
            if blipp.get("Name").lower() == blipp_name.lower() and blipp.get("Status") != "DELETED":
                blipps.append(blipp.get('Id'))
            else:
                assert False, "Blipp with name {name} not found in campaign {camp_id}".format(name=blipp_name, camp_id=campaign_id)
    return blipps[0]

def get_campaign_id_from_name(context, campaign_name, user_role="blippar_admin",include_deleted=False):
    # original -> "/api/campaigns?limit=0&metadata=0" is really slow
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/campaigns?orderby=created_at__desc&limit=1000")
    get_method(context, url, user_role)
    campaigns = []
    response = get_last_response(context).json()
    if response != []:
        for campaign in response:
            if include_deleted == True:
                if campaign.get('Name').lower() == campaign_name.lower():
                    campaigns.append(campaign.get('Id'))
            elif include_deleted == False:
                if campaign.get('Name').lower() == campaign_name.lower() and campaign.get('Deleted') == 0:
                    campaigns.append(campaign.get('Id'))
    if len(campaigns) > 0:
        return campaigns
    else:
        assert False, "Campaign {campaign_name} not found!".format(campaign_name=campaign_name)

def get_blipps_from_campaign(context, campaign_id, user_role="blippar_admin"):
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/campaign/{campaign_id}/blipps?metadata=full".format(campaign_id=str(campaign_id[0])))
    get_method(context, url, user_role, check_response_code=False)
    response = get_last_response(context).json()
    if response != []:
        return response
    return []

def get_blipp_versions(context, blipp_id, user_role="blippar_admin"):
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/blipp/{blipp_id}/versions?limit=1&metadata=full&orderby=-Version".format(blipp_id=blipp_id))
    get_method(context, url, user_role)
    blipp_versions = []
    response = get_last_response(context).json()
    for version in response:
        blipp_versions.append(version.get("Id"))
    return blipp_versions

def get_blipp_full_data_from_id(context, blipp_id, user_role):
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/blipp/{blipp_id}?metadata=full&metadata=1".format(blipp_id=blipp_id))
    get_method(context, url, user_role)
    return get_last_response(context).json()

def get_ad_id_from_name(context, ad_name, user_role):
    url = urlparse.urljoin(context.config.userdata['ads_api_url'], "/api/v1/ads")
    get_method(context, url, user_role)
    ads_ids = []
    response = get_last_response(context).json()
    if response:
        for ads in response:
            if ads.get('Title').lower() == ad_name.lower():
                ads_ids.append(ads.get('ID'))
    if len(ads_ids) > 0:
        return ads_ids
    else:
        assert False, "Ad {ad_name} not found!".format(ad_name=ad_name)

def create_empty_blipp(context, campaign_id, blipp_type_id, blipp_name, user_role):
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/campaign/{campaign_id}/blipp".format(campaign_id=str(campaign_id)))
    payload = {'campaignId': campaign_id, 'blippTypeId': blipp_type_id, 'name': blipp_name}
    post_method(context, url, user_role, json.dumps(payload))
    return get_last_response(context).json()

def create_blipp_version(context, blipp_id, type, user_role, blipp_file=None, country=""):
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], "api/blipp/{blipp_id}/version?limit=0&type={type}".format(blipp_id=str(blipp_id), type=type))
    if type == 'bespoke':
        files = {'file': (blipp_file, open(blipp_file, 'rb'))}
        payload = {'code': 'jjj'}  #Hardcoded to publish in a code by defaults, global only works with superadmin.
                                   # PRO and BASIC users can only publish in region, not global or code.
        post_method(context, url, user_role, payload=payload, files=files)
    if type == 'bespoke_country':
        url = urlparse.urljoin(context.config.userdata['hub_api_url'], "api/blipp/{blipp_id}/version?limit=0".format(blipp_id=str(blipp_id)))
        files = {'file': (blipp_file, open(blipp_file, 'rb'))}
        payload = {'country': country, 'type': 'bespoke'}
        post_method(context, url, user_role, payload=payload, files=files)
    elif type == 'builder_v2':
        post_method(context, url, user_role, payload=None)
    else:
        assert False, "Error: Wrong blipp type provided to create_blipp_version method"
    return get_last_response(context).json()

def create_blipp_plist(context, blipp_id, blipp_version_id, user_role):
    fd = open('assets/empty_plist', 'r')
    empty_plist = fd.read()
    #https://alpha-api.dev.blippar.com/api/blipp/101379/version/403204/plist
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/blipp/{blipp_id}/version/{blipp_version_id}/plist".format(blipp_id=blipp_id, blipp_version_id=blipp_version_id))
    post_method(context, url, user_role, payload=empty_plist)
    return get_last_response(context).json()

def upload_marker_to_empty_blipp(context, blipp_id, image_name, user_role):
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/blipp/{blipp_id}/marker".format(blipp_id=str(blipp_id)))
    file = [['file', [image_name, open(os.path.join(os.getcwd(), 'images', image_name), 'rb')]]]
    post_method(context, url, user_role, files=file, payload=None)
    return get_last_response(context).json()

def unpublish_blipp(context,blipp_id, blipp_version_id):
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/blipp/{blipp_id}/version/{blipp_version}/unpublish?blippVersionId={blipp_version}&id={blipp_version}&limit=0".format(blipp_id=str(blipp_id),blipp_version=str(blipp_version_id)))
    payload = {}
    patch_method(context, url, payload=json.dumps(payload))
    return get_last_response(context).json()

def publish_blipp(context,blipp_id, blipp_version_id,user_role):
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/blipp/{blipp_id}/version/{blipp_version}/generate?blippVersionId={blipp_version}&limit=0".format(blipp_id=str(blipp_id),blipp_version=str(blipp_version_id)))
    payload = {}
    post_method(context, url, user_role, payload=json.dumps(payload))
    return get_last_response(context).json()

def get_user_role(context, user):
    erase_last_response(context)
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/user")
    get_method(context, url,user)
    #response = get_last_response(context).json()
    #print("Response on User role:",user, response)

def get_user_group(context, user):
    erase_last_response(context)
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/user")
    get_method(context, url, user)
    context.user_group_id = get_last_response(context).json().get("Groups")[0].get("Id")
    print("Group ID: ", context.user_group_id)

def get_campaign_by_id(context, campaign_id, user_role):
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/campaign/{campaign_id}?metadata=full".format(campaign_id=campaign_id[0]))
    get_method(context, url, user_role)
    return get_last_response(context).json()

def get_campaign_creator_user_id(context, campaign_name):
    campaign_id = get_campaign_id_from_name(context, campaign_name)
    campaign = get_campaign_by_id(context, campaign_id, "blippar_admin")
    creator_id = campaign.get('CreatedByUserId')
    return creator_id

def get_user_permissions(context, user_id):
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/user/{user_id}/permissions?limit=0".format(user_id=user_id))
    get_method(context, url, "blippar_super_admin")
    return get_last_response(context).json()

def get_user_specific_permission(context, user_id, action):
    permissions = get_user_permissions(context, user_id)
    for permission in permissions:
        if permission.get("Action") == action:
            return permission.get('Permission')

def duplicate_blippbuilder_blipp(context, source_blipp_id, new_blipp_name, marker):
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/blipp/{blipp_id}/duplicate".format(blipp_id=str(source_blipp_id)))
    payload = {}
    post_method(context, url, user_role="blippar_admin", payload=json.dumps(payload))
    r = get_last_response(context).json()
    new_blipp_id = r.get("Id")
    #post image
    upload_marker_to_empty_blipp(context, new_blipp_id, marker, user_role="blippar_admin")
    print("POST response on duplicate: ", r, "New blipp id: ", new_blipp_id)
    blipp_version = create_blipp_version(context, new_blipp_id, type="builder_v2", user_role="blippar_admin").get('Id')
    plist = create_blipp_plist(context, new_blipp_id, blipp_version, user_role="blippar_admin")
    #set new blipp name in the payload and patch it!
    payload={"Id":int(new_blipp_id), "Name":new_blipp_name}
    new_url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/blipp/{new_blipp_id}".format(new_blipp_id=int(new_blipp_id)))
    print("NEW URL: ", new_url, "PAYLOAD:", payload)
    patch_method(context, new_url , payload=json.dumps(payload))
    return get_last_response(context).json()

def change_blipp_info(context, source_blipp_id, new_blipp_name, role):
    payload={"Id":int(source_blipp_id), "Name":str(new_blipp_name)}
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/blipp/{source_blipp_id}".format(source_blipp_id=int(source_blipp_id)))
   #print("NEW URL: ", new_url, "PAYLOAD:", payload)
    patch_method(context, url , payload=json.dumps(payload),check_response_code=False, user_role=role)
    return get_last_response(context).json()

def change_campaign_info(context, source_camp_id, new_camp_name, role):
    print("Source camp id:",source_camp_id)
    payload={"Id":int(source_camp_id[0]), "Name":str(new_camp_name)}
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/campaign/{campaign_id}".format(campaign_id=int(source_camp_id[0])))
   #print("NEW URL: ", new_url, "PAYLOAD:", payload)
    patch_method(context, url , payload=json.dumps(payload), check_response_code=False, user_role=role)
    return get_last_response(context).json()

def post_shared_stats_token(context, campaign_id, user_role):
    erase_last_response(context)
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/campaign/{campaign_id}/sharetoken".format(campaign_id=str(campaign_id[0])))
    payload = {}
    post_method(context, url, payload=payload, user_role=user_role)
    print("User role: ", user_role)
    context.shared_token = get_last_response(context).json().get('ShareToken')

def get_shared_link(context, campaign_id, stat, bad_token=False):
    erase_last_response(context)
    url = urlparse.urljoin(context.config.userdata['stats_api_url'], "/campaign/{campaign_id}/{stat}?metadata=full").format(campaign_id=campaign_id[0], stat=stat)
    #we can't use our get_method because it calls update_token with user roles, while this is about sharing with outside users
    print("SHARED URL: ", url, "SHARED TOKEN: ", context.shared_token )
    if bad_token == False:
        r=requests.get(url, headers = {'Authorization': "SHARED:" + context.shared_token})
        print(r.request.headers)
        assert r.status_code == 200, "Error on Shared link, status code is {code}, expected 200. The error is {error}".format(code=r.status_code, error=r.text)
    else:
        print ("We should hit permission errors:")
        r=requests.get(url, headers={'Authorization': "AUTOMATED_TESTS_INVALID_TOKEN"})
        assert r.status_code == 403

def upload_asset_bb(context, image_name):
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/media")
    file = [['file', [image_name, open(os.path.join(os.getcwd(), 'assets/img', image_name), 'rb')]]]
    post_method(context, url, user_role="blippar_admin", files=file, payload=None)
    r = get_last_response(context).json()
    context.asset_id = r.get("ID")
    return r

def manage_bb_asset(context, blipp_id, action,user_role="blippar_admin"):
    '''
    :param context:
    :param blipp_id:
    :param action: We can either Add or Delete an asset
    '''
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/blipp/{blipp_id}/media/{asset_id}").format(blipp_id=blipp_id, asset_id=context.asset_id )
    if action == 'add':
        post_method(context, url,user_role, payload=None)
    elif action == 'delete':
        delete_method(context, url,user_role)
    else:
        assert False, "Error, wrong action provided to step. Valid options are: add, delete"
    return get_last_response(context).json()

def add_bb_poll_to_blipp(context, blipp_id, user_role="blippar_admin"):
    '''

    :param blipp_id: the blipp on which we assign this poll
     Here I will use a predefined Poll question, because everything is wrapped inside html
     Poll Title: Behave Poll, Question: "Behave question?", Answers: "Yes/No/Maybe", Show results: yes; Response text: "Thanks for voting!"
     If we had proper payload one could extend this method to have all of the above as user input params!
    :return:
    '''
    url = urlparse.urljoin(context.config.userdata['bake_api_url'], "poll")
    # this is a predefined poll question in ugly HTML
    POLL_DATA_JSON = r'''{"blipp_id":109216,"data":{"saved":{"answerBackground":0,"questionHtml":"%3CHTML%3E%3CBODY%3E%3CP%20ALIGN%3D%22center%22%3E%3CFONT%20FACE%3D%22BBFontRegular%22%20SIZE%3D%2212%22%20COLOR%3D%22%23000000%22%20LETTERSPACING%3D%220%22%20KERNING%3D%221%22%3E%3CFONT%20FACE%3D%22Arial%22%20SIZE%3D%2218%22%20COLOR%3D%22%23666666%22%3E%3CB%3EBehave%20question%3F%3C/B%3E%3C/FONT%3E%3C/FONT%3E%3C/P%3E%3C/BODY%3E%3C/HTML%3E","questionScale":2,"name":"Behave Poll","response":"%3CHTML%3E%3CBODY%3E%3CP%20ALIGN%3D%22center%22%3E%3CFONT%20FACE%3D%22BBFontRegular%22%20SIZE%3D%2212%22%20COLOR%3D%22%23000000%22%20LETTERSPACING%3D%220%22%20KERNING%3D%221%22%3E%3CFONT%20FACE%3D%22Arial%22%20SIZE%3D%2218%22%20COLOR%3D%22%23666666%22%3E%3CB%3EThanks%20for%20voting%21%3C/B%3E%3C/FONT%3E%3C/FONT%3E%3C/P%3E%3C/BODY%3E%3C/HTML%3E","answerScale":2,"version":"2.7","answers":["Yes","No","Maybe",""],"showResults":true,"questionStyling":{"qTextColour":"0x0","fontFamily":"Arial","qButtonColour":"0x454545","qBackColour":"0xffffff","qButtonTextColour":"0xffffff"},"answerStyling":{"aBackColour":"0xcccccc","fontFamily":"Arial","aTextColour":"0xffffff","aContainerTextColour":"0x454545","aContainerColour":"0x454545"},"questionBackground":0},"published":null},"name":"Behave Poll"}'''
    payload = json.loads(POLL_DATA_JSON) #convert the ugly JSON
    payload['blipp_id'] = int(blipp_id) # add our blipp_id
    post_method(context, url, user_role, json.dumps(payload))

    # PATCH https://bake-env.dev.blippar.com/poll/568e85b2bdd1c449a8000056/data
    r = get_last_response(context).json()
    context.poll_id = r.get('id')
    path_url = urlparse.urljoin(context.config.userdata['bake_api_url'], "poll/{poll_id}/data").format(poll_id=context.poll_id)
    POLL_BAKE_PATCH=r'''{"saved":null,"published":{"questionBackground":0,"answerStyling":{"aContainerColour":"0x454545","aTextColour":"0xffffff","fontFamily":"Arial","aContainerTextColour":"0x454545","aBackColour":"0xcccccc"},"answerBackground":0,"name":"bla","questionHtml":"%3CHTML%3E%3CBODY%3E%3CP%20ALIGN%3D%22center%22%3E%3CFONT%20FACE%3D%22BBFontRegular%22%20SIZE%3D%2212%22%20COLOR%3D%22%23000000%22%20LETTERSPACING%3D%220%22%20KERNING%3D%221%22%3E%3CFONT%20FACE%3D%22Arial%22%20SIZE%3D%2218%22%20COLOR%3D%22%23666666%22%3E%3CB%3EYour%20question%20goes%20here%20-%20a%20maximum%20of%20150%20characters%20can%20be%20used.%3C/B%3E%3C/FONT%3E%3C/FONT%3E%3C/P%3E%3C/BODY%3E%3C/HTML%3E","questionScale":2,"version":"2.7","response":"%3CHTML%3E%3CBODY%3E%3CP%20ALIGN%3D%22center%22%3E%3CFONT%20FACE%3D%22BBFontRegular%22%20SIZE%3D%2212%22%20COLOR%3D%22%23000000%22%20LETTERSPACING%3D%220%22%20KERNING%3D%221%22%3E%3CFONT%20FACE%3D%22Arial%22%20SIZE%3D%2218%22%20COLOR%3D%22%23666666%22%3E%3CB%3EThanks%20for%20voting%21%3C/B%3E%3C/FONT%3E%3C/FONT%3E%3C/P%3E%3C/BODY%3E%3C/HTML%3E","answerScale":2,"answers":["Yes","No","Maybe",""],"showResults":true,"pollId":"568e85b2bdd1c449a8000056","questionStyling":{"fontFamily":"Arial","qBackColour":"0xffffff","qButtonTextColour":"0xffffff","qTextColour":"0x0","qButtonColour":"0x454545"}}}'''
    payload = json.loads(POLL_BAKE_PATCH) #convert the ugly JSON
    payload['pollId'] = context.poll_id # add our poll_id
    patch_method(context, path_url, json.dumps(payload))

    #PATCH https://alpha-api.dev.blippar.com/api/blipp/109225/version/412763/data
    blipp_version_id = get_blipp_versions(context, blipp_id, user_role="blippar_admin")[0]
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], "api/blipp/{blipp_id}/version/{blipp_version}/data").format(blipp_id=str(blipp_id),blipp_version=blipp_version_id)
    payload={"body":"{\"scenes\":[{\"name\":\"Scene\",\"sequences\":[{\"sequenceUid\":null,\"defaultSequence\":true,\"id\":0,\"label\":\"Sequence 1\",\"name\":\"Sequence0\"}],\"groups\":[],\"uid\":5,\"children\":[{\"position\":{\"x\":0,\"y\":0,\"scaleY\":1,\"scaleX\":1,\"rotationX\":0,\"z\":0,\"alpha\":100,\"rotationZ\":0,\"rotationY\":0,\"uniformScale\":1,\"scaleZ\":1,\"time\":0},\"bothSides\":true,\"name\":\"penguins.jpg\",\"isMasterLocked\":false,\"bytes\":107992,\"matID\":353090,\"isMaster\":false,\"animation\":{\"tracks\":[{\"rot\":[],\"pos\":[],\"uid\":14,\"duration\":0,\"time\":0,\"a\":[],\"sca\":[]}]},\"meshID\":-1,\"masterUID\":-1,\"locked\":false,\"shapeID\":-1,\"tap\":[{\"type\":\"Poll\",\"_uid\":15,\"id\":\"568e8943bdd1c449a8000059\",\"name\":\"Survey Pollblaasdasd\"}],\"selected\":true,\"shapeData\":null,\"uid\":8,\"presetAnim\":true,\"animID\":4294967295,\"sequenceIndex\":0,\"meshType\":\"plane\",\"videoProps\":{\"hslSaturationRange\":0.8,\"highQ\":true,\"type\":\"Hold last frame\",\"chromaHue\":65280,\"hsvHueRange\":90,\"chroma\":false,\"delay\":0,\"hslBrightnessRange\":0.8,\"hslHue\":120},\"hotspot\":false,\"hiddenInView\":false,\"textureType\":\"IMAGE\",\"tlPosition\":0,\"assetDimension\":[512,362]}]}],\"share\":{\"in_global_default\":true,\"twitter\":\"twitter\",\"fb_global_default\":true,\"in_globalShare\":\"\",\"in_snap_default\":true,\"email\":\"email\",\"tw_global_default\":true,\"fb_snapShare\":\"\",\"share\":true,\"instagram\":\"instagram\",\"em_global_default\":true,\"tw_snapShare\":\"\",\"fb_globalShare\":\"\",\"fb_snap_default\":true,\"em_body_snapShare\":\"\",\"tw_globalShare\":\"\",\"tw_snap_default\":true,\"em_subj_snapShare\":\"\",\"em_body_globalShare\":\"\",\"em_snap_default\":true,\"facebook\":\"facebook\",\"in_snapShare\":\"\",\"em_subj_globalShare\":\"\"},\"name\":\"\",\"peel\":{\"peels\":true,\"type\":\"fit\",\"orient\":\"portrait\",\"scale\":75,\"dimensions\":{\"x\":800,\"y\":599,\"length\":999.400320192064},\"uid\":0,\"plist\":{\"peelParams\":\"orient=portrait, scale=75, type=fit, dx=0, dy=0, w=800, h=599\"},\"state\":{\"scale\":75,\"peels\":true,\"orient\":\"portrait\",\"type\":\"fit\"}},\"activeSceneIndex\":0,\"startup\":{},\"uid\":1,\"shareSettings\":{\"shareDefaultMessage\":true,\"photoDefaultMessage\":true,\"addToFavourites\":true,\"customShareMessage\":\"\",\"customPhotoMessage\":\"\",\"takePhoto\":true,\"shareBlipp\":true,\"sharePhoto\":true}}"}
    patch_method(context,url, payload)

def get_poll_data(context):
    url = urlparse.urljoin(context.config.userdata['bake_api_url'], "poll/{poll_id}").format(poll_id=context.poll_id)
    # get https://bake-env.dev.blippar.com/poll/568f7a3ebdd1c449a8000068
    get_method(context, url, user_role="blippar_admin")

def get_blipp_markerparams(context, blipp_id, blipp_version_id, type, user_role):
    '''
    HUB-112
    :param type: defines the type which we gave as input param on the scenario
    MarkerParams are attached to 4 different endpoints and we need to cover all.
    '''
    if type == "markeparams":
        url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/blipp/{blipp_id}/version/{blipp_version}/markerparams".format(blipp_id=str(blipp_id),blipp_version=str(blipp_version_id[0])))
    elif type == "version":
        url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/blipp/{blipp_id}/version/{blipp_version}?metadata=full".format(blipp_id=str(blipp_id),blipp_version=str(blipp_version_id[0])))
    elif type == "versions":
        url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/blipp/{blipp_id}/versions?metadata=full".format(blipp_id=str(blipp_id)))
    elif type == "metadata":
        url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/blipp/{blipp_id}?metadata=full".format(blipp_id=str(blipp_id)))
    get_method(context, url, user_role)
    print("Markerparams URL: ", url)
    return get_last_response(context).json()

def upload_video_to_transcoder(context, file_name, image_type, user_role):
    url = urlparse.urljoin(context.config.userdata['transcoder_api_url'], "/api/v1/transcoder/jobs")
    files = [['input_file', [file_name, open(os.path.join(os.getcwd(), 'videos', file_name), 'rb'), image_type]]]
    erase_last_response(context)
    get_bearer_token(context,user_role)

    #update_token(context, user_role)

    s = requests.Session()
    s.headers = context.config.userdata.get("bake_api_token")

    print('Running POST: '+url, "By role:", user_role)
    response = s.post(url, data=None, files=files, verify=VERIFY_SSL_CERT)
    assert response.status_code == 200 or response.status_code == 201, "Error, status code is {code}, expected 200 or 201. The error is {error}".format(code=response.status_code, error=response.text)
    set_api_response(context, response)

def poll_transcoder_job(context, job_id, user_role):
    url = urlparse.urljoin(context.config.userdata['transcoder_api_url'], "/api/v1/transcoder/jobs/{job_id}".format(job_id=job_id))
    get_method(context, url, user_role=user_role)
    return get_last_response(context).json()

def can_publish(context, blipp_id, user_role):
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], "api/blipp/{blipp_id}/canPublish".format(blipp_id=blipp_id))
    get_method(context, url, user_role=user_role)
    return get_last_response(context)

def perform_visual_search(context, image, role):
    url = urlparse.urljoin(context.config.userdata['reco_url'], "markerLookupV3")
    img_file = [['image_filename', [image, open(os.path.join(os.getcwd(), 'images', image), 'rb')]]]
    post_method(context, url, user_role=role, files=img_file, payload=None)
    return get_last_response(context)

def get_objects_from_search(context, text, type, role):
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], '/api/search'+text)
    get_method(context, url, role)
    objects = get_last_response(context).json()
    if type in objects:
        return objects.get(type)
    else:
        return None

def get_id_from_role(context, user_role):
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], "api/user")
    get_method(context, url, user_role=user_role)
    return get_last_response(context).json().get('Id')

def get_response_anonymous_call(context, endpoint):
    s = requests.Session()
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/{endpoint}").format(endpoint=endpoint)
    return requests.get(url)


# *****************************
# GIVEN STEPS
# *****************************

@Given('I delete the campaigns with the name {campaign_name} (API)')
def step(context, campaign_name):
    context.execute_steps(u"""when I delete the campaigns with the name {campaign_name} (API)""".\
                          format(campaign_name=campaign_name))


# *****************************
# WHEN STEPS
# *****************************

#objects: campaign, ads
@When('As {role} I delete the {object} with the name {name} (API)')
def step(context, role, object, name):
    try:
        if object.lower() == 'campaigns':
            campaigns = get_campaign_id_from_name(context, name)
            for campaign in campaigns:
                url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/campaign/{campaign_id}". \
                                       format(campaign_id=str(campaign)))
                print("Campaign to delete: ", url, "By role: ", role)
                delete_method(context, url, role, check_response_code=False)
        elif object.lower() == 'ads':
            ads = get_ad_id_from_name(context, name,role)
            if ads:
                for ad in ads:
                    url = urlparse.urljoin(context.config.userdata['ads_api_url'], "/api/v1/ads/{ad_id}". \
                                           format(ad_id=int(ad)))
                    print("Ad to delete: ", url, "By role: ", role)
                    delete_method(context, url, role, check_response_code=False)
            else:
                print("No ad found")
        else:
            assert False, "Error, invalid object type"
    except:
        print("No", object, name, " to delete")
        return

@When('I delete the {object} with the name {name} (API)')
def step(context, object, name):
    if object.lower() == 'campaigns' or object.lower() == 'ads':
        context.execute_steps(u"""When As blippar_admin I delete the {object} with the name {name} (API)"""\
                              .format(object=object, name=name))
    else:
        assert False, "Error, invalid object type"

@When('I create the campaign with the name {campaign_name} (API)')
def step(context, campaign_name):
    context.execute_steps(u"""When As blippar_admin I create the campaign with the name {campaign_name} (API)"""\
            .format(campaign_name=campaign_name))

@When('As {role} I create the campaign with the name {campaign_name} (API)')
def step(context, campaign_name, role):
    get_user_group(context,role)
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/group/{id}/campaign").format(id=context.user_group_id)
    payload = {"Name" : campaign_name, "GroupID" : int(context.user_group_id)}
    post_method(context, url, role, json.dumps(payload))

@When('I create the blipp type {blipp_type} with the name {blipp_name}, marker image {image_name} in the campaign {campaign_name} (API)')
def step(context, blipp_name, blipp_type, image_name, campaign_name):
    context.execute_steps(u"""When As blippar_admin I create the blipp type {blipp_type} with the name {blipp_name}, marker image {image_name} in the campaign {campaign_name} (API)"""\
                          .format(campaign_name=campaign_name, image_name=image_name, blipp_type=blipp_type, blipp_name=blipp_name))

# This is the old step used in most cases, for blipp builder type blipps
@When('As {role} I create the blipp type {blipp_type} with the name {blipp_name}, marker image {image_name} in the campaign {campaign_name} (API)')
def step(context, role, blipp_name, blipp_type, image_name, campaign_name):
    context.execute_steps(u"""When As {role} I create the blipp type {blipp_type} with the name {blipp_name}, using file {file} in the campaign {campaign_name} (API)"""\
            .format(role=role, blipp_type=blipp_type, blipp_name=blipp_name, file=image_name, campaign_name=campaign_name))

#General step for both kind of blipps. The idea is to use this step from now on.
@When('As {role} I create the blipp type {blipp_type} with the name {blipp_name}, using file {file} in the campaign {campaign_name} (API)')
def step(context, role, blipp_name, blipp_type, file, campaign_name):
    #If the campaign does not exists, then the campaign will be created.
    campaigns = get_campaign_id_from_name(context, campaign_name)
    if campaigns == []:
        context.execute_steps(u"""When As {role} I create the campaign with the name {campaign_name} (API)"""\
                .format(role=role, campaign_name=campaign_name))
        #context.execute_steps(u"""When I create the campaign with the name {campaign_name}""".format(campaign_name=campaign_name))
        campaigns = get_campaign_id_from_name(context, campaign_name)
    if blipp_type == "bespoke":
        blipp_type_id = 1
        type = 'bespoke'
        blipp_id = create_empty_blipp(context, campaigns[0], blipp_type_id, blipp_name, role).get('Id')
        create_blipp_version(context, blipp_id, type, role, blipp_file=file)
    if blipp_type == "bespoke country": #Hardcoded to publish in ARGENTINA
        blipp_type_id = 1
        type = 'bespoke_country'
        blipp_id = create_empty_blipp(context, campaigns[0], blipp_type_id, blipp_name, role).get('Id')
        create_blipp_version(context, blipp_id, type, role, blipp_file=file, country="AR")
    elif blipp_type == "blipp builder":
        blipp_type_id = 3
        type = 'builder_v2'
        blipp_id = create_empty_blipp(context, campaigns[0], blipp_type_id, blipp_name, role).get('Id')
        upload_marker = upload_marker_to_empty_blipp(context, blipp_id, file, role)
        blipp_version = create_blipp_version(context, blipp_id, type, role).get('Id')
        plist = create_blipp_plist(context, blipp_id, blipp_version, role)
    else:
        assert False, "Error, wrong blipp type provided"


#Actions: publish, unpublish, delete
@When('I {action} blipp with the name {blipp_name} in the campaign {campaign_name} (API)')
def step(context, action, blipp_name, campaign_name):
    context.execute_steps(u"""When As blippar_super_admin I {action} blipp with the name {blipp_name} in the campaign {campaign_name} (API)""".format(action=action, blipp_name=blipp_name, campaign_name=campaign_name))

@When('As {role} I {action} blipp with the name {blipp_name} in the campaign {campaign_name} (API)')
def step(context, role, action, blipp_name, campaign_name):
    campaign_id = get_campaign_id_from_name(context, campaign_name)
    blipps = get_blipps_from_campaign(context, campaign_id)
    for blipp in blipps:
        if blipp.get("Name") == blipp_name:
            blipp_id = blipp.get("Id")
            blipp_version_id = get_blipp_versions(context, blipp_id)[0]
            if action == "publish":
                publish_blipp(context, blipp_id, blipp_version_id, role)
            elif action == "unpublish":
                unpublish_blipp(context, blipp_id, blipp_version_id)
            elif action == "delete":
                url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/blipp/{blipp_id}").format(blipp_id=blipp_id)
                print("Blipp to delete:", url, "By role:", role)
                delete_method(context, url, role, check_response_code=False)
                time.sleep(0.2)
            else:
                assert False, "Error, wrong action provided to step. Valid options are: publish, unpublish, delete"

@when('I duplicate blipp {blipp_name} from campaign {campaign_name} into blipp {new_blipp_name} with marker image {image} (API)')
def step(context, blipp_name, campaign_name, new_blipp_name, image):
    campaign_id = get_campaign_id_from_name(context, campaign_name)
    source_blipp_id = get_blipp_id_from_name(context, blipp_name, campaign_id)
    duplicate_blippbuilder_blipp(context, source_blipp_id, new_blipp_name, image)

@when('I rename blipp {blipp_name} from campaign {campaign_name} into blipp {new_blipp_name} (API)')
def step(context, blipp_name, campaign_name, new_blipp_name):
    campaign_id = get_campaign_id_from_name(context, campaign_name)
    blipps = get_blipps_from_campaign(context, campaign_id, user_role="blippar_admin")
    for blipp in blipps:
        if blipp.get("Name") == blipp_name:
            source_blipp_id = blipp.get("Id")
            change_blipp_info(context, source_blipp_id, new_blipp_name, role="blippar_admin")

@when('As {role} I rename blipp {blipp_name} from campaign {campaign_name} into blipp {new_blipp_name} (API)')
def step(context, blipp_name, campaign_name, new_blipp_name,role):
    campaign_id = get_campaign_id_from_name(context, campaign_name)
    blipps = get_blipps_from_campaign(context, campaign_id)
    for blipp in blipps:
        if blipp.get("Name") == blipp_name:
            source_blipp_id = blipp.get("Id")
            change_blipp_info(context, source_blipp_id, new_blipp_name, role)

@when('As {role} I rename campaign {campaign_name} into campaign {new_camp_name} (API)')
def step(context, campaign_name, new_camp_name,role):
    campaign_id = get_campaign_id_from_name(context, campaign_name)
    change_campaign_info(context, campaign_id, new_camp_name, role)

@When('I get the stat {stat} of the blipp {blipp_name} from the date {date_from} to the date {date_to} in the campaign {campaign_name} (API)')
def step(context, blipp_name, stat, date_from, date_to, campaign_name):
    campaign_id = get_campaign_id_from_name(context, campaign_name)
    blipp_id = get_blipp_id_from_name(context, blipp_name, campaign_id)
    if stat in ["interactions", "users", "locations"]:
        get_stats_from_blipp(context, blipp_id, stat, date_from, date_to)
    else:
        assert False, "Error blipp stat should be one of [interactions,users,locations]"

#If date="Now" then the current date/time will be used
#Check dictionaries in post_interaction helper methods for other parameters options like user and location
@When('I send {interactions} interactions to the blipp {blipp_name} from campaign {campaign_name} as user {user} from location {location} on date {timestamp} (API)')
def step(context, interactions, blipp_name, campaign_name, location, user, timestamp):
    campaign_id = get_campaign_id_from_name(context, campaign_name)
    blipps = get_blipps_from_campaign(context, campaign_id, user_role="blippar_admin")
    if timestamp == "Now":
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    for blipp in blipps:
        if blipp.get("Name") == blipp_name:
            post_interaction(context, interactions, blipp.get('Id'), location=location, user=user, timestamp=timestamp, check_response_code=True)


@When('I get the stat {stat} of the campaign {campaign_name} from the date {date_from} to the date {date_to} (API)')
def step(context, stat, date_from, date_to, campaign_name):
    campaign_id = get_campaign_id_from_name(context, campaign_name)
    if stat in ["interactions", "users", "locations"]:
        get_stats_from_campaign(context, campaign_id, stat, date_from, date_to)
    else:
        assert False, "Error campaign stat should be one of [interactions,users,locations]"

@When('I calculate Average_User_Interaction of the blipp {blipp_name} from the date {date_from} to the date {date_to} in the campaign {campaign_name} is {expected_avg} (API)')
def step(context, blipp_name, date_from, date_to, campaign_name, expected_avg):
    campaign_id = get_campaign_id_from_name(context, campaign_name)
    blipp_id = get_blipp_id_from_name(context, blipp_name, campaign_id)
    obtained_interactions = get_stats_from_blipp(context, blipp_id, "interactions", date_from, date_to).get('total')
    obtained_users = get_stats_from_blipp(context, blipp_id, "users", date_from, date_to).get('total')
    if obtained_users > 0:
        average_user_interaction = "%.2f" % (obtained_interactions / obtained_users)
        assert str(expected_avg) == str(average_user_interaction), "Error, expected {expected_avg} average, calculated: {calculated} in campaign {campaign_id}".format(expected_avg=expected_avg, calculated=average_user_interaction, campaign_id=campaign_id)
    else:
        assert False, "There are no users interacted with this blipp."

@When('As {role} I get the {link_type} shared stats {stat} of the campaign {campaign_name} from the date {date_from} to the date {date_to} (API)')
def step(context, role, link_type, campaign_name, stat, date_from, date_to):
    campaign_id = get_campaign_id_from_name(context, campaign_name)
    post_shared_stats_token(context, campaign_id, role)

    if link_type =="complete":
        get_shared_link(context, campaign_id, stat)

        context.execute_steps(u"""When I get the stat {stat} of the campaign {campaign_name} from the date {date_from} to the date {date_to} (API)""".\
                          format(stat=stat, campaign_name=campaign_name, date_from=date_from, date_to=date_to))
    else:
        get_shared_link(context, campaign_id, stat, bad_token=True)
        r=get_last_response(context)

@when(u'as {user} I get the api endpoint {endpoint}')
def step(context, user, endpoint):
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/{endpoint}").format(endpoint=endpoint)
    get_method(context, url, user, check_response_code=False)

@When('I {action} asset {asset_name} to blipp {blipp_name} in the campaign {campaign_name} (API)')
def step(context, campaign_name, blipp_name, asset_name, action):
    campaign_id = get_campaign_id_from_name(context, campaign_name)
    blipp_id = get_blipp_id_from_name(context, blipp_name, campaign_id)
    upload_asset_bb(context, asset_name)
    manage_bb_asset(context, blipp_id, action)
    return get_last_response(context).json()

@when('I get DetectMode {type} of the blipp {blipp_name} in the campaign {campaign_name} (API)')
def step(context, blipp_name, campaign_name, type):
    campaign_id = get_campaign_id_from_name(context, campaign_name)
    blipp_id = get_blipp_id_from_name(context, blipp_name, campaign_id)
    blipp_version_id = get_blipp_versions(context, blipp_id)
    get_blipp_markerparams(context, blipp_id, blipp_version_id, type, user_role="blippar_admin")

@when('I add predefined poll to blipp {blipp_name} in the campaign {campaign_name} (API)')
def step(context, blipp_name, campaign_name):
    campaign_id = get_campaign_id_from_name(context, campaign_name)
    blipp_id = get_blipp_id_from_name(context, blipp_name, campaign_id)
    add_bb_poll_to_blipp(context, blipp_id)

@when('I get poll data (API)')
def step(context):
    get_poll_data(context)

@when('as a {role} I upload the video {file_name}, type {type} to the transcoder service (API)')
def step(context, role, file_name, type):
    upload_video_to_transcoder(context, file_name, type, role)

@when('as a {role} I poll for the last started job until it is completed (API)')
def step(context, role, timeout=20):
    job_id = get_last_response(context).json().get('job_id')
    while timeout > 0:
        poll_response = poll_transcoder_job(context, job_id, role)
        status = poll_response.get('status')
        if status.lower() == "completed":
            break
        else:
            time.sleep(1)
            timeout -= 1
    assert timeout > 0, "Test failed, timeout reached. The final status of the job is {status}".format(status=status)

@When('As {role} I run canPublish for the blipp with the name {blipp_name} in campaign {campaign_name} (API)')
def step(context, role, blipp_name, campaign_name):
    campaign_id = get_campaign_id_from_name(context, campaign_name, role)
    blipp_id = get_blipp_id_from_name(context, blipp_name, campaign_id, role)
    can_publish(context, blipp_id, role)

@When('As {role} I run reco endpoint using image {image} (API)')
def step(context, role, image):
    perform_visual_search(context, image, role)

@When('As {role} I create and publish {blipps_quantity} blipps in the campaign {campaign} (API)')
def step(context, role, blipps_quantity, campaign):
    for blipp_no in range(int(blipps_quantity)):
        if blipp_no == int(blipps_quantity) - 1:
            blipp_name = 'last_blipp'
        else:
            blipp_name = "blipp_"+str(blipp_no)
        context.execute_steps(u"""When As {role} I create the blipp type bespoke country with the name {name}, using file assets/zip/blipp.zip in the campaign {campaign} (API)""".\
                            format(role=role, name=blipp_name, campaign=campaign))
        # context.execute_steps(u"""When As {role} I publish blipp with the name {blipp_name} in the campaign {campaign_name} (API)""".\
        #                     format(role=role, blipp_name=blipp_name, campaign_name=campaign))


@When('I get the permissions for the user that created campaign {campaign_name} and store them in {variable} (API)')
def step(context, campaign_name, variable):
    user_id = get_campaign_creator_user_id(context, campaign_name)
    permissions = get_user_permissions(context, user_id)
    context.config.userdata[variable] = permissions

@When('I get the user id for user with role {role} and I store it in {variable}')
def step(context, role, variable):
    user_id = get_id_from_role(context, role)
    context.config.userdata[variable] = user_id


@when('I {action} user {role} permission for Developer (Network & Custom JS) access (API)')
def step(context, action, role):
    user_id = get_id_from_role(context, role)
    url1 = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/user/{user_id}/role/48").format(user_id=user_id)
    url2 = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/user/{user_id}/role/49").format(user_id=user_id)
    if action =="Add":
        post_method(context, url1, user_role="blippar_admin", payload=None)
        post_method(context, url2, user_role="blippar_admin", payload=None)
    elif action == "Revoke":
        delete_method(context, url1, user_role="blippar_admin")
        delete_method(context, url2, user_role="blippar_admin")
    else:
        assert False, "Wrong action provided. Need Add/Revoke"

# *****************************
# THEN STEPS
# *****************************

@Then ('I check that response code is {status}')
def step(context, status):
    r = get_last_response(context)
    assert str(r.status_code) == str(status) , "The status code is incorrect. Expected {expected}, received {obtained}".format(expected=status, obtained=r.status_code)


@Then('I check that the status of the blipp {blipp_name} in the campaign {campaign_name} is {status} (API)')
def step(context, blipp_name, campaign_name, status):
    campaign_id = get_campaign_id_from_name(context, campaign_name)
    blipps = get_blipps_from_campaign(context, campaign_id,user_role="blippar_admin")
    for blipp in blipps:
        if blipp.get("Name") == blipp_name:
            if blipp.get("Status") == status:
                assert True
                return
            else:
                assert False, "The status of the blipp is not the expected. Expected: {status}, observed: {observed}".format(expected=status, observed=blipp.get("Status"))
    assert False, "Error, blipp not found"

@Then('the number of total interactions is {interactions} (API)')
def step(context, interactions):
   response = get_last_response(context).json()
   if "interactions" in response:
       #that's the campaign case where total belongs to interactions
       obtained_interactions = response.get('interactions').get('total')
   else:
       obtained_interactions = response.get('total')
   assert str(obtained_interactions) == str(interactions), "Error, interactions expected {expected}, obtained: {obtained}".format(expected=interactions, obtained=obtained_interactions)

@Then('the number of total unique users is {users} (API)')
def step(context, users):
   response = get_last_response(context).json()
   obtained_users = response.get('total')
   assert str(obtained_users) == str(users), "Error, unique users expected {expected}, obtained: {obtained}".format(expected=users, obtained=obtained_users)

@then('I check that the campaign with the name {campaign_name} is {state} (API)')
def step(context, campaign_name, state):
    campaign_id = get_campaign_id_from_name(context, campaign_name, include_deleted=True)#[-1:] # get last campaign
    url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/campaign/{campaign_id}?".format(campaign_id=str(campaign_id[0])))
    get_method(context, url, user_role="blippar_admin")
    response = get_last_response(context).json()
    if state == "present":
        assert response.get('Deleted') == 0, "Error! Not present. Found {real_response} instead".format(real_response = response)
    elif state == "not present":
        assert response.get('Deleted') == 1, "Hmm, campaign is not deleted! Found {real_response} instead".format(real_response = response)
    else:
        assert False, "Error, wrong action provided to step. Valid options are: present / not present"

@then('I check that the blipp {blipp_name} in the campaign {campaign_name} is {state} (API)')
def step(context, blipp_name, campaign_name, state):
    campaign_id = get_campaign_id_from_name(context, campaign_name)
    blipps = get_blipps_from_campaign(context, campaign_id, user_role="blippar_admin")
    for blipp in blipps:
        if blipp.get("Name") == blipp_name:
            url = urlparse.urljoin(context.config.userdata['hub_api_url'], "/api/blipp/{blipp_id}?".format(blipp_id=str(blipp.get('Id'))))
            get_method(context, url, user_role="blippar_admin")
            response = get_last_response(context).json()
            if state == "present":
                assert response.get('Status') == "NOT_LIVE", "Error! Not Live. Found {real_response} instead".format(real_response = response)
            elif state == "not present":
                assert response.get('Status') == "DELETED", "Hmm, blipp is not deleted! Found {real_response} instead".format(real_response = response)
            else:
                assert False, "Error, wrong action provided to step. Valid options are: present / not present"


@Then('The Location is {location} with {interactions} interactions (API)')
def step(context, location, interactions):
    coordinates = LOCATIONS.get(location)
    obtained_interactions = get_last_response(context).json().get(coordinates)
    assert str(obtained_interactions) == str(interactions), "The obtained interactions {obtained} are not the expected {expected} for the specified location".format(obtained=str(obtained_interactions), expected=str(interactions))


@then('The number of total interactions for hour {hour} is {interactions} (API)')
def step(context, hour, interactions):
    response = get_last_response(context).json()
    obtained_interactions = response.get('hourly').get(str(hour))
    assert str(obtained_interactions) == str(interactions), "The obtained interactions {obtained} are not the expected {expected} for the specified hour".format(obtained=str(obtained_interactions), expected=str(interactions))

@then('The number of total interactions for day {day} is {interactions} (API)')
def step(context, day, interactions):
    response = get_last_response(context).json()
    obtained_interactions = response.get('daily').get(day)
    assert str(obtained_interactions) == str(interactions), "The obtained interactions {obtained} are not the expected {expected} for the specified hour".format(obtained=str(obtained_interactions), expected=str(interactions))

@Then('The number of unique users for hour {hour} is {users} (API)')
def step(context, hour, users):
   response = get_last_response(context).json()
   obtained_users = response.get('hourly').get(str(hour))
   assert str(obtained_users) == str(users), "Error, unique users expected for hour {expected}, obtained: {obtained}".format(expected=users, obtained=obtained_users)

@Then('The number of unique users for day {day} is {users} (API)')
def step(context, day, users):
   response = get_last_response(context).json()
   obtained_users = response.get('daily').get(day)  #(str(day))
   assert str(obtained_users) == str(users), "Error, unique users expected for day {expected}, obtained: {obtained}".format(expected=users, obtained=obtained_users)


@Then('response should contain {options} (API)')
def step(context, options):
    '''
     use regular expression and search on the response string
    '''
    r = get_last_response(context).json()
    options_list = options.split(",")
    for option in options_list:
        if re.search(option, json.dumps(r)):
            assert True
        else:
            assert False,"There is no match in response.Expected {expected}, obtained {obtained}".format(expected=options_list, obtained=str(r))

@Then('the status of the transcoder job is {status} (API)')
def step(context, status):
    obtained_status = get_last_response(context).json().get('status')
    assert obtained_status.lower() == status.lower(), "Wrong status. Expected: {expected}, observed: {observed}".format(expected=status, observed=obtained_status)

@Then('the output with key {key} is present (API)')
def step(context, key):
    output_list = get_last_response(context).json().get('outputs')
    for output in output_list:
        if output.get('key') == key:
            assert output.get('preset_id') != [], "Test failed, no preset id in key {key}".format(key=key)
            assert output.get('status') == "Complete", "Test failed, the status of the output with key {key} is not Completed".format(key=key)
            assert output.get('url') != [], "Test failed, no url in output with key {key}".format(key=key)
            return
    assert False, "Test failed, the output with key {key} was not found".format(key=key)

@Then('The playlist with name {name} is present (API)')
def step(context, name):
    playlists = get_last_response(context).json().get('playlists')
    for playlist in playlists:
        if playlist.get('name') == name:
            return
    assert False, "Test failed, the playlist with name {name} was not found".format(name=name)

#options: returns, does not return
@Then('I check that the reco endpoint {expected} a response (API)')
def step(context, expected):
    last_response = get_last_response(context)
    if expected == 'returns' and last_response.text == "":
        assert False, "Test failed, the endpoint does not contain any response"
    elif expected == 'does not return' and last_response.text != "":
        assert False, "Test failed, the endpoint contain a response"
    else:
        assert True

@Then('I check that coverimage and plist values matches with the blipp with the name {blipp_name} in the campaign {campaign_name} (API)')
def step(context, blipp_name, campaign_name):
    headers = get_last_response(context).headers
    campaign_id = get_campaign_id_from_name(context, campaign_name)

    blipp_id = get_blipp_id_from_name(context, blipp_name, campaign_id)
    blipp_cover_image_id = get_blipp_full_data_from_id(context, blipp_id, 'blippar_admin').get('CoverImageId')
    blipp_plist_id = get_blipp_full_data_from_id(context, blipp_id, 'blippar_admin').get('LastPlistId')
    reco_cover_image_id = headers.get('Blippableid')
    reco_plist_id = headers.get('Blippdefid')

    assert str(reco_cover_image_id).find(str(blipp_cover_image_id)) != -1, "Test failed: Expected cover image id {expected}, obtained {obtained}".format(expected=str(blipp_cover_image_id), obtained=str(reco_cover_image_id))
    assert str(reco_plist_id).find(str(blipp_plist_id)) != -1, "Test failed: Expected plist id {expected}, obtained {obtained}". format(expected=str(blipp_plist_id), obtained=str(reco_plist_id))


@Then('the response to the anonymous call to {endpoint} contains {options}')
def step(context, options, endpoint):

    r = get_response_anonymous_call(context, endpoint)

    options_list = options.split(",")
    for option in options_list:
        if re.search(option, r.text):
            assert True
        else:
            assert False, "There is no match in response.Expected {expected}, obtained {obtained}".format(
                expected=options_list, obtained=str(r))