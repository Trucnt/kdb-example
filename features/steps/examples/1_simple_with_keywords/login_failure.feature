Feature: Login


  Scenario: Login failure with invalid email-password
    Given Open <chrome> browser
    And Goto <https://stackoverflow.com/users/login>
    When Login with <no-exists@cucumber.io> and <correctPass>
    Then The error message is displayed: <An error occurred with log in.>
