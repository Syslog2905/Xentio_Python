from behave_base_lib.environment_helpers import before_all, before_feature, before_scenario, after_scenario, after_step, after_feature, after_all
try:
    import urllib3.contrib.pyopenssl
    urllib3.contrib.pyopenssl.inject_into_urllib3()
except ImportError:
    pass

#These are used steps.bake_api
USERS = {'blippar_super_admin' :{'email':'auto.blippar+superadmin@gmail.com', 'password' : 'blippar1', 'role' : 'Super Admin'},
        'blippar_admin' :{'email' :'auto.blippar@gmail.com', 'password' : 'blippar1', 'role' : 'Blippar Admin'},
         'blippar_admin2':{'email' : 'juan.moschino+blippar_admin@blippar.com', 'password' : 'layar123'},
         'blippar_user' :{'email' :'auto.blippar+blippar_user1@gmail.com', 'password': 'blippar1'},
         'group_admin' :{'email' :'auto.blippar+group_admin@gmail.com', 'password': 'blippar1'},
         'normal_user' :{'email' :'auto.blippar+group_user@gmail.com', 'password': 'layar123'},
         'normal_user_2' :{'email' :'evelin3933@gmail.com', 'password': 'gerg456ivaN'},#this user can not publish her blipps but pending group admin approval to publish
         'blippar_user2':{'email':'shyukri.shyukriev+blippar_user2@blippar.com', 'password':'blippar1'},
         'group_admin2' :{'email' :'shyukri.shyukriev+normal_user2@blippar.com', 'password': 'blippar1'},
         'normal_user3' :{'email' :'shyukri.shyukriev+normal_user3@blippar.com', 'password': 'blippar1'},
         'basic_user' :{'email':'juan.moschino+basic_user@blippar.com', 'password':'layar123'},
         'pro_user_no_credit' :{'email' :'juan.moschino+pro_user_no_credit@blippar.com', 'password': 'layar123'},
         'basic_user_no_credit' :{'email' :'juan.moschino+basic_user_no_credit2@blippar.com', 'password': 'layar123'},
         'bdn_membership_check_user' :{'email' :'juan.moschino+bdn_membership_check@blippar.com', 'password': 'layar123'},
}

LOCATIONS = {"Amsterdam": "52.3657,4.8931", "London": "51.5074,0.1278", "Sofia": "42.6954,23.3239", "Buenos Aires": "-34.6158,-58.4333", "San Francisco" : "37.7749,122.419", "Mountain View" :"37.3861,122.083", "Los Angeles" :"34.0522,118.243", "Tokyo" :"35.6895,139.691", "Istanbul" :"41.0082,28.978", "New Delhi":"28.4595,77.026", "Mumbai" : "19.076,72.877","Chennai" : "13.0827,80.27","Bangalore" : "12.9716,77.594"}
INTERACTION_USERS = {"user1": 'gqoohlake41qw3cw91jhfemhambj5g6zmgwguvyl', "user2": 'gqoohlake41qw3cw91jhfemhambj5g6zmgwguvye', "user3": 'gqoohlake41qw3cw91jhfemhambj5g6zmgwguvya'}

OAUTH_URL = 'https://alpha-accounts.dev.blippar.com/'
CLIENT_IDS = {"https://ams1-hub.dev.blippar.com" : "4253511319",
              "https://alpha-hub.dev.blippar.com" : "3157877802",
              "https://sf-qa-hub.dev.blippar.com" : "2142314324",
              "https://hub-qa.dev.blippar.com": "2111",
              "https://hub.dev.blippar.com": "1111"}

             # "https://alpha-hub.dev.blippar.com" : "3898562509"}

#Email account to use with gmail_client
EMAIL_ACCOUNT= {'email': 'email.auto.blippar.hub@gmail.com', 'password': 'dduqicyqpqferfdo'}
