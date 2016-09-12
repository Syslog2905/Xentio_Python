Feature: Hub campaign sharing tests

  
  This group of tests checks campaign sharing between the different user roles. The tests are UI and they use selenium.
  Scenarios tagged as HUB will be executed by daily jenkins jobs.

 
  @ORPHAN @CAMPAIGN_SHARING
  Scenario: Blippar admin shares a campaign

    When I login with user auto.blippar+blippar_user1@gmail.com and password blippar1
    Then the user Blippar User is logged in
    When I go to My Campaigns
    Then the screen My campaigns is opened
    When I delete the campaign BEHAVE_CAMPAIGN_SHARING
    And I login with user auto.blippar@gmail.com and password blippar1
    Then the user Blippar Admin is logged in
    When I go to My Campaigns
    Then the screen My campaigns is opened
    When I delete the campaign BEHAVE_CAMPAIGN_SHARING
    And I create the campaign with the name BEHAVE_CAMPAIGN_SHARING
    And I go to My Campaigns
    Then I check that there is a campaign card with the name BEHAVE_CAMPAIGN_SHARING
    When I share the campaign BEHAVE_CAMPAIGN_SHARING to the user auto.blippar+blippar_user1@gmail.com
    And I login with user auto.blippar+blippar_user1@gmail.com and password blippar1
    Then the user Blippar User is logged in
    When I go to My Campaigns
    Then the screen My campaigns is opened
    And I check that there is a campaign card with the name BEHAVE_CAMPAIGN_SHARING


  @ORPHAN @CAMPAIGN_SHARING @PRODUCTION_CHECK
  Scenario: Blippar user shares a campaign

    When I login with user auto.blippar@gmail.com and password blippar1
    Then the user Blippar Admin is logged in
    When I go to My Campaigns
    Then the screen My campaigns is opened
    When I delete the campaign BEHAVE_CAMPAIGN_SHARING
    And I login with user auto.blippar+blippar_user1@gmail.com and password blippar1
    Then the user Blippar User is logged in
    When I go to My Campaigns
    Then the screen My campaigns is opened
    When I delete the campaign BEHAVE_CAMPAIGN_SHARING
    And I create the campaign with the name BEHAVE_CAMPAIGN_SHARING
    And I go to My Campaigns
    Then I check that there is a campaign card with the name BEHAVE_CAMPAIGN_SHARING
    When I share the campaign BEHAVE_CAMPAIGN_SHARING to the user auto.blippar@gmail.com
    And I login with user auto.blippar@gmail.com and password blippar1
    Then the user Blippar Admin is logged in
    When I go to My Campaigns
    Then the screen My campaigns is opened
    And I check that there is a campaign card with the name BEHAVE_CAMPAIGN_SHARING


  @HUB-461 @COMPLETED @CAMPAIGN_SHARING @PRODUCTION_CHECK
  Scenario: Group admin user shares a campaign

    When I login with user auto.blippar+group_user@gmail.com and password blippar1
    Then the user Hub GroupUser is logged in
    When I go to My Campaigns
    Then the screen My campaigns is opened
    When I delete the campaign BEHAVE_CAMPAIGN_SHARING
    And I login with user auto.blippar+group_admin@gmail.com and password blippar1
    Then the user Blippar GroupAdmin is logged in
    When I go to My Campaigns
    Then the screen My campaigns is opened
    When I delete the campaign BEHAVE_CAMPAIGN_SHARING
    And I create the campaign with the name BEHAVE_CAMPAIGN_SHARING
    And I go to My Campaigns
    Then I check that there is a campaign card with the name BEHAVE_CAMPAIGN_SHARING
    When I share the campaign BEHAVE_CAMPAIGN_SHARING to the user auto.blippar+group_user@gmail.com
    And I login with user auto.blippar+group_user@gmail.com and password blippar1
    Then the user Hub GroupUser is logged in
    When I go to My Campaigns
    Then the screen My campaigns is opened
    And I check that there is a campaign card with the name BEHAVE_CAMPAIGN_SHARING


  @ORPHAN @CAMPAIGN_SHARING @PRODUCTION_CHECK @SANITY
  Scenario: Normal user shares a campaign

    When I login with user auto.blippar+group_user@gmail.com and password blippar1
    Then the user Hub GroupUser is logged in
    When I go to My Campaigns
    Then the screen My campaigns is opened
    When I delete the campaign BEHAVE_CAMPAIGN_SHARING
    And I create the campaign with the name BEHAVE_CAMPAIGN_SHARING
    And I go to My Campaigns
    Then I check that there is a campaign card with the name BEHAVE_CAMPAIGN_SHARING
    When I share the campaign BEHAVE_CAMPAIGN_SHARING to the user auto.blippar+group_admin@gmail.com
    And I login with user auto.blippar+group_admin@gmail.com and password blippar1
    Then the user Blippar GroupAdmin is logged in
    When I go to My Campaigns
    Then the screen My campaigns is opened
    And I check that there is a campaign card with the name BEHAVE_CAMPAIGN_SHARING


  @ORPHAN @AUTOMATABLE
  Scenario: Create the campaign with Bespoke and BB blipps, then navigate through all markers

    #Login and cleanup
    When I login with user auto.blippar+blippar_user1@gmail.com and password blippar1
    Then The user Blippar User is logged in
    When I go to My Campaigns
    Then The screen My campaigns is opened
    When I delete the campaign BEHAVE CAMPAIGN
    Then I check that there are not campaigns cards with the name BEHAVE CAMPAIGN
    #Campaign & Bespoke blipp creation
    When I create the campaign with the name BEHAVE CAMPAIGN
    Then The screen BEHAVE CAMPAIGN is opened
    When I click on Create Bespoke blipp button
    Then The modal Create blipp is opened
    And The modal step Name is active
    When Creating my blipp I give it the name BEHAVE BESPOKE_BLIPP_TEST
    And Creating my blipp I upload the zip blipp.zip
    And I click on next
    Then The modal step Publish is active
    When Creating my blipp I enter the test code btest
    And I click on test blipp
    Then I check that the blipp with the name BEHAVE BESPOKE_BLIPP_TEST is created
    When I go to Blipp Detail BEHAVE BESPOKE_BLIPP_TEST page
    Then The blipp must have 1 versions
    And The Latest Version should have the status In Progress
    #Adding BlippBuilder blipp also
    When I go to My Campaigns
    Then the screen My campaigns is opened
    When I open the campaign with the name BEHAVE CAMPAIGN
    Then The screen BEHAVE CAMPAIGN is opened
    When I click on Create BlippBuilder blipp button as a normal user
    Then The modal Create blipp is opened
    When Creating my blipp I give it the name BLIPP_GROUP_USER
    And Creating my blipp I upload the marker flowers.jpg
    And I click on next
    Then The modal step Publish is active
    When Creating my blipp I select Make your blipp live: choose countries
    And I choose GB as the country
    And I click on publish blipp
    And I click in back button from blippbuilder
    Then I check that the blipp with the name BLIPP_GROUP_USER is created

