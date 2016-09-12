Feature: New login and password reset


  Background:
    Given The testing account does not contain any emails

 
  @HUB-660 @assignee:ben.dalby @COMPLETED @LOGIN @STATS_HUB_UI
  Scenario: New login, check side menu

    Given the user is on the login page
    Then Log in to your Blippar account screen is opened
    When I login with user auto.blippar@gmail.com and password blippar1
    Then the user Blippar Admin is logged in
    Then the options in the side menu are My Campaigns,Group Campaigns,All Campaigns,Groups & Users,Approvals,Manage Advertisements,App


  @HUB-1003 @HUB-668 @HUB-669 @HUB-671 @HUB-673 @HUB-932 @assignee:gergana.ivanova @version:accounts-critical @version:next-version @COMPLETED @PASSWORD_RESET @PRODUCTION_CHECK @SANITY @STATS_HUB_UI
  Scenario: Reset password - full password reset flow from new login and dropdown

    Given the user is on the login page
    When the user clicks the reset password link
    Then Reset your password screen is opened
    When the user enter the email email.auto.blippar.hub+reset_password_test@gmail.com in the reset password screen and clicks in send email button
    And  the reset password link is obtained from the last email and it is opened
    Then Choose a new password screen is opened
    When a new password is generated and stored in global variable NEW_PASSWORD
    And the user set the password in the field New Password from the global variable NEW_PASSWORD
    And the user set the password in the field Retype new password from the global variable NEW_PASSWORD
    And the user clicks in SET NEW PASSWORD button
    Then the message in the reset form is Your password has been successfully changed
    When the user clicks Continue button after resetting the password
    Then the user email reset is logged in
    When the user clicks Change password upper right dropdown
    And the user set the password in the field enter your current password from the global variable NEW_PASSWORD
    And a new password is generated and stored in global variable NEW_PASSWORD2
    And the user set the password in the field choose a new password from the global variable NEW_PASSWORD2
    And the user set the password in the field confirm your new password from the global variable NEW_PASSWORD2
    And click the change password button in dropdown screen
    And The user opens the login page
    And the user logins using the email email.auto.blippar.hub+reset_password_test@gmail.com and the password from global var NEW_PASSWORD2
    Then the user email reset is logged in


  @ORPHAN @LOGIN @STATS_HUB_UI
  Scenario: Negative: Try to login with an non existing account

    #Precondition - the user is logged out
    Given the user is on the login page
    When I login with user dont_exist@blipar.com and password PASS123
    Then the message in the login window is Sorry. We didn't recognise your login details. Try again or reset your password.


  @HUB-660 @assignee:ben.dalby @COMPLETED @LOGIN @STATS_HUB_UI
  Scenario: Login - fields check

    Given the user is on the login page
    Then the user is redirected to the expected screen Log in to your Blippar account
    And the following fields are shown on the screen
    
    #Email address (text field)
    #Password (text field)
    #Remember me (checkbox)
    #Reset password (link)
    #Sign up for FREE (link)


  @HUB-661 @OPEN
  Scenario: Login - remember me

    #obsolete for now as Remeber me checkbox was removed
    When I login with user gergana.ivanova@blippar.com and password gerg456ivan
    And the user checks the checkbox 'Remember me'
    Then Next time the user goes to login,it happens without enter email and password


  @HUB-662 @HUB-673 @HUB-699 @assignee:gergana.ivanova @assignee:juanmoschino @version:next-version @COMPLETED @LOGIN @STATS_HUB_UI
  Scenario Outline: Negative: Login form submission - validation: invalid

    Given the user is on the login page
    When the user types email <email> and password <password>
    Then the response received is <expected_response>
            
     Examples:
     |email                          |password         |expected_response                       |
     |domain.com                     |pass123          |This does not look like an email address|
     |@2jkhkj.com                    |pass123          |This does not look like an email address|
     |gergana.ivanova@blipar         |pass1234         |This does not look like an email address|
     |empty value                    |pass123          | You didn’t enter an email address      |
     |a@gmail.com                    |empty value      | You didn’t enter a password            |


  @HUB-668 @HUB-673 @assignee:gergana.ivanova @version:accounts-critical @version:next-version @COMPLETED @PASSWORD_RESET @STATS_HUB_UI
  Scenario: Reset password page - fields check from password forgotten page

    #Precondition - the user is logged out
    Given the user is on the login page
    When the user clicks the reset password link
    Then Reset your password screen is opened
    And the email field is present
    And the submit button is present
    Then the link with the text Back to log in is present


  @HUB-664 @HUB-880 @assignee:ben.dalby @assignee:gergana.ivanova @COMPLETED @LOGIN @STATS_HUB_UI
  Scenario: Login with unverified user

    Given the user is on the login page
    When I login with user email.auto.blippar.hub+unverified@gmail.com and password layar123
    Then the user is redirected to the expected screen Confirm your email
    #Given the user is on the accounts login page
    #When the user clicks on the sign up for free link
    #Given the user is on the sign up for free page
    #Then Create your account screen is opened
    #When the user signs up with name TEST and surname ACCOUNT
    #And  a new email alias is generated using the base account email.auto.blippar.hub@gmail.com and stored in the global variable GENERATED_EMAIL_ALIAS
    #And  the user types the email from global GENERATED_EMAIL_ALIAS in email field and sets the password layar123
    #And  the user selects the country Netherlands
    #And  the user checks terms checkbox
    #And the user submits the form
    #Then the confirm your email screen is opened showing the email account stored in GENERATED_EMAIL_ALIAS
    #When The user opens the login page
    #And  the user logins using the email from global GENERATED_EMAIL_ALIAS and the password layar123
    #Then the confirm your email screen is opened showing the email account stored in GENERATED_EMAIL_ALIAS


  @ORPHAN @LOGIN @STATS_HUB_UI
  Scenario: Login - wrong password check

    Given the user is on the login page
    When I login with user gergana.ivanova@blippar.com and password gerg456
    Then the message in the login window is Sorry. We didn't recognise your login details. Try again or reset your password.
    #When clicks the 'Reset password' link
    #Then Reset your password screen is opened


  @HUB-671 @HUB-672 @HUB-700 @assignee:gergana.ivanova @version:next-version @COMPLETED @PASSWORD_RESET @STATS_HUB_UI
  Scenario: Reset password - invalid token

    Given the user is on the login page
    When clicks the 'Reset password' link
    Then Reset your password screen is opened
    When the user enter the email email.auto.blippar.hub+reset_password_test@gmail.com in the reset password screen and clicks in send email button
    And  the reset password link is obtained from the last email, the token is changed and it is opened
    Then the user is redirected to the expected screen Reset your password


  @ORPHAN @LOGIN @STATS_HUB_UI
  Scenario: Login form submission - unable to login with provided credentials error check

    Given the user is on the login page
    When the user types email skoutgg@gmail.com and password 567
    And the user submits the form
    Then the message in the login window is Unable to log in with provided credentials


  @HUB-669 @HUB-914 @assignee:gergana.ivanova @assignee:shyukri.shyukriev @version:accounts-critical @COMPLETED @LOGIN @PASSWORD_RESET @STATS_HUB_UI
  Scenario: Negative: Change password from user dropdown, old password verification is invalid

    Given the user is on the login page
    When I login with user gergana.ivanova@blippar.com and password gerg456ivan
    And the user clicks Change password upper right dropdown
    #the wrong old password is typed
    Then the user types the old password gerg456iv
    And type a new password pass1234 and retype it
    When the user submits the reset password form from dropdown
    Then an error Invalid password is shown and the password is not changed


  @HUB-669 @assignee:gergana.ivanova @version:accounts-critical @COMPLETED @LOGIN
  Scenario: Negative: Change password from user dropdown, set a short password

    Given the user is on the login page
    When I login with user auto.blippar@gmail.com and password blippar1
    Then the user Blippar Admin is logged in
    When the user clicks Change password upper right dropdown
    Then the user types the old password layar123
    And type a new password laya and retype it
    Then an error need at least 8 characters in your password is shown and the password is not changed


  @ORPHAN @PRODUCTION_CHECK
  Scenario: Normal login, check side menu - Production environment

    Given the user is on the login page
    Then Log in to your Blippar account screen is opened
    When I login with user auto.blippar+superadmin@gmail.com and password blippar1
    Then the user Blippar Super_Admin is logged in
    Then the options in the side menu are My Campaigns,Group Campaigns,All Campaigns,Groups & Users,Approvals

