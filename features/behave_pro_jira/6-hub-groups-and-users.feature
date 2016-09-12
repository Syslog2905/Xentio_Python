@GROUPS_AND_USERS @SANITY
Feature: Hub groups and users

  
  Different checks for groups and users using selenium.
  Scenarios tagged as HUB will be executed by jenkins daily jobs.


  Background:
    When I login with user auto.blippar@gmail.com and password blippar1
    Then The user Blippar Admin is logged in
    When navigating to Groups & Users
    Then the Groups overview is loaded

 
  @ORPHAN @PRODUCTION_CHECK
  Scenario: Filtering groups by ID

    And I wait for the filter to become visible
    When filtering by 1000
    Then the first result is a group with ID 1000
    When filtering by 7
    Then the first result is a group with ID 7


  @ORPHAN @GROUPS_AND_USERS
  Scenario: Creating a group

    When I click on the New Group button
    Then the create new group modal is visible
    When filling out the new group form with the group name BEHAVE TEST
    And I set BlippBuilder (Classic) checkbox enabled 
    Then the submit button is clickable
    When I click on the modal submit button
    Then a group is created with the group name BEHAVE TEST


  @ORPHAN @GROUPS_AND_USERS
  Scenario: Updating a group name

    When filtering by BEHAVE
    When navigating to the last group
    And I click on the edit group button
    Then the edit group modal is visible
    When filling out the new group form with the group name BEHAVE TEST RENAMED
    Then the submit button is clickable
    When I click on the modal submit button
    Then the group is renamed to BEHAVE TEST RENAMED


  @ORPHAN @GROUPS_AND_USERS
  Scenario: Creating a user

    When filtering by BEHAVE
    When navigating to the last group
    And I click on the users tab
    And I create a new user trying any of the buttons
    Then the create new user modal is visible
    When filling out the new user form with first name BEHAVE and last name TEST
    Then the submit button is clickable
    When I click on the modal submit button
    Then a user is created with first name BEHAVE and last name TEST


  @ORPHAN @PRODUCTION_CHECK
  Scenario: List users from blippar group

    When I open the user page for blippar group
    Then I wait up to 180 secs for the users to load


  @ORPHAN @AUTOMATABLE
  Scenario: Create new group: Choose group type

    #https://blippar.atlassian.net/wiki/pages/viewpage.action?pageId=31490309
    #As a PM I want the 'Group type' list to be updated to reflect the latest group creation
    Given a Blippar admin is in the 'Create group' modal
    When they select the 'Group Type' dropdown  
    Then they will see the following options to choose from
    #Internal,Lincensee,Education,Partner,Publisher,Other,Test,Free


  @ORPHAN @AUTOMATABLE
  Scenario: Edit Basic group

    Given the Blippar admin has chosen to 'Edit' a Basic group
    When the 'Edit group' modal window is opened
    Then the following fields are displayed
    #Groups name,Group status,Country,Group type (deactive),Start date (deactive),Account manager


  @ORPHAN @AUTOMATABLE
  Scenario: Edit Basic group - Cancel test

    Given the Blippar admin has chosen to 'Edit' a Basic group
    When the 'Edit group' modal window is opened
    Then the following fields are displayed
    #Groups name,Group status,Country,Group type (deactive),Start date (deactive),Account manager
    When the user clicks cancel next to the group type
    Then the group type is changed back to the original state  


  @ORPHAN @AUTOMATABLE
  Scenario: Edit a group - group details

    Given the Blippar admin has chosen to 'Edit' a Standard group
    When the 'Edit group' modal window is opened
    Then the following fields are displayed
    #Groups name,Group status,Country,Group type (deactive),Start date (deactive),Account manager


  @ORPHAN @AUTOMATABLE
  Scenario: Edit group status

    Given the 'Edit group' scenario
    When the Blippar admin changes the group status
    Then a message is displayed:Before you change the license type make sure you have cancelled their monthly payments in the Stripe dashboard, otherwise they will be continued to be charged  
    And the following fields appear
    #Payments,Duration,Publishing permission,Creation tools  


  @ORPHAN @AUTOMATABLE
  Scenario: Edit group status - cancel the change

    Given the 'Edit group' scenarion
    When the Blippar admin changes the group status
    Then a message is displayed:Before you change the license type make sure you have cancelled their monthly payments in the Stripe dashboard, otherwise they will be continued to be charged  
    And the following fields appear
    #Payments,Duration,Publishing permissions,Creation tools  
    When the user clicks cancel
    Then the group type is changed back to the original state  


  @ORPHAN @AUTOMATABLE
  Scenario: Edit group type

    Given the 'Edit group' scenario
    When the Blippar admin clicks 'Edit' next to the group type
    Then the group type field becomes active
    And a message is displayed:Before you change the license type make sure you have cancelled their monthly payments in the Stripe dashboard, otherwise they will be continued to be charged  
    And the following fields appear
    #Payments,Duration,Publishing permissions,Creation tools  


  @ORPHAN @AUTOMATABLE
  Scenario: Edit group type - cancel the change 

    Given the 'Edit group' scenario
    When the Blippar admin clicks 'Edit' next to the group type
    Then the group type field becomes active
    And a message is displayed:Before you change the license type make sure you have cancelled their monthly payments in the Stripe dashboard, otherwise they will be continued to be charged  
    And the following fields appear
    #Payments,Duration,Publishing permissions,Creation tools
    When the user clicks cancel
    Then the group type is changed back to the original state   


  @ORPHAN @AUTOMATABLE
  Scenario: Filtering the groups by name or part of the name

    And I wait for the filter to become visible
    When filtering by "Group name"
    Then the first result is a group with "Group name"
    When filtering by "Group name 2"
    Then the first result is a group with "Group name 2"

