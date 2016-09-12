Feature: Stats navigation

  
  Navigation UI mixed scenarios


  Background:
    Given I delete the campaigns with the name CAMPAIGN_NAVIGATION (API)
    When I create the campaign with the name CAMPAIGN_NAVIGATION (API)
    And I create the blipp type blipp builder with the name BLIPP_NAVIGATION, marker image Airplane.JPG in the campaign CAMPAIGN_NAVIGATION (API)

 
  @ORPHAN @STATS
  Scenario: Navigate to blipp page, move the blipp, check it is moved

    When I delete the campaigns with the name #2_CAMPAIGN_NAVIGATION (API)
    When I create the campaign with the name #2_CAMPAIGN_NAVIGATION (API)
    When I login with user auto.blippar@gmail.com and password blippar1
    Then the user Blippar Admin is logged in
    When I go to My Campaigns
    Then the screen My campaigns is opened
    Then I check that there is a campaign card with the name CAMPAIGN_NAVIGATION
    When I open the campaign with the name CAMPAIGN_NAVIGATION
    Then The screen CAMPAIGN_NAVIGATION is opened
    Then I click on More option button on blipp BLIPP_NAVIGATION (UI)
    And I click on Move button on blipp BLIPP_NAVIGATION (UI)
    Then I wait to see modal dialog Move Blipp (UI)
    When I select campaign #2_CAMPAIGN_NAVIGATION from dropdown (UI)
    Then I click button Submit (UI)
    When I go to My Campaigns
    Then the screen My campaigns is opened
    Then I check that there is a campaign card with the name CAMPAIGN_NAVIGATION
    When I open the campaign with the name CAMPAIGN_NAVIGATION
    Then The screen CAMPAIGN_NAVIGATION is opened
    Then I checked that in the campaign CAMPAIGN_NAVIGATION there is no blipps available (UI)


  @ORPHAN @STATS
  Scenario: Navigate to blipp page, move LIVE blipp, check it is moved

    When I delete the campaigns with the name #2_CAMPAIGN_NAVIGATION (API)
    When I create the campaign with the name #2_CAMPAIGN_NAVIGATION (API)
    When I login with user auto.blippar@gmail.com and password blippar1
    Then the user Blippar Admin is logged in
    When I go to My Campaigns
    Then the screen My campaigns is opened
    Then I check that there is a campaign card with the name CAMPAIGN_NAVIGATION
    When I open the campaign with the name CAMPAIGN_NAVIGATION
    And I publish the blipp with the name BLIPP_NAVIGATION in the campaign CAMPAIGN_NAVIGATION (API)
    Then I check that the status of the blipp BLIPP_NAVIGATION in the campaign CAMPAIGN_NAVIGATION is LIVE (API)
    Then The screen CAMPAIGN_NAVIGATION is opened
    Then I click on More option button on blipp BLIPP_NAVIGATION (UI)
    And I click on Move button on blipp BLIPP_NAVIGATION (UI)
    Then I wait to see modal dialog Move Blipp (UI)
    When I select campaign #2_CAMPAIGN_NAVIGATION from dropdown (UI)
    Then I click button Submit (UI)
    When I go to My Campaigns
    Then the screen My campaigns is opened
    Then I check that there is a campaign card with the name CAMPAIGN_NAVIGATION
    When I open the campaign with the name CAMPAIGN_NAVIGATION
    Then The screen CAMPAIGN_NAVIGATION is opened
    Then I checked that in the campaign CAMPAIGN_NAVIGATION there is no blipps available (UI)

