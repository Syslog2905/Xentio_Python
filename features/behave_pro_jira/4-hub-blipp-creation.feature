Feature: Hub blipp creation

  
  Tests related to blipps creation and publishing. The tests are UI and they use selenium.
  Scenarios tagged as HUB will be executed by daily jenkins jobs.

 
  @ORPHAN @PUBLISHING @SANITY
  Scenario: Create Bespoke blipp and publish it on a test code with role Blippar Admin

    #Login and cleanup
    When I login with user auto.blippar@gmail.com and password blippar1
    Then The user Blippar Admin is logged in
    When I go to My Campaigns
    Then The screen My campaigns is opened
    When I delete the campaign BEHAVE CAMPAIGN
    Then I check that there are not campaigns cards with the name BEHAVE CAMPAIGN
    #Campaign and blipp creation
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
    # Bug: https://trello.com/c/uODr7qO6/472-custom-blipp-creation-blipp-status-is-not-updated-post-creation
    # Then I check that the blipp with the name BEHAVE BESPOKE_BLIPP_GLOBAL has the status Live
    # Instead, go to blipp-detail page:
    When I go to Blipp Detail BEHAVE BESPOKE_BLIPP_TEST page
    Then The Latest Version should have the status In Progress
    When back to the previous page


  @ORPHAN @PRODUCTION_CHECK @PUBLISHING @SANITY
  Scenario: Create Bespoke blipp and publish it globally with role Blippar Admin

    #Login and cleanup
    When I login with user auto.blippar@gmail.com and password blippar1
    Then The user Blippar Admin is logged in
    When I go to My Campaigns
    Then The screen My campaigns is opened
    When I delete the campaign BEHAVE CAMPAIGN
    Then I check that there are not campaigns cards with the name BEHAVE CAMPAIGN
    #Campaign and blipp creation
    When I create the campaign with the name BEHAVE CAMPAIGN
    Then The screen BEHAVE CAMPAIGN is opened
    When I click on Create Bespoke blipp button
    Then The modal Create blipp is opened
    And The modal step Name is active
    When Creating my blipp I give it the name BEHAVE BESPOKE_BLIPP_GLOBAL
    And Creating my blipp I upload the zip blipp.zip
    And I click on next
    Then The modal step Publish is active
    When Creating my blipp I select Make your blipp live: global
    And I click on publish blipp
    Then I check that the blipp with the name BEHAVE BESPOKE_BLIPP_GLOBAL is created
    # Bug: https://trello.com/c/uODr7qO6/472-custom-blipp-creation-blipp-status-is-not-updated-post-creation
    # Then I check that the blipp with the name BEHAVE BESPOKE_BLIPP_GLOBAL has the status Live
    # Instead, go to blipp-detail page:
    When I go to Blipp Detail BEHAVE BESPOKE_BLIPP_GLOBAL page
    Then The Latest Version should have the status Live
    When back to the previous page


  @ORPHAN @PUBLISHING @SANITY
  Scenario: Create Bespoke blipp, publish it to a region and unpublish it with role Blippar Admin

    #Login and cleanup
    When I login with user auto.blippar@gmail.com and password blippar1
    Then The user Blippar Admin is logged in
    When I go to My Campaigns
    Then The screen My campaigns is opened
    When I delete the campaign BEHAVE CAMPAIGN
    Then I check that there are not campaigns cards with the name BEHAVE CAMPAIGN
    #Campaign & blipp creation
    When I create the campaign with the name BEHAVE CAMPAIGN
    Then The screen BEHAVE CAMPAIGN is opened
    When I click on Create Bespoke blipp button
    Then The modal Create blipp is opened
    And The modal step Name is active
    When Creating my blipp I give it the name BEHAVE BESPOKE_BLIPP_GB
    And Creating my blipp I upload the zip blipp.zip
    And I click on next
    Then The modal step Publish is active
    When Creating my blipp I select Make your blipp live: choose countries
    And I choose GB as the country
    And I click on publish blipp
    Then I check that the blipp with the name BEHAVE BESPOKE_BLIPP_GB is created
    When I go to Blipp Detail BEHAVE BESPOKE_BLIPP_GB page
    Then The Latest Version should have the status Live
    Then The blipp must have 1 versions
    #Unpublish
    When I unpublish the latest version of the blipp
    Then The Latest Version should have the status Unpublished


  @HUB-446 @assignee:gergana.ivanova @COMPLETED @BLIPP_CREATION @PRODUCTION_CHECK @SANITY
  Scenario: Create BlippBuilder blipp with role managed normal user

    When I login with user auto.blippar+group_user@gmail.com and password blippar1
    Then The user Hub GroupUser is logged in
    When I go to My Campaigns
    Then The screen My campaigns is opened
    When I delete the campaign BEHAVE CAMPAIGN
    Then I check that there are not campaigns cards with the name BEHAVE CAMPAIGN
    When I create the campaign with the name BEHAVE CAMPAIGN
    Then The screen BEHAVE CAMPAIGN is opened
    When I click on Create Blipp default button
    Then The modal Create new blipp is opened
    When Creating my blipp I give it the name BEHAVE BUILDER_BLIPP
    And Creating my blipp I upload the marker marker.png
    And I click in back button from blippbuilder
    Then I check that the blipp with the name BEHAVE BUILDER_BLIPP is created


  @ORPHAN @BLIPP_CREATION
  Scenario: Create/Delete new Bespoke blipp version on a test code with role managed normal user

    #Login and cleanup
    When I login with user auto.blippar+blippar_user1@gmail.com and password blippar1
    Then The user Blippar User is logged in
    When I go to My Campaigns
    Then The screen My campaigns is opened
    When I delete the campaign BEHAVE CAMPAIGN
    Then I check that there are not campaigns cards with the name BEHAVE CAMPAIGN
    #Campaign & blipp creation
    When I create the campaign with the name BEHAVE CAMPAIGN
    Then The screen BEHAVE CAMPAIGN is opened
    When I click on Create Bespoke blipp button
    Then The modal Create new blipp is opened
    And The modal step Name is active
    When Creating my blipp I give it the name BEHAVE BESPOKE_BLIPP_TEST
    And Creating my blipp I upload the zip blipp.zip
    And I click on next
    Then The modal step Publish is active
    When Creating my blipp I enter the test code btest
    And I click on test blipp
    Then I check that the blipp with the name BEHAVE BESPOKE_BLIPP_TEST is created
    # Bug: https://trello.com/c/uODr7qO6/472-custom-blipp-creation-blipp-status-is-not-updated-post-creation
    # Then I check that the blipp with the name BEHAVE BESPOKE_BLIPP_GLOBAL has the status Live
    # Instead, go to blipp-detail page:
    When I go to Blipp Detail BEHAVE BESPOKE_BLIPP_TEST page
    #Refreshing the page to update version info in the screen, workaround to avoid HUB-1210
    And I refresh the page
    Then The blipp must have 1 versions
    And The Latest Version should have the status In Progress
    #Adding a new version
    When I click on new version
    Then The modal Create new version is opened
    And The modal step Blipp Zip is active
    When Creating my blipp I upload the zip blipp.zip
    And I click on next
    Then The modal step Publish is active
    When Creating my blipp I enter the test code btest
    And I click on test blipp
    #Refreshing the page to update version info in the screen, workaround to avoid HUB-1210
    And I refresh the page
    Then The blipp must have 2 versions
    And The Latest Version should have the status In Progress


  @ORPHAN @PUBLISHING
  Scenario: Create/Delete new Bespoke blipp version and publish into a region as a Blippar Admin

    #Login and cleanup
    When I login with user auto.blippar@gmail.com and password blippar1
    Then The user Blippar Admin is logged in
    When I go to My Campaigns
    Then The screen My campaigns is opened
    When I delete the campaign BEHAVE CAMPAIGN
    Then I check that there are not campaigns cards with the name BEHAVE CAMPAIGN
    #Campaign & blipp creation
    When I create the campaign with the name BEHAVE CAMPAIGN
    Then The screen BEHAVE CAMPAIGN is opened
    When I click on Create Bespoke blipp button
    Then The modal Create new blipp is opened
    And The modal step Name is active
    When Creating my blipp I give it the name BEHAVE BESPOKE_BLIPP_TEST
    And Creating my blipp I upload the zip blipp.zip
    And I click on next
    Then The modal step Publish is active
    When Creating my blipp I select Make your blipp live: choose countries
    And I choose GB as the country
    And I click on publish blipp
    Then I check that the blipp with the name BEHAVE BESPOKE_BLIPP_TEST is created
    # Bug: https://trello.com/c/uODr7qO6/472-custom-blipp-creation-blipp-status-is-not-updated-post-creation
    # Then I check that the blipp with the name BEHAVE BESPOKE_BLIPP_GLOBAL has the status Live
    # Instead, go to blipp-detail page:
    When I go to Blipp Detail BEHAVE BESPOKE_BLIPP_TEST page
    #Refreshing the page to update version info in the screen, workaround to avoid HUB-1210
    And I refresh the page
    Then The blipp must have 1 versions
    And The Latest Version should have the status In Progress
    #Adding a new version
    When I click on new version
    Then The modal Create new version is opened
    And The modal step Blipp Zip is active
    When Creating my blipp I upload the zip blipp.zip
    And I click on next
    Then The modal step Publish is active
    When Creating my blipp I select Make your blipp live: choose countries
    And I choose GB as the country
    And I click on publish blipp
    #Refreshing the page to update version info in the screen, workaround to avoid HUB-1210
    And I refresh the page
    Then The blipp must have 2 versions
    And The Latest Version should have the status In Progress


  @ORPHAN @BLIPP_CREATION
  Scenario: Delete a Bespoke blipp with many versions as a Blippar Admin

    #Login and cleanup
    When I login with user auto.blippar@gmail.com and password blippar1
    Then The user Blippar Admin is logged in
    When I go to My Campaigns
    Then The screen My campaigns is opened
    When I delete the campaign BEHAVE CAMPAIGN
    Then I check that there are not campaigns cards with the name BEHAVE CAMPAIGN
    #Campaign & blipp creation
    When I create the campaign with the name BEHAVE CAMPAIGN
    Then The screen BEHAVE CAMPAIGN is opened
    When I click on Create Bespoke blipp button
    Then The modal Create new blipp is opened
    And The modal step Name is active
    When Creating my blipp I give it the name BEHAVE BESPOKE_BLIPP_TEST
    And Creating my blipp I upload the zip blipp.zip
    And I click on next
    Then The modal step Publish is active
    When Creating my blipp I select Make your blipp live: choose countries
    And I choose GB as the country
    And I click on publish blipp
    Then I check that the blipp with the name BEHAVE BESPOKE_BLIPP_TEST is created
    # Bug: https://trello.com/c/uODr7qO6/472-custom-blipp-creation-blipp-status-is-not-updated-post-creation
    # Then I check that the blipp with the name BEHAVE BESPOKE_BLIPP_GLOBAL has the status Live
    # Instead, go to blipp-detail page:
    When I go to Blipp Detail BEHAVE BESPOKE_BLIPP_TEST page
    #Refreshing the page to update version info in the screen, workaround to avoid HUB-1210
    And I refresh the page
    Then The blipp must have 1 versions
    And The Latest Version should have the status In Progress
    #Adding 2 new versions
    When I click on new version
    Then The modal Create new version is opened
    And The modal step Blipp Zip is active
    When Creating my blipp I upload the zip blipp.zip
    And I click on next
    Then The modal step Publish is active
    When Creating my blipp I select Make your blipp live: choose countries
    And I choose GB as the country
    And I click on publish blipp
    When I click on new version
    Then The modal Create new version is opened
    And The modal step Blipp Zip is active
    When Creating my blipp I upload the zip blipp.zip
    And I click on next
    Then The modal step Publish is active
    When Creating my blipp I select Make your blipp live: choose countries
    And I choose GB as the country
    And I click on publish blipp
    #Refreshing the page to update version info in the screen, workaround to avoid HUB-1210
    And I refresh the page
    Then The blipp must have 3 versions
    And The Latest Version should have the status In Progress
    #Deleting the blipp
    When I go to My Campaigns
    Then The screen My campaigns is opened
    When I open the campaign with the name BEHAVE CAMPAIGN
    And I delete the blipp BEHAVE BESPOKE_BLIPP_TEST
    Then I check that there are not blipp cards with the name BEHAVE BESPOKE_BLIPP_TEST


  @ORPHAN @AUTOMATABLE
  Scenario: Create a blipp as normal user and approve publishing it using admin user

    When I delete the campaigns with the name GROUP_USER_CAMPAIGN (API)
    When I login with user evelin3933@gmail.com and password gerg456ivaN
    Then the user Blipp Approval Waiting is logged in
    When I go to My Campaigns
    Then the screen My campaigns is opened
    When I create the campaign with the name GROUP_USER_CAMPAIGN
    Then The screen GROUP_USER_CAMPAIGN is opened
    When I click on Create BlippBuilder blipp button as a normal user
    Then The modal Create new blipp is opened
    When Creating my blipp I give it the name BLIPP_GROUP_USER
    And Creating my blipp I upload the marker flowers.jpg
    And I click on next
    Then The modal step Publish is active
    When Creating my blipp I select Make your blipp live: choose countries
    And I choose GB as the country
    And I click on publish blipp
    And I click in back button from blippbuilder
    Then I check that the blipp with the name BLIPP_GROUP_USER is created
    When I go to Blipp Detail BLIPP_GROUP_USER page
    #When I click on publish blipp
    Then The Latest Version should have the status APPROVAL
    # Then I check that the blipp with the name BLIPP_GROUP_USER has small.ng-binding with the text "Gerry users waiting for blipps approval"
    When I login with user gergana.ivanova@blippar.com and password gerg456ivan
    Then the user Gergana Ivanova is logged in
    When I go to All Campaigns
    When I open the campaign with the name GROUP_USER_CAMPAIGN
    Then The screen GROUP_USER_CAMPAIGN is opened
    And I wait to see modal dialog Publish Your Blipp (UI)
    When I publish blipp with the name BLIPP_GROUP_USER in the campaign GROUP_USER_CAMPAIGN globally (UI)
    When I go to Blipp Detail BLIPP_GROUP_USER page
    Then I check that the blipp with the name BLIPP_GROUP_USER has the status LIVE


  @HUB-197 @assignee:caroline.palmer @COMPLETED @DUPLICATE_BLIPP
  Scenario Outline: Duplicate Blippbuilder blipp with new marker (UI) with different users roles

    #Precondition - do NOT delete CAMPAIGN_TEST_STATS_1 for different user roles
    When I login with user <user> and password <password>
    Then The user <user_name> is logged in
    When I go to My Campaigns
    Then The screen My campaigns is opened
    Then I check that there is a campaign card with the name CAMPAIGN_TEST_STATS_1
    When I open the campaign with the name CAMPAIGN_TEST_STATS_1
    Then The screen CAMPAIGN_TEST_STATS_1 is opened
    Then I check that the blipp with the name BLIPP_TEST_STATS is there (UI)
    Then I click on More option button on blipp BLIPP_TEST_STATS (UI)
    And I click on Duplicate button on the blipp (UI)
    Then I write the name as COPY_OF_BLIPP_TEST_STATS (UI)
    When Duplicating my blipp I upload the marker flowers.jpg
    Then I check that the status of the blipp BLIPP_TEST_STATS detail page is Draft (UI)
    #Restore initial test state
    When back to the previous page
    Then I check that the blipp with the name COPY_OF_BLIPP_TEST_STATS is there (UI)
    When I delete the blipp COPY_OF_BLIPP_TEST_STATS
    Examples:
     | user                               | password| user_name        |
     |auto.blippar@gmail.com              |blippar1 |Blippar Admin     |
     |auto.blippar+blippar_user1@gmail.com|blippar1 |Blippar User      |
     |auto.blippar+group_admin@gmail.com  |blippar1 |Blippar GroupAdmin|
     |auto.blippar+group_user@gmail.com   |blippar1 |Hub GroupUser     |
     |auto.blippar+superadmin@gmail.com   |blippar1 |Blippar Super_Admin|


  @HUB-197 @assignee:caroline.palmer @COMPLETED @AUTOMATABLE
  Scenario: Duplicate Blippbuilder blipp with new marker and publish it as a normal user

    When I login with user auto.blippar+blippar_user1@gmail.com and password blippar1
    Then The user Blippar User is logged in
    When I go to My Campaigns
    Then The screen My campaigns is opened
    Then I check that there is a campaign card with the name CAMPAIGN_TEST_STATS_1
    When I open the campaign with the name CAMPAIGN_TEST_STATS_1
    Then The screen CAMPAIGN_TEST_STATS_1 is opened
    Then I check that the blipp with the name BLIPP_TEST_STATS is there (UI)
    Then I click on More option button on blipp BLIPP_TEST_STATS (UI)
    And I click on Duplicate button on the blipp (UI)
    Then I write the name as COPY_OF_BLIPP_TEST_STATS (UI)
    When Duplicating my blipp I upload the marker flowers.jpg
    Then I check that the status of the blipp BLIPP_TEST_STATS detail page is Draft (UI)
    When back to the previous page
    Then I check that the blipp with the name COPY_OF_BLIPP_TEST_STATS is there (UI)
    When I go to Blipp Detail COPY_OF_BLIPP_TEST_STATS page
    Then The Latest Version should have the status UNPUBLISHED
    When I go to All Campaigns
    When I open the campaign with the name CAMPAIGN_TEST_STATS_1
    Then The screen CAMPAIGN_TEST_STATS is opened
    And I click on More option button on blipp COPY_OF_BLIPP_TEST_STATS (UI)
    #when duplicate blipp its state can not be LIVE so I need to publish it and it is possible ONLY through API
    And I wait to see modal dialog Publish Your Blipp (UI)
    #the next step is failing currently as the functionality is still not implemented
    When I publish blipp with the name COPY_OF_BLIPP_TEST_STATS in the campaign CAMPAIGN_TEST_STATS_1 globally (UI)
    When I go to Blipp Detail COPY_OF_BLIPP_TEST_STATS page
    Then I check that the blipp with the name COPY_OF_BLIPP_TEST_STATS has the status LIVE


  @ORPHAN @BLIPP_CREATION
  Scenario: Cancel Duplicate Blippbuilder blipp with new marker - negative test as a Blipp Admin

    #Precondition - do NOT delete CAMPAIGN_TEST_STATS_1
    When I login with user auto.blippar@gmail.com and password blippar1
    Then The user Blippar Admin is logged in
    When I go to My Campaigns
    Then The screen My campaigns is opened
    Then I check that there is a campaign card with the name CAMPAIGN_TEST_STATS_1
    When I open the campaign with the name CAMPAIGN_TEST_STATS_1
    Then The screen CAMPAIGN_TEST_STATS_1 is opened
    Then I check that the blipp with the name BLIPP_TEST_STATS is there (UI)
    Then I click on More option button on blipp BLIPP_TEST_STATS (UI)
    And I click on Duplicate button on the blipp (UI)
    Then I write the name as COPY_OF_BLIPP_TEST_STATS (UI)
    Then I cancel uploading
    When back to the previous page
    Then the page title must be My campaigns | Blippar Dashboard


  @ORPHAN @DUPLICATE_BLIPP
  Scenario: Close Duplicate Blippbuilder blipp with new marker - negative test as a Blipp Admin

    #Precondition - do NOT delete CAMPAIGN_TEST_STATS_1
    When I login with user auto.blippar@gmail.com and password blippar1
    Then The user Blippar Admin is logged in
    When I go to My Campaigns
    Then The screen My campaigns is opened
    Then I check that there is a campaign card with the name CAMPAIGN_TEST_STATS_1
    When I open the campaign with the name CAMPAIGN_TEST_STATS_1
    Then The screen CAMPAIGN_TEST_STATS_1 is opened
    Then I check that the blipp with the name BLIPP_TEST_STATS is there (UI)
    Then I click on More option button on blipp BLIPP_TEST_STATS (UI)
    And I click on Duplicate button on the blipp (UI)
    Then I write the name as COPY_OF_BLIPP_TEST_STATS (UI)
    Then I close uploading
    When back to the previous page
    Then the page title must be My campaigns | Blippar Dashboard


  @ORPHAN @DUPLICATE_BLIPP
  Scenario: Тhe duplicated blipp is not updated after the original data is changed as a Blipp Admin

    When I delete the campaigns with the name CAMPAIGN_CHANGE_SOURCE (API)
    When I create the campaign with the name CAMPAIGN_CHANGE_SOURCE (API)
    And I create the blipp type blipp builder with the name BLIPP_CHANGE, marker image Airplane.JPG in the campaign CAMPAIGN_CHANGE_SOURCE (API)
    When I publish blipp with the name BLIPP_CHANGE in the campaign CAMPAIGN_CHANGE_SOURCE (API)
    When I login with user auto.blippar@gmail.com and password blippar1
    Then The user Blippar Admin is logged in
    When I go to My Campaigns
    Then The screen My campaigns is opened
    Then I check that there is a campaign card with the name CAMPAIGN_CHANGE_SOURCE
    When I open the campaign with the name CAMPAIGN_CHANGE_SOURCE
    Then The screen CAMPAIGN_CHANGE_SOURCE is opened
    Then I check that the blipp with the name BLIPP_CHANGE is there (UI)
    Then I click on More option button on blipp BLIPP_CHANGE (UI)
    And I click on Duplicate button on the blipp (UI)
    Then I write the name as COPY_OF_BLIPP_CHANGE (UI)
    When Duplicating my blipp I upload the marker flowers.jpg
    Then I check that the status of the blipp COPY_OF_BLIPP_CHANGE detail page is Draft (UI)
    When back to the previous page
    Then I check that the blipp with the name COPY_OF_BLIPP_CHANGE is there (UI)
    Then I check that the blipp with the name BLIPP_CHANGE is there (UI)
    Then I check that the status of the blipp BLIPP_CHANGE in the campaign CAMPAIGN_CHANGE_SOURCE is LIVE (API)
    When I rename blipp BLIPP_CHANGE from campaign CAMPAIGN_CHANGE_SOURCE into blipp BLIPP_CHANGE_NEW (API)
    When back to the previous page
    Then I check that the blipp with the name BLIPP_CHANGE_NEW is there (UI)
    And I check that the blipp with the name COPY_OF_BLIPP_CHANGE is there (UI)


  @ORPHAN @DUPLICATE_BLIPP
  Scenario: Duplicate Blippbuilder blipp with default name as a normal user

    #Precondition - the campaign CHECK_DUPLICATED_BLIPP_NAME with the blipp DEFAULT_NAME
    When I login with user auto.blippar+blippar_user1@gmail.com and password blippar1
    Then The user Blippar User is logged in
    When I go to My Campaigns
    Then The screen My campaigns is opened
    Then I check that there is a campaign card with the name CHECK_DUPLICATED_BLIPP_NAME
    When I open the campaign with the name CHECK_DUPLICATED_BLIPP_NAME
    Then The screen CHECK_DUPLICATED_BLIPP_NAME is opened
    Then I check that the blipp with the name DEFAULT_NAME is there (UI)
    Then I click on More option button on blipp DEFAULT_NAME (UI)
    And I click on Duplicate button on the blipp (UI)
    When Duplicating my blipp I upload the marker flowers.jpg
    Then I check that the status of the blipp COPY_OF_BLIPP_CHANGE detail page is Draft (UI)
    Then I can see duplicated Blipp name
    #Restore initial test state
    When back to the previous page
    Then I check that the blipp with the name COPY OF DEFAULT_NAME is there (UI)
    When I delete the blipp COPY OF DEFAULT_NAME


  @ORPHAN @AUTOMATABLE
  Scenario Outline: Unpublish duplicated live Blippbuilder blipp

    #Precondition - do NOT delete UNPUBLISH_PUBLISHED_DUPL_BLIPP for different user roles
    When I login with user <user> and password <password>
    Then The user <user_name> is logged in
    When I go to My Campaigns
    Then the screen My campaigns is opened
    Then I check that there is a campaign card with the name UNPUBLISH_PUBLISHED_DUPL_BLIPP
    When I open the campaign with the name UNPUBLISH_PUBLISHED_DUPL_BLIPP
    Then The screen UNPUBLISH_PUBLISHED_DUPL_BLIPP is opened
    When I go to Blipp Detail COPY_OF_DUPL_BB page
    Then I check that the status of the blipp COPY_OF_DUPL_BB detail page is LIVE (UI)
    #Unpublish
    When I unpublish the latest version of the blipp
    Then I check that the status of the blipp COPY_OF_DUPL_BB detail page is UNPUBLISHED (UI)
    #Restore predefined initial condition of the test so Jenkins runs will not fail
    When I go to My Campaigns
    Then the screen My campaigns is opened
    When I open the campaign with the name UNPUBLISH_PUBLISHED_DUPL_BLIPP
    Then The screen UNPUBLISH_PUBLISHED_DUPL_BLIPP is opened
    And I click on More option button on blipp COPY_OF_DUPL_BB (UI)
    And I wait to see modal dialog Publish Your Blipp (UI)
    When I publish blipp with the name COPY_OF_DUPL_BB globally (UI)
    When I go to Blipp Detail COPY_OF_DUPL_BB page
    Then I check that the blipp with the name COPY_OF_DUPL_BB has the status LIVE #research def get_blipp_card(context, name) as this steps failt due to it
    Examples:
      | user                  | password | user_name    |
      | auto.blippar@gmail.com| blippar1 | Blippar Admin|


  @HUB-112 @assignee:leonardo.santagada @COMPLETED @BLIPP_CREATION
  Scenario: Check MarkerParams DetectMode on a Bespoke blipp via API and UI HUB-112 as Blipp Admin

    #Login and cleanup
    When I login with user auto.blippar@gmail.com and password blippar1
    Then The user Blippar Admin is logged in
    When I go to My Campaigns
    Then The screen My campaigns is opened
    When I delete the campaign MARKERPARAMS_CAMPAIGN
    Then I check that there are not campaigns cards with the name MARKERPARAMS_CAMPAIGN
    #Campaign & blipp creation
    When I create the campaign with the name MARKERPARAMS_CAMPAIGN
    Then The screen MARKERPARAMS_CAMPAIGN is opened
    When I click on Create Bespoke blipp button
    Then The modal Create new blipp is opened
    And The modal step Name is active
    When Creating my blipp I give it the name MARKERPARAMS_BLIPP_TEST
    And Creating my blipp I upload the zip markerparams_hub112.zip
    And I click on next
    Then The modal step Publish is active
    When Creating my blipp I select Make your blipp live: choose countries
    And I choose GB as the country
    And I click on publish blipp
    Then I check that the blipp with the name MARKERPARAMS_BLIPP_TEST is created
    #Next 2 steps are commented as the API is unreachable on PRODUCTION
    #When I get DetectMode markeparams of the blipp MARKERPARAMS_BLIPP_TEST in the campaign MARKERPARAMS_CAMPAIGN (API)
    #Then response should contain onDetectForcepeel,onDetect (API)
    When I get DetectMode version of the blipp MARKERPARAMS_BLIPP_TEST in the campaign MARKERPARAMS_CAMPAIGN (API)
    Then response should contain onDetectForcepeel,onDetect (API)
    When I get DetectMode versions of the blipp MARKERPARAMS_BLIPP_TEST in the campaign MARKERPARAMS_CAMPAIGN (API)
    Then response should contain onDetectForcepeel,onDetect (API)
    When I get DetectMode metadata of the blipp MARKERPARAMS_BLIPP_TEST in the campaign MARKERPARAMS_CAMPAIGN (API)
    Then response should contain onDetectForcepeel,onDetect (API)
    When I go to Blipp Detail MARKERPARAMS_BLIPP_TEST page
    Then I check that blipp has DetectModes ON TRACKING,ON DETECT,FORCE PEEL


  @ORPHAN @DISABLED @PUBLISHING @RECO_CHECK
  Scenario: Publish BlippBuilder blipp and check that can be blipped as a Blippar Admin

    When I login with user auto.blippar@gmail.com and password blippar1
    Then The user Blippar Admin is logged in
    When I go to My Campaigns
    Then The screen My campaigns is opened
    When I delete the campaign reco_hub_api_campaign
    Then I check that there are not campaigns cards with the name reco_hub_api_campaign
    When I create the campaign with the name reco_hub_api_campaign (API)
    And I create the blipp type blipp builder with the name reco_hub_api_blipp, marker image reco1.jpg in the campaign reco_hub_api_campaign (API)
    And I publish blipp with the name reco_hub_api_blipp in the campaign reco_hub_api_campaign (API)
    Then I check that the status of the blipp reco_hub_api_blipp in the campaign reco_hub_api_campaign is LIVE (API)
    When As blippar_admin I run reco endpoint using image reco1.jpg (API)
    Then I check that the reco endpoint returns a response (API)
    And I check that coverimage and plist values matches with the blipp with the name reco_hub_api_blipp in the campaign reco_hub_api_campaign (API)
    When I unpublish blipp with the name reco_hub_api_blipp in the campaign reco_hub_api_campaign (API)
    Then I check that the status of the blipp reco_hub_api_blipp in the campaign reco_hub_api_campaign is NOT_LIVE (API)
    When As blippar_admin I run reco endpoint using image reco1.jpg (API)
    Then I check that the reco endpoint does not return a response (API)


  @ORPHAN
  Scenario: Signed up user creates and sending the blipp for approval (workflow 1)

    #Login with a signed up user
    When I login with user testit11@abv.bg and password gerg456ivan
    #Given I am logged in as a normal_user_2 user # seems this user is disabled - can not login
    Then The user Ganka Pospalanka is logged in
    Then The screen My campaigns is opened
    When I delete the campaign APPROVAL_CAMPAIGN
    Then I check that there are not campaigns cards with the name APPROVAL_CAMPAIGN
    #Campaign and blipp creation
        When I create the campaign with the name APPROVAL_CAMPAIGN
        When I click on Create Blipp default button
        Then The modal Create new blipp is opened
        When Creating my blipp I give it the name APPROVAL_BLIPP
        When Creating my blipp I upload the marker flowers.jpg
        And I click in back button from blippbuilder
        Then I check that the blipp with the name APPROVAL_BLIPP is created
        When I go to Blipp Detail APPROVAL_BLIPP page
        Then I check that the status of the blipp APPROVAL_BLIPP detail page is PROCESSED (UI)
        # Steps to check admin email notificaion - we have a bug here now


  @ORPHAN
  Scenario: Signed up with BDN access user creates and sending the blipp for approval (workflow 3)

    #Login with a signed up user
     Given I am logged in as a normal_user_2 user
        When I Revoke user normal_user_2 permission for Developer (Network & Custom JS) access (API)
        When the user is on the My profile page
        When click in link with text Show me how
        Then the modal window with text Join the Blippar Development Program is displayed
        When click on Count me in
        Then they are signed up to the developer network and the text I am a Blipp developer is shown
        When click in link with text Go to the BDN webpage
        And I switch to next browser window
        Then the user is logged into the Dev Portal started with text 'Create your own'
        And ending with text 'augmented reality experiences'
        And the page title must be Index | Blippar Developers
        #Login to hub
        When they create a campaign in Hub
        Then they will see the option to create a 'Custom - Javascript' blipp 
    
    #When I login with user testit11@abv.bg and password gerg456ivan
    When I click on My account in the dropdown top right menu
    When I Add access to Developer (Network & Custom JS) on group or user level
    When I switch to next browser window
    When click in link with text Go to the BDN webpage
    When I switch to next browser window
    Then the user is logged into the Dev Portal started with text 'Create your own'
    And ending with text 'augmented reality experiences'
    #Campaign and blipp creation
        When I create the campaign with the name APPROVAL_CAMPAIGN
        When I click on Create Blipp default button
        Then The modal Create new blipp is opened
        When Creating my blipp I give it the name APPROVAL_BLIPP
        When Creating my blipp I upload the marker flowers.jpg
        And I click in back button from blippbuilder
        Then I check that the blipp with the name APPROVAL_BLIPP is created
        When I go to Blipp Detail APPROVAL_BLIPP page
        Then I check that the status of the blipp APPROVAL_BLIPP detail page is PROCESSED (UI)
        # Steps to check admin email notificaion - we have a bug here now


  @ORPHAN
  Scenario: Managed user with Blipp Builder tool access creates and sending the blipp for approval (workflow 4)

    When I click on My account in the dropdown top right menu
    When I Add access to BlippBuilder (Classic) on group or user level
    When I switch to next browser window
    When click in link with text Go to the BDN webpage
    When I switch to next browser window
    Then the user is logged into the Dev Portal started with text 'Create your own'
    And ending with text 'augmented reality experiences'
    #Campaign and blipp creation - workflow2
        When I create the campaign with the name APPROVAL_CAMPAIGN
        When I click on Create Blipp default button
        Then The modal Create new blipp is opened
        When Creating my blipp I give it the name APPROVAL_BLIPP
        When Creating my blipp I upload the marker flowers.jpg
        And I click in back button from blippbuilder
        Then I check that the blipp with the name APPROVAL_BLIPP is created
        When I go to Blipp Detail APPROVAL_BLIPP page
        Then I check that the status of the blipp APPROVAL_BLIPP detail page is PROCESSED (UI)

