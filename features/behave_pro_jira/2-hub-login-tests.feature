Feature: Hub login tests

  
  Login UI HUB tests to verify permissions with different users. The tests are written in selenium.
  Tests tagged as HUB will be executed daily by jenkins jobs.

 
  @ORPHAN @LOGIN
  Scenario: Login as blippar admin and verify side menu visualization

    When I login with user auto.blippar@gmail.com and password blippar1
    Then the user Blippar Admin is logged in
    Then the options in the side menu are My Campaigns,Group Campaigns,All Campaigns,Groups & Users,Approvals,Manage Advertisements,App


  @ORPHAN @LOGIN
  Scenario: Login as blippar user and verify side menu visualization

    When I login with user auto.blippar+blippar_user1@gmail.com and password blippar1
    Then the user Blippar User is logged in
    Then the options in the side menu are My Campaigns,Group Campaigns,All Campaigns,Groups & Users,Approvals


  @ORPHAN @LOGIN
  Scenario: Login as group admin and verify side menu visualization

    When I login with user auto.blippar+group_admin@gmail.com and password blippar1
    Then the user Blippar GroupAdmin is logged in
    Then the options in the side menu are My Campaigns,Group Campaigns,Manage users


  @ORPHAN @LOGIN
  Scenario: Login as normal user and verify side menu visualization

    When I login with user auto.blippar+group_user@gmail.com and password blippar1
    Then the user Hub GroupUser is logged in
    Then the options in the side menu are My Campaigns
    When I go to My Campaigns
    Then The screen My campaigns is opened
    Then I check all campaigns under My Campaigns are created by Hub GroupUser


  @ORPHAN @LOGIN @PRODUCTION_EXCLUDED
  Scenario: Login as blippar Super admin and verify side menu visualization

    When I login with user auto.blippar+superadmin@gmail.com and password blippar1
    Then The user Blippar Super_Admin is logged in
    Then the options in the side menu are My Campaigns,Group Campaigns,All Campaigns,Groups & Users,Approvals,Manage Advertisements,Permissions,Tools,Connect,App


  @HUB-665 @assignee:ben.dalby @COMPLETED @LOGIN
  Scenario: Login with valid credentials and logout

    When I login with user auto.blippar@gmail.com and password blippar1
    Then The user Blippar Admin is logged in
    When the logout option is selected in user dropdown menu
    Then Log out screen is opened
    When the user clicks in LOGOUT button
    Then Log in to your Blippar account screen is opened


  @HUB-665 @assignee:ben.dalby @COMPLETED @LOGIN
  Scenario: Cancel logout

    When I login with user auto.blippar@gmail.com and password blippar1
    Then The user Blippar Admin is logged in
    When  the logout option is selected in user dropdown menu
    Then  the logout confirmation message is opened
    When  the user clicks in STAY LOGGED IN button
    Then  the user Blippar Admin is logged in

