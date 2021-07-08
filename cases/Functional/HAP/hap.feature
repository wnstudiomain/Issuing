Feature: Login to My Store
    Basic login flows to my-store.ca

Scenario: Valid Login
    Given I visit the login page
    Then I should be on the inventory page
