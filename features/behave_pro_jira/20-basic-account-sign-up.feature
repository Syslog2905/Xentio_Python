Feature: Basic account sign up


  Background:
    Given The testing account does not contain any emails

 
  @HUB-513 @HUB-681 @HUB-863 @assignee:caroline.palmer @assignee:juanmoschino @COMPLETED @SANITY @SIGNUP_BASIC
  Scenario: Sign up with a Basic (free) account - verification email & verified account

    Given the user has chosen a 'free' account
    Then Create your account screen is opened
    When the user signs up with name TEST and surname ACCOUNT
    And  a new email alias is generated using the base account email.auto.blippar.hub@gmail.com and stored in the global variable GENERATED_EMAIL_ALIAS
    And  the user types the email from global GENERATED_EMAIL_ALIAS in email field and sets the password layar123
    And  the user selects the country Netherlands
    Then the newsletter checkbox is selected by default
    When  the user checks terms checkbox
    And  the user submits the form
    Then the confirm your email screen is opened showing the email account stored in GENERATED_EMAIL_ALIAS
    And  an activation mail is sent for the account stored in GENERATED_EMAIL_ALIAS
    When the activation link is obtained from the email received and it is opened
    Then the message in the login window is Done. Just log in now and start blipping. Enjoy!
    When the user logins using the email from global GENERATED_EMAIL_ALIAS and the password layar123
    Then the user TEST ACCOUNT is logged in
    #And the user is assigned to a unique group ID (TODO LATER)


  @HUB-516 @HUB-678 @assignee:caroline.palmer @assignee:gergana.ivanova @COMPLETED @SIGNUP_BASIC
  Scenario: Checkbox Terms and Conditions - deselected by default check

    Given the user has chosen a 'free' account
    Then the user is on the screen Create your account
    When the terms & conditions checkbox is displayed
    Then the checkbox is deselected by default


  @HUB-516 @assignee:caroline.palmer @COMPLETED @SIGNUP_BASIC
  Scenario: Error message when checkbox Terms and Conditions is deselected

    Given the user has chosen a 'free' account
    When the user signs up with name Gergana and surname Ivanova
    When the user types email email@test.bg, password pass1234 and reenter password pass1234
    And the user selects the country Netherlands
    And the user deselects the terms & conditions checkbox
    And the user submits the form
    Then terms checkbox error message is displayed
    #Error message: In order to create a Blippar account, you must agree to Blippar’s Terms and Conditions and Privacy Policy.


  @HUB-513 @HUB-517 @HUB-523 @HUB-678 @HUB-713 @assignee:caroline.palmer @assignee:gergana.ivanova @COMPLETED @SIGNUP_BASIC
  Scenario: Sign up form - Subscribe to email updates checkbox selected by default

    Given the user has chosen a 'free' account
    When the newsletter subscription checkbox is displayed
    Then the newsletter checkbox is selected by default


  @HUB-518 @HUB-678 @assignee:gergana.ivanova @COMPLETED @SIGNUP_BASIC
  Scenario Outline: Sign up form submission - validate email address and password

    Given the user has chosen a 'free' account
    When the user signs up with name Gergana and surname Ivanova
    When the user types email <email>, password <password1> and reenter password <password2> 
    And the user selects the country Andorra
    And the user checks terms checkbox
    Then the response received is <expected_response>
       
    Examples:
      |email            |password1  |password2    |expected_response                                |
      |domain.com       |pass1234   |pass1234     |This does not look like an email address         |
      |@2jkhkj.com      |pass1234   |pass1234     |This does not look like an email address         |
      |mrwrong@gmail.com|pass1234   |pass1234     |This email address is already registered. Log in.|
      |a@gmail.com      |pass12     |pass12       |You need at least 8 characters in your password  |
      |right@gmail.com  |pass1234   |pass1234     |No message                                       |
      |a@gmail.com      |pass1234   |pass1234     |No message                                       |
      |empty value      |pass1234   |pass1234     |You can't leave this empty                       |
      |a@gmail.com      |empty value|pass1234     |You can't leave this empty                       |
      |a@gmail.com      |pass1234   |empty value  |You can't leave this empty                       |


  @HUB-678 @HUB-679 @assignee:caroline.palmer @assignee:gergana.ivanova @COMPLETED @SIGNUP_BASIC
  Scenario: Sign up form - Display terms & conditions

    Given the user has chosen a 'free' account
    #When the user clicks on a link with the text 'terms and conditions' and a proper modal text is shown
    When they click on the terms & conditions link
    When I switch to next tab
    Then the terms & conditions are opened in a new browser tab
    And a button with text Download as PDF is displayed
    Then Download as PDF button is clicked
    # a step to check the terms&conditions check can be implemented


  @HUB-678 @HUB-679 @assignee:caroline.palmer @assignee:gergana.ivanova @COMPLETED
  Scenario: Sign up form - Display privacy policy

    #Obsolete - no Privacy policy anymore
    Given the user has chosen a 'free' account
    When the user clicks on a link with the text 'Privacy policy' and a proper modal text is shown


  @HUB-513 @assignee:caroline.palmer @COMPLETED @SIGNUP_BASIC
  Scenario: Sign up form - fields and checkboxes check

    Given the user has chosen a 'free' account
    Then the following fields are shown on the screen
    #Email address text field
    #Password password field
    #Confirm password password field
    #I agree to Blippar’s terms & conditions and privacy policy checkbox
    #I would like to receive product updates and news from Blippar checkbox


  @HUB-536 @HUB-692 @assignee:caroline.palmer @assignee:juanmoschino @version:next-version @COMPLETED @SIGNUP_BASIC
  Scenario: Sign up form submission - verification email & invalid verification link

    Given the user has chosen a 'free' account
    Then Create your account screen is opened
    When the user signs up with name TEST and surname ACCOUNT
    And  a new email alias is generated using the base account email.auto.blippar.hub@gmail.com and stored in the global variable GENERATED_EMAIL_ALIAS
    And  the user types the email from global GENERATED_EMAIL_ALIAS in email field and sets the password layar123
    And  the user selects the country Netherlands
    And  the user checks terms checkbox
    And  the user submits the form
    Then the confirm your email screen is opened showing the email account stored in GENERATED_EMAIL_ALIAS
    And  an activation mail is sent for the account stored in GENERATED_EMAIL_ALIAS
    When the activation link is obtained from the email, the token is modified and the link is opened
    Then the message in the login window is Your link has expired, log in to get a new one.


  @HUB-525 @HUB-530 @HUB-980 @assignee:caroline.palmer @assignee:juanmoschino @assignee:shyukri.shyukriev @COMPLETED @SIGNUP_BASIC
  Scenario: Sign up form submission - verification email, re-send email

    Given the user has chosen a 'free' account
    Then Create your account screen is opened
    When the user signs up with name TEST and surname ACCOUNT
    And  a new email alias is generated using the base account email.auto.blippar.hub@gmail.com and stored in the global variable GENERATED_EMAIL_ALIAS
    And  the user types the email from global GENERATED_EMAIL_ALIAS in email field and sets the password layar123
    And  the user selects the country Netherlands
    And  the user checks terms checkbox
    And  the user submits the form
    Then the confirm your email screen is opened showing the email account stored in GENERATED_EMAIL_ALIAS
    And an activation mail is sent for the account stored in GENERATED_EMAIL_ALIAS
    When the user clicks in RESEND EMAIL button
    Then an activation mail is sent for the account stored in GENERATED_EMAIL_ALIAS
    When the activation link is obtained from the email received and it is opened
    Then the message in the login window is Done. Just log in now and start blipping. Enjoy!

