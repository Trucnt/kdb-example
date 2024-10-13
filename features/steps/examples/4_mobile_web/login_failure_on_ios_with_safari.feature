Feature: Login


  Scenario: Login failure with invalid email-password on iOS with Safari browser
    Given Open <ios> browser
    When Login with <no-exists@cucumber.io> and <correctPass> with page object
    Then The error message is displayed: <An error occurred with log in.>
