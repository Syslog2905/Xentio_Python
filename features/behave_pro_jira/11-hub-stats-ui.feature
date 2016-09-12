Feature: Hub Stats UI

  
  This tests are using a combination of API and selenium steps to verify the correct visualisation of STATS information in HUB. 
  The tests tagged as STATS_HUB_UI will be executed daily by jenkins jobs.


  Background:
    Given I delete the campaigns with the name CAMPAIGN_TEST_STATS (API)
    When I create the campaign with the name CAMPAIGN_TEST_STATS (API)
    And I create the blipp type blipp builder with the name BLIPP_TEST_STATS, marker image fish1.jpeg in the campaign CAMPAIGN_TEST_STATS (API)

 
  @ORPHAN @SANITY @STATS_HUB_UI
  Scenario: Verify UI stats numbers of a Published Blipp

    When I publish blipp with the name BLIPP_TEST_STATS in the campaign CAMPAIGN_TEST_STATS (API)
    When I send 1 interactions to the blipp BLIPP_TEST_STATS from campaign CAMPAIGN_TEST_STATS as user user1 from location Amsterdam on date Now (API)
    And I send 5 interactions to the blipp BLIPP_TEST_STATS from campaign CAMPAIGN_TEST_STATS as user user2 from location Sofia on date Now (API)
    When I get the stat users of the blipp BLIPP_TEST_STATS from the date 2015-01-01 to the date Now in the campaign CAMPAIGN_TEST_STATS (API)
    Then the number of total unique users is 2 (API)
    When I calculate Average_User_Interaction of the blipp BLIPP_TEST_STATS from the date 2015-01-01 to the date Now in the campaign CAMPAIGN_TEST_STATS is 3.00 (API)
    When I login with user auto.blippar@gmail.com and password blippar1
    And I go to My Campaigns
    Then I check that there is a campaign card with the name CAMPAIGN_TEST_STATS
    When I open the campaign with the name CAMPAIGN_TEST_STATS
    And I go to Blipp Detail BLIPP_TEST_STATS page
    When I click View Stats
    Then the number of average interactions per user is 3.0 (UI)
    Then the number of total interactions for day Now is 6 (UI)
    Then the number of unique users is 2 (UI)


  @ORPHAN @STATS_HUB_UI
  Scenario: Verify Total Interactions of a published blipp for the last day

    When I publish blipp with the name BLIPP_TEST_STATS in the campaign CAMPAIGN_TEST_STATS (API)
    Then I check that the status of the blipp BLIPP_TEST_STATS in the campaign CAMPAIGN_TEST_STATS is LIVE (API)
    When I send 2 interactions to the blipp BLIPP_TEST_STATS from campaign CAMPAIGN_TEST_STATS as user user1 from location Amsterdam on date Now (API)
    And I send 2 interactions to the blipp BLIPP_TEST_STATS from campaign CAMPAIGN_TEST_STATS as user user3 from location Sofia on date Now (API)
    When I get the stat interactions of the blipp BLIPP_TEST_STATS from the date 2015-01-01 to the date Now in the campaign CAMPAIGN_TEST_STATS (API)
    Then the number of total interactions is 4 (API)
    When I login with user auto.blippar@gmail.com and password blippar1
    And I go to My Campaigns
    Then I check that there is a campaign card with the name CAMPAIGN_TEST_STATS
    When I open the campaign with the name CAMPAIGN_TEST_STATS
    And I go to Blipp Detail BLIPP_TEST_STATS page
    When I click View Stats
    Then the number of total interactions for day Now is 4 (UI)


  @ORPHAN @STATS_HUB_UI
  Scenario: Check stats in Campaign with multiple blipps

    When I create the blipp type blipp builder with the name SECOND_BLIPP, marker image fish1.jpeg in the campaign CAMPAIGN_TEST_STATS (API)
    When I publish blipp with the name BLIPP_TEST_STATS in the campaign CAMPAIGN_TEST_STATS (API)
    And I publish blipp with the name SECOND_BLIPP in the campaign CAMPAIGN_TEST_STATS (API)
    When I send 2 interactions to the blipp BLIPP_TEST_STATS from campaign CAMPAIGN_TEST_STATS as user user1 from location Amsterdam on date Now (API)
    And I send 2 interactions to the blipp BLIPP_TEST_STATS from campaign CAMPAIGN_TEST_STATS as user user2 from location Sofia on date Now (API)
    And I send 5 interactions to the blipp SECOND_BLIPP from campaign CAMPAIGN_TEST_STATS as user user3 from location London on date Now (API)
    When I login with user auto.blippar@gmail.com and password blippar1
    And I go to My Campaigns
    Then I check that there is a campaign card with the name CAMPAIGN_TEST_STATS
    When I open the campaign with the name CAMPAIGN_TEST_STATS
    When I click View Stats
    Then the number of average interactions per user is 3.0 (UI)
    And the number of total interactions for day Now is 9 (UI)
    And the number of unique users is 3 (UI)
    When I select blipp BLIPP_TEST_STATS from dropdown (UI)
    Then the number of average interactions per user is 2.0 (UI)
    And the number of total interactions for day Now is 4 (UI)
    And the number of unique users is 2 (UI)
    When I select blipp SECOND_BLIPP from dropdown (UI)
    Then the number of average interactions per user is 5.0 (UI)
    And the number of total interactions for day Now is 5 (UI)
    And the number of unique users is 1 (UI)


  @ORPHAN @STATS_HUB_UI
  Scenario: Verify zero stats of a blipp without interactions - campaign page

    When I publish blipp with the name BLIPP_TEST_STATS in the campaign CAMPAIGN_TEST_STATS (API)
    When I login with user auto.blippar@gmail.com and password blippar1
    And I go to My Campaigns
    Then I check that there is a campaign card with the name CAMPAIGN_TEST_STATS
    When I open the campaign with the name CAMPAIGN_TEST_STATS
    When I click View Stats
    Then the number of average interactions per user is 0.0 (UI)
    And the number of total interactions for day Now is 0 (UI)
    And the number of unique users is 0 (UI)


  @HUB-44 @assignee:caroline.palmer @COMPLETED @AUTOMATABLE
  Scenario: Verify users with unique link can see shared campaign stats

    Given I login as blippar_admin
    When I go to All Campaigns
    And I open campaign <name>
    And I click View Stats link
    Then I should see campaign <name> stats
    When I click share stats button
    Then I should see a share statistics dashboard popup
    And I should see a unique url
    When I click Copy Link button
    Then the unique url is saved in my clipboard
    When I click Done button
    Then I should not see shared statistics dashboard popup
    And I logout
    When as an outsite_user I open unique url
    Then I should see SHARED DASHBOARD VIEW
    And I should see shared campaign <name> stats
    And I should not see left menu items,  Search, User name and global menu, Breadcrumb trail
    Then the number of average interactions per user is xx (UI)
    And the number of total interactions for day Now is yy (UI)
    And the number of unique users is zz (UI)


  @HUB-44 @assignee:caroline.palmer @COMPLETED
  Scenario: Outside users can interact with shared stats elements

    Given I am an outside_user with shared link
    And I should see SHARED DASHBOARD VIEW
    ###And I can change the date range
    Then I verify all stats are changed accordingly
    When I change Hour/Day switches
    Then the graph changes accordingly
    And I can zoom in/out the map with locations


  @HUB-455 @assignee:gergana.ivanova @COMPLETED @AUTOMATABLE
  Scenario: Verify zero stats of a blipp without interactions - Blipp page

    When I publish blipp with the name BLIPP_TEST_STATS in the campaign CAMPAIGN_TEST_STATS (API)
    When I login with user auto.blippar@gmail.com and password blippar1
    And I go to My Campaigns
    Then I check that there is a campaign card with the name CAMPAIGN_TEST_STATS
    When I open the campaign with the name CAMPAIGN_TEST_STATS
    When I go to Blipp Detail BLIPP_TEST_STATS page
    #issue: No Data Pie Chart at all -https://layardev.atlassian.net/browse/HUB-444
    When I click View Stats
    Then I check that the pie chart is showing NO DATA (UI)
    Then I check that in Interaction Per Blipp table, the blipp has 0 interactions and 0% percentage (UI)

