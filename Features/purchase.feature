@bdd
Feature: Purchase
  Tests related to buying a product

  Scenario Outline: Registered user buys a product
    Given a registered user exists
    And the user is on the login page
    When I log in with the registered user
    And I search for <product> and add it to the cart
    And I check out and pay with a test card
    Then the order is placed successfully

    Examples:
      | product    |
      | Men Tshirt |