Feature: Login with data


  Scenario: Login failure with invalid email-password
    Given Open <chrome> browser
    Then Login with invalid email/password then verifying the error message is displayed
      | email                    | password    | error_message                     |
      | invalidemail@cucumber.io | invalidPass | No user found with matching email |
      | blabla@gmail.com         | invalidPass | An error occurred with log in.    |
