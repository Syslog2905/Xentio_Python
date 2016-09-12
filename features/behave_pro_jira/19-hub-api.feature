Feature: Hub API

  
  
  This feature includes API tests for HUB. They are purely API tests.
  Scenarios tagged as HUB_API will be executed by daily jenkins jobs.


  Background:
    Given I delete the campaigns with the name hub_api_campaign (API)

 
  @ORPHAN @HUB_API
  Scenario: Create and delete a campaign

    When I create the campaign with the name hub_api_campaign (API)
    And I create the blipp type blipp builder with the name hub_api_blipp, marker image fish1.jpeg in the campaign hub_api_campaign (API)
    Then I check that the campaign with the name hub_api_campaign is present (API)
    When I delete the campaigns with the name hub_api_campaign (API)
    Then I check that the campaign with the name hub_api_campaign is not present (API)


  @ORPHAN @HUB_API
  Scenario: Create and delete a blipp

    When I create the campaign with the name hub_api_campaign (API)
    And I create the blipp type blipp builder with the name hub_api_blipp, marker image fish1.jpeg in the campaign hub_api_campaign (API)
    Then I check that the blipp hub_api_blipp in the campaign hub_api_campaign is present (API)
    When I delete blipp with the name hub_api_blipp in the campaign hub_api_campaign (API)
    Then I check that the blipp hub_api_blipp in the campaign hub_api_campaign is not present (API)


  @ORPHAN @HUB_API
  Scenario: Publish and unpublish flow

    When I create the campaign with the name hub_api_campaign (API)
    And I create the blipp type blipp builder with the name hub_api_blipp, marker image fish1.jpeg in the campaign hub_api_campaign (API)
    And I publish blipp with the name hub_api_blipp in the campaign hub_api_campaign (API)
    Then I check that the status of the blipp hub_api_blipp in the campaign hub_api_campaign is LIVE (API)
    When I unpublish blipp with the name hub_api_blipp in the campaign hub_api_campaign (API)
    Then I check that the status of the blipp hub_api_blipp in the campaign hub_api_campaign is NOT_LIVE (API)


  @HUB-36 @assignee:caroline.palmer @COMPLETED @HUB_API
  Scenario: Duplicate published blipp and publish the duplicate

    When I create the campaign with the name hub_api_campaign (API)
    And I create the blipp type blipp builder with the name hub_api_blipp, marker image fish1.jpeg in the campaign hub_api_campaign (API)
    And I publish blipp with the name hub_api_blipp in the campaign hub_api_campaign (API)
    When I duplicate blipp hub_api_blipp from campaign hub_api_campaign into blipp copy_hub_api_blipp with marker image birds.jpg (API)
    Then I check that the status of the blipp copy_hub_api_blipp in the campaign hub_api_campaign is NOT_LIVE (API)
    When I publish blipp with the name copy_hub_api_blipp in the campaign hub_api_campaign (API)
    Then I check that the status of the blipp copy_hub_api_blipp in the campaign hub_api_campaign is LIVE (API)


  @ORPHAN @AUTOMATABLE
  Scenario: Create custom blipp

    And I create the blipp type custom with the name hub_custom_api_blipp zip <zip_name> in the campaign hub_api_campaign (API)
    And I publish blipp with the name hub_custom_api_blipp in the campaign hub_api_campaign (API)


  @ORPHAN @AUTOMATABLE
  Scenario: Create 2nd version of an existing custom blipp

    And I create the blipp type custom with the name hub_custom_api_blipp zip <zip_name> in the campaign hub_api_campaign (API)
    When I create new version of the custom blipp hub_custom_api_blipp using zip <zip_name> in the campaign hub_api_campaign (API)
    Then I check the versions of the blipp hub_custom_api_blipp in the campaign hub_api_campaign are 2 (API)


  @ORPHAN @HUB_API
  Scenario: Duplicate unpublished blipp and publish the duplicate

    When I create the campaign with the name hub_api_campaign (API)
    And I create the blipp type blipp builder with the name hub_api_blipp, marker image fish1.jpeg in the campaign hub_api_campaign (API)
    When I duplicate blipp hub_api_blipp from campaign hub_api_campaign into blipp copy_hub_api_blipp with marker image birds.jpg (API)
    Then I check that the status of the blipp copy_hub_api_blipp in the campaign hub_api_campaign is NOT_LIVE (API)
    When I publish blipp with the name copy_hub_api_blipp in the campaign hub_api_campaign (API)
    Then I check that the status of the blipp copy_hub_api_blipp in the campaign hub_api_campaign is LIVE (API)


  @ORPHAN @BB_API @HUB_API
  Scenario: Add assets and predefined poll to BlipBuilder blipp

    When I create the campaign with the name hub_api_campaign (API)
    And I create the blipp type blipp builder with the name asset_api_blipp, marker image fish1.jpeg in the campaign hub_api_campaign (API)
    And I add asset penguins.jpg to blipp asset_api_blipp in the campaign hub_api_campaign (API)
    And I add asset music.mp3 to blipp asset_api_blipp in the campaign hub_api_campaign (API)
    When I add predefined poll to blipp asset_api_blipp in the campaign hub_api_campaign (API)
    And I get poll data (API)
    Then response should contain Behave Poll,Yes,No,Maybe (API)


  @ORPHAN @PERMISSIONS
  Scenario Outline: Permissions for campaign rename and deletion with different roles

    When As blippar_admin I delete the campaigns with the name campaign_permissions (API)
    When As blippar_admin I delete the campaigns with the name altered_campaign_permissions (API)
    When As <camp_owner> I create the campaign with the name campaign_permissions (API)                                
    When As <action_performer> I rename campaign campaign_permissions into campaign altered_campaign_permissions (API) 
    Then I check that response code is <camp_rename_status>
    When As <action_performer> I delete the campaigns with the name <campaign_to_delete> (API)
    Then I check that response code is <camp_delete_status>                                                        
    Examples: Owner - Blippar User
              | camp_owner   | action_performer |camp_rename_status |campaign_to_delete          |camp_delete_status|
              | blippar_user | blippar_user2    | 200               |altered_campaign_permissions| 403              |
              | blippar_user | normal_user      | 403               |campaign_permissions        | 403              |
              | blippar_user | blippar_admin    | 200               |altered_campaign_permissions| 200              |
              | blippar_user | blippar_user     | 200               |altered_campaign_permissions| 200              |
              | blippar_user | group_admin      | 403               |campaign_permissions        | 403              |
                                                                                                                               
    Examples: Owner - Group Admin
              | camp_owner  | action_performer |camp_rename_status |campaign_to_delete          |camp_delete_status |
              | group_admin | blippar_user     | 200               |altered_campaign_permissions| 403               |
              | group_admin | normal_user      | 403               |campaign_permissions        | 403               |
              | group_admin | blippar_admin    | 200               |altered_campaign_permissions| 200               |
              | group_admin | group_admin2     | 403               |campaign_permissions        | 403               |
              | group_admin | group_admin      | 200               |altered_campaign_permissions| 200               |
                                   
    Examples: Owner - Blippar Admin
              | camp_owner    | action_performer |camp_rename_status |campaign_to_delete          |camp_delete_status |
              | blippar_admin | normal_user      | 403               |campaign_permissions        | 403               |
              | blippar_admin | blippar_admin    | 200               |campaign_permissions        | 200               |
              | blippar_admin | blippar_user     | 200               |altered_campaign_permissions| 403               |
              | blippar_admin | group_admin      | 403               |campaign_permissions        | 403               |


  @ORPHAN @PERMISSIONS
  Scenario Outline: Blipp rename and deletion with different roles

    When As blippar_admin I delete the campaigns with the name campaign_permissions (API)
    When As <camp_owner> I create the campaign with the name campaign_permissions (API)
    And As <blipp_owner> I create the blipp type blipp builder with the name hub_api_blipp, marker image fish1.jpeg in the campaign campaign_permissions (API)
    When As <action_performer> I rename blipp hub_api_blipp from campaign campaign_permissions into blipp <blipp_to_delete> (API)
    Then I check that response code is <blipp_rename_status>
    When As <action_performer> I delete blipp with the name <blipp_to_delete> in the campaign campaign_permissions (API)
    Then I check that response code is <blipp_delete_status>
    
    Examples: Owner - Blippar User
             | camp_owner   | blipp_owner  | action_performer |blipp_rename_status|blipp_to_delete|blipp_delete_status|
             | blippar_user | blippar_user | blippar_user     | 200               |renamed_blipp  | 200               |
             | blippar_user | blippar_user | normal_user      | 403               |hub_api_blipp  | 403               |
             | blippar_user | blippar_user | blippar_admin    | 200               |renamed_blipp  | 200               |
             | blippar_user | blippar_user | blippar_user2    | 200               |renamed_blipp  | 200               |
             | blippar_user | blippar_user | group_admin      | 403               |hub_api_blipp  | 403               |
    
    Examples: Owner - Group Admin
             | camp_owner  | blipp_owner  | action_performer |blipp_rename_status|blipp_to_delete|blipp_delete_status|
             | group_admin | group_admin  | blippar_user     | 200               |renamed_blipp  | 200               |
     #       | group_admin | normal_user  | normal_user      | 200               |renamed_blipp  | 403               |
     #       | group_admin | normal_user  | group_admin      | 200               |renamed_blipp  | 200               |
             | group_admin | blippar_user | blippar_admin    | 200               |renamed_blipp  | 200               |
             | group_admin | blippar_admin| group_admin      | 200               |renamed_blipp  | 200               |


  @HUB-613 @assignee:juanmoschino @COMPLETED @CanPublishEndpoint @DISABLED @HUB_API
  Scenario Outline: CanPublish endpoint

    When As <role> I delete the campaigns with the name <campaign_name> (API)
    And As <role> I create the campaign with the name <campaign_name> (API)
    And As <role> I create and publish <blipp_quantity> blipps in the campaign <campaign_name> (API)
    And As <role> I run canPublish for the blipp with the name last_blipp in campaign <campaign_name> (API)
    Then response should contain <response> (API)
    Examples:
      | role                | campaign_name | blipp_quantity  |  response |
      | basic_user_no_credit| quota_b_basic |     1           |  true     |
      | basic_user_no_credit| quota_b_basic |     2           |  false    |
      | pro_user_no_credit  | quota_b_pro   |     9           |  true     |
      | pro_user_no_credit  | quota_b_pro   |     10          |  false    |


  @ORPHAN @DISABLED @HUB_API @PRODUCTION_EXCLUDED @RECO_CHECK
  Scenario: Reco responses when publishing and unpublishing

    Given I delete the campaigns with the name reco_hub_api_campaign (API)
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


  @HUB-1183 @assignee:juanmoschino @COMPLETED @PERMISSIONS
  Scenario Outline: Check app and dev portal permissions for all blippar roles

    When I get the user id for user with role <role> and I store it in user_id
    And  I build the url for endpoint /api/user/{user_id}/permissions?limit=0 using variable in user_id and I store it in endpoint_var
    And  As role <role> I run a GET using endpoint stored in variable endpoint_var with base in hub_api_url
    Then the response contains the value <permission_1>
    And  the response contains the value <permission_2>
    And  the response contains the value <permission_3>
    And  the response contains the value <permission_4>
    And  the response contains the value <permission_5>
    And  the response contains the value <permission_6>
    And  the response contains the value <permission_7>
    Examples:
          | role               | permission_1                                    | permission_2                                 | permission_3                               | permission_4                                      | permission_5                                        | permission_6                                        | permission_7                                               |
          | blippar_super_admin| "app_change_servers","Entity":"","Permission":1 | "app_qa_features","Entity":"","Permission":1 | "app_debugging","Entity":"","Permission":1 | "app_extended_logging","Entity":"","Permission":1 | "app_sideload_js_blipps","Entity":"","Permission":1 | "app_sideload_bb_blipps","Entity":"","Permission":1 | "dev_portal_additional_content","Entity":"","Permission":1 |
          | blippar_admin      | "app_change_servers","Entity":"","Permission":1 | "app_qa_features","Entity":"","Permission":1 | "app_debugging","Entity":"","Permission":1 | "app_extended_logging","Entity":"","Permission":1 | "app_sideload_js_blipps","Entity":"","Permission":1 | "app_sideload_bb_blipps","Entity":"","Permission":1 | "dev_portal_additional_content","Entity":"","Permission":1 |
     #    | blippar_admin2| "app_change_servers","Entity":"","Permission":1 | "app_qa_features","Entity":"","Permission":1 | "app_debugging","Entity":"","Permission":1 | "app_extended_logging","Entity":"","Permission":1 | "app_sideload_js_blipps","Entity":"","Permission":1 | "app_sideload_bb_blipps","Entity":"","Permission":1 | "dev_portal_additional_content","Entity":"","Permission":1 |
          | blippar_user  | "app_change_servers","Entity":"","Permission":1 | "app_qa_features","Entity":"","Permission":1 | "app_debugging","Entity":"","Permission":1 | "app_extended_logging","Entity":"","Permission":1 | "app_sideload_js_blipps","Entity":"","Permission":1 | "app_sideload_bb_blipps","Entity":"","Permission":1 | "dev_portal_additional_content","Entity":"","Permission":1 |

