Feature: Connect Creator integration

  
  The scenarios in this feature verifies the integration of CC with HUB.

 
  @CC-359 @CC-398 @CC-427 @assignee:ben.dalby @assignee:maurice @assignee:nikola_layar @OPEN @AUTOMATABLE
  Scenario: Create a connect blipp in a new campaign setting it for approval

    #User must be normal user with CC permission
    When I login with user <user> and password <password>
    And I go to My Campaigns
    Then the screen My campaigns is opened
    When I create the campaign BEHAVE_CC_campaign and open it
    And I click on the create connect blipp option
    Then the Connect Creator is opened
    When the user creates a new connect blipp with name cc_blipp within the Connect Creator
    And set the blipp for approval
    Then the screen My campaigns is opened
    And the blipp with name cc_blipp is be added to the Project
    #Verify visibility for normal user
    And check that in the card menu of blipp cc_blipp the options are move,delete
    #Login as blippar admin user and check approval process
    When I login with user <user> and password <password>
    And I go to approvals
    When I select the blipp with the name cc_blipp and approve it
    Then the blipp with the name cc_blipp is approved


  @CC-359 @CC-390 @CC-427 @assignee:ben.dalby @assignee:maurice @assignee:nikola_layar @OPEN @AUTOMATABLE
  Scenario: Create a connect blipp in a new campaign publishing it

    #User must be blippar admin user with CC permission
    When I login with user <user> and password <password>
    And I go to My Campaigns
    Then the screen My campaigns is opened
    When I create the campaign BEHAVE_CC_campaign and open it
    And I click on the create connect blipp option
    Then the Connect Creator is opened
    When the user creates a new connect blipp with name cc_blipp within the Connect Creator
    And I publish the blipp
    Then the screen My campaigns is opened
    And the blipp with name cc_blipp is added to the Project
    #Verify visibility for blipp admin user
    And check that in the card menu of blipp cc_blipp the options are publish,unpublish,move,delete


  @CC-359 @CC-385 @CC-427 @assignee:ben.dalby @assignee:maurice @OPEN @AUTOMATABLE
  Scenario: Create a connect blipp in a new campaign without approving or publishing it

    When I login with user <user> and password <password>
    And I go to My Campaigns
    Then the screen My campaigns is opened
    When I create the campaign BEHAVE_CC_campaign and open it
    And I click on the create connect blipp option
    Then the Connect Creator is opened
    When the user creates a new connect blipp with name cc_blipp within the Connect Creator
    And I go back to hub campaigns page
    Then the screen My campaigns is opened
    And the blipp with name cc_blipp is added to the Project
    When I click in the blipp with name cc_blipp
    Then the CC editor is opened


  @CC-390 @CC-427 @assignee:ben.dalby @assignee:nikola_layar @COMPLETED @AUTOMATABLE
  Scenario: Create a connect blipp in an existing campaign with other blipps, setting it for approval

    #User must be normal user with CC permission
    When I login with user <user> and password <password>
    And I go to My Campaigns
    Then the screen My campaigns is opened
    When I create the campaign BEHAVE_CC_campaign and open it
    #BB blipp creation
    And I create a BB blipp with the name BEHAVE_BB_CC_TEST using marker.png marker image
    Then I check that the blipp with the name BEHAVE BUILDER_BLIPP is created
    #Bespoke blipp creation
    When I create a bespoke blipp with the name BEHAVE_BSPK_CC_TEST using blipp.zip file
    Then I check that the blipp with the name BEHAVE BESPOKE_BLIPP_GLOBAL is created
    #CC blipp creation
    When I click on the create connect blipp option
    Then the Connect Creator is opened
    When the user creates a new connect blipp with name cc_blipp within the Connect Creator
    And set the blipp for approval
    Then the screen My campaigns is opened
    And the blipp with name cc_blipp is be added to the Project


  @CC-390 @CC-427 @assignee:ben.dalby @assignee:nikola_layar @COMPLETED @AUTOMATABLE
  Scenario: Create a connect blipp in an existing campaign with other blipps, publishing it

    #User must be normal user with CC permission
    When I login with user <user> and password <password>
    And I go to My Campaigns
    Then the screen My campaigns is opened
    When I create the campaign BEHAVE_CC_campaign and open it
    #BB blipp creation
    And I create a BB blipp with the name BEHAVE_BB_CC_TEST using marker.png marker image
    Then I check that the blipp with the name BEHAVE BUILDER_BLIPP is created
    #Bespoke blipp creation
    When I create a bespoke blipp with the name BEHAVE_BSPK_CC_TEST using blipp.zip file
    Then I check that the blipp with the name BEHAVE BESPOKE_BLIPP_GLOBAL is created
    #CC blipp creation
    When I click on the create connect blipp option
    Then the Connect Creator is opened
    When the user creates a new connect blipp with name cc_blipp within the Connect Creator
    And I publish the blipp
    Then the screen My campaigns is opened
    And the blipp with name cc_blipp is be added to the Project


  @CC-390 @CC-427 @assignee:ben.dalby @assignee:nikola_layar @COMPLETED @AUTOMATABLE
  Scenario: Create a connect blipp in an existing campaign with other blipps, without approving or publishing it

    #User must be normal user with CC permission
    When I login with user <user> and password <password>
    And I go to My Campaigns
    Then the screen My campaigns is opened
    When I create the campaign BEHAVE_CC_campaign and open it
    #BB blipp creation
    And I create a BB blipp with the name BEHAVE_BB_CC_TEST using marker.png marker image
    Then I check that the blipp with the name BEHAVE BUILDER_BLIPP is created
    #Bespoke blipp creation
    When I create a bespoke blipp with the name BEHAVE_BSPK_CC_TEST using blipp.zip file
    Then I check that the blipp with the name BEHAVE BESPOKE_BLIPP_GLOBAL is created
    #CC blipp creation
    When I click on the create connect blipp option
    Then the Connect Creator is opened
    When the user creates a new connect blipp with name cc_blipp within the Connect Creator
    And I go back to hub campaigns page
    Then the screen My campaigns is opened
    And the blipp with name cc_blipp is be added to the Project


  @ORPHAN @AUTOMATABLE
  Scenario: Add existing CC blipp to new campaign

    When I login with user <user> and password <password>
    And I go to My Campaigns
    Then the screen My campaigns is opened
    When I create the campaign BEHAVE_CC_campaign and open it
    And I click on the create connect blipp option
    Then the Connect Creator is opened
    When I search for an existing blipp called cc_blipp and I add it
    And I go back to hub campaigns page
    Then the screen My campaigns is opened
    And the blipp with name cc_blipp is be added to the Project


  @ORPHAN @AUTOMATABLE
  Scenario: Add existing CC blipp to a campaign with other blipps

    When I login with user <user> and password <password>
    And I go to My Campaigns
    Then the screen My campaigns is opened
    When I create the campaign BEHAVE_CC_campaign and open it
    #BB blipp creation
    And I create a BB blipp with the name BEHAVE_BB_CC_TEST using marker.png marker image
    Then I check that the blipp with the name BEHAVE BUILDER_BLIPP is created
    #Bespoke blipp creation
    When I create a bespoke blipp with the name BEHAVE_BSPK_CC_TEST using blipp.zip file
    Then I check that the blipp with the name BEHAVE BESPOKE_BLIPP_GLOBAL is created
    #CC blipp creation
    And I click on the create connect blipp option
    Then the Connect Creator is opened
    When I search for an existing blipp called cc_blipp and I add it
    And I go back to hub campaigns page
    Then the screen My campaigns is opened
    And the blipp with name cc_blipp is be added to the Project


  @CC-394 @assignee:ben.dalby @COMPLETED @AUTOMATABLE
  Scenario: Publish and unpublish a CC blipp from campaigns without approval

    #User must be blippar admin user
    When I login with user <user> and password <password>
    And I go to My Campaigns
    Then the screen My campaigns is opened
    When I create the campaign BEHAVE_CC_campaign and open it
    And I click on the create connect blipp option
    Then the Connect Creator is opened
    When the user creates a new connect blipp with name cc_blipp within the Connect Creator
    And I go back to hub campaigns page
    Then the screen My campaigns is opened
    And the blipp with name cc_blipp is added to the Project
    When click in publish from the card menu of blipp cc_blipp
    Then the blipp cc_blipp is published
    When click in unpublish from the card menu of blipp cc_blipp
    Then the blipp cc_blipp is not published


  @CC-396 @assignee:ben.dalby @COMPLETED @AUTOMATABLE
  Scenario: Delete a CC blipp from campaigns

    When I login with user <user> and password <password>
    And I go to My Campaigns
    Then the screen My campaigns is opened
    When I create the campaign BEHAVE_CC_campaign and open it
    And I click on the create connect blipp option
    Then the Connect Creator is opened
    When the user creates a new connect blipp with name cc_blipp within the Connect Creator
    And I go back to hub campaigns page
    Then the screen My campaigns is opened
    And the blipp with name cc_blipp is added to the Project
    When click in delete from the card menu of blipp cc_blipp
    And the blipp with the name cc_blipp is not in the campaign


  @ORPHAN @MANUAL_FROM_APP
  Scenario: Blipp a CC blipp published using approval flow

    Given a blipp created as a normal user
    When I approve the blipp as a blippar admin user and publish it
    And I blipp the blipp from the app
    Then the blipp can be blipped


  @ORPHAN @MANUAL_FROM_APP
  Scenario: Blipp a CC blipp published from CC

    Given a blipp created as a blippar admin user
    And I publish the blipp in CC
    And I blipp the blipp from the app
    Then the blipp can be blipped


  @ORPHAN @MANUAL_FROM_APP
  Scenario: Blipp a CC blipp published from campaign screen

    Given a blipp created as a blippar admin user but not published
    When I go to campaign pages
    And I open the menu in the blipp card
    When I select publish
    And I blipp the blipp from the app
    Then the blipp can be blipped


  @CC-395 @CC-398 @CC-399 @assignee:ben.dalby @assignee:nikola_layar @COMPLETED @AUTOMATABLE
  Scenario: Publish and unpublish a CC blipp from campaigns with approval flow

    #User must be normal user with CC permission
    When I login with user <user> and password <password>
    And I go to My Campaigns
    Then the screen My campaigns is opened
    When I create the campaign BEHAVE_CC_campaign and open it
    And I click on the create connect blipp option
    Then the Connect Creator is opened
    When the user creates a new connect blipp with name cc_blipp within the Connect Creator
    And I go back to hub campaigns page
    Then the screen My campaigns is opened
    And the blipp with name cc_blipp is added to the Project
    When click in publish from the card menu of blipp cc_blipp
    Then the status of blipp cc_blipp must be pending_approval
    #Login as blippar admin user to approve the blipp
    When I login with user <user> and password <password>
    And I go to approvals
    Then the blipp with name cc_blipp is added to approvals
    When I click in approve button in the blipp with the name cc_blipp
    Then the blipp cc_blipp is published
    #Login as normal user again to unpublish the blipp
    When I login with user <user> and password <password>
    And I go to My Campaigns
    Then the screen My campaigns is opened
    When click in unpublish from the card menu of blipp cc_blipp
    Then the blipp cc_blipp is not published


  @CC-397 @assignee:nikola_layar @COMPLETED @AUTOMATABLE
  Scenario: Move CC blipp to another campaign

    When I login with user <user> and password <password>
    And I go to My Campaigns
    Then the screen My campaigns is opened
    When I create the campaign BEHAVE_CC_campaign2
    And I create the campaign BEHAVE_CC_campaign and open it
    And I click on the create connect blipp option
    Then the Connect Creator is opened
    When the user creates a new connect blipp with name cc_blipp within the Connect Creator
    And I go back to hub campaigns page
    Then the screen My campaigns is opened
    And the blipp with name cc_blipp is added to the Project
    When I click in move option in the card menu of blipp cc_blipp
    And I select the campaign BEHAVE_CC_campaign2
    Then the blipp is not present in campaign BEHAVE_CC_campaign
    When I go to My Campaigns
    Then the screen My campaigns is opened
    When I open the campaign BEHAVE_CC_campaign2
    Then the blipp is present in campaign BEHAVE_CC_campaign2


  @CC-400 @assignee:ben.dalby @COMPLETED @AUTOMATABLE
  Scenario: Reject CC blipp

    #User must be normal user with CC permission
    When I login with user <user> and password <password>
    And I go to My Campaigns
    Then the screen My campaigns is opened
    When I create the campaign BEHAVE_CC_campaign and open it
    And I click on the create connect blipp option
    Then the Connect Creator is opened
    When the user creates a new connect blipp with name cc_blipp within the Connect Creator
    And I go back to hub campaigns page
    Then the screen My campaigns is opened
    And the blipp with name cc_blipp is added to the Project
    When click in publish from the card menu of blipp cc_blipp
    Then the status of blipp cc_blipp must be pending_approval
    #Login as blippar admin user to approve the blipp
    When I login with user <user> and password <password>
    And I go to approvals
    Then the blipp with name cc_blipp is added to approvals
    When I click in reject button in the blipp with the name cc_blipp
    Then the blipp cc_blipp is not published

