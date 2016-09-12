Feature: Barcode and some duplicate blipp tests - UI

 
  @HUB-430 @assignee:caroline.palmer @COMPLETED @AUTOMATABLE
  Scenario: Barcode assigned to custom blipp - UI

    Given that the barcode is assigned to the custom blipp through zip file
    And the zip file is uploaded and the blipp is created on HUB
    When test/publish the blipp
    And navigate to the Blipp detail page
    Then you should be able to see Barcode placeholder images same as how other markers are displayed


  @HUB-430 @assignee:caroline.palmer @COMPLETED @BARCODE @SANITY
  Scenario Outline: Barcode blipp - UI

    #Login and cleanup
    When I login with user <user> and password <password>
    Then The user <user_name> is logged in
    When I go to My Campaigns
    Then The screen My campaigns is opened
    When I delete the campaign BEHAVE BARCODE_CAMPAIGN
    #When I delete all the campaigns
    Then I check that there are not campaigns cards with the name BEHAVE BARCODE_CAMPAIGN
    #Campaign and blipp creation
    When I create the campaign with the name BEHAVE BARCODE_CAMPAIGN
    Then The screen BEHAVE BARCODE_CAMPAIGN is opened
    When I click on Create Bespoke blipp button
    Then The modal Create blipp is opened
    And The modal step Name is active
    When Creating my blipp I give it the name BEHAVE BARCODE_BLIPP
    And Creating my blipp I upload the zip barcode.zip
    # And I add additional data that will trigger a blipp, next to the detect marker(s)
    And I click on next
    Then The modal step Publish is active
    When Creating my blipp I select Make your blipp live: choose countries
    And I choose GB as the country
    And I click on publish blipp
    Then I check that the blipp with the name BEHAVE BARCODE_BLIPP is created
    When I go to Blipp Detail BEHAVE BARCODE_BLIPP page
    Then I can see Barcode numbers
    Examples:
      | user                               | password| user_name     |
      | auto.blippar+blippar_user@gmail.com| blippar1| Blippar User  |
      | auto.blippar@gmail.com             | blippar1| Blippar Admin |


  @ORPHAN @BARCODE
  Scenario Outline: Metadata json blipp - UI

    #Login and cleanup
    When I login with user <user> and password <password>
    Then The user <user_name> is logged in
    When I go to My Campaigns
    Then The screen My campaigns is opened
    When I delete the campaign BEHAVE BARCODE_CAMPAIGN
    #When I delete all the campaigns
    Then I check that there are not campaigns cards with the name BEHAVE BARCODE_CAMPAIGN
    #Campaign and blipp creation
    When I create the campaign with the name BEHAVE BARCODE_CAMPAIGN
    Then The screen BEHAVE BARCODE_CAMPAIGN is opened
    When I click on Create Bespoke blipp button
    Then The modal Create blipp is opened
    And The modal step Name is active
    When Creating my blipp I give it the name BEHAVE BARCODE_BLIPP
    And Creating my blipp I upload the zip metadata.zip
    # And I add additional data that will trigger a blipp, next to the detect marker(s)
    And I click on next
    Then The modal step Publish is active
    When Creating my blipp I select Make your blipp live: choose countries
    And I choose GB as the country
    And I click on publish blipp
    Then I check that the blipp with the name BEHAVE BARCODE_BLIPP is created
    When I go to Blipp Detail BEHAVE BARCODE_BLIPP page
    Then I can see Barcode numbers
    Examples:
     | user                               | password| user_name     |
     | auto.blippar+blippar_user@gmail.com| blippar1| Blippar User  |
     | auto.blippar@gmail.com             | blippar1| Blippar Admin |


  @ORPHAN @BARCODE @DUPLICATE_BLIPP
  Scenario Outline: Duplicate Blippbuilder blipp with many assets (UI)

    #Precondition - do NOT delete 2_ASSETS
    When I login with user <user> and password <password>
    Then The user <user_name> is logged in
    When I go to My Campaigns
    Then The screen My campaigns is opened
    Then I check that there is a campaign card with the name 2_ASSETS
    When I open the campaign with the name 2_ASSETS
    Then The screen 2_ASSETS is opened
    Then I check that the blipp with the name 2_ASSETS_BLIPP is there (UI)
    Then I click on More option button on blipp 2_ASSETS_BLIPP (UI)
    And I click on Duplicate button on the blipp (UI)
    Then I write the name as COPY_OF_2_ASSETS_BLIPP (UI)
    When Duplicating my blipp I upload the marker birds.jpg
    Then I check that the status of the blipp 2_ASSETS_BLIPP detail page is Draft (UI)
    When back to the previous page
    Then I check that the blipp with the name COPY_OF_2_ASSETS_BLIPP is there (UI)
    #step for removing the duplicated blipp so every time when run the test the duplicated blipp will be only one
    When I delete the blipp COPY_OF_2_ASSETS_BLIPP
    Examples:
      | user                             | password | user_name     |
      | auto.blippar@gmail.com           | blippar1 | Blippar Admin |
      | auto.blippar+superadmin@gmail.com| blippar1 | Blippar Super_Admin |

