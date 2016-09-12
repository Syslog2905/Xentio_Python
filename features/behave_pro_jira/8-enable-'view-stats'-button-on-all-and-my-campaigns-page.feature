Feature: Enable 'view stats' button on all and my campaigns page

 
  @HUB-19 @assignee:caroline.palmer @COMPLETED @STATS_HUB_UI
  Scenario: Live stats icon and check blipp creation date in My Campaign page

    When I delete the campaigns with the name CAMPAIGN_TEST_STATS (API)
    When I create the campaign with the name CAMPAIGN_TEST_STATS (API)
    And I create the blipp type blipp builder with the name BLIPP_TEST_STATS, marker image fish1.jpeg in the campaign CAMPAIGN_TEST_STATS (API)
    When I publish blipp with the name BLIPP_TEST_STATS in the campaign CAMPAIGN_TEST_STATS (API)
    When I login with user auto.blippar@gmail.com and password blippar1
    And I go to My Campaigns
    Then I check that there is a campaign card with the name CAMPAIGN_TEST_STATS
    When I open the campaign with the name CAMPAIGN_TEST_STATS
    And I go to Blipp Detail BLIPP_TEST_STATS page
    Then I check that the blipp BLIPP_TEST_STATS has date and time of creation (UI)
    When I click View Stats
    Then the page title must be Blipp Stats | Blippar Dashboard


  @HUB-19 @assignee:caroline.palmer @COMPLETED @STATS_HUB_UI
  Scenario: Deactivated stats icon when blipps are not published for a campaign on My Campaign page

    When I delete the campaigns with the name CAMPAIGN_TEST_STATS (API)
    When I create the campaign with the name CAMPAIGN_TEST_STATS (API)
    And I create the blipp type blipp builder with the name BLIPP_TEST_STATS, marker image fish1.jpeg in the campaign CAMPAIGN_TEST_STATS (API)
    When I login with user auto.blippar@gmail.com and password blippar1
    And I go to My Campaigns
    Then I check that there is a campaign card with the name CAMPAIGN_TEST_STATS
    When I open the campaign with the name CAMPAIGN_TEST_STATS
    And I go to Blipp Detail BLIPP_TEST_STATS page
    Then I check View Stats is not active


  @ORPHAN @STATS_HUB_UI
  Scenario: Live stats icon and check blipp creation date in All Campaign page

    When I delete the campaigns with the name CAMPAIGN_TEST_STATS (API)
    When I create the campaign with the name CAMPAIGN_TEST_STATS (API)
    And I create the blipp type blipp builder with the name BLIPP_TEST_STATS, marker image fish1.jpeg in the campaign CAMPAIGN_TEST_STATS (API)
    When I publish blipp with the name BLIPP_TEST_STATS in the campaign CAMPAIGN_TEST_STATS (API)
    When I login with user auto.blippar@gmail.com and password blippar1
    And I go to All Campaigns
    Then I check that there is a campaign card with the name CAMPAIGN_TEST_STATS
    When I open the campaign with the name CAMPAIGN_TEST_STATS
    And I go to Blipp Detail BLIPP_TEST_STATS page
    Then I check that the blipp BLIPP_TEST_STATS has date and time of creation (UI)
    When I click View Stats
    Then the page title must be Blipp Stats | Blippar Dashboard


  @ORPHAN @STATS_HUB_UI
  Scenario: Deactivated stats icon when blipps are not published for a campaign on All Campaign page

    When I delete the campaigns with the name CAMPAIGN_TEST_STATS (API)
    When I create the campaign with the name CAMPAIGN_TEST_STATS (API)
    And I create the blipp type blipp builder with the name BLIPP_TEST_STATS, marker image fish1.jpeg in the campaign CAMPAIGN_TEST_STATS (API)
    When I login with user auto.blippar@gmail.com and password blippar1
    And I go to All Campaigns
    Then I check that there is a campaign card with the name CAMPAIGN_TEST_STATS
    When I open the campaign with the name CAMPAIGN_TEST_STATS
    And I go to Blipp Detail BLIPP_TEST_STATS page
    Then I check View Stats is not active

