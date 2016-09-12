Feature: Stats API

  
  This set of scenarios are tests related to api checks for hub API feature. The tests are purely API.
  The scenarios tagged as STATS_API will be executed by daily jenkins jobs.


  Background:
    Given I delete the campaigns with the name campaign_test_stats (API)
    When I create the campaign with the name campaign_test_stats (API)
    And I create the blipp type blipp builder with the name blipp_test_stats, marker image fish1.jpeg in the campaign campaign_test_stats (API)

 
  @ORPHAN @STATS_API
  Scenario: Verify Total Interactions of a published blipp

    When I publish blipp with the name blipp_test_stats in the campaign campaign_test_stats (API)
    Then I check that the status of the blipp blipp_test_stats in the campaign campaign_test_stats is LIVE (API)
    When I send 1 interactions to the blipp blipp_test_stats from campaign campaign_test_stats as user user1 from location Amsterdam on date 2015-09-20 12:35:22 (API)
    And I get the stat interactions of the blipp blipp_test_stats from the date 2015-01-01 to the date 2015-09-22 in the campaign campaign_test_stats (API)
    Then The number of total interactions is 1 (API)


  @ORPHAN @STATS_API
  Scenario: Add interactions in a published blipp, unpublish it and check interactions

    When I publish blipp with the name blipp_test_stats in the campaign campaign_test_stats (API)
    And I send 5 interactions to the blipp blipp_test_stats from campaign campaign_test_stats as user user1 from location Amsterdam on date 2015-09-20 12:35:22 (API)
    And I unpublish blipp with the name blipp_test_stats in the campaign campaign_test_stats (API)
    And I get the stat interactions of the blipp blipp_test_stats from the date 2015-01-01 to the date 2015-09-22 in the campaign campaign_test_stats (API)
    Then the number of total interactions is 5 (API)


  @HUB-453 @assignee:gergana.ivanova @COMPLETED @STATS_API
  Scenario: Check interactions with a blipp republished

    When I publish blipp with the name blipp_test_stats in the campaign campaign_test_stats (API)
    And I send 1 interactions to the blipp blipp_test_stats from campaign campaign_test_stats as user user1 from location Amsterdam on date 2015-09-20 12:35:22 (API)
    And I unpublish blipp with the name blipp_test_stats in the campaign campaign_test_stats (API)
    And I publish blipp with the name blipp_test_stats in the campaign campaign_test_stats (API)
    And I send 1 interactions to the blipp blipp_test_stats from campaign campaign_test_stats as user user1 from location Amsterdam on date 2015-09-20 12:35:22 (API)
    And I get the stat interactions of the blipp blipp_test_stats from the date 2015-01-01 to the date 2015-09-22 in the campaign campaign_test_stats (API)
    Then The number of total interactions is 2 (API)


  @ORPHAN @STATS_API
  Scenario: Verify Blipp Unique Users of an unpublished blipp

    When I get the stat users of the blipp blipp_test_stats from the date 2015-09-01 to the date 2015-09-22 in the campaign campaign_test_stats (API)
    Then the number of total unique users is 0 (API)


  @ORPHAN @STATS_API
  Scenario: Add Unique Users in a published blipp, unpublish it and check Total Unique Users

    When I publish blipp with the name blipp_test_stats in the campaign campaign_test_stats (API)
    And I send 1 interactions to the blipp blipp_test_stats from campaign campaign_test_stats as user user1 from location Amsterdam on date 2015-09-21 12:35:22 (API)
    And I send 2 interactions to the blipp blipp_test_stats from campaign campaign_test_stats as user user2 from location Amsterdam on date 2015-09-19 12:35:22 (API)
    When I unpublish blipp with the name blipp_test_stats in the campaign campaign_test_stats (API)
    When I get the stat users of the blipp blipp_test_stats from the date 2015-09-01 to the date 2015-09-25 in the campaign campaign_test_stats (API)
    Then the number of total unique users is 2 (API)


  @ORPHAN @STATS_API
  Scenario: Check Unique Users with a blipp republished

    When I publish blipp with the name blipp_test_stats in the campaign campaign_test_stats (API)
    When I send 1 interactions to the blipp blipp_test_stats from campaign campaign_test_stats as user user1 from location Amsterdam on date 2015-09-21 12:35:22 (API)
    And I send 2 interactions to the blipp blipp_test_stats from campaign campaign_test_stats as user user2 from location Amsterdam on date 2015-09-19 13:35:20 (API)
    When I unpublish blipp with the name blipp_test_stats in the campaign campaign_test_stats (API)
    And I publish blipp with the name blipp_test_stats in the campaign campaign_test_stats (API)
    When I get the stat users of the blipp blipp_test_stats from the date 2015-08-01 to the date 2015-09-25 in the campaign campaign_test_stats (API)
    Then the number of total unique users is 2 (API)


  @ORPHAN @STATS_API
  Scenario: Verify Blipp Location of Globally Published blipp

    When I publish blipp with the name blipp_test_stats in the campaign campaign_test_stats (API)
    Then I check that the status of the blipp blipp_test_stats in the campaign campaign_test_stats is LIVE (API)
    When I send 1 interactions to the blipp blipp_test_stats from campaign campaign_test_stats as user user1 from location Amsterdam on date 2015-09-20 12:35:22 (API)
    And I send 1 interactions to the blipp blipp_test_stats from campaign campaign_test_stats as user user1 from location Amsterdam on date 2015-09-19 12:35:22 (API)
    And I send 4 interactions to the blipp blipp_test_stats from campaign campaign_test_stats as user user1 from location Sofia on date 2013-09-20 12:35:22 (API)
    And I send 5 interactions to the blipp blipp_test_stats from campaign campaign_test_stats as user user1 from location Buenos Aires on date 2014-09-20 12:35:22 (API)
    When I get the stat locations of the blipp blipp_test_stats from the date 2012-09-10 to the date 2015-09-22 in the campaign campaign_test_stats (API)
    Then The Location is Amsterdam with 2 interactions (API)
    Then The Location is Sofia with 4 interactions (API)
    And The Location is Buenos Aires with 5 interactions (API)


  @ORPHAN @STATS_API
  Scenario: Verify Interactions of a published blipp hourly and daily

    When I publish blipp with the name blipp_test_stats in the campaign campaign_test_stats (API)
    Then I check that the status of the blipp blipp_test_stats in the campaign campaign_test_stats is LIVE (API)
    When I send 1 interactions to the blipp blipp_test_stats from campaign campaign_test_stats as user user1 from location Amsterdam on date 2015-09-20 12:35:22 (API)
    And I send 1 interactions to the blipp blipp_test_stats from campaign campaign_test_stats as user user1 from location Amsterdam on date 2015-09-20 12:40:22 (API)
    And I send 1 interactions to the blipp blipp_test_stats from campaign campaign_test_stats as user user1 from location Amsterdam on date 2015-08-20 2:30:22 (API)
    And I send 1 interactions to the blipp blipp_test_stats from campaign campaign_test_stats as user user1 from location Amsterdam on date 2015-08-20 5:30:22 (API)
    And I send 1 interactions to the blipp blipp_test_stats from campaign campaign_test_stats as user user1 from location Amsterdam on date 2015-07-20 5:03:00 (API)
    And I get the stat interactions of the blipp blipp_test_stats from the date 2015-01-01 to the date 2015-09-22 in the campaign campaign_test_stats (API)
    Then The number of total interactions for hour 12 is 2 (API)
    And The number of total interactions for hour 2 is 1 (API)
    And The number of total interactions for hour 5 is 2 (API)
    And The number of total interactions for day 2015-09-20 is 2 (API)
    And The number of total interactions for day 2015-08-20 is 2 (API)
    And The number of total interactions for day 2015-07-20 is 1 (API)


  @ORPHAN @STATS_API
  Scenario: Interactions Date Ranges Check

    When I publish blipp with the name blipp_test_stats in the campaign campaign_test_stats (API)
    Then I check that the status of the blipp blipp_test_stats in the campaign campaign_test_stats is LIVE (API)
    When I send 1 interactions to the blipp blipp_test_stats from campaign campaign_test_stats as user user1 from location Amsterdam on date 2015-09-20 12:35:22 (API)
    And I send 1 interactions to the blipp blipp_test_stats from campaign campaign_test_stats as user user1 from location Amsterdam on date 2015-08-20 12:35:22 (API)
    And I send 1 interactions to the blipp blipp_test_stats from campaign campaign_test_stats as user user1 from location Amsterdam on date 2014-09-20 12:35:22 (API)
    When I get the stat interactions of the blipp blipp_test_stats from the date 2015-01-01 to the date 2015-09-22 in the campaign campaign_test_stats (API)
    Then the number of total interactions is 2 (API)
    When I get the stat interactions of the blipp blipp_test_stats from the date 2014-01-01 to the date 2015-09-22 in the campaign campaign_test_stats (API)
    Then the number of total interactions is 3 (API)
    When I get the stat interactions of the blipp blipp_test_stats from the date 2015-09-23 to the date 2015-09-23 in the campaign campaign_test_stats (API)
    Then the number of total interactions is 0 (API)


  @ORPHAN @STATS_API
  Scenario: Verify Unique Users of a Published Blipp per hour and day

    When I publish blipp with the name blipp_test_stats in the campaign campaign_test_stats (API)
    Then I check that the status of the blipp blipp_test_stats in the campaign campaign_test_stats is LIVE (API)
    When I send 1 interactions to the blipp blipp_test_stats from campaign campaign_test_stats as user user1 from location Amsterdam on date 2015-09-20 12:35:22 (API)
    And I send 2 interactions to the blipp blipp_test_stats from campaign campaign_test_stats as user user2 from location Amsterdam on date 2015-09-20 12:40:22 (API)
    And I send 1 interactions to the blipp blipp_test_stats from campaign campaign_test_stats as user user3 from location Amsterdam on date 2015-08-20 2:30:22 (API)
    When I get the stat users of the blipp blipp_test_stats from the date 2015-08-20 to the date 2015-09-20 in the campaign campaign_test_stats (API)
    Then the number of unique users for hour 12 is 2 (API)
    Then the number of unique users for hour 2 is 1 (API)
    Then the number of unique users for day 2015-09-20 is 2 (API)


  @ORPHAN @STATS_API
  Scenario: Verify Blipp interactions of an unpublished blipp

    When I get the stat interactions of the blipp blipp_test_stats from the date 2015-09-01 to the date 2015-09-22 in the campaign campaign_test_stats (API)
    Then the number of total interactions is 0 (API)


  @ORPHAN @STATS_API
  Scenario: Campaign stats (interactions/users/locations) with multiple blipps

    When I create the blipp type blipp builder with the name blipp_test_stats_2, marker image fish1.jpeg in the campaign campaign_test_stats (API)
    And I publish blipp with the name blipp_test_stats in the campaign campaign_test_stats (API)
    And I publish blipp with the name blipp_test_stats_2 in the campaign campaign_test_stats (API)
    And I send 2 interactions to the blipp blipp_test_stats from campaign campaign_test_stats as user user1 from location Amsterdam on date 2015-09-20 12:35:22 (API)
    And I send 3 interactions to the blipp blipp_test_stats_2 from campaign campaign_test_stats as user user3 from location Sofia on date 2015-09-22 12:35:22 (API)
    When I get the stat interactions of the campaign campaign_test_stats from the date 2015-08-20 to the date 2015-09-25 (API)
    Then the number of total interactions is 5 (API)
    When I get the stat users of the campaign campaign_test_stats from the date 2015-08-20 to the date 2015-09-25 (API)
    Then the number of total unique users is 2 (API)
    When I get the stat locations of the campaign campaign_test_stats from the date 2015-08-20 to the date 2015-09-25 (API)
    Then The Location is Amsterdam with 2 interactions (API)
    And The Location is Sofia with 3 interactions (API)


  @ORPHAN @SHARED_STATS @STATS_API
  Scenario Outline: Verify Shared Campaign stats as an outside user when posted from Blippar users

    When I publish blipp with the name blipp_test_stats in the campaign campaign_test_stats (API)
    And I send 3 interactions to the blipp blipp_test_stats from campaign campaign_test_stats as user user3 from location Sofia on date Now (API)
    When I get the stat interactions of the campaign campaign_test_stats from the date 2015-08-20 to the date Now (API)
    Then the number of total interactions is 3 (API)
    When As <role> I get the complete shared stats interactions of the campaign campaign_test_stats from the date 2015-08-20 to the date Now (API)
    Then the number of total interactions is 3 (API)
    When As <role> I get the complete shared stats users of the campaign campaign_test_stats from the date 2015-08-20 to the date Now (API)
    Then the number of total unique users is 1 (API)
    When As <role> I get the complete shared stats locations of the campaign campaign_test_stats from the date 2015-08-20 to the date Now (API)
    Then The Location is Sofia with 3 interactions (API)
    Examples:
      | role          |
      | blippar_user  |
      | blippar_admin |
      | normal_user   |
      | group_admin   |


  @ORPHAN @SHARED_STATS @STATS_API
  Scenario: Shared Campaign stats with bad token will get permission errors

    When I publish blipp with the name blipp_test_stats in the campaign campaign_test_stats (API)
    And I send 3 interactions to the blipp blipp_test_stats from campaign campaign_test_stats as user user3 from location Sofia on date Now (API)
    When As blippar_admin I get the incomplete shared stats interactions of the campaign campaign_test_stats from the date 2015-08-20 to the date Now (API)

