@DISABLED @SIGNUP_PRO
Feature: Paid account (Payments) sign up

  As a unregistered user
  I want to be able to sign up for paid account
  In order to use Blippar cool features.


  Background:
    Given the user has chosen a 'paid' account
    When a new email alias is generated using the base account email.auto.blippar.hub@gmail.com and stored in the global variable GENERATED_EMAIL_ALIAS
    And the user types the email from global GENERATED_EMAIL_ALIAS in email field and sets the password layar123

 
  @HUB-1185 @HUB-763 @HUB-768 @HUB-774 @assignee:caroline.palmer @assignee:shyukri.shyukriev @WIP @SIGNUP_PRO
  Scenario Outline: Payments: Pro user signup Company account inside EU

    When the user signs up with name <name> and surname <surname>
    And the user selects the country <country>
    And the user checks terms checkbox
    When I proceed
    Then the page title must be Secure payment
    When I enter <credit_card_number> in card number field
    And  I select month 01 and year 2020 in expiration fields
    And  I set 123 in security code field
    When I set country <company_country> for company
    When I enable This is for business use checkbox
    And  I set <company_name> in company name field
    And  I set <VAT_number> in vat number field
    And  I set <street_address> in street address field
    And  I set <ZIP_CODE> in postal code field
    And  I set <city> in city field
    When I proceed
    Then the page title must be Review your order
    Then the Card with value <card_type> credit card ending in <card_last_digists> is present in credit card
    #And the Name with value test_user is present in billing details
    #And the Company name with value test_company is present in billing details
    #And the VAT number with value BG121745404 is present in billing details
    And the Street address with value <street_address> is present in billing details
    And the Zip or Postal code with value <ZIP_CODE> is present in billing details
    And the City with value <city> is present in billing details
    And the Country with value <country_code> is present in billing details
    And the VAT with value <vat_percentage> is present in order summary
    And the order summary with value <plan_price> is present in order summary
    When I proceed
    Then the page title must be Your payment is successful
    When click in link with text Get Started
    When the user logins using the email from global GENERATED_EMAIL_ALIAS and the password layar123
    ### https://stripe.com/docs/testing
    Then The screen My campaigns is opened
    When I logout
    #be carefull with copy/pasting currencies!
    Examples:
    |name|surname|country|credit_card_number|company_country|company_name|VAT_number|street_address|ZIP_CODE|city|country_code|card_type|card_last_digists|vat_percentage  |plan_price|
    |UK_user|Pro_VAT|United Kingdom|4242424242424242|United Kingdom|UK_company|GB339072747|UK_str 11     |W1      |London|GB|Visa|4242|20% VAT included|Total per month £ 60.00|
    |NL_user|Pro_VAT|Netherlands|4242424242424242|Netherlands|NL_company|NL010000446B01|NL_str 55     |1012PS  |Amsterdam|NL|Visa|4242|21% VAT included|Total per month € 60.50|
    |BG_user|Pro_VAT|Bulgaria|5555555555554444|Bulgaria|BG_company|BG121745404|Trakia 35     |1305    |Sofia|BG|MasterCard|4444|20% VAT included|Total per month € 60.00|


  @HUB-763 @HUB-774 @assignee:caroline.palmer @assignee:shyukri.shyukriev @WIP @SIGNUP_PRO
  Scenario: Payments: Pro user signup Company account OUTSIDE EU

    When the user signs up with name Pro_User and surname Signup_USA
    And the user selects the country United States of America
    And the user checks terms checkbox
    When I proceed
    Then the page title must be Secure payment
    When I enter 4242424242424242 in card number field
    And  I select month 01 and year 2020 in expiration fields
    And  I set 123 in security code field
    #Country should be same as in previous step HUB-552
    #When I set country United States of America for company
    When I enable This is for business use checkbox
    And  I set test_company_USA in company name field
    And  I set test_address in street address field
    And  I set 10007 in postal code field
    And I set New York in city field
    When I proceed
    Then the page title must be Review your order
    Then the Card with value Visa credit card ending in 4242 is present in credit card
    #And the Name with value test_user is present in billing details
    #And the Company name with value test_company_USA is present in billing details
    And the Street address  with value test_address is present in billing details
    And the Zip or Postal code with value 10007 is present in billing details
    And the City with value New York is present in billing details
    And the Country with value US is present in billing details
    And the order summary with value Total per month US$ 50.00 is present in order summary
    When I proceed
    Then the page title must be Your payment is successful
    When click in link with text Get Started
    When the user logins using the email from global GENERATED_EMAIL_ALIAS and the password layar123
    Then The screen My campaigns is opened
    When I logout


  @HUB-884 @assignee:shyukri.shyukriev @COMPLETED
  Scenario: Payment details should be pre-populated when clicking on change links on review page

    When the user types the email from global GENERATED_EMAIL_ALIAS in email field and sets the password layar123
    And the user signs up with name Pro_User and surname Signup
    And the user selects the country Netherlands
    And the user checks terms checkbox
    When I proceed
    Then the page title must be Secure payment
    When I enter 4242424242424242 in card number field
    And  I select month 01 and year 2020 in expiration fields
    And  I set 123 in security code field
    When I set country Bulgaria for company
    When I enable This is for business use checkbox
    And  I set test_company in company name field
    And  I set BG121745404 in vat number field
    And  I set test_address in street address field
    And  I set 1000 in postal code field
    And  I set Sofia in city field
    When I proceed
    Then the page title must be Review your order
    Then the Card with value Visa credit card ending in 4242 is present in credit card
    When click in link with text Change
    Then the page title must be Secure payment
    Then card number field contains 4242424242424242
    And security code field contains 123


  @HUB-767 @OPEN
  Scenario: Card declined

    When the user signs up with name Pro_User and surname Signup
    And the user selects the country Netherlands
    And the user checks terms checkbox
    When I proceed
    Then the page title must be Secure payment
    When I enter 4000000000000002 in card number field
    And  I select month 01 and year 2020 in expiration fields
    And  I set 123 in security code field
    When I set country Bulgaria for company
    And  I set test_address in street address field
    And  I set 1000 in postal code field
    And  I set Sofia in city field
    When I proceed
    Then the page title must be Review your order
    Then the Card with value Visa credit card ending in 0002 is present in credit card
    When I proceed
    Then the page title must be Review your order

