Feature: Accounts API

 
  @HUB-1071 @assignee:juanmoschino @COMPLETED @ACCOUNTS_API
  Scenario: check_permissions endpoint

    When I set payload {"permissions": ["publish_blipp_live", "developer_app_login", "app_debugging"]}
    And  I set aditional header {'Content-Type':'application/json'}
    And  As blippar_admin I run a POST in the endpoint /api/v1/user/check_permissions with base in var accounts_url
    Then the response contains the value "publish_blipp_live":true
    And  the response contains the value "developer_app_login":false
    And  the response contains the value "app_debugging":true


  @HUB-1179 @assignee:caroline.palmer @version:next-version @WIP @ACCOUNTS_API
  Scenario Outline: Get user/group endpoint

    When As <role> I run a GET in the endpoint /api/v1/user/group with base in var accounts_url
    Then the response contains the value <id>
    And  the response contains the value <country>
    And  the response contains the value <name>
    Examples:
      | role          | id      | country       | name                                                   |
      | blippar_admin |"id":7   | "country":"GB"| "name":"Blippar"                                       |
      | normal_user   |"id":2059| "country":"GB"| "name":"automated.group"                               |
      | group_admin   |"id":2059| "country":"GB"| "name":"automated.group"                               |
      | basic_user    |"id":5278| "country":"DE"| "name":"UserGroup:juan.moschino+basic_user@blippar.com"|


  @HUB-1186 @assignee:caroline.palmer @WIP @ACCOUNTS_API
  Scenario Outline: Get user/roles endpoint

    When As <role> I run a GET in the endpoint /api/v1/user/roles with base in var accounts_url
    Then the response contains the value <key>
    Examples:
      | role          | key                                                                                                                                                            |
      | blippar_admin |{"roles":[{"key":"blippar_admin"},{"key":"ad_user"},{"key":"blippbuilder_flash_user"},{"key":"blippbuilder_javascript_user"},{"key":"bespoke_javascript_user"}]}|
      | normal_user   |"key":"normal_user"                                                                                                                                             |
      | group_admin   |"key":"group_admin"                                                                                                                                             |
      | basic_user    |"key":"signup_user"                                                                                                                                             |


  @HUB-1198 @assignee:caroline.palmer @WIP @ACCOUNTS_API
  Scenario Outline: BDN membership endpoint check

    When I set payload <post_value>
    And I set aditional header {'Content-Type':'application/json'}
    And As bdn_membership_check_user I run a POST in the endpoint /api/v1/user/bdn with base in var accounts_url
    And As bdn_membership_check_user I run a GET in the endpoint /api/v1/user/bdn with base in var accounts_url
    Then the response contains the value <get_value>
       Examples:
          | post_value                 | get_value         |
          | {"member": 'true'}         | {"member":true}   |
          | {"member": 'false'}        | {"member":false}  |

