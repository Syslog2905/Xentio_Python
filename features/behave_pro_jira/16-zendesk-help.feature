@DISABLED @HELP @ZENDESK
Feature: Zendesk Help

 
  @HUB-494 @HUB-497 @HUB-558 @assignee:caroline.palmer @COMPLETED
  Scenario: Open Help with user logged in HUB (HUB-494) and chek user ID is available (HUB-497) + logout

    When I login with user auto.blippar@gmail.com and password blippar1
    Then the user Blippar Admin is logged in
    When I open Help from user menu
    And I switch to next tab
    Then the page title must be Help
    When click in link with text Browse tutorials
    Then the page title must be Tutorials – Help
    When back to the previous page
    When click in link with text Get inspired
    Then the page title must be Inspiration – Help
    Then The user blippar.admin is logged in Zendesk
    When I logout from Zendesk
    Then the user is logged out


  @HUB-495 @assignee:caroline.palmer @COMPLETED
  Scenario: Open Help with user not logged in HUB (HUB-495)

    # we're clearing all cookies and calling logout url on support.blippar.com
    When I open https://support.blippar.com/hc/en-us and login with user auto.blippar@gmail.com and password blippar1
    Then the page title must be Help


  @HUB-496 @assignee:caroline.palmer @COMPLETED
  Scenario: Verify redirection to correct page after login (HUB-496)

    #Not sure is the # in the url will be valid in the future.
    When I open https://support.blippar.com/hc/en-us/articles/207845928-Adding-a-call-to-action-CTA- and login with user auto.blippar@gmail.com and password blippar1
    Then the page title must be Adding a call to action (CTA) – Help

