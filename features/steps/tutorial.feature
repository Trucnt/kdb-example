Feature: showing off behave


  Scenario: run a simple test
    Given we have behave installed
    And the following users exist
      | name   | email              | twitter         |
      | Aslak  | aslak@cucumber.io  | @aslak_hellesoy |
      | Julien | julien@cucumber.io | @jbpros         |
      | Matt   | matt@cucumber.io   | @mattwynne      |
    When we implement a test
    Then behave will test it for us
    But I not implement it


  Scenario Outline: eating
    Given there are <start> cucumbers
    When I eat <eat> cucumbers
    Then I should have <left> cucumbers

    Examples: ex1
      | start | eat | left |
      | 12    | 5   | 7    |
      | 20    | 5   | 15   |

    Examples: ex2
      | start | eat | left |
      | 11    | 8   | 3   |