Feature: Hub Campaign creation, update and deletion

  
  This set checks campaign actions using different user roles. The tests are UI and they use selenium.
  Scenarios tagged as HUB will be executed by daily jenkins jobs.

 
  @ORPHAN @AUTOMATABLE
  Scenario: Creating campaign with BB blipp with new marker

    Given I delete the campaigns with the name CAMPAIGN_NAVIGATION (API)
    When I create the campaign with the name CAMPAIGN_NAVIGATION (API)
    When I login with user auto.blippar@gmail.com and password blippar1
    Then the user Blippar Admin is logged in
    When I go to My Campaigns
    Then the screen My campaigns is opened
    Then I check that there is a campaign card with the name CAMPAIGN_NAVIGATION
    When I open the campaign with the name CAMPAIGN_NAVIGATION
    Then The screen CAMPAIGN_NAVIGATION is opened
    When I click on Create BlippBuilder blipp button
    When Creating my blipp I give it the name BB_Blipp
    When Creating my blipp I upload the marker Airplane.JPG
    Then I check that the status of the blipp Airplane.JPG detail page is Draft (UI)


  @ORPHAN @BLIPP_CREATION
  Scenario: Creating campaign with BB and Bespoke blipps, navigate through the markers

    Given I delete the campaigns with the name CAMPAIGN_NAVIGATION_2 (API)
    When I create the campaign with the name CAMPAIGN_NAVIGATION_2 (API)
    And I create the blipp type blipp builder with the name BLIPP_NAVIGATION, marker image Airplane.JPG in the campaign CAMPAIGN_NAVIGATION_2 (API)
    When I login with user auto.blippar@gmail.com and password blippar1
    Then The user Blippar Admin is logged in
    When I go to My Campaigns
    Then I check that there is a campaign card with the name CAMPAIGN_NAVIGATION_2
    When I open the campaign with the name CAMPAIGN_NAVIGATION_2
    Then the screen CAMPAIGN_NAVIGATION_2 is opened
    When I click on Create Bespoke blipp button in the toolbar
    Then The modal Create blipp is opened
    And The modal step Name is active
    When Creating my blipp I give it the name BEHAVE BESPOKE_BLIPP_TEST
    And Creating my blipp I upload the zip blipp.zip
    And I click on next
    Then The modal step Publish is active
    When Creating my blipp I select Make your blipp live: choose countries
    And I choose GB as the country
    And I click on publish blipp
    Then I check that the blipp with the name BEHAVE BESPOKE_BLIPP_TEST is created
    When I go to Blipp Detail BEHAVE BESPOKE_BLIPP_TEST page
    Then The blipp must have 1 versions
    And The Latest Version should have the status LIVE
    When back to the previous page
    And tap on All markers
    Then go through all Bespoke markers to check them


  @ORPHAN @CAMPAIGN_CREATION
  Scenario Outline: Create, update and delete a campaign with different roles

     Given I delete the campaigns with the name BEHAVE_CAMPAIGN_CREATION (API)
     Given I delete the campaigns with the name BEHAVE_CAMPAIGN_CREATION_UPDATED (API)
     When I login with user <user_email> and password <password>
     Then the user <display_name> is logged in
     When I go to My Campaigns
     Then the screen My campaigns is opened
     When I delete the campaign BEHAVE_CAMPAIGN_CREATION
     Then I check that there are not campaigns cards with the name BEHAVE_CAMPAIGN_CREATION
     When I create the campaign with the name BEHAVE_CAMPAIGN_CREATION
     When I go to My Campaigns
     Then the screen My campaigns is opened
     Then I check that there is a campaign card with the name BEHAVE_CAMPAIGN_CREATION
     When I open the campaign with the name BEHAVE_CAMPAIGN_CREATION
     When I update the name of the campaign to BEHAVE_CAMPAIGN_CREATION_UPDATED
     When I go to My Campaigns
     When I delete the campaign BEHAVE_CAMPAIGN_CREATION_UPDATED
     Then I check that there are not campaigns cards with the name BEHAVE_CAMPAIGN_CREATION_UPDATED
     When I logout
     Examples:
    |user_email|password|display_name|
    |auto.blippar@gmail.com|blippar1|Blippar Admin|
    |auto.blippar+blippar_user1@gmail.com|blippar1|Blippar User|
    |auto.blippar+group_admin@gmail.com|blippar1|Blippar GroupAdmin|
    |auto.blippar+group_user@gmail.com|blippar1|Hub GroupUser|
      #|managed user|pass|managed user|managed user| #sync with Shyukri about the user

