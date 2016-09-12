Feature: New creation tools

 
  @HUB-822 @HUB-869 @assignee:gergana.ivanova @version:tool-chooser @COMPLETED @GROUPS_AND_USERS
  Scenario Outline: Set group permissions: new group

    Given I am logged in as a blippar_admin user
    When All emails are deleted from test account
    #Creating a group
    And  navigating to Groups & Users
    Then the Groups overview is loaded
    When I click on the New Group button
    Then the create new group modal is visible
    When filling out the new group form with the group name BEHAVE TEST GROUP PERMISSIONS
    And  I set BlippBuilder (Classic) checkbox <bb_classic_set>
    And  I set BlippBuilder (New) checkbox <bb_new_set>
    And  I set Custom (JavaScript) checkbox <javascript_set>
    Then the submit button is clickable
    When I click on the modal submit button
    Then a group is created with the group name BEHAVE TEST GROUP PERMISSIONS
    #Creating a new managed user
    #When I click on the users tab
    When I create a new user trying any of the buttons
    Then the create new user modal is visible
    When a new email alias is generated using the base account email.auto.blippar.hub@gmail.com and stored in the global variable GENERATED_EMAIL_ALIAS
    And  creating a user with first name GROUP_PERMISSIONS_TEST and last name USER and email from global var GENERATED_EMAIL_ALIAS
    Then the submit button is clickable
    When I click on the modal submit button
    Then a user is created with first name GROUP_PERMISSIONS_TEST and last name USER
    When I logout
    #Activating this newly created user account
    And the activation link is obtained from the email received and it is opened
    And the user activates the managed account setting password layar123 and confirmation layar123
    And the user submits the form
    Then Account activated screen is opened
    When clicks the 'Get Started' link
    Then the user GROUP_PERMISSIONS_TEST USER is logged in
    When I go to My Campaigns
    And  I create the campaign with the name CAMPAIGN_TEST_GROUP_PERMISSIONS
    Then the screen CAMPAIGN_TEST_GROUP_PERMISSIONS is opened
    And  the options for blipp creations are <blipp_options>
       Examples:
              | bb_classic_set| bb_new_set | javascript_set|  blipp_options       |
              |      enabled  |  enabled   |  enabled      |  bb_classic,bb_new,js|
              |      enabled  |  disabled  |  disabled     |  bb_classic          |
              |      disabled |  enabled   |  disabled     |  bb_new              |
              |      disabled |  disabled  |  enabled      |  js                  |


  @HUB-869 @assignee:gergana.ivanova @version:tool-chooser @COMPLETED @AUTOMATABLE @GROUPS_AND_USERS
  Scenario Outline: Set group permissions: update group settings

    Given I am logged in as a blippar_admin user
    When navigating to Groups & Users
    Then the Groups overview is loaded
    When I open the group TEST_UPDATE_GROUP_NEW_TOOLS for edition
    #When I click on the users tab
    #When filtering by testit14
    #When I open the group shown
    #When I click on the edit group button
    And I set BlippBuilder (Classic) checkbox <bb_classic_set>
    And I set BlippBuilder (New) checkbox <bb_new_set>
    And I set Custom (JavaScript) checkbox <javascript_set>
    Then the submit button is clickable
    When I click on the modal submit button
    Then a group is updated
    When I login with user testit14@abv.bg and password gerg456ivan
    When I go to My Campaigns
    And I create the campaign with the name CAMPAIGN_TEST
    Then the options for blipp creations are <blipp_options>
        
    Examples:
          | bb_classic_set| bb_new_set | javascript_set|  blipp_options       |
          |      enabled  |  enabled   |  enabled      |  bb_classic,bb_new,js|
          |      enabled  |  disabled  |  disabled     |  Create a blipp      |
          |      disabled |  enabled   |  disabled     |  Create a blipp      |
          |      disabled |  disabled  |  enabled      |  Create a blipp      |


  @HUB-823 @HUB-870 @assignee:gergana.ivanova @assignee:juanmoschino @version:tool-chooser @COMPLETED @GROUPS_AND_USERS
  Scenario Outline: Check the tools available depending on user permissions

    When I login with user auto.blippar@gmail.com and password blippar1
    Then the user Blippar Admin is logged in
    When navigating to Groups & Users
    Then the Groups overview is loaded
    When I select the group TEST_UPDATE_GROUP_NEW_TOOLS
    When I click on the users tab
    When filtering by shyukri.shyukriev
    And I revoke access to all tools for user shyukri
    Then I check that the user has all tools revoked
    When I <bb_classic_set> access to BlippBuilder (Classic) on group or user level
    And I <bb_new_set> access to BlippBuilder (New) on group or user level
    And I <javascript_set> access to Custom (JavaScript) on group or user level
    When I login with user shyukri.shyukriev+new_tools@blippar.com and password layar123
    When I go to My Campaigns
    When I open the campaign with the name CAMPAIGN_TO_EDIT
    #bb_classic acces is set during Group creation, so it can't be revoked!
    Then the options for blipp creations are <blipp_options>
    	Examples:
             | bb_classic_set| bb_new_set| javascript_set|    blipp_options       |
             |      Add      |  Add      |  Add          |  bb_classic,bb_new,js  |
             |      Revoke   |  Revoke   |  Revoke       |  bb_classic            |
             |      Add      |  Revoke   |  Revoke       |  bb_classic            |
             |      Revoke   |  Add      |  Revoke       |  bb_new,bb_classic     |
             |      Revoke   |  Revoke   |  Add          |  js,bb_classic         |


  @ORPHAN @GROUPS_AND_USERS
  Scenario Outline: Match user permissions in API with blipp creation options in UI

    Given I delete the campaigns with the name <campaign_name> (API)
    When As <role> I create the campaign with the name <campaign_name> (API)
    Given I am logged in as a <role> user
    When  I go to My Campaigns
    Then The screen My campaigns is opened
    When I open the campaign with the name <campaign_name>
    Then The screen <campaign_name> is opened
    When I get the permissions for the user that created campaign <campaign_name> and store them in USER_PERMS (API)
    Then I check that the options for blipp creation are correct according to the permissions in USER_PERMS
    Examples:
          | role          | campaign_name                          |
          | blippar_admin |BEHAVE_RANDOM_BLIPP_CHECK_BLIPPAR_ADMIN |
          | blippar_user  |BEHAVE_RANDOM_BLIPP_CHECK_BLIPPAR_USER  |
          | group_admin   |BEHAVE_RANDOM_BLIPP_CHECK_GROUP_ADMIN   |
          | normal_user   |BEHAVE_RANDOM_BLIPP_CHECK_NORMAL_USER   |

