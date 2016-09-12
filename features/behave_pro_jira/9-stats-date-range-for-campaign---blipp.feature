Feature: Stats date range for Campaign - Blipp

  
  Verify and Select date range for selected campaign and blipps
  Verify data displayed for selected date range for

 
  @ORPHAN @AUTOMATABLE @STATS
  Scenario: Verify and Select date range for Campaign Stats

    #Navigate to the stats page
    Given that I am Blippar Admin
    When Log in to the Dashboard
    And navigate to the stats for campaign {campaign_name}
    Then I check that the Campaign {campaign_name} stats page is open
    #Select date range for campaign
    Then I check that the date range is starting from {Publish Date} (API)
    And I check that the date range is ending at {today’s date}
    When I click on the date picker field
    And I select any date range between the Publish Date and Today’s Date
    #Total Interactions & Total Unique Users
    Then I check that {total_interactions}, {total_unique_users} are updated in UI accordingly (API verification based on dates and compare with displayed date in UI)
    #Chart data
    And {daily} and {hourly} data is updated on Chart for User and Interaction
    #Map data
    And location of User interactions are updated
    #Interactions per Blipp / Marker breakdown
    And I check that the {blipp_name} has Interactions and Percentage updated (API)


  @ORPHAN @AUTOMATABLE @STATS
  Scenario: Verify and Select date range for Blipp Stats

    #Navigate to stats page for Blipp
    Given that I am Blippar Admin
    When Log in to the Dashboard
    And Open the Campaign {campaign_name}
    And navigate to the stats for blipp {blipp_name)
    Then I check that blipp {blipp_name} stats page is open
    #Select date range for campaign
    Then I check that the date range is starting from {publish_date} (API)
    And I check that the date range is ending at {today’s date}
    When I click on the date picker field
    And I select any date range between the Publish Date and Today’s Date
    #Total Interactions & Total Unique Users
    Then I check that {total_interactions}, {total_unique_users} are updated in UI accordingly (API verification based on dates and compare with displayed date in UI)
    #Chart data
    And {daily} and {hourly} data is updated on Chart for User and Interaction
    #Map data
    And location of User interactions are updated
    #Interactions per Blipp / Marker breakdown - Not displayed for Blipp level stats
    And I check that there is no Interaction per Blipp data displayed for the {blipp_name}

