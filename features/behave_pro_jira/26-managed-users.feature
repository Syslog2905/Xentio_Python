Feature: Managed users

 
  @ORPHAN @AUTOMATABLE
  Scenario: Managed users: Sending of moderation notification for blipp publishing approval to the account manager

    
    #Login with a managed user
    When I login with user auto.blippar+group_user@gmail.com and password blippar1
    Then The user Hub GroupUser is logged in
    Then The screen My campaigns is opened
    When I delete the campaign APPROVAL_CAMPAIGN
    Then I check that there are not campaigns cards with the name APPROVAL_CAMPAIGN
    #Campaign and blipp creation
        When I create the campaign with the name APPROVAL_CAMPAIGN
        When I click on Create Blipp default button
        Then The modal Create new blipp is opened
        When Creating my blipp I give it the name APPROVAL_BLIPP
        When Creating my blipp I upload the marker flowers.jpg
        And I click in back button from blippbuilder
        Then I check that the blipp with the name APPROVAL_BLIPP is created
        When I go to Blipp Detail APPROVAL_BLIPP page
        Then I check that the status of the blipp APPROVAL_BLIPP detail page is PROCESSED (UI)
    #Need step to publish but it's too tricky
    # Steps to check admin email notificaion - we have a bug here now


  @ORPHAN @AUTOMATABLE
  Scenario: Managed users: Login as group admin and check publishing approval pending blipp from the previous scenario

    When I login with user auto.blippar@gmail.com and password blippar1
    Then The user Blippar Admin is logged in
    When navigating to Groups & Users
    When I click on Approvals on the left sidebar
    Then I check that the blipp with the name APPROVAL_BLIPP is there (UI)
    And I check that the status of the blipp APPROVAL_BLIPP detail page is APPROVAL (UI)


  @ORPHAN @GROUPS_AND_USERS
  Scenario: Managed users: Login as SuperAdmin and approves  a pending blipp

    #When I login with user gergana.ivanova@blippar.com and password gerg456ivan
    #Then The user Gerry Ivanova is logged in
    When I login with user auto.blippar@gmail.com and password blippar1
    Then The user Blippar Admin is logged in
    When navigating to Groups & Users
    When I click on Approvals on the left sidebar
    Then I check that the blipp with the name APPROVAL_BLIPP is there (UI)
    And I check that the status of the blipp APPROVAL_BLIPP detail page is APPROVAL (UI)
    Then admin sets checkbox blipp APPROVAL_BLIPP enabled
    And I check that the status of the blipp APPROVAL_BLIPP detail page is PROCESSED (UI)
    When I click on Approvals on the left sidebar
    Then admin sets checkbox blipp APPROVAL_BLIPP enabled


  @HUB-654 @assignee:juanmoschino @version:accounts-critical @COMPLETED @GROUPS_AND_USERS @PRODUCTION_CHECK
  Scenario: Managed users: Creation and activation of a managed user, valid token

    When All emails are deleted from test account
    And  navigating to Groups & Users
    #Creating a new group
    Then the Groups overview is loaded
    When I click on the New Group button
    Then the create new group modal is visible
    When filling out the new group form with the group name BEHAVE TEST
    And  I set BlippBuilder (Classic) checkbox enabled
    Then the submit button is clickable
    When I click on the modal submit button
    Then a group is created with the group name BEHAVE TEST
    #Generating and creation of new gmail user
    When I click on the users tab
    And  I create a new user trying any of the buttons
    Then the create new user modal is visible
    When a new email alias is generated using the base account email.auto.blippar.hub@gmail.com and stored in the global variable GENERATED_EMAIL_ALIAS
    And  creating a user with first name MANAGED and last name USER and email from global var GENERATED_EMAIL_ALIAS
    Then the submit button is clickable
    When I click on the modal submit button
    Then a user is created with first name MANAGED and last name USER
    When I logout
    And the activation link is obtained from the email received and it is opened
    And the user activates the managed account setting password layar123 and confirmation layar123
    And the user submits the form
    #Activation of the user account
    Then Account activated screen is opened
    When clicks the 'Get Started' link
    Then the user MANAGED USER is logged in


  @HUB-653 @assignee:juanmoschino @version:accounts-critical @COMPLETED @GROUPS_AND_USERS
  Scenario: Managed users: Creation and activation of a managed user, invalid token

    When All emails are deleted from test account
    And  navigating to Groups & Users
    #Creating a new group
    Then the Groups overview is loaded
    When I click on the New Group button
    Then the create new group modal is visible
    When filling out the new group form with the group name BEHAVE TEST
    And  I set BlippBuilder (Classic) checkbox enabled
    Then the submit button is clickable
    When I click on the modal submit button
    Then a group is created with the group name BEHAVE TEST
    #Generating and creation of new gmail user
    When I click on the users tab
    And  I create a new user trying any of the buttons
    Then the create new user modal is visible
    When a new email alias is generated using the base account email.auto.blippar.hub@gmail.com and stored in the global variable GENERATED_EMAIL_ALIAS
    And  creating a user with first name MANAGED and last name USER and email from global var GENERATED_EMAIL_ALIAS
    Then the submit button is clickable
    When I click on the modal submit button
    Then a user is created with first name MANAGED and last name USER
    When I logout
    And the activation link is obtained from the email, the token is modified and the link is opened
    Then Something went wrong screen is opened

