# Created by Admin at 10/12/2024
Feature: API testing
  # Enter feature description here

  Scenario: GET request
    When 5_api - Execute the GET request with id=1
    Then 5_api - Verify json schema of response
    """
    {
      "type": "object",
      "properties": {
        "userId": {"type": "number"},
        "id": {"type": "number"},
        "title": {"type": "string"},
        "body": {"type": "string"}
      },
      "required": [
        "userId",
        "id",
        "title",
        "body"
      ]
    }
    """
    Then 5_api - Verify response's body
      | id | userId |
      | 1  | 1      |

  Scenario: GET request with data table
    When 5_api - Execute the GET request and verify response with data table
      | id | userId | title                                                                      | body                                                                                                                                                                                                              |
      | 1  | 1      | sunt aut facere repellat provident occaecati excepturi optio reprehenderit | quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto                                                 |
      | 2  | 1      | qui est esse                                                               | est rerum tempore vitae\nsequi sint nihil reprehenderit dolor beatae ea dolores neque\nfugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis\nqui aperiam non debitis possimus qui neque nisi nulla |

  Scenario: POST request with data table
    When 5_api - Execute the POST request and verify response
      | userId | title    | body    |
      | 10     | my title | my body |
      | 11     | foo      | bar     |