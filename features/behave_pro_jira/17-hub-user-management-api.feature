@HUB_API
Feature: Hub user management API

  
  As a different user roles
  I want to check that API endpoints related to user mngmt returns correct content

 
  @ORPHAN
  Scenario Outline: Get different user endpoints and verify the return status

    When as <role> I get the api endpoint <endpoint>
    Then I check that response code is <status>
    Examples:
      | role          | endpoint      | status |
      | blippar_admin | groups        | 200    |
      | blippar_admin | groupstatuses | 200    |
      | blippar_admin | grouptypes    | 200    |
      | blippar_admin | userroles     | 200    |
      | blippar_admin | userstatuses  | 200    |
      | blippar_admin | users         | 200    |
      | blippar_admin | userroles     | 200    |
    Examples:
      | role        | endpoint      | status |
      | normal_user | groups        | 403    |
      | normal_user | groupstatuses | 200    |
      | normal_user | grouptypes    | 403    |
      | normal_user | userroles     | 200    |
      | normal_user | userstatuses  | 403    |
      | normal_user | users         | 200    |
      | normal_user | userroles     | 200    |
      | normal_user | constants     | 200    |
    Examples:
      | role        | endpoint      | status |
      | group_admin | groups        | 403    |
      | group_admin | groupstatuses | 200    |
      | group_admin | grouptypes    | 403    |
      | group_admin | userroles     | 200    |
      | group_admin | userstatuses  | 403    |
      | group_admin | users         | 403    |
      | group_admin | userroles     | 200    |
    Examples:
      | role         | endpoint      | status |
      | blippar_user | groups        | 200    |
      | blippar_user | groupstatuses | 200    |
      | blippar_user | grouptypes    | 200    |
      | blippar_user | userroles     | 200    |
      | blippar_user | userstatuses  | 200    |
      | blippar_user | users         | 200    |
      | blippar_user | userroles     | 200    |
    Examples:
      | role               | endpoint  | status |
      | blippar_user       | functions | 403    |
      | blippar_user       | services  | 403    |
      | normal_user        | functions | 403    |
      | normal_user        | services  | 403    |
      | group_admin        | services  | 200    |
      | group_admin        | functions | 403    |
      | blippar_super_admin| services  | 200    |
      | blippar_super_admin| functions | 200    |


  @HUB-609 @assignee:ben.dalby @COMPLETED
  Scenario Outline: Get Groups PublishQuota property

    When as <role> I get the api endpoint <group_metadata>
    Then response should contain <quota> (API)
        Examples: Old groups
          |role|group_metadata|quota|
          |blippar_admin|group/7?metadata=full|"PublishQuota"\: -1|
          |group_admin  |group/2059?metadata=full|"PublishQuota"\: -1|
    
        Examples: Pro and Basic user groups
          |role|group_metadata|quota|
      ## we need to create new signup for paid user and use that group!
          ##|blippar_admin|group/4541?metadata=full|"Name"\: "Pro","PublishQuota"\: 10|
    ##new groups has unlimited publish quota now!(it was 2 before)
          |blippar_admin|group/4542?metadata=full|"PublishQuota"\: -1|


  @HUB-619 @assignee:shyukri.shyukriev @COMPLETED
  Scenario Outline: Get users publish rules

    When as <user_role> I get the api endpoint <permissions_url>
    Then response should contain <key_value> (API)
    Examples:
          |user_role            |permissions_url      |key_value|
          |basic_user_no_credit |user/3791/permissions|"Action"\: "publish_testcode","Action"\: "publish_region"|
          |pro_user_no_credit   |user/3789/permissions|"Action"\: "publish_testcode","Action"\: "publish_region"|
          |blippar_super_admin  |user/1995/permissions|"Action"\: "publish_global","Action"\: "publish_testcode","Action"\: "publish_region"|

