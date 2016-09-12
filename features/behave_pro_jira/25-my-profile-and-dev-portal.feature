@STATS_HUB_UI
Feature: My Profile and Dev Portal

 
  @HUB-837 @assignee:gergana.ivanova @COMPLETED @MY_PROFILE
  Scenario: Checking My Profile link on top right menu

    #As a user I would like to change my details so they are kept up to date
    Given I am logged in as a normal_user_2 user
    When I click on My account in the dropdown top right menu
    And I switch to next browser window
    Then the page title must be User Profile


  @HUB-837 @assignee:gergana.ivanova @COMPLETED @MY_PROFILE
  Scenario: Checking My Profile fields

    Given I am logged in as a normal_user user
    When I Revoke user normal_user_2 permission for Developer (Network & Custom JS) access (API)
    When I click on My account in the dropdown top right menu
    And I switch to next browser window
    Then the page title must be User Profile
    Then they will see user first name, surname, Change password and Show me how links


  @HUB-1236 @assignee:bogdan.leseyko @OPEN @MY_PROFILE
  Scenario: My Profile - validation

    Given I am logged in as a normal_user_2 user
    When the user is on the My profile page
    When the user deletes name and surname
    Then errors You did not enter your first name and You did not enter your surname are displayed


  @ORPHAN @MY_PROFILE
  Scenario: My Profile - subscribe for newsletters

    Given I am logged in as a normal_user_2 user
    When the user is on the My profile page
    When the users checks newsletter checkbox
    And the user clicks Save button
    Then the user sees Your profile updated.


  @HUB-1244 @HUB-840 @assignee:gergana.ivanova @OPEN @MY_PROFILE
  Scenario: My Profile - Change Password link

    #This test fails due to the bug #1244
    Given I am logged in as a normal_user user
    When the user is on the My profile page
    When click in link with text Change password
    Then the modal window with text Change your password is displayed
    When the user types the old password blippar1
    And the user enters the new password blippar22
    And the user confirms the new password blippar22
    When the user saves changes
    Then the user sees Your password has been changed.
    #restoring the old password
    #Given the user is on the My profile page
    When click in link with text Change password
    Then the modal window with text Change your password is displayed
    When the user types the old password blippar22
    And the user enters the new password blippar22
    And the user confirms the new password blippar1
    When the user clicks Save button
    Then the user sees Your password has been changed.


  @ORPHAN @MY_PROFILE
  Scenario Outline: My Profile - Change Password errors

    Given I am logged in as a normal_user user
    When the user is on the My profile page
    When click in link with text Change password
    Then the modal window with text Change your password is displayed
    When the user types the old password <password1>
    And the user enters the new password <password2>
    And the user confirms the new password <password2>
    When the user saves changes
    Then the user sees <expected_response>
    
     Examples:
      |password1   |password2  |expected_response                                 |
      |blippar567  |blip1234   |Invalid password                                  |
      |blippar1    |blip123    |Please enter a longer password                    |
      |blippar1    |123456781  |This password is entirely numeric.                |
      |blippar     |blippar    |You’ll need at least 8 characters in your password|
      |blippar1    |empty value|You can’t leave this empty                        |
      |empty value |blip4555   |You can’t leave this empty                        |


  @HUB-933 @WIP @MY_PROFILE
  Scenario: Developer network - existing user signs up to the developer network

    Given I am logged in as a normal_user_2 user
    When I Revoke user normal_user_2 permission for Developer (Network & Custom JS) access (API)
    When the user is on the My profile page
    When click in link with text Show me how
    Then the modal window with text Join the Blippar Development Program is displayed


  @HUB-933 @WIP @MY_PROFILE
  Scenario: Developer network - Developer Portal non-member

    Given I am logged in as a normal_user_2 user
    When I Revoke user normal_user_2 permission for Developer (Network & Custom JS) access (API)
    When the user is on the My profile page
    When click in link with text Show me how
    Then the modal window with text Join the Blippar Development Program is displayed
    When click in link with text Visit the BDN homepage
    And I switch to next browser window
    Then the user is logged into the Dev Portal started with text 'Create your own'
    And the page title must be Index | Blippar Developers


  @HUB-933 @WIP @MY_PROFILE
  Scenario: Developer network - enroll in Developer Portal  as member

    Given I am logged in as a normal_user_2 user
    When I Revoke user normal_user_2 permission for Developer (Network & Custom JS) access (API)
    When the user is on the My profile page
    When click in link with text Show me how
    Then the modal window with text Join the Blippar Development Program is displayed
    When click on Count me in
    Then they are signed up to the developer network and the text I am a Blipp developer is shown


  @HUB-933 @WIP @MY_PROFILE
  Scenario: Developer network - Developer Portal login as a member

    Given I am logged in as a normal_user_2 user
    When I Revoke user normal_user_2 permission for Developer (Network & Custom JS) access (API)
    When the user is on the My profile page
    When click in link with text Show me how
    Then the modal window with text Join the Blippar Development Program is displayed
    When click on Count me in
    Then they are signed up to the developer network and the text I am a Blipp developer is shown
    When click in link with text Go to the BDN webpage
    #And I switch to next tab
    #now it is opened in the same tab in automated run - bug? Also My Campaigns page is open instead expected page, weird as I can't reproduce it manually
    Then the user is logged into the Dev Portal started with text 'Create your own'
    And ending with text 'augmented reality experiences'
    And the page title must be Index | Blippar Developers


  @ORPHAN
  Scenario: Developer network - if the user is Developer Portal member, he can create a 'Custom - Javascript' blipp

    Given I am logged in as a normal_user_2 user
    When I Revoke user normal_user_2 permission for Developer (Network & Custom JS) access (API)
    When the user is on the My profile page
    When click in link with text Show me how
    Then the modal window with text Join the Blippar Development Program is displayed
    When click on Count me in
    Then they are signed up to the developer network and the text I am a Blipp developer is shown
    When click in link with text Go to the BDN webpage
    And I switch to next browser window
    Then the user is logged into the Dev Portal started with text 'Create your own'
    And ending with text 'augmented reality experiences'
    And the page title must be Index | Blippar Developers
    #Login to hub
    When they create a campaign in Hub
    Then they will see the option to create a 'Custom - Javascript' blipp 


  @ORPHAN @MY_PROFILE
  Scenario: Developer network - Developer Portal checking API documentation

    Given I am logged in as a normal_user_2 user
    When I Revoke user normal_user_2 permission for Developer (Network & Custom JS) access (API)
    When the user is on the My profile page
    When click in link with text Show me how
    Then the modal window with text Join the Blippar Development Program is displayed
    When click on Count me in
    Then they are signed up to the developer network and the text I am a Blipp developer is shown
    When click in link with text Visit the API documentation
    And I switch to next browser window
    Then the user is logged into the API page started with text 'Introduction'
    And the page title must be Api | Blippar Developers


  @ORPHAN @MY_PROFILE
  Scenario: Developer Network - assign 'Developer Network' permissions to an individual user in a group

    Given I am logged in as a blippar_admin user
    Then the user Blippar Admin is logged in
    When I go to My campaigns
    When navigating to Groups & Users
    Then the Groups overview is loaded
    When I select the group BLIPP_ALL_TEST
    And I click on the users tab
    And filtering by testit11
    When I Add access to Developer (Network & Custom JS) on group or user level
    When I login with user testit11@abv.bg and password gerg456ivan
    When I click on My account in the dropdown top right menu
    When I switch to next browser window
    When click in link with text Go to the BDN webpage
    When I switch to next browser window
    Then the user is logged into the Dev Portal started with text 'Create your own'
    And ending with text 'augmented reality experiences'
    #Restoring test initial state
    Given I am logged in as a blippar_admin user
    Then the user Blippar Admin is logged in
    When I go to My campaigns
    When navigating to Groups & Users
    Then the Groups overview is loaded
    When I select the group BLIPP_ALL_TEST
    And I click on the users tab
    And filtering by testit11
    When I Revoke access to Developer (Network & Custom JS) on group or user level

