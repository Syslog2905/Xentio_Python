Feature: Navigation tests requiring live blipp


  Background:
    Given I delete the campaigns with the name CAMPAIGN_NAVIGATION (API)
    When I create the campaign with the name CAMPAIGN_NAVIGATION (API)
    And I create the blipp type blipp builder with the name BLIPP_NAVIGATION, marker image fish1.jpeg in the campaign CAMPAIGN_NAVIGATION (API)

 
  @HUB-455 @assignee:gergana.ivanova @COMPLETED @STATS_HUB_UI
  Scenario: Navigate to the stats from campaign page

    When I publish blipp with the name BLIPP_NAVIGATION in the campaign CAMPAIGN_NAVIGATION (API)
    Then I check that the status of the blipp BLIPP_NAVIGATION in the campaign CAMPAIGN_NAVIGATION is LIVE (API)
    When I login with user auto.blippar@gmail.com and password blippar1
    Then the user Blippar Admin is logged in
    When I go to My Campaigns
    Then the screen My campaigns is opened
    Then I check that there is a campaign card with the name CAMPAIGN_NAVIGATION
    When I open the campaign with the name CAMPAIGN_NAVIGATION
    When I click View Stats
    Then the page title must be Campaign Stats | Blippar Dashboard


  @ORPHAN @BLIPP_CREATION
  Scenario: Navigate to blipp page and check blipp details

    When I login with user auto.blippar@gmail.com and password blippar1
    Then the user Blippar Admin is logged in
    When I go to My Campaigns
    Then the screen My campaigns is opened
    Then I check that there is a campaign card with the name CAMPAIGN_NAVIGATION
    When I open the campaign with the name CAMPAIGN_NAVIGATION
    Then The screen CAMPAIGN_NAVIGATION is opened
    And I click on More option button on blipp BLIPP_NAVIGATION (UI)
    And I wait to see modal dialog Publish Your Blipp (UI)
    When I publish the blipp with the name BLIPP_NAVIGATION globally (UI)
    When I go to Blipp Detail BLIPP_NAVIGATION page
    Then I check that the status of the blipp BLIPP_NAVIGATION detail page is LIVE (UI)
    Then I click on Change Country blipp button
    When I choose GB as the country
    When I click on next
    Then the page title must be BLIPP_NAVIGATION | Blipp | Blippar Dashboard

